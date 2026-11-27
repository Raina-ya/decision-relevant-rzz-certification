import json
import math
from pathlib import Path
import tempfile
import unittest

from hardware.approval import ApprovalError, file_sha256, verify_hardware_approval
from hardware.preflight import circuit_receipt, offline_capability_receipt, write_dry_run_receipt
from src.types import ProbeKey


class OfflinePreflightTests(unittest.TestCase):
    def test_capability_check_is_explicitly_offline(self):
        repo = Path(__file__).resolve().parents[1]
        receipt = offline_capability_receipt(repo)
        self.assertFalse(receipt.network_queried)
        self.assertFalse(receipt.hardware_job_submitted)
        if (repo / ".git").exists():
            self.assertIsNotNone(receipt.git_commit)
        else:
            # Exported source trees (git archive, sdist) have no commit to record.
            self.assertIsNone(receipt.git_commit)

    def test_circuit_receipt_preserves_repetition(self):
        receipt = circuit_receipt(ProbeKey(math.pi / 8, 16, 0, 1, 0.0))
        self.assertEqual(receipt.rzz_count, 16)
        self.assertEqual(len(receipt.circuit_hash), 64)

    def test_dry_run_receipt_round_trips(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "receipt.json"
            write_dry_run_receipt(output, repo, (ProbeKey(math.pi / 4, 2, 1, 2, 0.0),))
            payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(len(payload["circuits"]), 1)
        self.assertFalse(payload["capability"]["hardware_job_submitted"])


class ApprovalGuardTests(unittest.TestCase):
    def test_missing_approval_is_rejected(self):
        repo = Path(__file__).resolve().parents[1]
        with self.assertRaises(ApprovalError):
            verify_hardware_approval(
                repo,
                repo / "docs" / "decisions" / "missing.json",
                repo / "hardware" / "run_hardware.py",
                "deadbeef",
            )

    def test_exact_approval_contract_can_be_verified_in_isolated_repo(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            decisions = repo / "docs" / "decisions"
            hardware = repo / "hardware"
            decisions.mkdir(parents=True)
            hardware.mkdir()
            script = hardware / "runner.py"
            script.write_text("print('locked')\n", encoding="utf-8")
            approval = decisions / "hardware.json"
            approval.write_text(
                json.dumps(
                    {
                        "approved": True,
                        "commit": "abc123",
                        "script": "hardware/runner.py",
                        "script_sha256": file_sha256(script),
                        "backend": "example_backend",
                        "issued_by": "Zhen-Jun Liu",
                    }
                ),
                encoding="utf-8",
            )
            payload = verify_hardware_approval(repo, approval, script, "abc123")
            self.assertEqual(payload["backend"], "example_backend")

    def test_hash_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            decisions = repo / "docs" / "decisions"
            hardware = repo / "hardware"
            decisions.mkdir(parents=True)
            hardware.mkdir()
            script = hardware / "runner.py"
            script.write_text("print('changed')\n", encoding="utf-8")
            approval = decisions / "hardware.json"
            approval.write_text(
                json.dumps(
                    {
                        "approved": True,
                        "commit": "abc123",
                        "script": "hardware/runner.py",
                        "script_sha256": "0" * 64,
                        "backend": "example_backend",
                        "issued_by": "Zhen-Jun Liu",
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ApprovalError):
                verify_hardware_approval(repo, approval, script, "abc123")


if __name__ == "__main__":
    unittest.main()

