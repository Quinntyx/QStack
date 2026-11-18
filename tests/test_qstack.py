"""Run with: python3 -m unittest discover -s tests"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSTACK = ROOT / "bin" / "qstack"
COUNCIL_LOG = ROOT / "shared" / "council" / "bin" / "council-log"

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


class CouncilLog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = {**os.environ, "QSTACK_STATE": self.tmp.name}

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, rec):
        return run([COUNCIL_LOG, "record", "-"], input=json.dumps(rec), env=self.env)

    def round(self, n, better, a, b):
        def model(name, counts, score):
            keys = ("raised", "confirmed", "refuted", "unique", "missed")
            return {"model": name, "verdict": "CHANGES", "score": score, **dict(zip(keys, counts))}
        return {"run": "r", "subject": "PR", "mode": "converge", "attempt": 1, "round": n,
                "outcome": "continue", "seats": [
                    {"seat": "sol", "tier": "voting", "verdict": "CHANGES", "better": better,
                     "models": [model("gpt-6.2-sol", a, 7), model("gpt-6.1-sol", b, 8)]},
                    {"seat": "glm", "tier": "jester", "verdict": None,
                     "models": [{"model": "glm-5.3", "absent": True}]}]}

    def test_summary_aggregates_pairs_and_absences(self):
        self.assertEqual(self.record(self.round(1, "gpt-6.2-sol", (4, 3, 1, 2, 0), (1, 1, 0, 0, 2))).returncode, 0)
        self.assertEqual(self.record(self.round(2, "tie", (2, 1, 1, 0, 1), (2, 2, 0, 1, 0))).returncode, 0)
        rows = {r["model"]: r for r in json.loads(
            run([COUNCIL_LOG, "summary", "--json"], env=self.env).stdout)}
        new, old, jester = rows["gpt-6.2-sol"], rows["gpt-6.1-sol"], rows["glm-5.3"]
        self.assertEqual((new["rounds"], new["raised"], new["confirmed"], new["unique"], new["missed"]),
                         (2, 6, 4, 2, 1))
        self.assertEqual((new["better"], new["paired"], new["ties"], new["precision"]), (1, 2, 1, 0.67))
        self.assertEqual((old["better"], old["missed"], old["avg_score"]), (0, 2, 8.0))
        self.assertEqual((jester["rounds"], jester["absent"], jester["tiers"]), (0, 2, ["jester"]))
        self.assertIn("1/2 (1 tie)", run([COUNCIL_LOG, "summary"], env=self.env).stdout)

    def test_invalid_records_are_rejected_and_not_written(self):
        bad = self.round(1, "gpt-9", (1, 3, 0, 0, 0), (1, 1, 0, 0, 0))
        result = self.record(bad)
        self.assertEqual(result.returncode, 1)
        self.assertIn("`better` must be `tie` or one of its models", result.stderr)
        self.assertIn("confirmed + refuted exceeds raised", result.stderr)
        self.assertFalse((Path(self.tmp.name) / "council" / "rounds.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
