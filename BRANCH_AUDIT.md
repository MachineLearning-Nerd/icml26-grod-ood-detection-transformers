# Branch and attribution audit

## Audit repository

| Item | Required state | Evidence |
| --- | --- | --- |
| Canonical repository | `MachineLearning-Nerd/icml26-grod-ood-detection-transformers` | `git remote -v`, `verify_final.py` |
| Former repository | `MachineLearning-Nerd/icml26-repro-94FOsjgeHK-ood-learning-theory-transformers` | `AUTONOMOUS_STATE.json` |
| Canonical branch | `main` | local and fresh-clone branch checks |
| Local branch set | exactly `main` | `verify_final.py` |
| Stale backup refs | none under `refs/original` | `verify_final.py` |
| Commit identity | `MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>` for author and committer | every reachable `main` commit checked by `verify_final.py` |
| Co-authorship trailers | none | commit-message scan in `verify_final.py` |

The author implementation was audited at its public `main` commit `f64b493e38def879b96b3adf2282846fdec80bbb`. Its branch state is evidence about that external repository and is not copied into this audit repository.

The normalized audit branch contains the paper contract, pinned source, claim evidence, and bounded local fixtures. A branch name or commit identity is not evidence that any paper-scale metric was reproduced.

