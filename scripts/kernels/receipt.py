"""Specialized premise checker, not a general UPPAAL verifier."""
import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODEL = "models/S/model.xml"
QUERY = "queries/S/completion-safety.q"
MANIFEST = "manifests/baselines/uav-service-completion-r1.yaml"
MODEL_HASH = "b8ab50e112b71491f8242789cc7906497baf8440c473d7a5a4d5214840187e02"
QUERY_HASH = "f3cfb3800063b21045d94625f616950944663fcba61956a3498aba62ca32edf9"
MANIFEST_HASH = "4b4bf71f55767123cc5934074024179289fa5ad3355fa4c0e37385e8261ef98d"
APP = "u0_app_A_REQ"
JOB = "C82_ResultJob"
PHY = "u0_phy_Template_A_SQ"
ENV = "u0_Boundary_E_SERVICE"

class PremiseError(ValueError):
    pass

def require(test, message):
    if not test:
        raise PremiseError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def uncomment(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text or "", flags=re.S)

def norm(text):
    # Whitespace is irrelevant only between tokens, never inside an identifier/operator.
    return " ".join(re.findall(r"[A-Za-z_]\w*|\d+|==|!=|<=|>=|&&|\|\||\+\+|--|[-+*/%&|^]=|[^\s]", uncomment(text)))

def compact(text):
    return re.sub(r"\s+", "", uncomment(text))

