"""Reproduce #101 static premises and a finite abstract graph; never run verifyta.

Only the hash-pinned N=1..4 inputs can receive published certificates. The
structural routine is deliberately restrictive and exposed for mutation tests;
it is not a general UPPAAL parser or an arbitrary-model proof service.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = "manifests/baselines/uav-family-r1.yaml"
MANIFEST_SHA256 = "5480bef5b00020735259f10eb43bdd9bc79ebc364a3bbcacad34c78fd0552cbf"
RUN_ROOT = "evidence/scalability/runs/uav-family-p4-20260929"
RUNS = RUN_ROOT + "/campaign-002/runs.json"
RUNS_SHA256 = "1ec3a64b5e012e4b5072107f23ec12b60ed04ac22ba2ba0a0e5f16b003efc0c8"
BASE = "f0fcd770e3e6b93f99868b9116e4f0929f60d0fa"
DOMAIN = (1, 2, 3, 4)
PROTECTED = re.compile(r"\bfamily_(?:grant_\w*|last_server)\b")
IDENT = r"[A-Za-z_][A-Za-z_0-9]*"


class PremiseError(ValueError):
    """An input identity or a necessary supported premise could not be checked."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PremiseError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def pinned(root: Path, relative: str, expected: str) -> bytes:
    require(not Path(relative).is_absolute(), "absolute input path")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "input path escapes repository")
    data = path.read_bytes()
    require(digest(data) == expected, "hash mismatch: " + relative)
    return data


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def query_for(n: int) -> str:
    terms = " + ".join(f"(family_grant_{i} ? 1 : 0)" for i in range(n))
    return f"A[] ({terms} <= 1)"


def guard_for(n: int) -> str:
    terms = ["tick == u0_bus_T_mac_tick"]
    for i in range(n):
        terms.append(f"(server != {i} || (u{i}_mac_queue_q > 0 && "
                     f"(u{i}_mac_scheduleMode == u{i}_mac_SCH_COMM || "
                     f"u{i}_mac_scheduleMode == u{i}_mac_SCH_JOINT)))")
    return " && ".join(terms)


def split_updates(text: str) -> list[str]:
    """Split only the accepted scalar-expression update dialect, without eval."""
    require(not re.search(r"[^A-Za-z_0-9\s(),=?:!<>&|+\-]", text),
            "unsupported character in writer update")
    require(not re.search(r"\+\+|--|\+=|-=|(?<![&])&(?![&])|(?<![|])\|(?![|])", text),
            "side effect or reference syntax in writer update")
    # A function call could mutate a passed selector; no calls are needed here.
    require(not re.search(rf"\b{IDENT}\s*\(", text), "function call in writer update")
    depth, start, result = 0, 0, []
    for pos, char in enumerate(text):
        depth += (char == "(") - (char == ")")
        require(depth >= 0, "unbalanced writer update")
        if char == ",":
            require(depth == 0, "nested comma in writer update")
            result.append(text[start:pos].strip())
            start = pos + 1
    require(depth == 0, "unbalanced writer update")
    result.append(text[start:].strip())
    for statement in result:
        match = re.fullmatch(rf"({IDENT})\s*=\s*(.+)", statement, re.S)
        require(match is not None, "unsupported writer statement")
        lhs, rhs = match.groups()
        require(lhs != "server", "selector is modified")
        require(not re.search(r"(?<![=!<>])=(?!=)", rhs), "nested assignment in writer update")
    return result


@dataclass(frozen=True)
class Premises:
    n: int
    initial_server: int
    initial_grants: tuple[bool, ...]
    grant_targets: tuple[int, ...]
    source: str
    target: str
    processes: int
    templates: int
    locations: int
    transitions: int
    protected_occurrences: int


