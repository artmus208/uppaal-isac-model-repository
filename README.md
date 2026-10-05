# UPPAAL ISAC model repository

Scientific artifacts for **A Hierarchical Timed-Automata Model for SDN-Managed Resource Orchestration in 6G ISAC Networks**, by Artur Mustafin and Vadim Tinishov.

This snapshot contains timed-automata models, property queries, mathematical arguments, static premise checks, recorded native results, counterexamples, and readable automata figures. Time and radio-quality classes are abstract; no physical calibration is claimed.

## Start here

| Material | Location |
|---|---|
| Configuration identities and SHA256 hashes | [models/index.json](models/index.json) |
| Scientific conclusions and limitations | [RESULTS.md](RESULTS.md) |
| Recorded experiments | [results/summary.csv](results/summary.csv), [results/index.json](results/index.json) |
| Offline reproduction and native query examples | [REPRODUCIBILITY.md](REPRODUCIBILITY.md) |
| Mathematical arguments | [proofs](proofs) |
| Readable PHY, MAC, SDN and APP fragments | [figures/fragments](figures/fragments) |
| Complete automata figures | [figures/full](figures/full) |
| File integrity and transformations | [MANIFEST.json](MANIFEST.json), [PROVENANCE.md](PROVENANCE.md) |

## Configurations

| ID | Meaning | XML |
|---|---|---|
| H | Historical composed model used for overflow and acknowledgement diagnostics | [model](models/H/model.xml) |
| F/n1 through F/n4 | Finite family with 1–4 UAV contexts and 50, 99, 148, 197 processes | [family](models/F) |
| S | One request/result with correlated sensing-result receipt; 51 processes | [model](models/S/model.xml) |
| R | Diagnostic observer erasure of S, retaining 29 production/environment processes | [model](models/R/model.xml) |
| Hnom | Nominal-environment restriction used by bounded-response Q1–Q5 | [model](models/Hnom/model.xml) |

The existing standalone component models remain in `models/phy`, `models/mac`, `models/sdn`, and `models/app`. They are component assets; the scientific results below are bound to the explicitly indexed composed XML files. A verdict for one configuration must not be transferred to another without an applicable argument.

## Check the snapshot

Python 3.10 or later is sufficient for the offline checks; no third-party Python packages or UPPAAL installation is required:

```sh
python -B scripts/verify_artifacts.py
```

The command verifies file hashes, model/query/result bindings, historical verdict counts, and four specialized static premise audits. It does not run a native verifier and does not establish independent scientific acceptance.

The snapshot date is **2026-10-05**. An extended diagnostic campaign was still running at the recorded observation time and is not counted as a completed experiment; see [results/snapshot.json](results/snapshot.json). Publication of this snapshot does not imply completion of that campaign.

To cite these artifacts, use [CITATION.cff](CITATION.cff). Redistribution permissions are described in [RIGHTS.md](RIGHTS.md).
