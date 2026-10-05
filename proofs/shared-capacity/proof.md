# A projection proof for the recorded shared-service capacity

Evidence kind: **mathematical argument**, supported by a **static premise audit**.
Author mathematical argument; independent scientific acceptance is pending.
The argument is about the exact frozen XML instances, not a successful UPPAAL
verification run. All twelve historical native attempts retain `timeout` and
`property_verdict: null` in the run index (see the release result catalogue).

## 1. Statement and interpretation

Fix one of the accepted instances `N in {1,2,3,4}` of
`uav-family-r1-20260929`. Let `g_i` denote the Boolean global
`family_grant_i`, and `l` the bounded integer `family_last_server`.
For each reachable semantic state of this instance, the proposed conclusion is

\[
  J_N(l,g)\;\equiv\;
  l\in\{-1,0,\ldots,N-1\}\ \land\
  \bigwedge_{i=0}^{N-1}\bigl(g_i\leftrightarrow(l=i)\bigr).
\]

Consequently,

\[
  \sum_{i=0}^{N-1}\mathbf 1[g_i]
    =\mathbf 1[l\ne-1]\leq 1, \tag{1}
\]

which is the state predicate in the existing `shared-capacity` query. For example,
the N=2 query is exactly

```text
A[] ((family_grant_0 ? 1 : 0) + (family_grant_1 ? 1 : 0) <= 1)
```

These are **recorded service opportunities** at an epoch. They are not packet
departures, acknowledgements, simultaneous physical transmissions, resource
occupancy intervals, or a throughput guarantee. The flags persist between
writer transitions, so the assertion is not a count of events over an interval.
In particular, absorbing queue overflow can make a recorded opportunity useless.
This interpretation comes from the frozen `p4-queries.json` and family contract,
not from an inferred physical meaning of a Boolean name.

## 2. Exact input and proof obligations

The exact model hashes are in ../../models/index.json; query hashes are in
the release manifest and individual result records. Process counts and writer premises are in
`../../results/static/shared-capacity.json` (see the release result catalogue). The checker reads existing files;
it neither regenerates the family nor modifies its domain or queries.

| ID | Required fact | Concrete evidence checked |
|---|---|---|
| O1 | Initially `l=-1`, every `g_i=false`; their types have the stated domains | Prefix of the global declaration, exactly one scalar declaration per protected name |
| O2 | The only state-changing occurrences of protected variables are on one internal edge of `SharedLoad` | Exhaustive protected-name occurrence accounting across XML text, tails and attributes; function bodies and other templates are included |
| O3 | That edge chooses one unchanged local integer `server in [-1,N-1]` | Exact select, pure eligibility guard, no selector shadowing/exposure elsewhere; restricted scalar update syntax with no calls or selector mutation |
| O4 | The same completed transition assigns every `g_i=(server==i)` and `l=server` exactly once | Parsed list of all writer assignments and index mapping |
| O5 | There is exactly one instantiated `shared_load=SharedLoad()` in the full composition | Explicit zero-argument process bindings and system list; 49N+1 processes |
| O6 | No alias, external code or lifecycle/update hook can bypass O1–O4 | No other protected reference, no template parameters, no external imports or special hooks in the accepted dialect |
| O7 | The property is exactly (1) | Byte-pinned query plus equality with its canonical formula and metadata |

O5 and the exact eligibility guard are stronger than the algebra needs. They
anchor this evidence to the accepted family and its service interpretation.
O2 deliberately rejects even an additional harmless read; this conservative
choice prevents unsupported uses from silently passing the audit.

For each N, the writer is
`SharedLoad: shared_Sample_N -> shared_Publish_0`, with no synchronization.
Its update also changes queues, their classes, other finite inputs, ages and
`tick`. None of those operations changes `server` or introduces another reference
to a protected variable. There are `2(N+1)` protected-name occurrences in the
entire XML: one declaration and one update for each of N grants and for `l`.

## 3. Semantic boundary

