# What Glonina's scalability results do and do not transfer

Comparison of compositional verification methods. This is a primary-source applicability
analysis and a proposed article contribution, awaiting independent review.
All page numbers below refer to **printed dissertation pages**, which coincide
with its PDF page numbers. For the 2020 journal article, printed page = PDF page
+15. Source identities and hashes are recorded in [sources.json](sources.json).

## 1. The actual source result

Glonina's dissertation, *Анализ конфигураций модульных вычислительных систем для
проверки выполнения ограничений реального времени* (2020), separates three
problems that should not be conflated:

1. **Component correctness.** Each parameterized component is paired with an
   observer for a particular interface requirement. Reaching the observer's bad
   location is a violation (sections 3.2 and Appendix B).
2. **Composition correctness.** A mathematical argument connects those component
   requirements to the modular computing system's global requirements and
   determinism of observable timed diagrams (sections 3.3–3.4, pp. 79–86).
3. **Configuration analysis.** For the resulting deterministic model, a generated
   execution can represent the relevant timed diagram. This enables efficient
   analysis of a configuration without exploring all network interleavings
   (definition on p. 63 and the tool architecture in the 2020 article, pp. 21–25).

The second step is not a generic consequence of using timed automata. It is proved
for the source's task/core/partition/channel contracts, configuration construction
and event semantics. In particular, its determinism means equivalence of the
observable timed diagrams of all executions, not merely one syntactic outgoing
edge per location. The component proof and timed-diagram determinism are required
before a representative execution can replace exhaustive configuration analysis.

At pp. 63–64 the dissertation explains how a new component can be admitted by
checking the requirements of its base type, relying on the already established
composition argument. The 2020 article describes the same distinction: UPPAAL
checks component models with observers, while generated C++ models are executed
inside the configuration-analysis workflow (printed pp. 21, 23, 25). Its runtime
results cannot simply be compared with exhaustive checking of the whole ISAC
composition. The tasks, guarantees and measurement units differ.

## 2. The finite reductions have different domains and premises

Appendix B does not contain a universal cutoff on the number of communicating
automata. It supplies reductions for particular kinds of component/observer
automata and their parameters. The following table is a navigation and
applicability summary, **not a replacement for the complete theorem hypotheses**.
Here `k`, `m`, `q` and array length `n` are the variables of the cited theorem;
none is automatically the number of UAVs in our generator.

