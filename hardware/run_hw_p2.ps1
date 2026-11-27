# One-click HW-P2 run for one account (owner only). Usage, from any folder:
#   powershell -ExecutionPolicy Bypass -File hardware\run_hw_p2.ps1 -Label A -MaxQpuSeconds 420
#   powershell -ExecutionPolicy Bypass -File hardware\run_hw_p2.ps1 -Label B -MaxQpuSeconds 420
# The IBM token is typed into a hidden prompt and saved only in your user
# profile by qiskit-ibm-runtime; it never enters the repository.
param(
    [ValidateSet("A", "B")][string]$Label = "A",
    [string]$Account = "",
    [string]$Backend = "ibm_marrakesh",
    [double]$MaxQpuSeconds = 420
)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($Account -eq "") { $Account = "acct$Label" }

if (-not (Test-Path ".venv-hw\Scripts\python.exe")) {
    $made = $false
    foreach ($v in @("3.12", "3.13", "3.11")) {
        try { py -$v -m venv .venv-hw; if ($LASTEXITCODE -eq 0) { $made = $true; break } } catch {}
    }
    if (-not $made) { throw "Need Python 3.11-3.13 (install from python.org), then rerun." }
}
$py = ".\.venv-hw\Scripts\python.exe"
& $py -m pip install -q --upgrade pip
& $py -m pip install -q -r requirements-hardware.txt

& $py -c "import sys; from qiskit_ibm_runtime import QiskitRuntimeService as S; sys.exit(0 if '$Account' in S.saved_accounts() else 1)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Saving IBM Quantum account '$Account' (token prompt is hidden)."
    & $py -c "import getpass; from qiskit_ibm_runtime import QiskitRuntimeService as S; S.save_account(channel='ibm_quantum_platform', token=getpass.getpass('IBM Quantum API key: '), instance=(input('Instance CRN (Enter to skip): ') or None), name='$Account', overwrite=True)"
}

Write-Host "== dry run (no network)"
& $py -m hardware.run_hw_p2 --label $Label
Write-Host "== submit: account $Account, backend $Backend, cap $MaxQpuSeconds s"
& $py -m hardware.run_hw_p2 --label $Label --submit --account $Account --backend $Backend --max-qpu-seconds $MaxQpuSeconds
if ($LASTEXITCODE -ne 0) { throw "submission stopped; see the message above" }

Write-Host "== prespecified analysis"
New-Item -ItemType Directory -Force -Path results\hw_p2 | Out-Null
& $py -m analysis.hardware.analyze_hw_p2 | Out-File -Encoding utf8 "results\hw_p2\analysis_raw_$Label.json"
git add results/hw_p2
git commit -m "Record HW-P2 results for account $Label"
Write-Host "Done. Push when ready: git push"
