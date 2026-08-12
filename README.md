# GROD: Source-Pinned Reproduction Audit

This repository records a source-pinned, claim-by-claim audit of **How Out-of-Distribution Detection Learning Theory Enhances Transformer: Learnability and Reliability**. The paper develops a PAC-style learnability theory for transformer OOD detection and proposes GROD, a feature-space synthetic-OOD fine-tuning method.

The audit is evidence-first. It keeps the paper source, the author implementation reference, a deterministic table arithmetic audit, and a small feature-space toy fixture in separate, explicitly labeled scopes. It does **not** currently claim a full reproduction of the paper's ViT, CIFAR, ImageNet, BERT, GPT-2, or Llama results.

| Resource | Link |
| --- | --- |
| Paper | [arXiv:2406.12915](https://arxiv.org/abs/2406.12915) |
| OpenReview submission | [94FOsjgeHK](https://openreview.net/forum?id=94FOsjgeHK) |
| Author implementation | [yjzscode/GROD-OOD-Detection-with-Transformers](https://github.com/yjzscode/GROD-OOD-Detection-with-Transformers) |
| Audited implementation commit | [f64b493e](https://github.com/yjzscode/GROD-OOD-Detection-with-Transformers/tree/f64b493e38def879b96b3adf2282846fdec80bbb) |

The author implementation was publicly available and had only a main branch at the audited head f64b493e38def879b96b3adf2282846fdec80bbb. Its own README reports testing with Python 3.8, CUDA 11.8, and PyTorch 2.2.0+cu118. The implementation was inspected at that exact commit; it was not executed end-to-end under this local-only audit.

## Current status

**Overall result: inconclusive.** Claim 1 has a deterministic arithmetic audit of the paper table and a reduced CPU toy that exercises several GROD mechanisms. Claims 2–6 remain unverified because the full pretrained backbones, benchmark datasets, and paper-scale training/evaluation were not run.

| Area | Current state |
| --- | --- |
| Paper association | Confirmed through the pinned arXiv source, OpenReview record, and author implementation |
| Claim 1 | Source/table arithmetic audit plus a reduced 2-D feature-space toy; neither verifies the paper benchmark |
| Claims 2–6 | Unverified; production paths are documented in the claim ledger |
| Official code | Audited at f64b493e; image, text, and Gaussian experiment paths are present |
| Compute policy | Local CPU and local GTX 1050 only; no paid, remote, upgraded, or HF Jobs compute |
| Branches | Only main is retained in this audit repository |
| Normalized repository name | icml26-grod-ood-detection-transformers |
| Publication gate | Not allowed for a full reproduction claim |

The machine-readable state is in AUTONOMOUS_STATE.json. The six anchored claims in contract/live_claims.json intentionally remain unverified; the local results below are bounded diagnostics and source audits, not replacements for those statuses.

## What the paper does

The paper studies OOD detection for transformer hypothesis spaces. Its theory argues that learnability depends on the data-distribution regime, the transformer capacity, and a loss that penalizes ID/OOD misclassification sufficiently. It derives approximation or Jackson-type bounds that relate transformer capacity to the probability of learnable OOD detection.

GROD, or Generate Rounded OOD Data, turns that perspective into a training pipeline:

1. Run the transformer backbone and extract feature representations and class labels.
2. Use PCA for global boundary features and LDA for class-conditional boundary features.
3. Extend those boundary points outward and sample Gaussian-mixture synthetic OOD feature vectors.
4. Remove synthetic vectors that are too ID-like with Mahalanobis-distance filtering, then apply a random cap to control the ID/OOD ratio.
5. Assign soft class/OOD labels to the retained synthetic vectors.
6. Fine-tune with the ordinary classification loss L₁ plus a binary ID-versus-OOD loss L₂.
7. At inference, pass features and adjusted logits to an OOD post-processor, primarily the modified VIM path used by the implementation.

The method flow is therefore:

    ID batch → transformer features → PCA/LDA boundaries → outward Gaussian OOD
    → Mahalanobis filter → soft labels → K+1 training with L₁/L₂
    → feature/logit post-processing → FPR@95, AUROC, AUPR, and ID accuracy

The paper states that training does not use real OOD examples. The synthetic OOD is generated from ID features, while the evaluation uses held-out near-OOD and far-OOD datasets.

## What the audited implementation contains

The author repository is a substantial implementation organized into three experiment families:

| Path in author repository | Role | Audit status |
| --- | --- | --- |
| OpenOOD_GROD/openood/networks/grod_net.py | Transformer backbone wrapper, feature extraction, PCA, LDA, and K+1 head | Inspected at f64b493e |
| OpenOOD_GROD/openood/trainers/grod_trainer.py | Warm-up, synthetic OOD generation, Mahalanobis filtering, soft labels, L₁/L₂ training | Inspected at f64b493e |
| OpenOOD_GROD/openood/postprocessors/ | VIM and other OOD post-processors | Present; not executed here |
| OpenOOD_GROD/configs/ and scripts/ | CIFAR-10, CIFAR-100, ImageNet-200 data/network/pipeline configurations | Present; pretrained weights and datasets not available locally |
| text_ood/code/ | BERT, GPT-2, and Llama feature extraction, GROD training, validation, and metrics | Present; not executed here |
| text_ood/scripts/ | Training and validation entry points for the text models | Present; not executed here |
| Gaussian_distribution/ | Synthetic Gaussian-distribution experiments related to the theory-to-training gap | Present; local audit uses a smaller independent fixture |
| README.md and framework.png | Author usage instructions and method overview | Inspected |

The local audit repository does not copy the author implementation. It links to the exact audited commit so that the implementation and the reproduction evidence remain separate.

## Paper-reported evaluation protocol

These are paper protocol details and reported values, not independent results produced by this repository.

| Experiment | Paper setup and production path |
| --- | --- |
| Image OOD | DINO with a ViT-B/16 backbone pretrained on ImageNet-1K; ID datasets CIFAR-10, CIFAR-100, and ImageNet-200; near-OOD and far-OOD datasets include CIFAR, Tiny ImageNet, MNIST, SVHN, Texture, Places365, SSB-hard, NINCO, iNaturalist, and OpenImage-O |
| Image training | Paper appendix: 10 fine-tuning epochs, batch size 64, learning rate 1e-4, AdamW weight decay 5e-2, GROD extension parameter a=0.1, binary-loss weight gamma=0.1; one RTX 4090 with 48 GiB is reported |
| Text OOD | BERT base, GPT-2 small, and Llama-3.1-8B; IMDB versus Yelp for background shift and CLINC150 intents versus unknown intents for semantic shift |
| Text training | Model-specific learning rates and weight decay are described in the appendix; no real OOD exposure is used during training |
| Metrics | ID accuracy, FPR@95, AUROC, AUPR_IN, and AUPR_OUT |
| Code configuration note | The current OpenOOD train_grod.yml sets optimizer.num_epochs to 50, while the paper appendix describes 10 image fine-tuning epochs. This audit does not silently resolve that protocol difference |

## Branch inventory

Only one branch is retained in the cleaned audit repository:

| Branch | Purpose | State |
| --- | --- | --- |
| main | Source-pinned GROD audit, contract, evidence, and local fixtures | Current published branch; no feature or stale legacy branch |

The author implementation also exposed only main at the audited commit. There is no undocumented experiment branch whose behavior is used by this audit.

## Claim ledger: what each claim means and how it is produced

The six claims below are the anchored claims in contract/live_claims.json. The production path says what would be required to verify the claim; the evidence column says what this repository actually contains.

| ID | Paper claim | How the paper produces the claim | Evidence in this repository | Status |
| --- | --- | --- | --- | --- |
| C1 | GROD reduces FPR@95 on image OOD detection from 21.97% to 0.12%, an improvement of 21.85 percentage points (Table 1). | Fine-tune the DINO ViT-B/16 with synthetic feature-space OOD and L₁/L₂, run the CIFAR-10 OOD evaluation against the OpenOOD protocol, compute FPR@95, and compare the MSP baseline row with GROD. | outputs/claim1_source_audit/ contains a source transcription and arithmetic check: 21.97 − 0.12 = 21.85 percentage points. outputs/claim1_synthetic_grod_toy/ contains a reduced 2-D feature-space fixture with three seeds, a nearest-ID Mahalanobis control, and held-out synthetic OOD metrics. Neither runs DINO, CIFAR-10, OpenOOD, or Table 1. | Inconclusive source audit; toy only |
| C2 | GROD improves AUROC on image OOD tasks from 93.62% to 99.98% (Table 1). | Use the same CIFAR-10/DINO/OpenOOD pipeline and aggregate AUROC across the paper's OOD datasets, comparing the MSP and GROD rows. | The pinned source records the baseline 93.62% and GROD 99.98% values. No local AUROC result uses the paper's backbone or datasets; the toy's mean AUROC is a separate synthetic diagnostic. | Unverified; values are paper-reported only |
| C3 | On BERT text OOD tasks, GROD improves FPR@95 by 12.89 percentage points and AUROC by 2.27 percentage points over baselines (Table 3). | Fine-tune BERT on the IMDB/Yelp and CLINC150 protocols, generate feature-space OOD during training, run the text OOD post-processing/evaluation, and compute the claimed aggregate improvements. | The author code contains text_ood/code/grod_trainer.py, train.py, val.py, and metrics.py. The pinned TeX source contains the BERT/GPT-2 table at content/8_app.tex, label bert_gpt_NLP, but the literal 12.89 and 2.27 strings are not present in that source snapshot; the exact contract wording still requires reconciliation. | Unverified; source/claim numbering needs reconciliation |
| C4 | Theorem 1 (also described in the contract as Informal Theorem 4) says transformer OOD learnability requires finite training data and an OOD misclassification penalty greater than the ID misclassification penalty (Section 3). | Check the theorem assumptions and proof in the theory section; an independent numerical audit would test finite toy transformer/data cases and a control that relaxes the penalty or finiteness condition. A numerical audit would not replace a proof. | The pinned source contains the necessary/sufficient learnability theorem and Jackson-type results in content/3_theory.tex. The current TeX labels the central result as Theorem2, so the contract's theorem numbering also needs reconciliation. No independent numerical theorem audit is present. | Unverified |
| C5 | Ablations show that the binary loss, synthetic OOD generation, and Mahalanobis filtering each contribute to GROD's gains (Table 4). | Run controlled ablations that remove L₂, remove synthetic OOD, and remove Mahalanobis filtering while keeping backbone, data, seed, and evaluation fixed; compare the OOD metrics and ID accuracy. | content/8_app.tex describes sensitivity to the synthetic-OOD extension parameter and gamma, and the implementation exposes the corresponding trainer paths. The local toy exercises generation, filtering, and binary loss together but does not isolate the three paper ablations. | Unverified |
| C6 | GROD outperforms MSP, ODIN, VIM, GEN, ASH, G-ODIN, NPOS, and CIDER on CIFAR-10-based image OOD benchmarks (Table 1). | Run each OpenOOD baseline and GROD under the same DINO backbone, ID/OOD datasets, preprocessing, and metric aggregation, then compare every method row. | The exact author code, OpenOOD configuration, and pinned paper tables are available as references. No full baseline matrix or GROD benchmark output is present locally. | Unverified |

### Reproduction labels

- **Paper-reported:** a value or conclusion transcribed from the pinned paper.
- **Source-audited:** the paper source, formula, protocol, or author implementation has been pinned and inspected.
- **Toy support:** a reduced local fixture exercises selected mechanics.
- **Reproduced here:** the relevant paper-scale experiment ran with verifiable outputs in this repository.
- **Unverified:** the repository does not yet contain enough evidence to support the claim.

At present, Claim 1 has an inconclusive source audit and toy support. No claim has the reproduced-here label.

## Local Claim 1 evidence

### Source/table arithmetic audit

The source audit reads the CIFAR-10 average row in content/6_experiment.tex and records:

    MSP baseline FPR@95: 21.97%
    GROD FPR@95:          0.12%
    arithmetic reduction: 21.85 percentage points
    verdict:              inconclusive

This verifies the subtraction in the paper table, not the experiment that produced the table.

### Reduced feature-space GROD toy

The local toy uses only 2-D Gaussian features and three fixed seeds. It preserves a narrow subset of the method:

- outward synthetic-OOD center generation;
- Mahalanobis removal of ID-like synthetic samples;
- a binary ID/OOD logistic loss;
- a held-out synthetic OOD set not used to generate training outliers;
- comparison with a nearest-ID Mahalanobis control.

Its mean diagnostics are:

| Metric | Nearest-ID control | Reduced GROD toy |
| --- | ---: | ---: |
| AUROC | 1.000000 | 0.999669 |
| FPR@95 | 0.000000 | 0.000694 |

The separable toy is intentionally not interpreted as a GROD improvement. It is a mechanism check and does not verify the paper's Table 1.

## Evidence integrity

The pinned source artifacts have these SHA-256 hashes:

| Artifact | SHA-256 |
| --- | --- |
| evidence/source/arxiv-2406.12915.pdf | 905b941fed15e57ef469d51ffb24b17cab35490cd2a3b62ee3e1401998162892 |
| evidence/source/arxiv-2406.12915-source.tar.gz | 5e0b7e925faa9862b43e5c52b49887378c0a9313adc76cadf480f9942ec59817 |

The source/table audit is checksummed:

| Artifact | SHA-256 |
| --- | --- |
| outputs/claim1_source_audit/summary.json | 3956918cd7bb46b1deaaf5b3e60b903a96f9cc2e7b08296bdeebeecb1086ed7b |
| outputs/claim1_source_audit/results.csv | a0421ac7c34f5bd9a617a4e0c2c36e2cb4e6a38fe5774512b6eb9ad2b751c800 |

The reduced toy artifacts are checksummed:

| Artifact | SHA-256 |
| --- | --- |
| outputs/claim1_synthetic_grod_toy/PROTOCOL.md | aeea5a494742d49b6879d5e2e2570b4987b5691abe8fd2e83792d712a2c63ff6 |
| outputs/claim1_synthetic_grod_toy/raw.json | 5a117055235c95888bb902a73163293544b1b34a29ea35d66ca0257f8b6aa0a8 |
| outputs/claim1_synthetic_grod_toy/results.csv | be9bb0d278a03c8e578dc3cbaace59c46a2ceb01cbf4e51fd6185ad8aa24562d |
| outputs/claim1_synthetic_grod_toy/summary.json | d63a91a7b45956cc991dc9fd3056ba92f1abfaa0c7f212789dd4de045ddc7f93 |

From the repository root, verify the evidence with:

    (cd evidence/source && sha256sum -c SHA256SUMS)
    (cd outputs/claim1_source_audit && sha256sum -c SHA256SUMS)
    (cd outputs/claim1_synthetic_grod_toy && sha256sum -c SHA256SUMS)

To regenerate the source arithmetic audit without overwriting the checked-in toy:

    python3 src/claim1_table1_audit.py
    python3 src/claim1_synthetic_grod_toy.py --out /tmp/grod-toy-check

These commands are small CPU checks. They do not train the paper's DINO, BERT, GPT-2, or Llama models.

## Reproduction boundary and next checkpoint

The strongest current statement is:

    verdict: inconclusive
    scope: source-pinned table audit plus reduced 2-D feature-space toy
    official code: available and pinned, not executed end-to-end
    paper benchmarks: not reproduced
    publication_allowed: false

The next technical checkpoint is an independent review of the Claim 1 toy and source arithmetic, followed by a Claim 2 source audit. A full reproduction would need to reconcile the contract/source numbering, install the author's dependency stack, obtain the pretrained DINO and language-model assets, obtain the OpenOOD/text datasets, execute the exact configs, and preserve per-claim metric artifacts.

## Citation

If this audit or the paper is useful, please cite the paper:

    @misc{zhou2024oodtransformer,
      title={How Out-of-Distribution Detection Learning Theory Enhances Transformer: Learnability and Reliability},
      author={Yijin Zhou and Yutang Ge and Wenyuan Xie and Linqian Zeng and Xiaowen Dong and Yuguang Wang},
      year={2024},
      eprint={2406.12915},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2406.12915},
      note={ICML 2026 paper}
    }

## Thank you

Thank you to **Yijin Zhou, Yutang Ge, Wenyuan Xie, Linqian Zeng, Xiaowen Dong, and Yuguang Wang** for developing GROD, publishing the theoretical framing, and making the image, text, and Gaussian experiment code available. The author implementation makes the connection between transformer OOD theory and synthetic feature-space training concrete and inspectable.