| Source result | Sufficient finite domain, when its hypotheses hold | Decisive hypotheses | Status for the accepted UAV family |
|---|---|---|---|
| Proposition 6, pp. 165–177, statement p. 169 | Array sizes at most `k+m`; `k` index variables, `m` type-(a) selection functions | Class У6: equal array sizes, restricted extremal selection / universal-condition / uniform-reset functions, restricted index use, arbitrary interface-array updates available through unconditional self-loops, permutation invariance and uniqueness conditions | No qualifying component/observer encoding has been constructed. The family uses unrolled names and mutable queues, not the required unrestricted environment and array operations. No UAV cutoff follows. |
| Proposition 7, pp. 180–189, statement p. 185 | A synchronization sequence **within one iteration**, with the same timestamps, has a representative at array size 1 or 2 | Class У7 plus Lemma 2: no interface variables, arrays only of time parameters/channels, at most one nonstopping clock, prescribed cyclic traversal/reset topology, an always-ready complementary partner, ordered timing parameters | The shared environment reads/writes global per-UAV state and retains queue history. Its staging/publish/offer chain has no demonstrated equivalence to this class. This is not a whole-network theorem for N=2. |
| Corollary to Proposition 7, pp. 189–191 | Bad observer-location unreachability for **all parameter values at sizes 1, 2 and 3** suffices | A qualifying model plus a specially structured observer; modified condition 6' allows wrong-index synchronization to a bad location; iteration alignment and other hypotheses remain essential | No such observer pair or trace-preserving transformation is supplied for the family. Existing N=1..4 experiments do not discharge these premises. |
| Proposition 8, pp. 194–196 | For `k` channel-index parameters, `q=k` and all index values `0..k-1` suffice for location unreachability | Equal-sized binary-channel arrays; highly restricted occurrences of index parameters and array length in model/observer synchronization labels; complementary communication directions | The UAV index controls much more than channel selection: persistent data namespaces, additional automata and the shared queue update. Renaming UAV indices is not this theorem. |
| Proposition 9, pp. 197–201 | Interface-integer values at most `k`, for `k` such variables | Unconditional arbitrary resets, arbitrary initial interface values, no right-hand-side use in assignments, only specified mutual order/equality comparisons | Queue arithmetic `q := q - service + arrival` depends on its old value and bounded history. It violates the relevant restriction if treated as such an interface variable. |
| Propositions 3/10, pp. 148, 204 | All nonnegative integer timing values at most `k`, for `k` timing parameters | One nonstopping clock; comparisons only with parameters or zero; for variables, Lemma 5 separation and update conditions | The full composition has multiple independently reset clocks. A local reduction might be designed, but no family-wide timing theorem is established. |
| Propositions 4/11, pp. 157, 204–205 | Timing values at most 22 | At most four timing parameters and two stopwatches; synchronous resets; constrained clock comparisons/rates/bounds; class Л1 (modified for variables) | The complete model is not shown to satisfy these specialized restrictions. In particular, its independent clock resets cannot be silently replaced by synchronous resets. |
| Propositions 5/12, pp. 162, 205 | The one timing parameter takes values 0 and 1 | Exactly one timing parameter, comparisons only with it or zero; at least one nonstopping clock; Lemma 5 for variables | The family has distinct command, bus, input, completion and layer timing constants. Collapsing them to one parameter changes the model unless a separate preservation proof is supplied. |

The source counts `k` and `m` across **both** the model and observer when using
Proposition 6 on their product (p. 177). Ignoring observer indices would therefore
give an unjustified cutoff even for a component that otherwise fits.

For Proposition 7, the short list of restrictions hides important details.
Class У7 on pp. 180–181 requires an index initialized to -1, a last-element flag,
and prescribed `start`/`next` operations. Other internal variables are reset
at iteration boundaries; the clock resets at the prescribed sweep boundaries.
Lemma 2 (pp. 182–183) restricts clock comparisons to `<=` or `==`, constrains
invariants, orders array timing entries, and orders scalar time parameters after
the last entries. A vaguely similar loop over UAVs is insufficient.

The compatibility table on p. 207 also matters: the premises of Propositions
6 and 7 are incompatible, as are those of 7 and 9, for example. One cannot
multiply independently convenient bounds without checking compatibility.
The source recommends decomposition when necessary and explains on p. 208 that
models outside the structural/syntactic conditions must be modified or checked
over explicitly bounded parameter ranges. The four accepted finite instances
are consistent with bounded analysis; they are not evidence of an unbounded
cutoff by themselves.

## 3. Concrete model-to-condition audit

The following facts can be checked directly in the pinned N=2 XML and have the
same construction pattern in N=1,3,4. XPath-like selectors are preferable to
fragile line numbers. The generator references explain origin; the XML bytes
are the actual proof inputs.

