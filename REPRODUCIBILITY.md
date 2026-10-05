# Reproduce the artifact checks

## Offline checks

Use Python 3.10 or later:

```sh
python -B scripts/verify_artifacts.py
```

This checks every manifest entry, each recorded model/query binding, completed native family verdicts against saved stdout, and the four specialized premise audits. Observer erasure also reproduces the exact archived R XML bytes. Certificates are compared with the deterministic files in `results/static`; no native experiment is launched.

The kernels in `scripts/kernels` preserve the original mathematical audit functions. Their wrappers and file locations were adapted for this standalone distribution. They are specialized checks for fixed inputs, not a general theorem prover or replacement for scientific review.

## Open a model

Open an indexed `model.xml` in UPPAAL and load the corresponding `.q` files from `queries`. The engine observed in the recent native evidence was **UPPAAL 5.0.0, revision 714BA9DB36F49691, June 2023**. Older simulation records report the server variant of the same revision. UPPAAL executables and third-party runtime libraries are not distributed here.

For example, from the repository root, a user who has an appropriate UPPAAL installation can run:

```sh
verifyta -o 0 -t 0 models/R/model.xml queries/R/completion-safety.q
verifyta -o 0 -t 0 models/R/model.xml queries/R/success.q
```

These are new executions and can be expensive. The examples do not reproduce the historical resource stop thresholds on their own. Historical records specify the query, model hashes, timeout, memory threshold and elapsed time. The F records additionally retain the native verifier arguments with public paths. Preserve tool version, options and resource controls when comparing new results.

## Saved traces

Large symbolic XML traces are compressed losslessly with gzip. Decompress a trace to a new file:

```sh
python scripts/unpack_trace.py results/bounded-response/uav-br89-q4-001/trace1.xml.gz Q4-trace.xml
```

Then inspect or replay it using the exact model named in that run's `result.json`. Q4 binds to Hnom; Q6 binds to S. Q1's saved output is diagnostic evidence of a failed result and must not be treated as an accepted positive trace.

The successful completion witness also includes the saved `.xtr` prefix, state/transition JSONL records, native stdout, and replay results. A query search, a directed simulation, and replay of an existing path are different experiments. They are labelled separately in `results/index.json`.

## Resource and semantic limits

The F campaign used a 60-second execution cap plus cleanup allowance, with 2 GiB sampled memory stopping. In the R campaign, the initial cap was 600 seconds and the later cap 1800 seconds, also with 2 GiB stopping. The full S campaign used eleven 600-second searches. Native RSS and sampled stop thresholds are not hard allocation limits. Exact recorded values take precedence over these overview labels.

Timeout, memory_limit and error have no property verdict. A partial formula message followed by parsing or result-handling failure is insufficient for a positive claim. Models use abstract time units; no conversion to seconds of network service is justified by these experiments.