We use ordinary UPPAAL symbolic timed-transition semantics. A delay changes
clock valuations; an internal action applies an edge update to produce its
successor, subject to enabling and target-invariant conditions. A transition
that is disabled contributes no successor. An invalid evaluation is an error,
not evidence that a property holds. [U1: system semantics](https://docs.uppaal.org/language-reference/system-description/semantics/)

Select binds a bounded local integer; expressions in an update are evaluated in
sequence. [U2: edges](https://docs.uppaal.org/language-reference/system-description/templates/edges/)
State predicates are observed at initialization and after the **complete**
transition successor has been computed. They are not observed between two
assignments on one edge. [U3: symbolic queries](https://docs.uppaal.org/language-reference/query-semantics/symb_queries/)

This distinction is essential. For N=2, take an old grant vector `(false,true)`
and select `server=0`. Assigning `g_0` before `g_1` temporarily produces
`(true,true)`, then the completed update produces `(true,false)`. The temporary
valuation is not a semantic state checked by `A[]`. Conversely, splitting those
writes into **two edges** would expose the intermediate state, even if its
location were committed. Committed locations prevent time passage and constrain
the next action; they do not fuse consecutive edges into one transition.
[U4: locations](https://docs.uppaal.org/language-reference/system-description/templates/locations/)

The audit excludes special hooks and by-reference exposure, both supported
features of the broader language. [U5: functions](https://docs.uppaal.org/language-reference/system-description/declarations/functions/)
It therefore need not reason about callbacks between assignments or initialization
code that changes a protected global. The frozen models and their existing native
compile records are the surrounding modelling context. This argument does not
establish general absence of invalid arithmetic or other errors in all executions.

## 4. Inductive proof in the full composition

**Base.** O1 gives `l=-1` and all grants false. For each `i>=0`, both sides of
`g_i <-> (l=i)` are false, so `J_N` holds.

**Delay step.** The protected variables are Booleans and an integer, not clocks.
A permitted delay leaves them unchanged. Thus it preserves `J_N`.

**Other action.** By O2 and O6, any transition not using the writer leaves all
protected variables unchanged, including any synchronized transition among other
processes. Other processes may block, interleave, or update arbitrary unrelated
state; the conclusion is unaffected.

**Writer action.** Let its selected value be `j`. O3 gives
`j in {-1,...,N-1}` throughout the update. O4 and the observation boundary give
`l'=j` and `g_i'=(j=i)` simultaneously in the successor state, in the sense of
the final valuation. Hence `J_N(l',g')`. Earlier values of grants, queues and
clocks are irrelevant to this implication. Eligibility only removes some choices
of `j`; it cannot introduce a successor violating the implication.

These cases cover every legal transition of the full system. By induction over
finite reachable prefixes, `J_N` holds at every reachable state, including
states on infinite runs and final states of deadlocked prefixes. Equation (1)
follows because a single integer cannot equal two distinct indices. No fairness,
work-conservation, absence of deadlock, or time-divergence assumption is used.

The proof is intentionally stronger than counting flags alone: it also establishes
the exact relation to `family_last_server` and pairwise exclusion of all distinct
grant pairs. For N=1 the capacity inequality is already Boolean tautology; the
relation to the recorded server still has content. N=2,3,4 exercise exclusion.

## 5. Explicit full-to-abstract simulation

For an independent way to inspect the reasoning, define an abstract system
`A_N` with the entire valuation domain

\[
 Q_N=\{-1,\ldots,N-1\}\times\{0,1\}^N.
\]

This domain includes inconsistent and multi-grant valuations. The invariant is
not built into the state space by assuming that only one-hot vectors exist.
The initial state is `a_init=(-1,0,...,0)`. From every abstract state `a`:

1. for each `j in {-1,...,N-1}`, `commit(j)` leads to
   `a_j=(j, [j=0], ..., [j=N-1])`;
2. a hidden discrete action `tau` may stutter at `a`;
3. every real delay `d>=0` may stutter at `a`.

For any full state `s`, define `pi(s)=(l(s),g_0(s),...,g_{N-1}(s))` and the
relation `R(s,a) iff a=pi(s)`. Relabel the full writer as `commit(j)`, every
other full action as `tau`, and each full delay by the same duration.
The initial pair belongs to R by O1. The three step cases in section 4 give,
for every full step `s -> s'` related to `a`, a matching abstract step
`a -> pi(s')`. This is a forward simulation of the relabelled timed transition
system. Equality of the protected predicates under R then transfers the abstract
safety assertion to the full system.

The abstraction deliberately forgets eligibility, queues, clocks, publication
order, control locations, missed offers and all other processes. It allows
**more** actions and delays. There is no reverse simulation claim. For example,
`A_N` allows `commit(i)` immediately from its initial state. The concrete writer
requires `tick==5`, with `tick` initially zero. The corresponding zero-time
abstract step has no concrete counterpart.

Reachable abstract states are exactly `{a_-1,a_0,...,a_(N-1)}`: each commit
produces one of them, stutters preserve them, and each is reachable from the
initial abstract state. Therefore there are N+1 reachable states. The full
abstract domain has `(N+1)2^N` valuations, but the enumeration visits only
reachable states. There are `(N+1)^2` distinct source/target pairs, counting
self-loops. If commit labels and the extra tau label are distinguished there
are `(N+1)(N+2)` discrete edges; delay transitions are not counted in either
finite edge count.

| N | Concrete processes | Abstract valuation domain | Reachable abstract states | Unique source/target pairs | Labelled discrete edges |
|---:|---:|---:|---:|---:|---:|
| 1 | 50 | 4 | 2 | 4 | 6 |
| 2 | 99 | 12 | 3 | 9 | 12 |
| 3 | 148 | 32 | 4 | 16 | 20 |
| 4 | 197 | 80 | 5 | 25 | 30 |

These are structural/enumeration counts, **not** measured UPPAAL explored-state
counts and not a speedup ratio. The linear abstract state count concerns this
one observation; nothing here bounds the full composition's reachable space.

## 6. Reproduction and trust boundary

The original specialized checker rejects mismatches in its pinned inputs; the standalone
wrapper checks the published byte identities and invokes the unchanged structural audit for the model, query,
query metadata or instance-vector bytes. It then checks O1–O7 using XML parsing
and a restricted writer-expression recognizer, extracts the grant-index mapping,
and enumerates `A_N` with that mapping. The graph evaluator is separately tested
with corrupted mappings and initial states, so its conclusion is not just a
constant emitted by the recognizer. Historical run hashes and saved stdout/stderr
are checked independently.

`test_proof.py` includes deliberate mutations for missing/duplicate/wrong writes,
initialization errors, hidden function writers, aliases, selector mutation,
extra instances, query drift, hooks, and a split writer. The split-writer example
in section 3 is an abstract mutation witness, not a trace from the accepted XML.

This is an auditable script and a human-readable proof, **not a proof-assistant
kernel, a general UPPAAL compiler, or verification of the checker itself**.
The trusted basis comprises the pinned files, the stated language semantics,
Python/XML execution and the review of this argument and recognizer. The public
CLI issues certificates only for N=1..4; direct calls to `check_structure` in the
tests do not authorize certification of modified or arbitrary models. Unknown
syntax and changed inputs require renewed analysis rather than an automatic
extension of the claim.

## 7. Parametric lemma and boundaries of the result

The induction of section 4 is a schema: for **any finite positive N**, any
transition system satisfying O1–O4 and the no-bypass/frame condition O6 obeys
(1). Its proof has no dependence on the number of unrelated processes. This is
a conditional algebraic lemma, not an empirical extrapolation from four tests.

Only the four accepted XML instances have been connected to those premises here.
The generator still supports exactly N=1..4; no hypothetical N=5 XML, arbitrary
network theorem, Glonina cutoff, or general timed equivalence is asserted.

In particular, none of the following follows from this projection:

- `E<> family_grant_i` in the concrete model: an abstract witness can be spurious;
- eventual service, absence of starvation, useful throughput or work-conservation;
- queue safety, backlog reachability, observer correctness, SLA satisfaction,
  physical timing, deadlock freedom or time divergence;
- determinism of observable timed diagrams, a bound on full model-checking cost,
  or replacement of the original native verification record.

The historical service-nonvacuity queries remain unresolved by this package.
The capacity result is a structural safety statement that remains meaningful
even when a concrete instance makes no useful progress. It therefore supports a
carefully delimited article claim, not closure of the network's liveness problem.
