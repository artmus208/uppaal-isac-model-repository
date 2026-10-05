# FIFO freshness feasibility and conditional terminal progress

## Object and semantics

M is the exact model `models/S/model.xml`,
SHA256 `b8ab50e112b71491f8242789cc7906497baf8440c473d7a5a4d5214840187e02`.
Its configuration is N=1, 51 processes, one request/result without identity reuse.
The completion-safety argument supplies causal one-shot history and truthful receipt records. We use
its finite-prefix argument, not its historical engine witness as a universal premise.

Executions here are concrete sequences of legal discrete actions and nonnegative
delays. Ordinary clocks increase by each delay; guards read the pre-state and
updates of a binary sender precede receiver updates. Every visited state satisfies
its location invariant. Committed locations permit no positive delay and may
restrict otherwise enabled transitions. These are the [official timed-system
semantics](https://docs.uppaal.org/language-reference/system-description/semantics/).
Time divergence means unbounded sum of delays on the execution, not merely an
infinite number of actions. The mathematical theorems below are not submitted
UPPAAL queries. No query-semantic fairness convention is silently assumed.

Write `te` for request emission, `tm` for completed measurement, `tq` for enqueue,
`td` for result dispatch, `ta` for transmission attempt and `tr` for APP receipt.
They are nondecreasing along a successful history. Measurement freshness starts
at **completed acquisition**: `c82_store_measurement()` resets sample_age there.
The sole service_age reset is request emission. Ages at receipt are consequently
`tr-tm` and `tr-te`. Time units are abstract, without physical calibration.

M has service period T=5, freshness F=5 with strict acceptance `<F`, service
deadline D=40 with inclusive receipt `<=D`, transmission bound B=1, and admission
bound A=15. A five-unit sensing acquisition precedes measurement completion;
it does not consume the post-measurement freshness budget.

## Lemma 1 — service epochs and FIFO accounting

Call SharedLoad edge 1 a *decision*: it chooses `server` in [-1,0]. Only server=0
is a serving decision; server=-1 is legal even when a queue is eligible.
Each decision is preceded by edge 0 at local tick=T. Edge 1 tests tick=T and
resets tick=0. Sample_1, Publish_0 and Offer_0 are committed, and the closed graph
returns to Wait before another edge 0/1. The only tick write is this reset and
tick is an ordinary local clock. Thus consecutive decisions on any history
containing them are exactly T apart; no second service can occur at that same
timestamp. Blocking can stop this history from continuing; it cannot shorten
the separation. Committed interleavings with other processes consume no time.

Enqueue occurs on SharedLoad edge 5 from Wait: pre-state q<K, then
`c82_insert_result()` increments q, copies q into rank, and marks enqueued.
The sender (job edge 4) has no update. Hence initial result rank r is 1..K=4.
There is only one enqueue: its receiver tests !enqueued and no writer resets
enqueued. `c82_mac_service` is called only on decision edge 1, before aggregate
queue update. For the active, enqueued, undispatched result in a nonoverflowed
queue it reduces rank by exactly one at server=0; at rank=1 it sets rank=0,
dispatched=true and transport IDs. No other site decreases the positive rank
or fabricates dispatch. Aggregate arrivals after enqueue enter behind this
token; they do not change its stored rank. Overflow is absorbing and prevents
dispatch, rather than improving the token's rank.

Induction on decisions therefore shows that dispatch requires exactly r serving
decisions after enqueue. At least r-1 full periods elapse between the first of
these and dispatch. At a timestamp shared by enqueue and an epoch, order matters:
enqueue before decision can count that epoch; enqueue after decision cannot.
Neither ordering allows two counted decisions at that timestamp.

## Theorem 1 — exact necessary freshness accounting

For a history that actually dispatches and receives this token, let `s0` be the
first service *decision* after enqueue in action order, `phi=s0-tq`, and k the
number of non-serving decisions from s0 through dispatch. Define enqueue latency
`e=tq-tm`, launch latency `l=ta-td`, and transport latency `b=tr-ta`.
All are nonnegative and k is a nonnegative integer. There are r serving decisions,
hence r+k total decisions, and Lemma 1 gives

```text
tr - tm = e + phi + (r - 1 + k) T + l + b.
```

Here b<=B on a legal received attempt; **l has no model-imposed upper bound**.
In a continuing dispatch history phi is in [0,T], with endpoint/order semantics
above. This equality characterizes this token's age conditional on the actual
events; it asserts neither dispatch reachability nor absence of loss. It implies
the necessary success inequality

```text
e + phi + (r - 1 + k) T + l + b < F,
tr - te <= D.
```

No clock reset can shorten the left hand side: the only sample_age reset sets
sampled=true on the unique acquisition, guarded by !sampled. Single enqueue,
single dispatch and one-shot job graph follow the audited writers and the completion-safety argument.

**Corollary 1 (queue obstruction).** In this exact M, any result initially enqueued
at r>=2 cannot subsequently cause successful APP completion. Its earliest possible
receipt age is at least (r-1)T>=5=F. Even e=phi=l=b=k=0 gives equality for r=2;
the guard is strict. Any counted skipped decision (k>=1) also excludes success.
This statement quantifies over all finite histories with such an enqueue. It
does not claim that each rank is reachable from M's initial state. No witness
for ranks 2..4 is supplied or needed to prove the implication. Delivery of such
a token can produce ServiceFailed, or some other terminal outcome may happen first.

**Corollary 2 (success filter).** Every successful history has r=1, k=0, and
`e+phi+l+b<5`. Since insertion sets r=q_pre+1, success requires an empty aggregate
queue at insertion (q_pre=0). Arrivals concurrent with or after insertion may
still cause overflow/failure, so an empty queue is necessary, not sufficient.

## Why fairness and capacity do not establish successful service

Eventual service, even service at every eligible epoch, cannot rescue r>=2 under
this strict freshness bound. For rank one, eventual service allows arbitrarily
many skipped epochs, each of which already costs the full freshness budget.
Continuous enabledness fairness is weaker still: server eligibility is sampled
at epochs and can change with schedule mode. No such fairness is part of M.

Even choosing server=0 at the first possible epoch does not ensure freshness for
every phase and allowed transport delay. With r=1, e=l=0, phi approaching 5 and
b=1, the age exceeds 5. Exact rational cases in `../../results/static/service-feasibility.json` demonstrate
this arithmetic obstruction; they are admissible timings of the *contract
arithmetic*, not claims of reachable full-network counterexamples.

K=4 bounds queue capacity, not freshness. In a hypothetical contract with period
T>0 and strict F>0, the bare earliest-time prerequisite is (r-1)T<F, giving
`r <= ceil(F/T)` before enqueue/phase/launch/transport costs. The actual M has
ceil(F/T)=1. For independently realizable closed latency bounds E,P,L,B' and
skip bound Kskip, a robust sufficient freshness budget is
`E+P+(r-1+Kskip)T+L+B'<F`. This is a contract formula, not parameter synthesis
or a theorem that such timing bounds are achievable by the current components.

## Theorem 2 — terminal location by 40 on time-divergent executions

Take any legal time-divergent execution of M containing request emission at te.
It visits a terminal APP location (Rejected, Completed, ServiceFailed,
ServiceTimeout or Cancelled) at some finite action index and time t<=te+40.
No fairness premise is needed beyond the stated time-divergent execution domain.

Proof: emission takes APP RequestReady to RequestPending and simultaneously
resets service_age and admission clock to zero. APP cannot revisit the pre-emission
prefix: the complete forward graph after this edge has exactly three nonterminal
locations, RequestPending, Accepted, AcceptedDegraded, and five absorbing terminals.
The only admission-clock reset is that emission edge; the only service_age reset
is its emit helper. There is one APP instance and no external/local alias writer.
In Pending its invariant implies t-te<=15. In Accepted/AcceptedDegraded their
invariants imply t-te<=40. The Pending exit can enter an accepted location only
by admission at age<=15; moves between the accepted pair do not reset the clocks.

If the execution never enters a terminal, every state after te must remain in
that three-location set, and its accumulated time since emission is at most 40.
This contradicts time divergence. Thus there is a finite first terminal entrance.
Its source is one of those bounded locations; a discrete action consumes no time,
so its entrance time is <=te+40. Terminals have no outgoing APP edge. This proves
both permanence of the terminal location and the claimed inclusive upper bound.

The argument remains valid if a termination message sets active=false while APP
is still nonterminal: the location/clock bound persists until the Cancelled edge
is actually selected. Hence the theorem is about actual APP location, rather
than mistaking an externally updated outcome flag for application notification.

**Nonextension caveat.** A finite maximal deadlock/time lock, an infinite Zeno
cycle, or an infinite sequence of delays converging to age 40 is outside the
domain. The theorem does not prove that any emitted prefix has a time-divergent
continuation. Invariants cannot by themselves force execution of an enabled
timeout when another committed process blocks it or a zero-time cycle is selected.
No global deadlock verdict, unconditional leads-to verdict, or revision of Q6
is obtained. A pending request cannot survive to time>40 on a legal continuing
time-divergent history; a request can still remain pending on a bounded-time one.

At age 40, successful receipt and local timeout are both alternatives in the
accepted APP graph. The theorem permits either. Receipt age 5 is always stale.

## Conditional success contract and its discharge status

For a concrete execution, successful completion follows if the following holds:

1. Emission captures strict requirements; APP receives matching accepted or
   permitted degraded admission, and stays in the accepted pair until receipt.
2. The one matching acquisition completes with a stored payload satisfying
   c82_payload_quality(), no sensing failure, correct IDs and no later reuse.
3. It is inserted into an empty queue; no absorbing overflow, cancellation or
   other terminal outcome occurs before receipt.
4. The first counted decision serves this token (server=0 with eligible mode),
   job launches an attempt, the delivery branch is selected, and all event
   latencies satisfy e+phi+l+b<5 and tr-te<40.

The causal identity/flag obligations are discharged by the audited events and
the completion-safety argument. At the actual binary delivery, APP's corresponding success guard is true,
and the failure receivers are false; its update records Completed/success. The
strict service inequality in item 4 excludes the age-40 timeout race. If it is
relaxed to <=40, one must explicitly assume delivery wins that boundary race.
The contract includes delivery selection and quantitative progress requirements;
it is deliberately conditional and makes no new guarantee of network delivery.

Items 1/2/3/4 are not universal guarantees of M. Optional service, loss, rejection,
quality choices and unbounded launch delay remain possible. No assumption may
be advertised as proved just because it would make this implication useful.
Time divergence alone yields Theorem 2, not successful service. The new result
identifies the required queue/phase budget that an implementation or a separately
approved revised model would have to enforce to make a success claim credible.

## Audit limits and evidence status

check.py pins full input/dependency bytes, closes all relevant writer callsites
and reads the complete APP/SharedLoad graphs. A fixed reviewed semantic capsule
rejects unsupported syntax, initialization, local shadowing, aliases, duplicate
instances, stopwatches and additional hidden writers. It is a specialized premise
checker supporting this human argument, not a proof assistant or general verifier.
Mutation tests exercise clock resets, graph escapes, weakened freshness, duplicate
service, rank shortcuts and hidden helper writers below the full-byte gate.
Rational examples test the inequalities independently of the XML extraction.
Independent scientific review must still assess the mathematical reasoning.

No new native verification run or whole-network reachability experiment is part
of this package. The historical the historical full-model campaign completion-safety timeout remains timeout/null;
The bounded-response results remain separate local execution evidence.
Nothing here establishes arbitrary-N, reused-request, physical accuracy, automatic
gate/requirement closure, or unconditional successful SLA.
