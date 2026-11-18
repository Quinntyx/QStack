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


if __name__ == "__main__":
    unittest.main()
