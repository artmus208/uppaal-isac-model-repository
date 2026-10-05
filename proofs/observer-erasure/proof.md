# Observer erasure for the fixed UAV service-completion model

Author mathematical argument prepared for independent review. This package is
not a native UPPAAL verdict or a machine-checked proof. The premises are audited
against exact accepted bytes; review of the argument remains necessary.

## 1. Inputs and the question answered

M is the unchanged N=1 model selected by `uav-service-completion-r1-20261002`:
51 instantiated processes, one request/result, no identity reuse. Exact model/query hashes are in ../../models/index.json and the release manifest.
The standalone wrapper audits the fixed premise capsule and reproduces R byte for byte.

Define O to be the 22 explicitly instantiated Obs templates and P to be the
other 29 processes. P includes the physical/protocol/application components,
all environment stimulus processes, all bridges, SharedLoad and C82_ResultJob.
This is **observer erasure**, not removal of environmental assumptions or a
single-layer abstraction. No theorem for arbitrary N is asserted.

R is `models/R/model.xml`: exactly O's templates and instance bindings are
removed, and the remaining system order is unchanged. Every global declaration
and surviving template is retained. Embedded queries are omitted to avoid
silently carrying formulas that refer to absent instances. Hidden recorder
variables still exist in R; deleting declarations/functions is unnecessary and
would require a separate transformation proof. R has 29 instantiated processes.

## 2. State partition and audited premises

Let H be the 27 identifiers listed in `../../results/static/observer-erasure.json`: eleven observer-reset
clocks (three PHY, four MAC, four SDN), eight APP sequence flags and their eight
age clocks. These are hidden in the **relation**, not deleted from the XML.
Every other global value, all local values of P, and all P locations are retained.
In particular `u0_mac_c_obs_ack`, `u0_sdn_c_obs_rec`, their associated flags and
attempt records remain retained: production guards use these clocks. Naming a
variable `obs` does not justify hiding it.

The audit covers all 51 bindings, 884 edges and 77 global helpers, with exact
declaration/local/parameter capsules. It certifies the following premises:

1. O has no location invariant, rate or urgent location; no initial O location
   is committed. O has 74 edges. Its eight synchronization edges are receives
   on ordinary broadcast channels; O never sends, uses a binary input or selects
   an index. All observer updates reset an H clock to zero or an H flag to false.
2. No production enabling expression, invariant, synchronization label or select
   depends on H. Production writes involving H occur through the exact eight
   void `u0_raise_app_*_seq()` helpers. A helper conditionally sets only its own
   hidden flag/age. Other helpers can call these helpers, but cannot directly
   read H or use it to choose a retained update. The relevant transitive helper
   sites and effects are recorded. Thus retained updates depend only on retained
   pre-state, parameters and the chosen production transition.
3. No process/channel priority is introduced by the transformation. Retained
   process order, and hence relative order of broadcast production updates, is
   unchanged. Observer guards/functions have no write effects; observer updates
   cannot affect a retained receiver, including the later C82_ResultJob instance.
4. The three PHY observers have five committed locations in total. Every such
   location has exactly two internal, update-free exits to noncommitted observer
   locations, partitioned by `x <= D` and `x > D`, where x is an observer clock
   and D a fixed integer constant. Equality takes the first exit. Neither exit
   synchronizes. There is no committed observer cycle. A configuration has at
   most three committed observer processes simultaneously.

The global initialization/types capsule is extracted from accepted source,
then read against the stated partition. It is a source binding, not an
independent semantic oracle. `check.py` is a specialized, conservative premise
checker; the exact outer hashes prevent unsupported syntax or arbitrary changed
programs from being certified as this baseline. Mutation tests call `audit()`
without that outer byte gate. One urgent-channel control also changes the
declaration capsule so it tests the channel condition itself.

## 3. Semantic convention and relation

Use symbolic timed-transition semantics. Delays increase clocks while honoring
all invariants and urgency; committed locations also restrict which process
can supply the next action. Broadcast-enabled receivers participate, and their
updates follow system order. See the official [system semantics][sem] and
[location semantics][loc]. The reasoning below assumes well-defined expression
evaluation in the accepted typed model; it is not an analysis of error-aborted
verifier computations, SMC distributions, strategies or external functions.

