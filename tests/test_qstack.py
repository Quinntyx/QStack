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
                                   ("claude", "harness-x", "Claude."), ("pi", pi_name, "Pi.")]:
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


if __name__ == "__main__":
    unittest.main()
