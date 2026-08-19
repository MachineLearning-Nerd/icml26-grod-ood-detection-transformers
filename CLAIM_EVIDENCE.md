# Claim-to-evidence ledger

This ledger keeps the challenge contract, the paper's production path, and the evidence actually present in this repository separate. `Paper-reported` means transcribed from the pinned source. `Source-audited` means the source or implementation path was inspected. `Toy support` is a reduced local diagnostic. None of the six claims is marked `reproduced here`.

## Overall verdict

`INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY` — the source/table arithmetic and a reduced feature-space fixture are auditable, but no ViT, benchmark, language-model, or paper-scale training result is reproduced. `publication_allowed` remains `false`.

## Claims

### C1 — image FPR@95 reduction

**Contract claim:** GROD reduces FPR@95 from 21.97% to 0.12%.

**How the paper produces it:** use the ViT-B/16 image pipeline, fine-tune with the GROD synthetic feature-space outliers and ID/OOD loss, run the OpenOOD evaluation over the three OOD datasets for the CIFAR-10 ID setting, and report the average FPR@95 in the main CV table. The pinned source records the MSP baseline as 21.97 and `Ours` as 0.12 in `content/6_experiment.tex` lines 58–102, specifically lines 66–71 and 98.

**Evidence here:** `outputs/claim1_source_audit/` transcribes the two source values and computes the 21.85 percentage-point difference. `outputs/claim1_synthetic_grod_toy/` exercises outward synthetic feature generation, Mahalanobis filtering, binary ID/OOD loss, and a held-out synthetic-OOD control in 2-D with three seeds.

**Status:** `INCONCLUSIVE_SOURCE_AUDIT_TOY`. The toy is not ViT, CIFAR-10, OpenOOD, or Table 1.

### C2 — image AUROC improvement

**Contract claim:** GROD improves AUROC from 93.62% to 99.98%.

**How the paper produces it:** use the same ViT-B/16/CIFAR-10/OpenOOD pipeline as C1 and aggregate AUROC over the three OOD datasets. The pinned source records 93.62 for MSP and 99.98 for `Ours` in `content/6_experiment.tex` lines 66–98.

**Evidence here:** the pinned source and the C1 source audit establish the table location and values. No local output runs the ViT, datasets, OpenOOD aggregation, or the paper's five-seed benchmark protocol.

**Status:** `UNVERIFIED_PAPER_REPORTED_ONLY`.

### C3 — BERT text-OOD improvement

**Contract claim:** BERT GROD improves FPR@95 by 12.89 percentage points and AUROC by 2.27 percentage points.

**How the paper produces it:** fine-tune BERT for IMDB-versus-Yelp background shift and CLINC150 known-versus-unknown-intent semantic shift, generate feature-space OOD during training, apply the text OOD post-processing/evaluation path, and aggregate FPR@95/AUROC.

**Evidence here:** the source table is `content/8_app.tex` lines 786–825 (`bert_gpt_NLP`). It reports the BERT row values directly, but the literal contract numbers 12.89 and 2.27 do not appear in the pinned source snapshot. The author code path is pinned in `SOURCE_AUDIT.md`; it was not run end-to-end.

**Status:** `UNVERIFIED_SOURCE_CLAIM_MISMATCH`.

### C4 — transformer OOD learnability theorem

**Contract claim:** finite training data and an OOD misclassification penalty exceeding the ID penalty are required for learnability.

**How the paper produces it:** define the transformer hypothesis space and ID/OOD loss, prove the necessary-and-sufficient result in the separate distribution space, and derive capacity/Jackson-type bounds. In the pinned source, the central result is labeled `Theorem2` in `content/3_theory.tex`; the contract's `Theorem 1 (Informal Theorem 4)` wording is not the same source label.

**Evidence here:** `SOURCE_AUDIT.md` records the source location and the label discrepancy. No independent proof audit or theorem-reproduction artifact is included.

**Status:** `UNVERIFIED_THEOREM_SOURCE_AUDITED`.

### C5 — ablation contribution of GROD modules

**Contract claim:** binary loss, synthetic OOD generation, and Mahalanobis filtering each individually contribute to the gains.

**How the paper produces it:** hold the model/data/evaluation protocol fixed while varying GROD components or their controlling parameters, then compare OOD metrics and ID accuracy. The pinned appendix describes a sensitivity ablation of the synthetic-OOD extension parameter `a` and binary-loss weight `γ` in `content/8_app.tex` lines 835–845.

**Evidence here:** the local toy uses generation, filtering, and binary loss together, but does not isolate each module. The pinned source does not provide a local artifact for the exact three-way leave-one-out comparison asserted by the contract.

**Status:** `UNVERIFIED_ABLATION_PAPER_REPORTED_ONLY`.

### C6 — superiority over baseline detectors

**Contract claim:** GROD outperforms MSP, ODIN, VIM, GEN, ASH, G-ODIN, NPOS, and CIDER on CIFAR-10-based image OOD benchmarks.

**How the paper produces it:** run each baseline and GROD with the same ViT-B/16 backbone, datasets, preprocessing, seeds, and metric aggregation, then compare rows in the CV table. The paper also lists OE, MIXOE, ATOM, POEM, and DivOE in its comparison paragraph.

**Evidence here:** the pinned source and the author implementation reference expose the comparison protocol, but this repository contains no full baseline matrix, model checkpoints, dataset copy, or benchmark outputs.

**Status:** `UNVERIFIED_BENCHMARK_MATRIX_ABSENT`.

## Evidence boundary

The deterministic table audit proves only the subtraction of pinned paper values. The reduced toy proves only that selected mechanics can execute in a small CPU fixture. Neither result validates the paper's learned models, theorem, benchmark datasets, baseline comparison, or reported scores.