For full state s and reduced state r, write s ~ r when all retained values and
P locations agree. H and O locations may differ. Retained clocks agree exactly,
so timestamps and clock-sensitive retained predicates are covered.

An O-only internal action is a stutter under this relation. A broadcast with
both P and O participants is a production action with attached observer work,
not an O-only action. An observation trace records retained states and delays,
ignoring O-only actions and allowing finite zero-time stuttering. We compare
these traces, rather than claiming a strong bisimulation of all XML states.

## 4. Zero-time normalization lemma

If an O process is committed, exactly one of its two certified exits is enabled
at the current clock value. That exit has no update or synchronization and its
destination has no invariant. It remains legal even if a P process is committed:
the action includes a committed source, satisfying the global committed rule.
No higher-priority action blocks it. It leaves every retained value unchanged.

Choose these exits before any other action. At most three exits discharge all
currently committed O processes. No chosen exit creates another committed
location. Time remains unchanged. This is a **chosen finite normalization**,
not a claim that every possible scheduler normalizes: other P actions may
interleave where the semantics permits them. Normalize whenever constructing a
lifted trace or a future production step.

## 5. Finite timed-trace correspondence theorem

**Theorem T1.** M and R have identical retained timed observation traces up to
finite zero-time stuttering. Consequently their projected reachable-state sets
are equal. No fairness assumption is used.

**Initialization.** Both compositions start all P processes at the same initial
locations and initialize globals/locals identically. All clocks start at zero,
and no O process starts committed. Hence the initial states are related.

**Projection of a full delay.** Every full legal delay satisfies the surviving
invariants and production urgency. The reduced delay is therefore legal and
changes retained clocks identically. O has no observer urgency/channel urgency
or invariant requiring an additional reduced constraint.

**Projection of a full action.** An O-only internal action updates only H and
is a stutter. For a P action, delete any participating O broadcast receives.
O supplies no binary partner or sender; surviving guards are independent of H.
Relative production update order and all retained assignments are preserved.
Surviving target invariants therefore hold. A committed O location has only
internal exits, so it cannot participate as a receiver in a P action. Therefore
if the full action takes place while any process is committed, a participating
committed source must belong to P and survives erasure. If there is no full
commitment, there is no retained commitment. Thus the projected action is legal.
This restriction matters: a general committed observer with a receive edge
could allow a production action while another production process is committed;
erasing that participant would invalidate the projected action.

**Lifting a reduced delay.** Start at any related full state and normalize O
commitments. O's remaining locations have no invariant/urgency. Only P imposes
delay restrictions, independent of H. Execute the same delay in M; every
retained value agrees throughout the delay, not merely at its endpoint.

**Lifting a reduced action.** Normalize first. Select the same P transition(s).
Binary production partners remain present. For a broadcast, include every
currently enabled O receiver, as required by broadcast semantics. Such receives
have no retained update or target invariant, so they cannot invalidate the
production successor. Their guards need not be input-total: an absent enabled
receive does not prevent an ordinary broadcast. Production committed/urgency
conditions are exactly those in R. Finally normalize any new O commitments.
The retained successor is the chosen reduced successor.

Induction on any finite delay/action sequence proves both inclusions. The
lifting maintains the same elapsed time, inserting only finitely many zero-time
steps per reduced step. For an endpoint that contains an O commitment, its
retained projection is still a reduced reachable state; normalization is not
needed to observe that endpoint. All retained terminal locations, including
APP Completed, are covered. No success, non-vacuity or deadlock-freedom verdict
is supplied by the existence of this relation.

## 6. Property transfer and its direction

For a well-defined state predicate phi using only retained values/locations:

| Property | Transfer justified by T1 |
|---|---|
| Universal reachable-state safety `A[] phi` | M iff R |
| Existential reachability `E<> phi` | M iff R |
| Reachability constrained by retained clocks/timestamps | M iff R, for the same finite-state trace condition |
| Observer Violation/location/hidden-age predicate | Outside the relation |
| Raw `deadlock` predicate or ordinary maximal-path liveness | No two-way equivalence |
| Stutter-sensitive next-step / observer-step counts | Outside the relation |
| SMC probabilities, costs, strategies | Outside the semantics used here |