| Family fact / evidence selector | Why it affects transfer |
|---|---|
| `family-series-68/generate.py`, `SIZES=(1,2,3,4)` and `build` domain guard | This repository exposes a finite family. A theorem schema alone does not extend that generator or its accepted input contract. |
| `/nta/declaration`: `family_grant_i`, `u{i}_mac_queue_q`, `u{i}_mac_scheduleMode`; `/nta/system`: 49N+1 explicit processes | Increasing N adds data and processes, not just a channel-array parameter of Proposition 8. |
| `/nta/template[name='SharedLoad']/transition[source/@ref='shared_Sample_2']/label[@kind='guard']` | Service eligibility reads mutable global queues and modes. Class У7's no-interface-variable condition is not met by this component as written. |
| Same edge, `label[@kind='assignment']` | `u{i}_mac_queue_q` is read in its own update. This is a concrete obstruction to treating it as a Proposition 9 order-only arbitrary interface variable. |
| `SharedLoad`: `shared_Publish_0 -> shared_Offer_0`, then `shared_Publish_1 -> shared_Offer_1` | Ordered interaction with specific recipients needs a symmetry/preservation argument. Equal per-UAV constants do not establish permutation invariance of timed traces. |
| `SharedLoad`: separate synchronized and skipped offer edges; `server=-1` is in the select range | The contract permits missed offers and optional service, with no fairness. A deterministic scheduling contract cannot be imported merely because both models have a shared resource. This audit does not claim a concrete timed-diagram counterexample. |
| Global clocks `u0_mac_c_queue`, `u0_sdn_c_mon`; updates in `u0_mac_Template_A_Q` and `u0_sdn_Template_A_MON` | These clocks reset on distinct layer transitions. The synchronous-reset timing reduction is not immediately applicable to their composition. |
| `p4-queries.json`: `u{i}-service` is a separate existential query | Safety of the recorded choice does not establish concrete service reachability; an abstract witness cannot close nonvacuity. |

Observer validity must also be retained. The dissertation's observers provide
complementary enabled actions, with exclusions justified by prerequisite
requirements and their dependency order (p. 67 and Appendix B, pp. 139–140).
Removing arbitrary environment processes or their blocking behavior from our
model is not automatically this construction. A local environment abstraction
must come with an explicit relation showing which properties it preserves.

## 4. A transfer that can actually be justified now

The general methodological lesson is useful: isolate the property-relevant
interface, state its environment assumptions, prove the composition implication,
and retain only the observation needed for the property. We carry this out for
the shared-service **record** in [PROOF.md](PROOF.md).

The protected interface consists of N grants and the recorded server. The rest
of the system may update its own state arbitrarily, delay, block or interleave,
but it does not write those protected variables. The one writer selects a
single index and updates the whole record on one internal transition. This
gives a direct inductive invariant and a forward simulation into a finite
overapproximation with N+1 reachable observation states.

This is an elementary property-specific proof developed for the accepted model.
It is **not an application of Proposition 6 or 7**, not a new general cutoff
theorem, and not a replacement for Glonina's composition/determinism argument.
The scientific contribution here is the audited connection between the full
model and a precisely scoped property, including the atomicity and alias
obligations that a mere inspection of the grant names would miss.

The distinction between mathematical and native evidence remains explicit.
The finite-family campaign contains twelve `shared-capacity` attempts (four sizes, three
repetitions), all timed out. [historical-runs.json](generated/historical-runs.json)
preserves the original IDs, commands, model/query hashes, measured tool version,
runtime, stdout/stderr hashes and source-record references. Our proof does not
turn any of those attempts into `success` or invent a native `satisfied` verdict.
An enumeration of five observation states is not a measured speedup over a
timeout in the full timed system.

## 5. What a stronger future result would require

For a genuine Glonina-style component cutoff, the next scientific artifact would
have to define a parameterized component/observer pair, map its indices and
channels to the UAV model, check **all** hypotheses of a specific proposition,
prove the abstraction relation, and discharge the corresponding bounded
obligations with accepted evidence. A change of array syntax alone is not enough.

For representative-run configuration analysis, one would additionally need a
fixed observable timed-diagram definition, component assumptions with justified
dependency order, and a composition/determinism proof. The present optional,
adversarial environment cannot simply be replaced by a favorable deterministic
scheduler while retaining the same conclusions.

For queue or SLA properties, the grant-only observation is too coarse. Useful
abstractions must retain the relevant history and explicitly account for overflow,
arrival/service coupling, observation timing and possible blocking. These are
separate scientific obligations, not tasks completed by this package.

R04 can be assessed against this comparison, the worked proof and the proposed
response. Acceptance and closure remain with the scientific reviewer. R03's
verifier-attempt measurements remain a different evidence strand; neither R03
nor C06/P3 is declared closed here.
