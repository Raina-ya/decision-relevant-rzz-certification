import importlib.util
from math import pi
import unittest

from src.types import CircuitKind, ProbeKey

HAVE_QISKIT = (
    importlib.util.find_spec("qiskit") is not None
    and importlib.util.find_spec("qiskit_ibm_runtime") is not None
)


@unittest.skipUnless(HAVE_QISKIT, "qiskit and qiskit-ibm-runtime not installed")
class QiskitAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from qiskit_ibm_runtime.fake_provider import FakeMarrakesh

        from src.qiskit_adapter import fractional_target

        cls.target = fractional_target(FakeMarrakesh().target)
        cls.pair = next(iter(cls.target["rzz"].keys()))

    def _isa(self, key):
        from src.qiskit_adapter import build_probe_circuit, rzz_duration_seconds, to_isa

        circuit = build_probe_circuit(key, rzz_duration_seconds(self.target, self.pair))
        return to_isa(circuit, self.target, self.pair)

    def test_repeated_rzz_is_not_merged_or_folded(self):
        from src.qiskit_adapter import verify_isa_probe

        for theta in (pi / 16, 0.6118624420100085, pi / 2):
            key = ProbeKey(theta, 16, 1, 2, pi / 2)
            report = verify_isa_probe(self._isa(key), key, self.pair)
            self.assertTrue(report.ok, report.detail)

    def test_delay_and_zero_circuits_have_no_rzz(self):
        from src.qiskit_adapter import verify_isa_probe

        for key in (
            ProbeKey(pi / 4, 4, 0, 1, 0.0, CircuitKind.DELAY),
            ProbeKey(pi / 4, 0, 0, 1, pi, CircuitKind.ZERO),
        ):
            report = verify_isa_probe(self._isa(key), key, self.pair)
            self.assertTrue(report.ok, report.detail)

    def test_noiseless_isa_probe_recovers_injected_residual(self):
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector

        from src.model import cycle_phase
        from src.probes import ANALYSIS_PHASES

        theta, epsilon, k = 0.6118624420100085, 0.013, 8

        def phase_of(kind, kk, control):
            signals = []
            for analysis in ANALYSIS_PHASES:
                key = ProbeKey(theta, kk, control, 1, analysis, kind)
                isa = self._isa(key)
                local = {self.pair[0]: 0, self.pair[1]: 1}
                perturbed = QuantumCircuit(2)
                for instruction in isa.data:
                    operation = instruction.operation
                    if operation.name in ("measure", "barrier", "delay"):
                        continue
                    qubits = [local[isa.find_bit(q).index] for q in instruction.qubits]
                    if operation.name == "rzz":
                        operation = operation.__class__(float(operation.params[0]) + epsilon)
                    perturbed.append(operation, qubits)
                probabilities = Statevector(perturbed).probabilities_dict(qargs=[0])
                signals.append(2.0 * probabilities.get("0", 0.0) - 1.0)
            return cycle_phase(tuple(signals))

        # The semantic preparation/analysis convention carries a fixed reference
        # offset; the k=0 circuits measure it and the analysis subtracts it.
        for control in (0, 1):
            offset = phase_of(CircuitKind.ZERO, 0, control)
            residual = phase_of(CircuitKind.PROBE, k, control) - offset
            expected = k * (epsilon if control == 0 else -epsilon)
            self.assertAlmostEqual(residual, expected, places=9)

if __name__ == "__main__":
    unittest.main()
