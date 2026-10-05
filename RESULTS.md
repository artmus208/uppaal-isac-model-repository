# Results and their scope

## Truthful successful receipt

For the exact one-shot S configuration, the completion-safety argument strengthens the target predicate with `!c82_active`. Each transition entering APP Completed establishes the 26 recorded conjuncts; later transitions preserve the stored receipt record. The causal order is emission, admission, measurement, enqueue, service, transmission, receipt. Freshness <5 and request age ≤40 are receipt-time conditions; live clocks continue afterwards.

This is a mathematical argument supported by a static premise audit. It does not prove inevitable successful completion. The eleven archived full-model searches remain timeout/null.

- [Full argument](proofs/completion-safety/proof.md)
- [Fixed premises](proofs/completion-safety/premises.json)
- [Reproduced static certificate](results/static/completion-safety.json)
- [Exact query](queries/S/completion-safety.q)

## Shared-service capacity

For the four F instances, one atomic writer preserves `family_grant_i ↔ family_last_server=i`, which implies at most one recorded grant. The property-specific abstract observations have 2, 3, 4 and 5 reachable states. These counts are not full UPPAAL state-space sizes or measured speedups.

Grants are service opportunities, not successful deliveries or a fairness guarantee. The finite-instance audit does not establish an arbitrary-UAV cutoff theorem. All twelve native shared-capacity attempts remain timeout/null.

- [Full argument](proofs/shared-capacity/proof.md)
- [Comparison with compositional verification methods](proofs/shared-capacity/GLONINA.md)
- [Reproduced static certificate](results/static/shared-capacity.json)

## FIFO freshness and terminal response

At successful receipt, sample age is `e + φ + (r − 1 + k)T + ℓ + b`, with `T=5` and nonnegative terms. Strict freshness <5 therefore requires insertion rank 1, no skipped service epoch, and remaining delays totaling <5. An empty insertion queue is necessary and insufficient. Rational examples are arithmetic examples, not native model traces.

Every legal time-divergent execution after emission must reach one of the five terminal outcomes by request age 40. This conditional mathematical statement does not prove inevitable success, absence of Zeno paths, or deadlock freedom.

- [Full argument](proofs/service-feasibility/proof.md)
- [Fixed premises](proofs/service-feasibility/premises.json)
- [Reproduced static certificate and examples](results/static/service-feasibility.json)

## Observer erasure

Removing 22 observer processes retains all 29 production/environment processes and all global declarations. The audit checks private observation dependencies and update-free committed normalization. Finite projected timed-trace correspondence supports the stated retained-predicate safety and existential arguments when their premises and proof obligations are accepted. It is not an unrestricted deadlock equivalence or a general liveness theorem.

The four archived R attempts produced timeout/null, error/null, memory_limit/null and memory_limit/null. No successful native verdict is claimed for R or transferred to S. The longer campaign remains a separately dated, unfinished observation.

- [Full argument](proofs/observer-erasure/proof.md)
- [Fixed premises](proofs/observer-erasure/premises.json)
- [Reproduced static certificate](results/static/observer-erasure.json)
- [Four recorded diagnostic attempts](results/diagnostic)

## Recorded native findings

| Evidence | Recorded outcome | Interpretation |
|---|---|---|
| F family: 90 verification attempts | 12 satisfied, 6 violated, 72 timeout/null | Results bind to the individual query and N; there is no universal family-wide success result |
| S: eleven exhaustive searches | 11 timeout/null | No native verification conclusion |
| S: 100-transition successful path and replay | Goal reached; 101 replay states | A concrete successful path, not universal completion |
| Two replay controls | Discrete-identity and clock constraints rejected | Negative controls for the recorded successful path |
| Bounded-response Q1 | error/null, despite partial positive engine output | Trace parsing failure prevents acceptance of a positive result |
| Bounded-response Q2, Q3, Q5 | timeout/null | No verification conclusion |
| Bounded-response Q4 on Hnom | success/false with rejection counterexample | Universal successful completion is false even under the nominal restriction |
| Bounded-response Q6 on S | success/false with bounded-time loop | Unconditional terminal progress fails; this does not refute the time-divergent theorem |
| H overflow safety | false; saved symbolic counterexample | Five arrivals exceed abstract capacity K=4; acknowledgements do not dequeue |

The historical H campaign includes its other completed and inconclusive attempts as well. Simulation/replay outcomes, process termination statuses and property verdicts remain distinct in the machine-readable index.

## Quantitative extensions

The literature analysis discusses priced optimal reachability, scheduler-dependent probabilistic bounds and UPPAAL SMC estimates. It reports no new energy, probability or statistical experiment. Costs, distributions, progress assumptions and compatibility with strict freshness guards require separate justification. See [the proposed discussion](proofs/quantitative-extensions/proposed-text.tex) and [references](proofs/quantitative-extensions/references.bib).

## Acceptance status

The completion-safety and shared-capacity arguments were incorporated into the manuscript after their scoped integration decisions. The service-feasibility and observer-erasure arguments remain candidates pending independent scientific acceptance in this snapshot. Static checker output is not an independent peer review, proof-assistant verification or native UPPAAL verdict. None of the proof packages establishes physically calibrated performance or universal successful service for an arbitrary number of UAVs.