def split_top(text, sep):
    result, start, depth = [], 0, 0
    i = 0
    while i < len(text):
        c = text[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            require(depth >= 0, "unbalanced expression")
        if depth == 0 and text.startswith(sep, i):
            result.append(text[start:i])
            i += len(sep)
            start = i
        else:
            i += 1
    require(depth == 0, "unbalanced expression")
    result.append(text[start:])
    return result

def strip_outer(text):
    text = compact(text)
    while text.startswith("(") and text.endswith(")"):
        depth = 0
        whole = True
        for i, c in enumerate(text):
            depth += (c == "(") - (c == ")")
            if depth == 0 and i != len(text)-1:
                whole = False
                break
        if not whole:
            break
        text = text[1:-1]
    return text

def conjuncts(text):
    text = strip_outer(text)
    parts = split_top(text, "&&")
    if len(parts) == 1:
        return [text] if text else []
    return [atom for part in parts for atom in conjuncts(part)]

def functions(declaration):
    """Parse balanced function bodies; remainder must match the reviewed declaration."""
    source = uncomment(declaration)
    pat = re.compile(r"\b(?:void|bool|int)\s+(\w+)\s*\(([^{};]*)\)\s*\{")
    found, spans = {}, []
    pos = 0
    while m := pat.search(source, pos):
        depth, end = 1, m.end()
        while depth and end < len(source):
            depth += (source[end] == "{") - (source[end] == "}")
            end += 1
        require(depth == 0, "unterminated function")
        require(m.group(1) not in found, "duplicate function")
        found[m.group(1)] = source[m.start():end]
        spans.append((m.start(), end))
        pos = end
    remainder = source
    for a, b in reversed(spans):
        remainder = remainder[:a] + remainder[b:]
    return found, remainder

def direct_writes(code):
    # Aliases, arrays, local shadowing and extra syntax are sealed separately.
    return set(re.findall(r"\b(c82_\w+)\s*(?:=(?!=)|\+\+|--|[-+*/%&|^]=)", uncomment(code)))

def calls(code, funcs):
    return sorted(set(re.findall(r"\b(\w+)\s*\(", uncomment(code))) & funcs.keys())

def writes(code, funcs, stack=()):
    result = direct_writes(code)
    for name in calls(code, funcs):
        require(name not in stack, "recursive helper unsupported")
        # Function header is excluded to avoid identifying itself as a call.
        body = funcs[name][funcs[name].index("{")+1:-1]
        result |= writes(body, funcs, stack+(name,))
    return result

def edges(root):
    result = []
    for t in root.findall("template"):
        name = t.findtext("name")
        loc = {l.get("id"): l.findtext("name") for l in t.findall("location")}
        require(len(loc) == len(t.findall("location")), "duplicate location id")
        for i, e in enumerate(t.findall("transition")):
            labs = e.findall("label")
            require(len({x.get("kind") for x in labs}) == len(labs), "duplicate edge label")
            result.append({
                "template": name, "index": i,
                "source": loc[e.find("source").get("ref")],
                "target": loc[e.find("target").get("ref")],
                **{x.get("kind"): x.text or "" for x in labs},
            })
    return result

def relevant_snapshot(root):
    """Reviewable c82 slice; unrelated semantics remain bound by input byte hashes."""
    funcs, remainder = functions(root.findtext("declaration"))
    require(all("c82_" not in name for name in funcs if not name.startswith("c82_")), "helper naming")
    selected = [e for e in edges(root) if e["template"] in (APP, JOB)
                or any("c82_" in str(v) for v in e.values())]
    locations = {}
    for t in root.findall("template"):
        n = t.findtext("name")
        if n in (APP, JOB, PHY, ENV, "SharedLoad"):
            locations[n] = {
                "init": t.find("init").get("ref"),
                "locations": [
                    {"id": l.get("id"), "name": l.findtext("name"),
                     "invariant": [norm(x.text) for x in l.findall("label")],
                     "committed": l.find("committed") is not None,
                     "urgent": l.find("urgent") is not None}
                    for l in t.findall("location")]}
    return {
        "system": norm(root.findtext("system")),
        "declaration_remainder": norm(remainder),
        "non_c82_helpers_sha256": sha(json.dumps({n:norm(f) for n,f in funcs.items()
            if not n.startswith("c82_")}, sort_keys=True).encode()),
        "c82_helpers": {n:norm(f) for n,f in funcs.items() if n.startswith("c82_")},
        "local_scopes": {t.findtext("name"): {
            "declaration":norm(t.findtext("declaration")), "parameter":norm(t.findtext("parameter"))
        } for t in root.findall("template")},
        "locations": locations,
        "relevant_edges": [{k: norm(v) if isinstance(v,str) else v for k,v in e.items()}
                           for e in selected],
    }

class Facts:
    """Small conjunction/equality calculus, deliberately not an expression evaluator."""
    def __init__(self, atoms):
        self.parent = {}
        self.atoms = set(atoms)
        for a in atoms:
            if m := re.fullmatch(r"(\w+)==(\w+)", a):
                self.union(*m.groups())
            elif re.fullmatch(r"\w+", a):
                self.union(a, "true")
            elif re.fullmatch(r"!\w+", a):
                self.union(a[1:], "false")

    def find(self, x):
        self.parent.setdefault(x, x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)

    def proves(self, atom):
        if atom == "true":
            return True
        if atom in self.atoms:
            return True
        if m := re.fullmatch(r"(\w+)==(\w+)", atom):
            return self.find(m[1]) == self.find(m[2])
        if re.fullmatch(r"\w+", atom):
            return self.find(atom) == self.find("true")
        if re.fullmatch(r"!\w+", atom):
            return self.find(atom[1:]) == self.find("false")
        if m := re.fullmatch(r"(\w+)>0", atom):
            return any(self.find(m[1]) == self.find(str(v)) for v in (1,2))
        return False

def entry_proof(edge, consequent, funcs):
    facts = Facts(conjuncts(edge.get("guard", "")))
    env = {}
    for update in split_top(compact(edge.get("assignment", "")), ","):
        m = re.fullmatch(r"(\w+)=(\w+)", update)
        require(m is not None, "entry update outside straight-line scalar subset")
        name, rhs = m.groups()
        env[name] = env.get(rhs, rhs)  # UPPAAL's sequential update order.
    def subst(expr):
        return re.sub(r"\b[A-Za-z_]\w*\b", lambda m: env.get(m[0], m[0]), expr)
    require(edge.get("synchronisation") == "c82_result_delivery?", "entry needs actual delivery")
    require(facts.proves("c82_sample_age<5"), "strict receipt freshness absent")
    require(facts.proves("c82_service_age<=c82_D_service"), "receipt deadline absent")
    require(env.get("c82_active") == "false", "completion must retire the request")
    require(facts.proves("c82_req_fresh==2") and facts.proves("c82_req_update==2"), "strict request")
    # Treat pure quality as a pre-state atom only if its dependencies do not change.
    quality = funcs["c82_payload_quality"]
    deps = set(re.findall(r"\bc82_\w+", quality)) - set(funcs)
    require(not (set(env) & deps), "entry changes stored quality after the guard")
    failed = [a for a in consequent if not facts.proves(subst(a))]
    require(not failed, "entry does not establish query atoms: " + str(failed))
    band = env.get("c82_receipt_service_band")
    require((band == "1" and facts.proves("c82_service_age<c82_D_service")) or
            (band == "2" and facts.proves("c82_service_age==c82_D_service")), "receipt band mismatch")
    return {"edge":edge["index"], "source":edge["source"], "query_atoms":len(consequent),
            "age_bounds":"sample < 5; service <= 40", "service_band":int(band)}

def check_premises(root, query, expected):
    """No outer XML hash here: controls exercise this function on changed XML."""
    ts = root.findall("template")
    require(len({t.findtext("name") for t in ts}) == len(ts), "duplicate template")
    funcs, _ = functions(root.findtext("declaration"))
    es = edges(root)
    app = next(t for t in ts if t.findtext("name") == APP)
    loc = {l.get("id"): l.findtext("name") for l in app.findall("location")}
    require(loc[app.find("init").get("ref")] != "Completed", "initial state is Completed")
    require(not any(e["template"] == APP and e["source"] == "Completed" for e in es),
            "Completed is not absorbing")
    q = compact(query)
    require(q.startswith("A[](u0_app_Req_0.Completedimply(") and q.endswith("))"),
            "unsupported query envelope")
    consequent = conjuncts(q.split("imply(", 1)[1][:-2])
    require(norm(query) == expected["query"], "query differs from frozen target")
    entrances = [e for e in es if e["template"] == APP and e["target"] == "Completed"]
    require(len(entrances) == 4, "four completion entrances required")
    entry_cert = [entry_proof(e, consequent, funcs) for e in entrances]
    senders = [e for e in es if compact(e.get("synchronisation","")) == "c82_result_delivery!"]
    require(len(senders) == 1 and senders[0]["template"] == JOB, "unique binary delivery sender")
    require(not writes(senders[0].get("assignment",""), funcs), "sender can invalidate receipt guard")
    decl = norm(root.findtext("declaration"))
    require("chan c82_enqueue , c82_enqueue_loss , c82_result_delivery ;" in decl,
            "delivery channel declaration is not the reviewed binary channel")
    writer_cert = []
    for e in es:
        for label in ("guard", "select", "synchronisation"):
            require(not writes(e.get(label,""), funcs), "side effects outside updates")
        w = writes(e.get("assignment",""), funcs)
        if not w:
            continue
        atoms = conjuncts(e.get("guard",""))
        if e["template"] == APP:
            require(e["source"] != "Completed", "APP terminal writer")
            reason = "APP source excluded once Completed (single absorbing instance)"
        elif "c82_active" in atoms:
            reason = "disabled by strengthened invariant !c82_active"
        elif e["template"] == "SharedLoad" and "c82_mac_service" in calls(e.get("assignment",""), funcs):
            require(w == {"c82_fifo_rank","c82_dispatched","c82_tx_request_id","c82_tx_sample_id"},
                    "unclassified shared-service writer")
            require("c82_active" in funcs["c82_mac_service"], "shared service lacks active check")
            reason = "reviewed helper writes only inside its c82_active conjunction"
        elif e["template"] == ENV:
            u = compact(e.get("assignment",""))
            require(w == {"c82_active","c82_cancelled","c82_outcome"}, "termination writes extra records")
            require("c82_cancelled=(c82_active||c82_cancelled)" in u and
                    "c82_outcome=(c82_active?5:c82_outcome)" in u and
                    u.endswith("c82_active=false"), "late cancellation fails identity rule")
            reason = "inactive termination preserves cancelled/outcome and active=false"
        else:
            raise PremiseError("unclassified record writer: " + repr(e))
        writer_cert.append({**e, "writes":sorted(w), "preservation":reason})
    # The shape certificate is part of the specialized proof premises, not generated
    # from the input under test. This closes unsupported syntax, helper bodies,
    # declaration aliases/shadowing, changed initialization, system multiplicity,
    # caller closure, and causal-order graph assumptions.
    actual = relevant_snapshot(root)
    for k, v in expected["snapshot"].items():
        require(actual[k] == v, "reviewed premise differs: " + k)
    return {"entry_obligations":entry_cert, "writer_sites":writer_cert,
            "templates":len(ts), "transitions_scanned":len(es),
            "helpers_scanned":len(funcs), "query_atoms":len(consequent),
            "scope":"exact N=1/51-process one-shot XML; mathematical argument pending review",
            "evidence_kind":"static_validation", "native_execution":False,
            "property_verdict":None, "premises_supported":True}
