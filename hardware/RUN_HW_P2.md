# Running HW-P2 on IBM Quantum (owner only)

Everything below runs on the owner's computer. No agent handles the token.

## 1. Environment (once)

```powershell
cd C:\Users\wits\Documents\Codex\2026-11-27\new-chat\decision-relevant-rzz-certification
py -3.12 -m venv .venv-hw          # use 3.12 or 3.13; Qiskit wheels may lag newer Pythons
.\.venv-hw\Scripts\Activate.ps1
pip install -r requirements-hardware.txt
python -m unittest discover -s tests   # qiskit tests run here instead of skipping
```

## 2. Save each account once (type the token yourself)

```powershell
python -c "from qiskit_ibm_runtime import QiskitRuntimeService as S; S.save_account(channel='ibm_quantum_platform', token=input('token: '), instance=input('instance CRN: '), name='acctA')"
python -c "from qiskit_ibm_runtime import QiskitRuntimeService as S; S.save_account(channel='ibm_quantum_platform', token=input('token: '), instance=input('instance CRN: '), name='acctB')"
```

## 3. Dry run, then submit

```powershell
python -m hardware.run_hw_p2 --label A                       # no network
python -m hardware.run_hw_p2 --label A --submit --account acctA --backend ibm_marrakesh --max-qpu-seconds 420
# later (>= 1 h if possible):
python -m hardware.run_hw_p2 --label B --submit --account acctB --backend ibm_marrakesh --max-qpu-seconds 420
```

If `ibm_marrakesh` is not available to an account, use another Heron backend
named in the approval (`ibm_fez`, `ibm_kingston`, `ibm_torino`, `ibm_aachen`,
`ibm_boston`); account B must use the same backend as account A.

Set `--max-qpu-seconds` to what you are willing to spend. The runner prints
measured seconds after each block and stops before a block that would exceed
the cap. Re-running the same command resumes and skips finished blocks.

## 4. Analysis

```powershell
python -m analysis.hardware.analyze_hw_p2 > results\hw_p2\analysis_raw.json
```

Then commit `results/hw_p2/` (never `hardware/private/`).
