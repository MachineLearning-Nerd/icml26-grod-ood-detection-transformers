# Source and implementation audit

## Pinned paper artifacts

| Artifact | SHA-256 |
| --- | --- |
| `evidence/source/arxiv-2406.12915.pdf` | `905b941fed15e57ef469d51ffb24b17cab35490cd2a3b62ee3e1401998162892` |
| `evidence/source/arxiv-2406.12915-source.tar.gz` | `5e0b7e925faa9862b43e5c52b49887378c0a9313adc76cadf480f9942ec59817` |

The source archive includes `00README.json`, `content/3_theory.tex`, `content/5_grod.tex`, `content/6_experiment.tex`, `content/8_app.tex`, the bibliography, ICML style files, and figures. `00README.json` identifies `pdflatex` and TeX Live 2025 for the archive's top-level example source; the audit does not compile the paper.

## Author implementation

- Repository: [yjzscode/GROD-OOD-Detection-with-Transformers](https://github.com/yjzscode/GROD-OOD-Detection-with-Transformers)
- Audited ref: [`f64b493e38def879b96b3adf2282846fdec80bbb`](https://github.com/yjzscode/GROD-OOD-Detection-with-Transformers/tree/f64b493e38def879b96b3adf2282846fdec80bbb)
- Branch at audit: `main`
- Audit boundary: public code was inspected, not executed end-to-end and not copied into this repository.

The inspected implementation exposes the image OpenOOD path under `OpenOOD_GROD/`, text paths under `text_ood/code/` and `text_ood/scripts/`, and Gaussian experiment material under `Gaussian_distribution/`. The local audit links to this exact commit so future changes in the author repository cannot silently change the cited implementation.

## Paper production map

1. Extract backbone features and labels.
2. Use PCA/LDA boundary features and outward shifts to construct synthetic feature-space OOD.
3. Apply Mahalanobis filtering and a cap/soft-label scheme.
4. Fine-tune with the ordinary classification loss plus binary ID/OOD loss.
5. Extract features/logits at evaluation and apply the modified VIM-style post-processor.
6. Aggregate ID accuracy, FPR@95, AUROC, AUPR-IN, and AUPR-OUT over the prescribed image or text datasets.

The local toy covers only a reduced part of steps 2–4. It does not instantiate a transformer or step 6's benchmark protocol.

## Source/contract discrepancies recorded

- C3's contract values `12.89` and `2.27` are not literal strings in the pinned `bert_gpt_NLP` source table.
- C4 names `Theorem 1 (Informal Theorem 4)` while the pinned theory source labels the central result `Theorem2`.
- C5 describes three module contributions, while the appendix source explicitly describes sensitivity to `a` and `γ`; no local three-way leave-one-out artifact is present.
- C6's method list is narrower than the comparison paragraph in the source, which also names OE, MIXOE, ATOM, POEM, and DivOE.

These are documented boundaries, not silently corrected claims.

