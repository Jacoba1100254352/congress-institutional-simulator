# Claims Ledger

| Claim | Supporting evidence currently available | Limitation | Citation needed |
|---|---|---|---|
| The artifact builds and tests through a Makefile-first workflow. | `Makefile`; `README.md`; targets `make test`, `make run`, `make campaign`. | Must be verified on a clean checkout before submission. | Software-paper venue instructions. |
| The artifact can reproduce the ACM paper outputs offline. | `README.md`; `make reproduce-paper-offline`; `paper/pdf-manifest.json`; generated paper PDFs. | TeX/PDF bytes may vary; tolerance rules need clearer documentation. | Artifact evaluation and reproducibility guidelines. |
| The simulator is implemented in Java 21 with generated reports under `reports/`. | Source tree and Makefile. | Need package/API overview for external users. | Java/software citation only if needed. |
| The project includes empirical and validation-related scripts. | `scripts/validation`; `reports/empirical-*`; `reports/calibration-baseline.*`. | These scripts perform sanity checks, not full validation. | Data-source documentation if discussed. |
| The project includes ODD+D-style model documentation. | `paper/technical-appendix/odd-d-appendix.pdf`. | Appendix is dense; may need a standalone software documentation page. | ODD/ODD+D documentation standards. |
| The repository is not yet a complete public software artifact. | No root `LICENSE`, `CITATION.cff`, or `codemeta.json` found during audit. | This can be fixed without changing scientific results. | Target venue artifact requirements. |
| The software should not claim real-world predictive validation. | Current ACM paper and empirical gap reports. | Software paper must keep scientific claims limited to implemented capabilities. | Simulation validation literature. |
