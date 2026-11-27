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



ALLOWED_POST_APPROVAL_PREFIXES = ("docs/decisions/", "results/", "plan/handoffs/", "hardware/private/")


def _git(repo: Path, *args: str) -> str:
    import subprocess

    completed = subprocess.run(["git", *args], cwd=repo, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise ApprovalError(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def verify_pilot_approval(repo: Path, approval_path: Path, script_path: Path) -> dict[str, object]:
    """Approval for a pilot runner that lives in the approved commit.

    The approval record is committed after the commit it names, so the named
    commit must be an ancestor of HEAD and every file changed since then must
    sit under ALLOWED_POST_APPROVAL_PREFIXES. The script hash must match, and
    tracked files outside those prefixes must have no uncommitted changes.
    """
    resolved = approval_path.resolve()
    decisions = (repo / "docs" / "decisions").resolve()
    if decisions not in resolved.parents or not resolved.is_file():
        raise ApprovalError("approval must exist under docs/decisions")
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    required = {"approved", "commit", "script", "script_sha256", "backends", "issued_by", "scope"}
    missing = required - payload.keys()
    if missing:
        raise ApprovalError(f"approval is missing fields: {sorted(missing)}")
    if payload["approved"] is not True or payload["issued_by"] != "Zhen-Jun Liu":
        raise ApprovalError("approval is not an affirmative owner approval")
    commit = str(payload["commit"])
    head = _git(repo, "rev-parse", "HEAD")
    if commit != head:
        _git(repo, "merge-base", "--is-ancestor", commit, head)
        changed = [line for line in _git(repo, "diff", "--name-only", commit, head).splitlines() if line]
        offending = [name for name in changed if not name.startswith(ALLOWED_POST_APPROVAL_PREFIXES)]
        if offending:
            raise ApprovalError(f"files changed since the approved commit: {offending}")
    dirty = [line[3:] for line in _git(repo, "status", "--porcelain", "--untracked-files=no").splitlines() if line]
    dirty = [name for name in dirty if not name.startswith(ALLOWED_POST_APPROVAL_PREFIXES)]
    if dirty:
        raise ApprovalError(f"uncommitted changes outside allowed paths: {dirty}")
    relative = script_path.resolve().relative_to(repo.resolve()).as_posix()
    if payload["script"] != relative or payload["script_sha256"] != file_sha256(script_path):
        raise ApprovalError("approval names a different script or script hash")
    return payload
