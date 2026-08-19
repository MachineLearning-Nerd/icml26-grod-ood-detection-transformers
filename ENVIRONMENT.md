# Environment and reproduction boundary

## Policy

This audit uses local CPU and the local GTX 1050 only. It does not use HF Jobs, paid compute, a CPU upgrade, remote execution, or a hidden benchmark service.

## Lightweight checks

From the repository root:

```bash
python3 -m unittest tests/test_claim1_synthetic_grod_toy.py tests/test_claim1_table1_audit.py
python3 src/claim1_table1_audit.py --out /tmp/grod-source-audit-check
python3 src/claim1_synthetic_grod_toy.py --out /tmp/grod-toy-check
python3 verify_final.py
```

The checked-in tests write generated files to temporary directories. The two audit scripts accept an explicit output directory so a rerun need not overwrite the pinned evidence.

## Not executed

The following are outside the evidence currently stored here:

- ViT-B/16 training or inference;
- CIFAR-10, CIFAR-100, Tiny ImageNet, ImageNet-200, SVHN, OpenOOD, IMDB, Yelp, or CLINC150 benchmark runs;
- BERT, GPT-2, or Llama-3.1-8B training;
- the author's full dependency stack and pretrained checkpoints;
- independent theorem/proof validation;
- the full baseline and ablation matrices.

The paper reports a GPU-based training setup and model-specific dependencies. Those paper-scale requirements must not be implied by the local toy commands.

