#!/usr/bin/env python3
"""Fail-closed integrity gate for the published GROD audit dossier."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL_EMAIL = "37579156+MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_CLAIMS = {
    "C1": "INCONCLUSIVE_SOURCE_AUDIT_TOY",
    "C2": "UNVERIFIED_PAPER_REPORTED_ONLY",
    "C3": "UNVERIFIED_SOURCE_CLAIM_MISMATCH",
    "C4": "UNVERIFIED_THEOREM_SOURCE_AUDITED",
    "C5": "UNVERIFIED_ABLATION_PAPER_REPORTED_ONLY",
    "C6": "UNVERIFIED_BENCHMARK_MATRIX_ABSENT",
}


def stop(message: str) -> None:
    raise SystemExit(f"FINAL_AUDIT=FAILED reason={message}")


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )
    if result.returncode:
        stop(f"git {' '.join(args)}")
    return result.stdout.strip()


def load_json(relative: str):
    path = ROOT / relative
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        stop(f"invalid_json:{relative}:{exc}")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_sum_file(relative: str) -> None:
    checksum_path = ROOT / relative
    base = checksum_path.parent
    for raw in checksum_path.read_text().splitlines():
        if not raw.strip():
            continue
        expected, name = raw.split(maxsplit=1)
        name = name.lstrip("*")
        target = (base / name).resolve()
        if ROOT not in target.parents and target != ROOT:
            stop(f"checksum_path_escape:{relative}:{name}")
        if not target.is_file() or digest(target) != expected:
            stop(f"checksum_mismatch:{relative}:{name}")


def verify_manifest() -> None:
    manifest = load_json("EVIDENCE_MANIFEST.json")
    files = manifest.get("files")
    excluded = set(manifest.get("excluded", []))
    if not isinstance(files, dict):
        stop("manifest_files_missing")
    actual = set(run_git("ls-files").splitlines()) - excluded
    if set(files) != actual:
        stop("manifest_file_set_mismatch")
    for relative, expected in files.items():
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            stop(f"manifest_hash_mismatch:{relative}")


def main() -> None:
    required = [
        "README.md",
        "STATUS.md",
        "AUTONOMOUS_STATE.json",
        "contract/metadata.json",
        "contract/live_claims.json",
        "contract/contract_manifest.json",
        "evidence/source/arxiv-2406.12915.pdf",
        "evidence/source/arxiv-2406.12915-source.tar.gz",
        "evidence/source/SHA256SUMS",
        "outputs/claim1_source_audit/SHA256SUMS",
        "outputs/claim1_synthetic_grod_toy/SHA256SUMS",
        "CLAIM_EVIDENCE.md",
        "SOURCE_AUDIT.md",
        "ENVIRONMENT.md",
        "REPORT.md",
        "BRANCH_AUDIT.md",
        "CITATION.cff",
        "AUTHOR_THANK_YOU.md",
        "claims.json",
        "reproduction_verdicts.json",
        "verify_final.py",
        "EVIDENCE_MANIFEST.json",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            stop(f"missing:{relative}")

    if run_git("branch", "--show-current") != "main":
        stop("branch_is_not_main")
    branches = [x for x in run_git("branch", "--format=%(refname:short)").splitlines() if x]
    if branches != ["main"]:
        stop("local_branches_are_not_main_only")
    if subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", "refs/original/refs/heads/main"],
        cwd=ROOT,
        check=False,
    ).returncode == 0:
        stop("refs_original_remains")
    if run_git("remote", "get-url", "origin") != "https://github.com/MachineLearning-Nerd/icml26-grod-ood-detection-transformers.git":
        stop("origin_is_not_canonical")
    if run_git("status", "--porcelain"):
        stop("working_tree_not_clean")

    commits = run_git("log", "--format=%an\t%ae\t%cn\t%ce").splitlines()
    if not commits:
        stop("no_commits")
    for row in commits:
        author_name, author_email, committer_name, committer_email = row.split("\t")
        if (author_name, author_email, committer_name, committer_email) != (
            "MachineLearning-Nerd",
            CANONICAL_EMAIL,
            "MachineLearning-Nerd",
            CANONICAL_EMAIL,
        ):
            stop("noncanonical_commit_identity")
    if "co-authored-by:" in run_git("log", "--format=%B").lower():
        stop("coauthor_trailer_present")

    metadata = load_json("contract/metadata.json")
    if metadata.get("orid") != "94FOsjgeHK" or metadata.get("arxiv") != "2406.12915":
        stop("contract_metadata_mismatch")
    live_claims = load_json("contract/live_claims.json")
    if len(live_claims) != 6 or any(claim.get("status") != "unverified" for claim in live_claims):
        stop("live_claims_are_not_unverified")
    claims = load_json("claims.json")
    statuses = {claim.get("id"): claim.get("status") for claim in claims.get("claims", [])}
    if statuses != EXPECTED_CLAIMS:
        stop("claim_verdicts_mismatch")
    verdicts = load_json("reproduction_verdicts.json")
    if verdicts.get("claims") != EXPECTED_CLAIMS or verdicts.get("publication_allowed") is not False:
        stop("reproduction_verdicts_mismatch")
    state = load_json("AUTONOMOUS_STATE.json")
    if state.get("phase") != "published_and_verified" or state.get("publication_allowed") is not False:
        stop("state_not_published_and_closed")
    if state.get("overall_verdict") != "INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY":
        stop("state_overall_verdict_mismatch")

    verify_sum_file("evidence/source/SHA256SUMS")
    verify_sum_file("outputs/claim1_source_audit/SHA256SUMS")
    verify_sum_file("outputs/claim1_synthetic_grod_toy/SHA256SUMS")
    archive = ROOT / "evidence/source/arxiv-2406.12915-source.tar.gz"
    required_members = {
        "00README.json",
        "content/3_theory.tex",
        "content/5_grod.tex",
        "content/6_experiment.tex",
        "content/8_app.tex",
    }
    with tarfile.open(archive, "r:gz") as handle:
        members = {member.name for member in handle.getmembers()}
        for member in members:
            if member.startswith("/") or ".." in Path(member).parts:
                stop("unsafe_source_archive_member")
        if not required_members <= members:
            stop("source_archive_members_missing")

    verify_manifest()
    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(branches)} commits={len(commits)} "
        "C1:inconclusive_toy C2:unverified C3:unverified "
        "C4:unverified C5:unverified C6:unverified publication_allowed=false"
    )


if __name__ == "__main__":
    main()

