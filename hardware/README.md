# Hardware tooling and evidence status

The repository contains offline preflight utilities, exact approval guards and
separate runners for owner-approved exploratory pilots. The default development
environment does not contain `qiskit` or `qiskit-ibm-runtime`, so its Qiskit
adapter tests are skipped rather than treated as passing evidence.

HW-P2 was executed by the owner on `ibm_marrakesh`. Its stored report provides
exploratory G0 evidence: fractional RZZ gates were exposed, submitted circuits
passed ISA checks and repeated RZZ operations were retained. The pilot
certificates were inconclusive because the model-adequacy diagnostic triggered;
this is not a G5 confirmatory result.

HW-P3 has a separate owner approval and prespecified exploratory protocol. A
selection file alone is not hardware-result evidence; a raw-output bundle and
analysis report are required before HW-P3 can be described as executed.

No exploratory approval substitutes for the G4 freeze required before G5-G6.
