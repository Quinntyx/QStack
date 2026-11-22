"""Run with: python3 -m unittest discover -s tests"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSTACK = ROOT / "bin" / "qstack"

SKILL = "---\nname: {name}\ndescription: \"Use when testing.\"\nmetadata:\n  type: guideline\n---\n\n{body}\n"


def run(cmd, env=None, **kwargs):
    with tempfile.TemporaryDirectory() as tmp:
        merged = dict(os.environ if env is None else env)
        if env is None or merged.get("HOME") == os.environ.get("HOME"):
            merged["HOME"] = tmp
        if env is None or merged.get("XDG_DATA_HOME") == os.environ.get("XDG_DATA_HOME"):
            merged["XDG_DATA_HOME"] = f"{merged['HOME']}/.local/share"
        return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, env=merged, **kwargs)


def files(path):
    return {str(f.relative_to(path)): f.read_bytes() for f in path.rglob("*")
            if f.is_file() and f.name != ".qstack-source"}


def assert_copy(test, path, source):
    """Antigravity gets a real directory, not a link, holding the source's files."""
    test.assertFalse(path.is_symlink())
    test.assertEqual(files(path), files(source))
    test.assertEqual((path / ".qstack-source").read_text().strip(), str(source))


class RepoCheck(unittest.TestCase):
    def test_repository_passes(self):
        result = run([QSTACK, "check"])
        self.assertEqual(result.returncode, 0, result.stdout)

    def fixture(self, tmp, pi_name="harness-x", body="See `../beta/SKILL.md` and `harness-x`."):
        root = Path(tmp)
        (root / "bin").mkdir()
        shutil.copy(QSTACK, root / "bin" / "qstack")
        for folder, name, text in [("shared", "alpha", body), ("shared", "beta", "Leaf."),
                                   ("claude", "harness-x", "Claude."), ("pi", pi_name, "Pi."),
                                   ("antigravity", "harness-x", "Antigravity.")]:
            (root / folder / name).mkdir(parents=True)
            (root / folder / name / "SKILL.md").write_text(SKILL.format(name=name, body=text))
        return root

    def test_valid_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            self.assertEqual(run([root / "bin" / "qstack", "check"]).returncode, 0)

    def test_broken_relative_link_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp, body="See `../gamma/SKILL.md`.")
            result = run([root / "bin" / "qstack", "check"])
            self.assertEqual(result.returncode, 1)
            self.assertIn("broken link `../gamma/SKILL.md`", result.stdout)

    def test_harness_skill_missing_from_one_harness_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp, pi_name="harness-y")
            result = run([root / "bin" / "qstack", "check"])
            self.assertEqual(result.returncode, 1)
            self.assertIn("same skill names", result.stdout)
            self.assertIn("names `harness-x`, absent from pi/", result.stdout)

    def test_antigravity_must_offer_the_same_harness_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "antigravity" / "harness-x").rename(root / "antigravity" / "harness-y")
            result = run([root / "bin" / "qstack", "check"])
            self.assertEqual(result.returncode, 1)
            self.assertIn("same skill names", result.stdout)
            self.assertIn("names `harness-x`, absent from antigravity/", result.stdout)