def check_structure(xml: bytes, query: str, n: int) -> Premises:
    require(n in DOMAIN, "N outside the accepted finite domain")
    # No DTD expansion, embedded foreign dialect, external code, or lifecycle
    # hooks are within this checker's trust boundary.
    require(b"<!" not in xml, "DTD/entity/comment extension unsupported")
    try:
        tree = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise PremiseError("malformed XML") from exc
    allowed = {"nta", "declaration", "template", "name", "location", "label",
               "committed", "urgent", "init", "transition", "source", "target",
               "nail", "system", "queries"}
    require(tree.tag == "nta" and all(e.tag in allowed for e in tree.iter()),
            "unsupported XML element")
    require(len(tree.findall("declaration")) == 1 and len(tree.findall("system")) == 1,
            "global declaration/system must be unique")
    fields = [(e, "text", e.text or "") for e in tree.iter()]
    fields += [(e, "tail", e.tail or "") for e in tree.iter()]
    fields += [(e, key, value) for e in tree.iter() for key, value in e.attrib.items()]
    all_text = "\n".join(value for _, _, value in fields)
    require(not re.search(r"\b(?:import|extern|__ON_\w*|(?:__)?before_update|(?:__)?after_update)\b", all_text),
            "external code or lifecycle hook unsupported")
    declaration = tree.find("declaration")
    prefix = f"const int FAMILY_N={n};\nint[-1,{n-1}] family_last_server=-1;\n"
    prefix += "\n".join(f"bool family_grant_{i}=false;" for i in range(n))
    global_text = declaration.text or ""
    require(global_text.startswith(prefix), "initial declarations/domain differ")
    require(not PROTECTED.search(global_text[len(prefix):]),
            "protected reference outside initial declarations")
    templates = tree.findall("template")
    names = [t.findtext("name") for t in templates]
    require(len(names) == len(set(names)) and all(names), "ambiguous template names")
    require(names.count("SharedLoad") == 1, "SharedLoad must be unique")
    shared = templates[names.index("SharedLoad")]
    writer_candidates = [edge for edge in shared.findall("transition")
                         if any(PROTECTED.search(label.text or "")
                                for label in edge.findall("label"))]
    require(len(writer_candidates) == 1, "expected exactly one protected writer edge")
    writer = writer_candidates[0]
    labels = writer.findall("label")
    require(sorted(label.get("kind") for label in labels) == ["assignment", "guard", "select"],
            "writer must be internal with one select, guard, and update")
    label_by_kind = {label.get("kind"): label for label in labels}
    require(compact(label_by_kind["select"].text or "") == f"server:int[-1,{n-1}]",
            "writer selector/domain differ")
    require(compact(label_by_kind["guard"].text or "") == compact(guard_for(n)),
            "unsupported eligibility guard")
    update = label_by_kind["assignment"]
    statements = split_updates(update.text or "")
    grant_targets = {}
    last_writes = 0
    for statement in statements:
        if PROTECTED.search(statement):
            grant = re.fullmatch(r"family_grant_(\d+)\s*=\s*\(server\s*==\s*(\d+)\)", statement)
            if grant:
                lhs, rhs = map(int, grant.groups())
                require(lhs not in grant_targets and lhs < n and lhs == rhs,
                        "duplicate, missing, or incorrect grant mapping")
                grant_targets[lhs] = rhs
            else:
                require(compact(statement) == "family_last_server=server", "unsupported protected update")
                last_writes += 1
        else:
            # Every selector occurrence elsewhere is a read of a service amount.
            residual = re.sub(r"\(\s*server\s*==\s*[0-9]+\s*\?\s*1\s*:\s*0\s*\)", "0", statement)
            require(not re.search(r"\bserver\b", residual), "unsupported selector use")
    require(set(grant_targets) == set(range(n)) and last_writes == 1,
            "all grants and last_server must be assigned exactly once")
    # This deliberately accounts for EVERY textual occurrence, including local
    # declarations, by-reference arguments, functions, guards, and attributes.
    for element, field, value in fields:
        if element is declaration and field == "text":
            value = value[len(prefix):]
        elif element is update and field == "text":
            value = ""
        require(not PROTECTED.search(value), "unaccounted protected reference")
        if element not in labels or field != "text":
            require(not re.search(r"\bserver\b", value), "selector shadow/exposure outside writer")
    source = writer.find("source")
    target = writer.find("target")
    require(source is not None and target is not None, "missing writer endpoint")
    require(source.get("ref") == f"shared_Sample_{n}" and target.get("ref") == "shared_Publish_0",
            "writer endpoints differ")
    system = tree.findtext("system") or ""
    parts = system.split(";")
    require(not parts[-1].strip() and len(parts) >= 3, "unsupported system definition")
    bindings = {}
    for statement in parts[:-2]:
        match = re.fullmatch(rf"\s*({IDENT})\s*=\s*({IDENT})\s*\(\s*\)\s*", statement)
        require(match is not None, "system must contain only zero-argument bindings")
        process, template = match.groups()
        require(process not in bindings and template in names, "invalid process binding")
        bindings[process] = template
    match = re.fullmatch(r"\s*system\s+(.+)\s*", parts[-2], re.S)
    require(match is not None, "missing system composition")
    processes = [p.strip() for p in match.group(1).split(",")]
    require(len(processes) == len(set(processes)) and set(processes) == set(bindings),
            "system processes differ from bindings")
    require(list(bindings.values()).count("SharedLoad") == 1 and
            bindings.get("shared_load") == "SharedLoad", "one shared_load instance required")
    require(len(processes) == 49 * n + 1, "unexpected finite-family process count")
    require(compact(query) == compact(query_for(n)), "query differs from shared-capacity")
    return Premises(n, -1, (False,) * n, tuple(grant_targets[i] for i in range(n)),
                    source.get("ref"), target.get("ref"), len(processes), len(templates),
                    len(list(tree.iter("location"))), len(list(tree.iter("transition"))),
                    len(PROTECTED.findall(all_text)))


def projected_step(premises: Premises, selector: int) -> tuple[int, tuple[bool, ...]]:
    require(-1 <= selector < premises.n, "abstract selector out of range")
    return selector, tuple(selector == target for target in premises.grant_targets)


def explore(premises: Premises) -> dict:
    """BFS over an overapproximation, not an UPPAAL state-space exploration."""
    initial = (premises.initial_server, premises.initial_grants)
    queue, reached, edges = deque([initial]), {initial}, set()
    while queue:
        state = queue.popleft()
        successors = [state] + [projected_step(premises, j) for j in range(-1, premises.n)]
        for successor in successors:
            edges.add((state, successor))
            if successor not in reached:
                reached.add(successor)
                queue.append(successor)
    ordered = sorted(reached)
    relation = all(all(g == (last == i) for i, g in enumerate(grants))
                   for last, grants in ordered)
    capacity = all(sum(grants) <= 1 for _, grants in ordered)
    require(relation and capacity, "abstract inductive conclusion failed")
    return {
        "evidence_kind": "finite_abstract_graph_enumeration_not_native_model_checking",
        "unrestricted_projection_valuations": (premises.n + 1) * 2 ** premises.n,
        "reachable_states": [{"last_server": last, "grants": list(grants)} for last, grants in ordered],
        "reachable_state_count": len(reached),
        "unique_source_target_pairs_including_self_loops": len(edges),
        "labeled_discrete_edges_including_stutter": len(reached) * (premises.n + 2),
        "delay_rule": "every nonnegative delay is a self-loop; not counted as discrete edges",
        "strong_relation_holds_on_enumerated_states": relation,
        "capacity_holds_on_enumerated_states": capacity,
        "native_property_verdict": None,
        "concrete_service_nonvacuity": "not_established",
    }
