"""Approval verification for any future hardware submission adapter."""

from hashlib import sha256
import json
from pathlib import Path


class ApprovalError(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def verify_hardware_approval(
    repo: Path,
    approval_path: Path,
    script_path: Path,
    current_commit: str,
) -> dict[str, object]:
    decisions = (repo / "docs" / "decisions").resolve()
    resolved_approval = approval_path.resolve()
    if decisions not in resolved_approval.parents:
        raise ApprovalError("approval must be stored under docs/decisions")
    if not resolved_approval.is_file():
        raise ApprovalError("approval file is missing")
    payload = json.loads(resolved_approval.read_text(encoding="utf-8"))
    required = {"approved", "commit", "script", "script_sha256", "backend", "issued_by"}
    missing = required - payload.keys()
    if missing:
        raise ApprovalError(f"approval is missing fields: {sorted(missing)}")
    if payload["approved"] is not True:
        raise ApprovalError("approval is not affirmative")
    if payload["issued_by"] != "Zhen-Jun Liu":
        raise ApprovalError("approval was not issued by the owner")
    if payload["commit"] != current_commit:
        raise ApprovalError("approval commit does not match the checked-out commit")
    relative_script = script_path.resolve().relative_to(repo.resolve()).as_posix()
    if payload["script"] != relative_script:
        raise ApprovalError("approval names a different script")
    if payload["script_sha256"] != file_sha256(script_path):
        raise ApprovalError("approved script hash does not match")
    if not isinstance(payload["backend"], str) or not payload["backend"]:
        raise ApprovalError("approval backend must be a non-empty string")
    return payload