class Install(unittest.TestCase):
    def test_install_links_shared_and_one_harness(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([QSTACK, "install", "pi", "--dir", tmp])
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(os.path.realpath(Path(tmp) / "council"), str(ROOT / "shared" / "council"))
            self.assertEqual(os.path.realpath(Path(tmp) / "harness-delegation"),
                             str(ROOT / "pi" / "harness-delegation"))
            # Sibling-relative references resolve in the installed view.
            self.assertTrue((Path(tmp) / "full-stop" / ".." / "full-send" / "SKILL.md").exists())

    def test_existing_directory_is_a_conflict_and_is_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            mine = Path(tmp) / "council"
            mine.mkdir()
            (mine / "SKILL.md").write_text("mine")
            result = run([QSTACK, "install", "claude", "--dir", tmp, "--only", "council,full-send"])
            self.assertEqual(result.returncode, 1)
            self.assertIn("CONFLICT  council", result.stdout)
            self.assertEqual((mine / "SKILL.md").read_text(), "mine")
            self.assertTrue((Path(tmp) / "full-send").is_symlink())

    def test_switching_harness_relinks_and_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            run([QSTACK, "install", "pi", "--dir", tmp, "--only", "harness-config"])
            dry = run([QSTACK, "install", "claude", "--dir", tmp, "--only", "harness-config", "--dry-run"])
            self.assertIn("relinked", dry.stdout)
            self.assertIn("/pi/", os.path.realpath(Path(tmp) / "harness-config"))
            run([QSTACK, "install", "claude", "--dir", tmp, "--only", "harness-config"])
            self.assertIn("/claude/", os.path.realpath(Path(tmp) / "harness-config"))


class SystemPrompt(unittest.TestCase):
    def test_claude_home_gets_skills_and_a_rules_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "other-claude"
            result = run([QSTACK, "install", "claude", "--home", home])
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertTrue((home / "skills" / "council").is_symlink())
            self.assertEqual(os.path.realpath(home / "rules" / "qstack.md"),
                             str(ROOT / "claude" / "APPEND_SYSTEM.md"))
            status = run([QSTACK, "status", "claude", "--home", home])
            self.assertRegex(status.stdout, r"linked\s+system prompt")
            run([QSTACK, "uninstall", "claude", "--home", home])
            self.assertFalse((home / "rules" / "qstack.md").exists())

    def test_claude_config_dir_env_is_the_default_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {**os.environ, "CLAUDE_CONFIG_DIR": tmp}
            run([QSTACK, "install", "claude", "--only", "council"], env=env)
            self.assertTrue((Path(tmp) / "skills" / "council").is_symlink())

    def test_pi_profile_block_keeps_the_rest_of_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {**os.environ, "HOME": tmp}
            profile = Path(tmp) / ".config" / "pi" / "profiles" / "p"
            profile.mkdir(parents=True)
            append = profile / "APPEND_SYSTEM.md"
            append.write_text("# Mine\n\nKeep this.\n")
            args = ["pi", "--profile", "p"]
            self.assertEqual(run([QSTACK, "install", *args], env=env).returncode, 0)
            text = append.read_text()
            self.assertTrue(text.startswith("# Mine\n\nKeep this.\n"))
            self.assertIn("estimate-time", text)
            again = run([QSTACK, "install", *args], env=env)
            self.assertRegex(again.stdout, r"ok\s+system prompt")
            self.assertEqual(append.read_text(), text)
            self.assertRegex(run([QSTACK, "status", *args], env=env).stdout,
                             r"linked\s+system prompt")
            run([QSTACK, "uninstall", *args], env=env)
            self.assertEqual(append.read_text(), "# Mine\n\nKeep this.\n")

    def test_dir_and_no_system_leave_the_prompt_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIn("skipped", run([QSTACK, "install", "claude", "--dir", tmp]).stdout)
            home = Path(tmp) / "h"
            run([QSTACK, "install", "claude", "--home", home, "--no-system"])
            self.assertFalse((home / "rules").exists())


class MultipleHarnesses(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.env = {k: v for k, v in os.environ.items()
                    if k not in ("CLAUDE_CONFIG_DIR", "PI_CODING_AGENT_DIR")}
        self.env.update(HOME=str(self.home), XDG_DATA_HOME=str(self.home / ".local/share"))
        self.skills = {"claude": self.home / ".claude/skills",
                       "pi": self.home / ".pi/agent/skills",
                       "antigravity": self.home / ".gemini/config/skills"}

    def command(self, *args):
        return run([QSTACK, *args], env=self.env)

    def assert_installed(self, harnesses):
        for harness in harnesses:
            if harness == "antigravity":
                assert_copy(self, self.skills[harness] / "council", ROOT / "shared/council")
                assert_copy(self, self.skills[harness] / "harness-config",
                            ROOT / "antigravity/harness-config")
                continue
            self.assertEqual((self.skills[harness] / "council").resolve(), ROOT / "shared/council")
            self.assertEqual((self.skills[harness] / "harness-config").resolve(),
                             ROOT / harness / "harness-config")

    def test_bare_install_installs_all_harnesses(self):
        result = self.command("install")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assert_installed(self.skills)
        self.assertEqual((self.home / ".claude/rules/qstack.md").resolve(),
                         ROOT / "claude/APPEND_SYSTEM.md")
        for prompt in (".pi/agent/APPEND_SYSTEM.md", ".gemini/GEMINI.md"):
            self.assertIn("estimate-time", (self.home / prompt).read_text())

    def test_explicit_multiple_harnesses_install_status_and_uninstall(self):
        harnesses = ["claude", "pi", "antigravity"]
        installed = self.command("install", *harnesses)
        self.assertEqual(installed.returncode, 0, installed.stderr + installed.stdout)
        self.assert_installed(harnesses)
        status = self.command("status", *harnesses)
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertNotIn("missing", status.stdout)
        for harness, skills in self.skills.items():
            self.assertIn(f"{harness}: {skills}", status.stdout)
        removed = self.command("uninstall", *harnesses)
        self.assertEqual(removed.returncode, 0, removed.stderr)
        for skills in self.skills.values():
            self.assertFalse(os.path.lexists(skills / "council"))

    def test_subset_only_and_dry_run_apply_to_every_selected_harness(self):
        args = ["install", "claude", "antigravity", "--only", "council", "--no-system"]
        dry = self.command(*args, "--dry-run")
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual(list(self.home.iterdir()), [])
        installed = self.command(*args)
        self.assertEqual(installed.returncode, 0, installed.stderr)
        for harness in ("claude", "antigravity"):
            self.assertEqual({p.name for p in self.skills[harness].iterdir()}, {"council"})
        self.assertFalse((self.home / ".pi").exists())
        self.assertFalse((self.home / ".gemini/GEMINI.md").exists())

    def test_pi_uses_active_directory_before_discovering_profiles(self):
        profile = self.home / ".config/pi/profiles/other"
        profile.mkdir(parents=True)
        self.env["PI_CODING_AGENT_DIR"] = "~/active pi"
        result = self.command("install", "pi")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / "active pi/skills/harness-config").resolve(),
                         ROOT / "pi/harness-config")
        self.assertFalse((profile / "skills").exists())
        self.assertFalse((self.home / ".pi").exists())

    def test_pi_home_override_ignores_the_active_directory(self):
        self.env["PI_CODING_AGENT_DIR"] = str(self.home / "active")
        result = self.command("install", "pi", "--home", "~/custom pi")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / "custom pi/skills/harness-config").resolve(),
                         ROOT / "pi/harness-config")
        self.assertFalse((self.home / "active").exists())

    def test_bare_install_no_system_skips_all_prompts(self):
        result = self.command("install", "--no-system")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_installed(self.skills)
        for prompt in (".claude/rules/qstack.md", ".pi/agent/APPEND_SYSTEM.md", ".gemini/GEMINI.md"):
            self.assertFalse((self.home / prompt).exists())

    def test_pi_discovers_existing_profiles_without_an_active_directory(self):
        profiles = self.home / ".config/pi/profiles"
        for name in ("work", "main"):
            (profiles / name).mkdir(parents=True)
        (profiles / "not-a-profile").write_text("Ignore files.")
        result = self.command("install", "claude", "pi", "antigravity")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("main", "work"):
            self.assertEqual((profiles / name / "skills/harness-config").resolve(),
                             ROOT / "pi/harness-config")
            self.assertIn("estimate-time", (profiles / name / "APPEND_SYSTEM.md").read_text())
        self.assertFalse((self.home / ".pi").exists())

    def test_profile_option_in_a_batch_overrides_the_active_directory(self):
        self.env["PI_CODING_AGENT_DIR"] = str(self.home / "active")
        result = self.command("install", "claude", "pi", "antigravity", "--profile", "chosen")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / ".config/pi/profiles/chosen/skills/council").resolve(),
                         ROOT / "shared/council")
        self.assertFalse((self.home / "active").exists())
        self.assert_installed(["claude", "antigravity"])

    def test_invalid_or_ambiguous_targets_fail_before_writing(self):
        cases = [(["install", "claude", "pi", "--dir", str(self.home / "skills")],
                  "--dir requires exactly one harness"),
                 (["install", "--home", str(self.home / "custom")],
                  "--home requires exactly one harness"),
                 (["install", "antigravity", "--profile", "wrong"],
                  "--profile requires pi"),
                 (["install", "claude", "pi", "unknown"], "unknown harness"),
                 (["install", "claude", "--home", str(self.home / "a"),
                   "--dir", str(self.home / "b")], "--dir cannot be combined"),
                 (["install", "pi", "--home", str(self.home / "a"), "--profile", "b"],
                  "--home cannot be combined")]
        for args, error in cases:
            with self.subTest(args=args):
                result = self.command(*args)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(error, result.stderr)
                self.assertEqual(list(self.home.iterdir()), [])

    def test_unknown_skill_is_validated_for_the_whole_batch(self):
        result = self.command("install", "--only", "does-not-exist")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown skills", result.stderr)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_conflicts_fail_the_batch_but_other_targets_are_installed(self):
        mine = self.skills["claude"] / "council"
        mine.mkdir(parents=True)
        (mine / "SKILL.md").write_text("Mine.")
        result = self.command("install", "claude", "antigravity")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("CONFLICT  council", result.stdout)
        self.assertEqual((mine / "SKILL.md").read_text(), "Mine.")
        self.assert_installed(["antigravity"])

    def test_repeated_harness_is_processed_once(self):
        result = self.command("install", "claude", "claude", "--only", "council")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("linked    council"), 1)

    def test_status_and_uninstall_still_require_explicit_harnesses(self):
        for cmd in ("status", "uninstall"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.command(cmd).returncode, 2)
        self.assertEqual(list(self.home.iterdir()), [])


