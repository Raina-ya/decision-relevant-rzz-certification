import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from hardware.approval import ApprovalError, _dirty_paths, file_sha256, verify_pilot_approval


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


class PilotApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "hardware" / "dry_run").mkdir(parents=True)
        (self.repo / "docs" / "decisions").mkdir(parents=True)
        (self.repo / "hardware" / "run.py").write_text("print(1)\n")
        (self.repo / "hardware" / "dry_run" / "s.json").write_text("{}\n")
        (self.repo / "src.py").write_text("x = 1\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "base")
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, capture_output=True, text=True).stdout.strip()
        self.approval = self.repo / "docs" / "decisions" / "a.json"
        self.approval.write_text(json.dumps({
            "approved": True, "issued_by": "Zhen-Jun Liu", "scope": "test", "commit": head,
            "script": "hardware/run.py", "script_sha256": file_sha256(self.repo / "hardware" / "run.py"),
            "backends": ["x"]}))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "approval")

    def tearDown(self):
        self.tmp.cleanup()

    def test_dirty_path_keeps_first_character(self):
        (self.repo / "hardware" / "dry_run" / "s.json").write_text('{"t": 1}\n')
        self.assertEqual(_dirty_paths(self.repo), ["hardware/dry_run/s.json"])

    def test_regenerated_dry_run_does_not_block(self):
        (self.repo / "hardware" / "dry_run" / "s.json").write_text('{"t": 2}\n')
        verify_pilot_approval(self.repo, self.approval, self.repo / "hardware" / "run.py")

    def test_code_change_blocks(self):
        (self.repo / "src.py").write_text("x = 2\n")
        with self.assertRaises(ApprovalError):
            verify_pilot_approval(self.repo, self.approval, self.repo / "hardware" / "run.py")


if __name__ == "__main__":
    unittest.main()
