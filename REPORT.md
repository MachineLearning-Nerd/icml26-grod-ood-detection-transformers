# Reproduction report

## Result

`INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY`

The repository is a trustworthy source-pinned audit, not a full reproduction. C1 has source-table arithmetic plus a reduced mechanism toy. C2–C6 remain unverified for the paper-scale experiments and theory.

| Claim | Local evidence | Verdict |
| --- | --- | --- |
| C1 | Source values 21.97 → 0.12; 2-D three-seed GROD-style toy | Inconclusive; toy only |
| C2 | Paper table location and values pinned | Unverified |
| C3 | Author path and BERT/GPT-2 table inspected; contract/source numbers differ | Unverified; mismatch recorded |
| C4 | Theorem source location and label discrepancy recorded | Unverified |
| C5 | Source parameter ablation and combined toy mechanics recorded | Unverified |
| C6 | Comparison protocol and methods recorded; no matrix outputs | Unverified |

## Publication gate

`publication_allowed: false` for any claim that this repository reproduced the paper's ViT, language-model, theorem, or benchmark results.

## What would change the verdict

The next useful work is a source/contract reconciliation for C3–C5, followed by paper-scale runs only when the exact checkpoints, datasets, dependencies, and compute budget are available. Any new result must add deterministic outputs, controls, configuration, and hashes to the relevant claim directory.