The exact `completion-safety.q` consequent and antecedent use retained state;
the checker audits its transitive helper reads. T1 therefore permits transfer
of an **actual complete native verdict** for that formula from R to M or M to R when the
full reduction/run protocol is accepted. Native runs are recorded separately
in the diagnostic results; the argument itself assumes no native verdict
and does not relabel historical timeouts or previously accepted proofs.

**Theorem T2 (one-way deadlock inclusion).** If s is a reachable full deadlock,
then its related projected reduced state r is a reduced deadlock. Hence a proof
of `A[] not deadlock` on R would imply deadlock freedom of M. The converse is
not supplied.

Use UPPAAL's deadlock definition: no discrete successor can be reached after
any permissible delay, not just absence of an immediately enabled edge
([query semantics][query]). A full deadlock cannot contain committed O because
the normalization exit is an immediate legal successor. Without such a
commitment, a reduced action after a delay would lift to a full action after
that same delay, contradicting full deadlock. This proves the inclusion.
An observer-only transition can make a full state nondeadlocked when P is
deadlocked. An internal observer cycle can mask that problem permanently under
the raw global deadlock predicate. The small LTS controls demonstrate the
failure of a general converse; they are **not a reachable full-model trace**.

**Theorem T3 (explicit divergent-path convention).** If paths are restricted
to executions with unbounded accumulated time, the two compositions have the
same retained observations up to stuttering. Projection preserves all delays;
a divergent full path cannot be reduced to a finite-duration observer-only
path. Conversely construct an infinite lift using the same finite normalization
for each prefix of a divergent reduced execution. Elapsed time is unchanged.
Thus retained, stutter-insensitive eventuality/response claims over this
explicit path class transfer both ways. This is not an assertion that M's
ordinary UPPAAL `A<>`/`-->` query silently adopts that path class, nor that every
finite prefix has a divergent continuation. Fairness restrictions require
their own correspondence and are not added here.

## 7. Error detection is a different obligation

Behavioral nonrestriction does not prove that a Violation observer recognizes
the intended contract exactly. MAC and several SDN observers poll production
flags using ordinary internal edges. They have neither urgency nor an invariant
forcing the poll at the triggering event. Therefore their local clock can be
reset arbitrarily later, or a transient trigger can be missed before a poll.
The actual reset/guard sites are in `../../results/static/observer-erasure.json`. Examples are
ObsQueueCritical's Idle->Wait reset of `u0_mac_c_obs_queue`, and
ObsCommandAck's Idle->Wait reset of `u0_sdn_c_obs_cmd`.

The MAC ACK and SDN recovery observers instead read retained recorder clocks
written by production at protocol events. Those production recorders are kept
in R. APP sequence ages are also written by raising helpers at the event,
although observer scheduling/latch handling is a separate issue. We do not
conflate these mechanisms or claim that all 22 observers miss triggers.

Three PHY observers receive broadcasts and classify deadline equality through
the committed partition. This avoids a post-receipt time delay before that
classification. It does not establish a one-to-one request pairing or total
trigger coverage while an observer is already waiting/in Violation. Missed
overlapping events, polling timeliness and error-predicate adequacy need their
own specification and proof.

## 8. Scientific outcome and operational limit

The supported result is a property-class-specific erasure theorem, with a
concrete 51-to-29-process diagnostic composition and auditable premises. It
provides a principled smaller input for a later completion-safety/reachability
campaign, without promising any speedup or successful verdict. It also identifies
why a raw monitored deadlock result or a polling observer's clock cannot be
interpreted as a production-progress or event-deadline theorem automatically.

The original model and queries are unchanged. Four archived native diagnostic
attempts and their inconclusive outcomes appear in ../../results/diagnostic/.
The longer campaign has no completed result at the snapshot observation time.
Independent acceptance of the proof remains pending.

[sem]: https://docs.uppaal.org/language-reference/system-description/semantics/
[loc]: https://docs.uppaal.org/language-reference/system-description/templates/locations/
[query]: https://docs.uppaal.org/language-reference/query-semantics/symb_queries/
