# Mathematical argument: truthful completion of the frozen N=1 model

Status: author argument submitted for independent scientific review, not an
UPPAAL verdict or a proof-assistant development. Input hashes are in the release manifest.
Throughout, M is the full unchanged 51-process XML, not Hnom, the old
50-process family member, or a reduced network.

## Statement and semantics

Let C(s) mean u0_app_Req_0.Completed in state s. Let P(s) be the **entire**
26-conjunct consequent of the exact accepted completion-safety.q (copied
canonically in premises.json, with its original byte hash). This includes
success/receipt/admission, all request/sample/job/transport equalities,
stored-payload quality, strict freshness/update requirements, all four
work-stage flags, receipt records, absence of four failure/cancellation flags,
and outcome=1.

**Theorem 1 (state safety).** Every state reachable from M's initial state by
a finite sequence of legal delay/action transitions satisfies

    I(s) = C(s) implies (P(s) and not c82_active).

Consequently M satisfies the mathematical interpretation of the exact
A[] (C imply P) formula. This is a mathematical_argument claim whose
acceptance is pending; the prior direct_model_checking verdict is still null.

We use standard symbolic timed-transition semantics: guards are evaluated
before a synchronization's updates; a binary sender's update precedes its
receiver's update; an observable successor follows the whole action.
A[] quantifies over reachable states, including delays, rather than
intermediate C-like assignments. See the official
[system semantics](https://docs.uppaal.org/language-reference/system-description/semantics/)
and [query semantics, Invariantly and State Properties](https://docs.uppaal.org/language-reference/query-semantics/symb_queries/).
No fairness or time-divergence premise is needed for this safety induction.

## Premise closure against the full XML

The checker scans all **51 templates, 884 transitions and 77 global helpers**.
Transitive helper analysis identifies **29 edge sites** that write c82 state.
Their complete guards, updates and preservation cases are in `../../results/static/completion-safety.json`.
Edge numbers are zero-based transition order within the named template,
matching the stored engine edge numbering.

The source capsule in premises.json binds global initialization, the binary
channel, helper bodies, every local scope/parameter list, system bindings,
the APP/job graphs and all other c82-related edges. Non-c82 global helpers
are sealed too: adding an indirect writer cannot evade the call-site audit.
There is one APP instance and one job; no local c82 shadow, reference alias,
external c82 writer, duplicate instance or hidden initializer is admitted.
The distribution check requires exact XML/query bytes and the published file hashes.

This is a specialized check of a fixed-model argument. The capsule was
extracted from, then reviewed against, the accepted XML; it is not an
independent oracle. Entry implications are calculated by a small
conjunction/equality/substitution calculus. Writer preservation uses the
explicit cases below plus exact audited helper bodies. Causal interpretation
is a mathematical argument over the sealed event graphs. This is not a parser/verifier
for arbitrary UPPAAL programs. An unsupported change is rejected and requires
a new scientific audit, even if that change would be harmless.

## Proof of Theorem 1

**Initial state.** APP starts in ServiceIdle, hence C is false. The initial
state satisfies I.

**Delay.** Delay changes clocks, not APP's location or any discrete variable
in P. The pure payload predicate reads only stored discrete requirements and
quality. Neither P nor c82_active contains a live clock. Thus any legal delay
preserves I, even if sample_age becomes 5 or service_age exceeds 40.

**Entering C.** APP has exactly four entrances: edges 12/13 from Accepted
and 18/19 from AcceptedDegraded. Each is a c82_result_delivery? receiver.
The unique matching binary sender is job edge 7 (Transmitting -> Done).
It has no update, so it cannot invalidate the APP guard between guard
evaluation and the receiver update. No third receiver or autonomous
termination/timer edge participates in this binary action.

Each entrance tests matching request/admitted/job/sample/transport IDs,
request_id=sample_id=1, admitted/sampled/enqueued/dispatched/attempted flags,
no prior receipt, cancellation or sensing/transport/queue failure, outcome=0,
strict freshness/update, payload_quality(), sample_age<5 and service_age<=40.
It writes received IDs from the checked transport IDs, records timely and
quality receipt, sample band 0, success=true, active=false, outcome=1 and
service band 1 (<40) or 2 (=40). No stored quality/requirement field changes.
Sequential substitution and the pre-state equalities establish every
conjunct of P and inactive in the successor. `../../results/static/completion-safety.json` gives four
independently checked entry implications, each with all 26 conjuncts.

**Preserving C after entry.** Completed has no outgoing edge. A transition
not writing any c82 variable cannot change P or inactive; ordinary delay was
already covered. Every remaining writer belongs to one of these cases:

| Writer sites | Why the c82 record is preserved when C holds |
|---|---|
| APP edges 2–5, 11–23 that actually write | Their source is a different location in the same unique APP instance. They cannot occur. |
| PHY edges 24, 25, 26 | Each requires c82_active as a conjunction, which I makes false. |
| Job edges 0, 6, 8 | Each likewise requires active. |
| SharedLoad enqueue/overflow edges 5, 6 | Each likewise requires active. |
| SharedLoad edge 1, c82_mac_service(server) | Its only c82 writes are inside a conjunction containing active. With active=false it leaves them unchanged; its other updates do not write P. |
| Boundary_E_SERVICE edges 6, 12, 18 | Sequentially assign cancelled=(active or cancelled), outcome=(active ? 5 : outcome), active=false. For inactive, these are cancelled'=cancelled, outcome'=outcome, active'=false. |

These cases exhaust all 29 sites, including clock resets (more state than P
actually needs). At an already Completed state no eligible synchronized
partner can reactivate the request: the sole active=true writer is the
unavailable APP request-emission edge. Thus the preservation cases also apply
to complete synchronized actions, not only isolated edge fragments.
A transition from a non-C state that does not enter C satisfies I vacuously.
Induction proves the theorem.

**Corollary 1.** After any successful receipt, its discrete P records remain
unchanged forever along every continuation. Later termination notices can
still be recorded elsewhere; they cannot retrospectively cancel this result.
This is not a statement that the whole network terminates.

## Event provenance and the meaning of the records

**Theorem 2 (causal history and receipt ages).** Every first entry into C has,
earlier on that same execution, the ordered discrete events below. Their
physical timestamps are nondecreasing; distinct events may share a timestamp.

| Order | Event and exact anchor | Reason it must have happened |
|---|---|---|
| 1 | APP RequestReady -> RequestPending, edge 2, service_request! | Only writer of request_id=1 and reset of service_age is c82_emit_request(). APP starts Idle and cannot return to this prefix. |
| 2 | APP edge 3 or 4, accepted/degraded admission receipt | The only admitted=true writers are in RequestPending, reached after emission. They store this request ID. |
| 3 | Job edge 0, then edge 1 / PHY edge 24 | The job binds admitted_id while active/admitted and starts the binary sensing event; its acyclic graph cannot skip these stages on a successful path. |
| 4 | PHY edge 25 / job edge 2, measurement | Only c82_store_measurement() writes sampled=true, sample IDs/quality and resets sample_age. It requires the matching job ID and !sampled. Initialization sampled=false plus no reset prevents a second sample. |
| 5 | Job edge 4 / SharedLoad edge 5, enqueue | Only c82_insert_result() sets enqueued=true. Its receiver requires active, sampled, !enqueued and q<K; rank becomes the post-increment occupancy. |
| 6 | SharedLoad edge 1, selected service with rank=1 | Only c82_mac_service() sets dispatched=true and transport IDs. Its inner test requires active, enqueued, !dispatched, rank>0 and no absorbing overflow; its rank=1 branch records the sample IDs. |
| 7 | Job edge 6, Queued -> Transmitting | Only writer of attempted=true; guarded by active and dispatched. |
| 8 | Job edge 7 / one APP Completed entrance | Actual binary result delivery; the only successful receipt. Sender enters Done while APP enters Completed. |

All relevant stage flags initially are false, and no other helper or edge
can fabricate them. The exact APP and job graphs, stage guards and closed
writer inventory establish the ordering; merely checking P's flag values
would not have established this fact. At a successful entry, failure branches
have not bypassed the path: those branches lead the job to absorbing Done,
or retire the request; none creates successful receipt.

The measurement clock is reset at sensing start and tested at the fixed
D_sense=5 acquisition completion. Sample age is reset **at that completion**,
not at initial sensing readiness or an unrelated KPI update. Service age is
reset only at actual request emission. Both are ordinary rate-one clocks and
are never reset again on this one-shot successful history. Therefore at the
receipt time tr, with request emission te and sample acquisition completion tm,

    0 <= tr - tm < 5,       0 <= tr - te <= 40.

The model measures freshness from acquisition completion. If an application
needs age from acquisition start, that includes the extra five acquisition
units and is a different contract. The source does not justify identifying
these abstract units with milliseconds or the measured physical accuracy.

Stored quality is the snapshot written by the measurement helper; later PHY
KPI changes cannot overwrite it because sampled never resets. The receipt
predicate checks that stored snapshot against captured request requirements.
Its update-class rule is sample-age based, not an observed inter-sample period.
A single admitted request/result with bounded IDs and **no reuse** is crucial;
neither theorem is a multi-request freshness, anti-replay or arbitrary-N result.

## Boundaries, non-vacuity and limitations

At sample age exactly 5, the successful guard is false. At request age exactly
40, a successful receipt has band 2; the timeout alternative is also enabled
locally. The theorem says a chosen successful entry is truthful, not that it
wins that nondeterministic race. After completion, live ages continue growing:
substituting sample_age<5 into an everlasting terminal predicate would change
the property and is not justified by this proof.

No assumption of successful delivery, absence of network loss, nominal inputs,
fair scheduling or guaranteed admission is used. Optional service, sensing
failure, transport loss, rejection, timeout and cancellation remain in M.
These can prevent completion; they do not create false success.

The historical 100-transition engine replay is separately audited by
the completion-witness records in ../../results/completion-witness/: it is an existing causal
success witness, not a new run or an exhaustive verdict. The original
completion-safety attempt in the historical full-model campaign remains timeout/null at 600.5930649 seconds.
The proof does not revise that record.

The result establishes neither universal completion within 40 nor progress,
deadlock freedom, fairness, queue capacity safety, physical validation or a
network-wide guarantee. It needs no assumption that every maximal run diverges
in time. It is a finite-reachability safety argument for exactly M. Acceptance
of this mathematical result and of any P3 milestone belongs to the independent
scientific reviewer.
