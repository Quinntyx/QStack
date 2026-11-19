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


def run(cmd, **kwargs):
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kwargs)


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
            self.assertEqual((home / "config/skills/council").resolve(), ROOT / "shared/council")
            self.assertEqual((home / "config/skills/harness-config").resolve(),
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
            self.assertEqual((profile / "config/skills/harness-delegation").resolve(),
                             ROOT / "antigravity/harness-delegation")
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
            self.assertFalse((home / "config/skills/council").is_symlink())
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
            self.assertEqual((dest / "harness-config").resolve(), ROOT / "antigravity/harness-config")
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
            self.assertTrue((home / "config/skills/council").is_symlink())
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
            self.assertIn("relinked", dry.stdout)
            self.assertEqual((Path(tmp) / "harness-config").resolve(), ROOT / "pi/harness-config")
            self.assertEqual(run([QSTACK, "install", *args]).returncode, 0)
            self.assertEqual((Path(tmp) / "harness-config").resolve(),
                             ROOT / "antigravity/harness-config")

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


if __name__ == "__main__":
    unittest.main()
