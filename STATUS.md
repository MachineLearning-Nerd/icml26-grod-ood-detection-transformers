# Status

- Paper: **How Out-of-Distribution Detection Learning Theory Enhances Transformer: Learnability and Reliability**.
- OpenReview ID: 94FOsjgeHK; six anchored claims / 12 maximum points.
- Source pin: arXiv 2406.12915 PDF and source archive under evidence/source/.
- Author implementation: yjzscode/GROD-OOD-Detection-with-Transformers at commit f64b493e38def879b96b3adf2282846fdec80bbb; only main was present at the audited head.
- Compute: local CPU/local GTX 1050 only; no HF Jobs, CPU upgrade, paid, or remote compute.
- Claim 1 source audit: the pinned CV table arithmetic is 21.97% − 0.12% = 21.85 percentage points; verdict remains inconclusive because no CIFAR-10/DINO/OpenOOD run was performed.
- Claim 1 toy: reduced 2-D feature-space generator, Mahalanobis filter, binary ID/OOD loss, three seeds, and held-out synthetic OOD control. It is not a ViT, CIFAR, ImageNet, or Table-1 reproduction.
- Claims 2–6: source and code paths documented in README; no paper-scale result reproduced.
- Branch state: only main is retained; normalized target name is icml26-grod-ood-detection-transformers.
- Publication: blocked for a full reproduction claim; AUTONOMOUS_STATE.json records publication_allowed=false.
- Next: independently review Claim 1, then audit Claim 2 and reconcile the contract's text/theorem numbering with the pinned source.
