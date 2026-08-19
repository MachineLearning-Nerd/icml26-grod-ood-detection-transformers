# Status

- Paper: **How Out-of-Distribution Detection Learning Theory Enhances Transformer: Learnability and Reliability**.
- OpenReview ID: `94FOsjgeHK`; arXiv: `2406.12915`; six anchored claims / 12 maximum points.
- Overall verdict: `INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY`.
- Claim 1: source-table arithmetic plus a reduced 2-D feature-space GROD-style toy; not a ViT/CIFAR/OpenOOD reproduction.
- Claims 2–6: unverified; C3's contract numbers, C4's theorem label, and C5's ablation wording are reconciled against the pinned source in `CLAIM_EVIDENCE.md` and `SOURCE_AUDIT.md`.
- Official implementation: `yjzscode/GROD-OOD-Detection-with-Transformers` at `f64b493e38def879b96b3adf2282846fdec80bbb`; inspected, not executed end-to-end.
- Compute: local CPU/local GTX 1050 only; no HF Jobs, paid, remote, or upgraded compute.
- Repository: canonical `MachineLearning-Nerd/icml26-grod-ood-detection-transformers`; former name: `icml26-repro-94FOsjgeHK-ood-learning-theory-transformers`.
- Branch: one published `main` branch; history attribution is canonical `MachineLearning-Nerd`.
- Publication gate: `publication_allowed=false` for paper-scale claims.
- Final gate: run `python3 verify_final.py`; it checks source/output hashes, contract statuses, archive members, branch state, attribution, and the evidence manifest.