class Antigravity(unittest.TestCase):
    def test_default_home_works_without_a_cli_on_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Managed runtimes need not be on PATH. Keep only Python for QStack's shebang.
            bindir = Path(tmp) / "bin"
            bindir.mkdir()
            (bindir / "python3").symlink_to(shutil.which("python3"))
            env = {**os.environ, "HOME": tmp, "PATH": str(bindir),
                   "CLAUDE_CONFIG_DIR": str(Path(tmp) / "claude")}
            self.assertIsNone(shutil.which("antigravity", path=env["PATH"]))
            result = run([QSTACK, "install", "antigravity"], env=env)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            home = Path(tmp) / ".gemini"
            assert_copy(self, home / "config/skills/council", ROOT / "shared/council")
            assert_copy(self, home / "config/skills/harness-config",
                        ROOT / "antigravity/harness-config")
            self.assertIn("estimate-time", (home / "GEMINI.md").read_text())
            self.assertFalse((Path(tmp) / "claude").exists())

    def test_t3_private_profile_sees_the_same_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".gemini"
            profile = Path(tmp) / ".t3/userdata/providers/antigravity/account"
            # T3 links the user's global skills into its private GEMINI_HOME at startup.
            env = {**os.environ, "HOME": tmp, "GEMINI_HOME": str(profile)}
            result = run([QSTACK, "install", "antigravity"], env=env)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            (profile / "config").mkdir(parents=True)
            (profile / "config/skills").symlink_to(home / "config/skills", target_is_directory=True)
            self.assertEqual((profile / "config/skills/council/SKILL.md").read_text(),
                             (ROOT / "shared/council/SKILL.md").read_text())
            # Antigravity only reads skill files whose real path stays in a skills directory.
            self.assertEqual((profile / "config/skills/harness-delegation/SKILL.md").resolve(),
                             (home / "config/skills/harness-delegation/SKILL.md").resolve())
            self.assertFalse((profile / "GEMINI.md").exists())
            status = run([QSTACK, "status", "antigravity"], env=env)
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertNotIn("missing", status.stdout)

    def test_custom_home_install_status_and_uninstall_preserve_user_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "custom gemini"
            home.mkdir()
            prompt = home / "GEMINI.md"
            original = "# My rules\n\nKeep this.\n"
            prompt.write_text(original)
            args = ["antigravity", "--home", home]
            result = run([QSTACK, "install", *args])
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            text = prompt.read_text()
            self.assertTrue(text.startswith(original))
            self.assertEqual(text.count("<!-- qstack:begin -->"), 1)
            again = run([QSTACK, "install", *args])
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(prompt.read_text(), text)
            status = run([QSTACK, "status", *args])
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertNotIn("missing", status.stdout)
            self.assertNotIn("stale", status.stdout)
            removed = run([QSTACK, "uninstall", *args])
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertEqual(prompt.read_text(), original)
            self.assertFalse(os.path.lexists(home / "config/skills/council"))
            self.assertIn("missing", run([QSTACK, "status", *args]).stdout)

    def test_stale_prompt_is_updated_without_losing_surrounding_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            prompt = home / "GEMINI.md"
            prompt.write_text("Before.\n\n<!-- qstack:begin -->\nold\n<!-- qstack:end -->\nAfter.\n")
            args = ["antigravity", "--home", home]
            self.assertRegex(run([QSTACK, "status", *args]).stdout, r"stale\s+system prompt")
            result = run([QSTACK, "install", *args])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("updated", result.stdout)
            self.assertTrue(prompt.read_text().startswith("Before.\n\n"))
            self.assertTrue(prompt.read_text().endswith("After.\n"))
            self.assertNotIn("\nold\n", prompt.read_text())

    def test_dir_installs_skills_only_and_only_limits_the_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project/.agents/skills"
            args = ["antigravity", "--dir", dest, "--only", "council,harness-config"]
            result = run([QSTACK, "install", *args])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in dest.iterdir()}, {"council", "harness-config"})
            assert_copy(self, dest / "harness-config", ROOT / "antigravity/harness-config")
            self.assertRegex(run([QSTACK, "status", *args]).stdout, r"skipped\s+system prompt")
            result = run([QSTACK, "uninstall", *args])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(dest.iterdir()), [])
            self.assertFalse((dest.parent / "GEMINI.md").exists())

    def test_no_system_and_subset_leave_existing_prompt_alone(self):
        for flags in (["--no-system"], ["--only", "council"]):
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as tmp:
                prompt = Path(tmp) / "GEMINI.md"
                prompt.write_text("Mine.\n")
                result = run([QSTACK, "install", "antigravity", "--home", tmp, *flags])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(prompt.read_text(), "Mine.\n")

    def test_dry_run_does_not_create_a_home_or_remove_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "gemini"
            args = ["antigravity", "--home", home]
            result = run([QSTACK, "install", *args, "--dry-run"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(home.exists())
            self.assertEqual(run([QSTACK, "install", *args]).returncode, 0)
            before = (home / "GEMINI.md").read_text()
            result = run([QSTACK, "uninstall", *args, "--dry-run"])
            self.assertEqual(result.returncode, 0, result.stderr)
            assert_copy(self, home / "config/skills/council", ROOT / "shared/council")
            self.assertEqual((home / "GEMINI.md").read_text(), before)

    def test_conflicting_skill_directory_and_foreign_link_are_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            skills = home / "config/skills"
            (skills / "council").mkdir(parents=True)
            (skills / "council/SKILL.md").write_text("Mine.")
            foreign = home / "foreign"
            foreign.mkdir()
            (skills / "full-send").symlink_to(foreign, target_is_directory=True)
            args = ["antigravity", "--home", home, "--only", "council,full-send"]
            result = run([QSTACK, "install", *args])
            self.assertEqual(result.returncode, 1)
            self.assertIn("2 conflicts", result.stdout)
            status = run([QSTACK, "status", *args])
            self.assertRegex(status.stdout, r"conflict\s+council")
            self.assertRegex(status.stdout, r"foreign-link\s+full-send")
            self.assertEqual(run([QSTACK, "uninstall", *args]).returncode, 0)
            self.assertEqual((skills / "council/SKILL.md").read_text(), "Mine.")
            self.assertEqual((skills / "full-send").resolve(), foreign)

    def test_switching_from_another_harness_relinks_only_qstack_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run([QSTACK, "install", "pi", "--dir", tmp,
                                  "--only", "harness-config"]).returncode, 0)
            args = ["antigravity", "--dir", tmp, "--only", "harness-config"]
            dry = run([QSTACK, "install", *args, "--dry-run"])
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertIn("recopied", dry.stdout)
            self.assertEqual((Path(tmp) / "harness-config").resolve(), ROOT / "pi/harness-config")
            self.assertEqual(run([QSTACK, "install", *args]).returncode, 0)
            assert_copy(self, Path(tmp) / "harness-config", ROOT / "antigravity/harness-config")

    def test_old_links_and_changed_copies_are_replaced_with_current_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = Path(tmp) / "config/skills"
            skills.mkdir(parents=True)
            (skills / "council").symlink_to(ROOT / "shared/council", target_is_directory=True)
            args = ["antigravity", "--home", tmp, "--only", "council,deslop"]
            self.assertEqual(run([QSTACK, "install", *args]).returncode, 0)
            (skills / "deslop/SKILL.md").write_text("edited")
            self.assertRegex(run([QSTACK, "status", *args]).stdout, r"stale\s+deslop")
            result = run([QSTACK, "install", *args])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("recopied  deslop", result.stdout)
            assert_copy(self, skills / "council", ROOT / "shared/council")
            assert_copy(self, skills / "deslop", ROOT / "shared/deslop")
            self.assertEqual({p.name for p in skills.iterdir()}, {"council", "deslop"})

    def test_dir_without_subset_skips_system_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([QSTACK, "install", "antigravity", "--dir", tmp])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("skipped", result.stdout)
            self.assertTrue((Path(tmp) / "council/SKILL.md").is_file())
            self.assertFalse((Path(tmp) / "GEMINI.md").exists())

    def test_unknown_skill_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([QSTACK, "install", "antigravity", "--home", tmp,
                          "--only", "does-not-exist"])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown skills for antigravity", result.stderr)


class Orphans(unittest.TestCase):
    def test_orphans_detected_and_cleaned_without_touching_foreign_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = {k: v for k, v in os.environ.items()
                   if k not in ("CLAUDE_CONFIG_DIR", "PI_CODING_AGENT_DIR")}
            env.update(HOME=str(home), XDG_DATA_HOME=str(home / ".local/share"))
            repo = home / "repo"
            (repo / "bin").mkdir(parents=True)
            qstack = repo / "bin/qstack"
            shutil.copy(QSTACK, qstack)
            for name in ("alpha", "stay"):
                (repo / "shared" / name).mkdir(parents=True)
                (repo / "shared" / name / "SKILL.md").write_text(SKILL.format(name=name, body="Body."))
            for harness in ("claude", "pi", "antigravity"):
                (repo / harness).mkdir()
                (repo / harness / "APPEND_SYSTEM.md").write_text("Reminder.\n")

            self.assertEqual(run([qstack, "install"], env=env).returncode, 0)
            targets = [home / ".claude/skills", home / ".pi/agent/skills", home / ".gemini/config/skills"]
            chain = home / "chain-stay"
            chain.symlink_to(repo / "shared/stay")
            for dest in targets:
                (dest / "keep-me").mkdir()
                (dest / "keep-me/SKILL.md").write_text("Foreign.")
                (dest / "other-checkout").mkdir()
                (dest / "other-checkout/.qstack-source").write_text(f"{home}/other/shared/other-checkout\n")
            (targets[0] / "chained-stay").symlink_to(chain)

            # Rename alpha -> beta so alpha becomes orphaned across all three harnesses.
            (repo / "shared/alpha").rename(repo / "shared/beta")
            (repo / "shared/beta/SKILL.md").write_text(SKILL.format(name="beta", body="Renamed."))

            status = run([qstack, "status", "claude", "pi", "antigravity"], env=env)
            self.assertEqual(status.stdout.count("orphaned     alpha"), 3)
            self.assertNotIn("keep-me", status.stdout)
            self.assertNotIn("other-checkout", status.stdout)

            # --only and --dry-run leave orphans intact.
            self.assertEqual(run([qstack, "install", "--only", "stay"], env=env).returncode, 0)
            self.assertEqual(run([qstack, "install", "--dry-run"], env=env).returncode, 0)
            self.assertTrue(all(os.path.lexists(d / "alpha") for d in targets))
            self.assertNotEqual(run([qstack, "install", "--only", ""], env=env).returncode, 0)

            # Full install trashes orphans and installs beta while keeping foreign entries.
            res = run([qstack, "install"], env=env)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertEqual(res.stdout.count("removed   alpha (orphaned)"), 3)
            for dest in targets:
                self.assertFalse(os.path.lexists(dest / "alpha"))
                self.assertTrue((dest / "beta/SKILL.md").is_file())
                self.assertEqual((dest / "keep-me/SKILL.md").read_text(), "Foreign.")
                self.assertTrue((dest / "other-checkout").is_dir())
            self.assertTrue((targets[0] / "chained-stay").is_symlink())

            # Full uninstall also cleans newly orphaned skills and honors --no-system.
            (repo / "shared/beta").rename(home / "deleted-beta")
            rm = run([qstack, "uninstall", "claude", "pi", "antigravity", "--no-system"], env=env)
            self.assertEqual(rm.returncode, 0, rm.stderr)
            self.assertEqual(rm.stdout.count("removed   beta (orphaned)"), 3)
            self.assertTrue((home / ".claude/rules/qstack.md").is_symlink())
            for dest in targets:
                self.assertFalse(os.path.lexists(dest / "beta"))
                self.assertEqual((dest / "keep-me/SKILL.md").read_text(), "Foreign.")


if __name__ == "__main__":
    unittest.main()
