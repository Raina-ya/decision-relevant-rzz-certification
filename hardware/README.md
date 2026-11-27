# Hardware preflight status

Only offline preflight utilities exist. They inspect local package availability,
create semantic circuit receipts, and verify the future approval contract.
They do not instantiate `QiskitRuntimeService`, query a backend, or submit a
job.

G0 remains open because Qiskit and `qiskit-ibm-runtime` are not installed in
the current environment, and backend fractional-gate support has not been
queried. `run_hardware.py` is deliberately fail-closed and contains no
submission adapter.

