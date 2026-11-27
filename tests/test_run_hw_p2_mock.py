import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

HAVE_QISKIT = (
    importlib.util.find_spec("qiskit") is not None
    and importlib.util.find_spec("qiskit_ibm_runtime") is not None
)


class _Counts:
    def __init__(self, n):
        self.n = n

    def get_counts(self):
        return {"00": self.n}


class _Pub:
    def __init__(self, circuit, shots):
        creg = circuit.cregs[0].name
        self.data = type("D", (), {creg: _Counts(shots)})()


class _Job:
    counter = 0

    def __init__(self, pubs, shots):
        _Job.counter += 1
        self._id = f"mock-{_Job.counter}"
        self._pubs = [_Pub(p[0], shots) for p in pubs]
        self._seconds = 1e-4 * shots * len(pubs)

    def job_id(self):
        return self._id

    def result(self):
        return self._pubs

    def usage(self):
        return self._seconds


class _Options:
    def __init__(self):
        self.dynamical_decoupling = type("x", (), {})()
        self.twirling = type("y", (), {})()


class _Sampler:
    def __init__(self, mode):
        self.options = _Options()

    def run(self, pubs, shots):
        assert len(pubs) <= 290
        return _Job(pubs, shots)


@unittest.skipUnless(HAVE_QISKIT, "qiskit and qiskit-ibm-runtime not installed")
class RunnerMockTests(unittest.TestCase):
    def test_submit_writes_blocks_respects_cap_and_keeps_job_ids_private(self):
        from qiskit_ibm_runtime.fake_provider import FakeMarrakesh

        import hardware.run_hw_p2 as runner
        from src.qiskit_adapter import fractional_target

        target = fractional_target(FakeMarrakesh().target)
        backend = type("B", (), {"target": target, "name": "ibm_mock"})()
        service = mock.MagicMock()
        service.return_value.backend.return_value = backend
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            shutil.copytree(runner.REPO / "analysis", repo / "analysis")
            with mock.patch.object(runner, "REPO", repo), \
                 mock.patch.object(runner, "FAMILY", repo / "analysis" / "tolerance" / "instances_development.json"), \
                 mock.patch.object(runner, "verify_pilot_approval", return_value={"commit": "abc", "backends": ["ibm_mock"]}), \
                 mock.patch("qiskit_ibm_runtime.QiskitRuntimeService", service), \
                 mock.patch("qiskit_ibm_runtime.SamplerV2", _Sampler):
                runner.submit("A", "acct", "ibm_mock", max_seconds=60.0, only=None)
            written = sorted(p.name for p in (repo / "results" / "hw_p2" / "A").glob("*.json"))
            self.assertIn("selection.json", written)
            self.assertIn("A0-calibration.json", written)
            self.assertIn("A1-decision-2q.json", written)
            a1 = json.loads((repo / "results" / "hw_p2" / "A" / "A1-decision-2q.json").read_text())
            self.assertEqual(len(a1["records"]), 364)
            self.assertNotIn("job_id", json.dumps(a1))
            self.assertNotIn("A3-grid.json", written)  # stopped by the 60 s cap
            log = json.loads((repo / "hardware" / "private" / "A_jobs.json").read_text())
            self.assertTrue(all(entry["job_ids"] for entry in log))


if __name__ == "__main__":
    unittest.main()
