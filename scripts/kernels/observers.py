"""Fixed-model observer-erasure premise audit. This is not a model checker."""
import argparse
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = 'models/S/model.xml'
MANIFEST = 'manifests/baselines/uav-service-completion-r1.yaml'
QUERY = 'queries/S/completion-safety.q'
PINS = {
    MODEL: 'b8ab50e112b71491f8242789cc7906497baf8440c473d7a5a4d5214840187e02',
    MANIFEST: '4b4bf71f55767123cc5934074024179289fa5ad3355fa4c0e37385e8261ef98d',
    QUERY: 'f3cfb3800063b21045d94625f616950944663fcba61956a3498aba62ca32edf9',
}
SEQ = {'u0_app_' + x + '_seq' for x in (
    'service_request', 'sla_warn', 'sla_violation', 'freshness_expired',
    'update_violation', 'fa_critical', 'miss_critical', 'safety_violation')}
CLOCKS = {'u0_phy_c_obs_' + x for x in ('sense', 'fresh', 'beam')}
CLOCKS |= {'u0_mac_c_obs_' + x for x in ('queue', 'sensing', 'buf', 'report')}
CLOCKS |= {'u0_sdn_c_obs_' + x for x in ('rule', 'admission', 'cmd', 'sensing')}
HIDDEN = SEQ | CLOCKS | {x + '_age' for x in SEQ}
RAISE = {'u0_raise_app_' + x[len('u0_app_'):]: x for x in SEQ}


class PremiseError(ValueError):
    pass


def require(test, message):
    if not test:
        raise PremiseError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean(text):
    return re.sub(r'/\*.*?\*/|//[^\n]*', '', text or '', flags=re.S)


def tokens(text):
    return set(re.findall(r'\b[A-Za-z_]\w*\b', clean(text)))


def norm(text):
    return ' '.join(re.findall(r'[A-Za-z_]\w*|\d+|==|!=|<=|>=|&&|\|\||\+\+|--|[-+*/%&|^]=|[^\s]', clean(text)))


def functions(text):
    source = clean(text)
    result, spans, pos = {}, [], 0
    pattern = re.compile(r'\b(void|bool|int)\s+([A-Za-z_]\w*)\s*\(([^{};]*)\)\s*\{')
    while m := pattern.search(source, pos):
        end, depth = m.end(), 1
        while depth and end < len(source):
            depth += (source[end] == '{') - (source[end] == '}')
            end += 1
        require(depth == 0, 'unterminated helper')
        name = m[2]
        require(name not in result, 'duplicate helper')
        require('&' not in m[3], 'reference parameter unsupported')
        result[name] = {'type': m[1], 'parameters': m[3], 'body': source[m.end():end-1]}
        spans.append((m.start(), end))
        pos = end
    remainder = source
    for start, end in reversed(spans):
        remainder = remainder[:start] + remainder[end:]
    require(not re.search(r'\bextern\b|\bimport\b|\bstruct\b', remainder), 'external/aggregate declarations unsupported')
    return result, remainder


def direct_writes(text):
    return set(re.findall(r'\b([A-Za-z_]\w*)\s*(?:\[[^\]]*\]\s*)?(?:=(?!=)|\+\+|--|[-+*/%&|^]=)', clean(text)))


def calls(text, funcs):
    return tokens(text) & {n for n in funcs if re.search(r'\b' + re.escape(n) + r'\s*\(', clean(text))}


def effects(text, funcs, stack=()):
    callable_names = set(re.findall(r'\b([A-Za-z_]\w*)\s*\(', clean(text)))
    syntax = {'if', 'while', 'for', 'switch', 'return', 'imply'}
    require(callable_names <= set(funcs) | syntax,
            'unknown callable syntax: ' + ','.join(sorted(callable_names - set(funcs) - syntax)))
    reads, writes, used = tokens(text), direct_writes(text), set()
    for name in sorted(calls(text, funcs)):
        require(name not in stack, 'recursive helper unsupported: ' + name)
        r, w, c = effects(funcs[name]['body'], funcs, stack + (name,))
        reads |= r
        writes |= w
        used |= c | {name}
    return reads, writes, used


def labels(element):
    values = {}
    for lab in element.findall('label'):
        kind = lab.get('kind')
        if kind == 'comments':
            continue
        require(kind not in values, 'duplicate label')
        values[kind] = clean(lab.text).strip()
    return values


def audit(root, query, capsule):
    """No byte gate here: used independently by mutation controls."""
    templates = root.findall('template')
    names = [t.findtext('name') for t in templates]
    require(len(names) == len(set(names)) == 51, 'exact template inventory required')
    funcs, remainder = functions(root.findtext('declaration'))
    # Bind declaration syntax/types/initial values without using the XML hash.
    # Bodies are audited below; this capsule does not seal changed function bodies.
    require(norm(remainder) == capsule['declaration_remainder'], 'global declaration capsule changed')
    require(set(funcs) == set(capsule['function_signatures']), 'helper inventory changed')
    for name, f in funcs.items():
        require([f['type'], norm(f['parameters'])] == capsule['function_signatures'][name], 'helper signature changed')
        require(not (tokens(f['parameters']) & HIDDEN), 'hidden parameter shadow')
        if tokens(f['body']) & HIDDEN:
            require(name in RAISE, 'hidden read/write in non-recorder helper: ' + name)
            seq = RAISE[name]
            expected = f'if (!{seq}) {{ {seq} = true; {seq}_age = 0; }}'
            require(norm(f['body']) == norm(expected), 'recorder must affect hidden state only: ' + name)
        effects(f['body'], funcs, (name,))
    system = clean(root.findtext('system'))
    require('<' not in system and 'priority' not in system, 'process priority unsupported')
    binding_matches = list(re.finditer(r'([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*\(\s*\)\s*;', system))
    bindings = {m[1]: m[2] for m in binding_matches}
    order_match = re.search(r'\bsystem\s+([A-Za-z_\w,\s]+);', system)
    require(order_match is not None, 'system declaration unsupported')
    order = [x.strip() for x in order_match[1].split(',')]
    residue = system
    for m in reversed(binding_matches):
        residue = residue[:m.start()] + residue[m.end():]
    require(norm(residue) == norm(order_match[0]), 'unsupported system statement')
    require(len(bindings) == len(binding_matches) == len(order) == 51 and len(set(order)) == 51, 'unique instance inventory required')
    require(set(order) == set(bindings) and set(bindings.values()) == set(names), 'one instance per template required')
    require(bindings == capsule['bindings'] and order == capsule['order'], 'system binding/order changed')
    observer_names = {n for n in names if 'Obs' in n}
    require(observer_names == set(capsule['observers']) and len(observer_names) == 22, 'observer inventory changed')
    # Parse only simple global channel declarations; exact remainder seal guards the grammar.
    channels = {}
    for m in re.finditer(r'\b(?:(urgent)\s+)?(?:(broadcast)\s+)?chan\s+([^;]+);', remainder):
        for chan in m[3].split(','):
            chan = chan.strip()
            require(re.fullmatch(r'[A-Za-z_]\w*', chan) is not None, 'array/compound channel unsupported')
            channels[chan] = {'urgent': bool(m[1]), 'broadcast': bool(m[2])}
    observer_edges, committed_exits, production_sites = [], [], []
    helper_sites = []
    sync_receives = 0
    for t in templates:
        name = t.findtext('name')
        observer = name in observer_names
        require(norm(t.findtext('declaration')) == capsule['locals'][name], 'local declaration changed: ' + name)
        require(norm(t.findtext('parameter')) == capsule['parameters'][name], 'template parameter changed')
        require(not (tokens(t.findtext('declaration')) & HIDDEN), 'local hidden shadow')
        locs = {l.get('id'): l for l in t.findall('location')}
        require(len(locs) == len(t.findall('location')), 'duplicate location')
        require(t.find('init').get('ref') in locs, 'invalid init')
        committed = {i for i, l in locs.items() if l.find('committed') is not None}
        if observer:
            require(not clean(t.findtext('declaration')).strip(), 'observer local state unsupported')
            require(t.find('init').get('ref') not in committed, 'observer starts committed')
        for lid, loc in locs.items():
            labs = labels(loc)
            if observer:
                require(not labs, 'observer invariant/rate unsupported: ' + name)
                require(loc.find('urgent') is None, 'urgent observer location: ' + name)
            else:
                for kind, text in labs.items():
                    r, w, c = effects(text, funcs)
                    require(not (r & HIDDEN), 'hidden dependency in production location: ' + name)
                    require(not w, 'side effect in production invariant')
        outgoing = {i: [] for i in sorted(committed)} if observer else {}
        for idx, edge in enumerate(t.findall('transition')):
            src, dst = edge.find('source').get('ref'), edge.find('target').get('ref')
            require(src in locs and dst in locs, 'bad edge endpoint')
            labs = labels(edge)
            require(set(labs) <= {'guard', 'assignment', 'synchronisation', 'select'}, 'unsupported edge annotation')
            record = {'template': name, 'edge': idx, 'source': locs[src].findtext('name'),
                      'target': locs[dst].findtext('name'), 'labels': labs}
            if src in outgoing:
                outgoing[src].append(record)
            for kind, text in labs.items():
                r, w, c = effects(text, funcs)
                if kind != 'assignment':
                    require(not w, 'side effect in guard/sync/select: ' + name)
                if observer:
                    require(kind != 'select', 'observer select unsupported')
                    require(w <= HIDDEN, 'observer writes retained state: ' + name)
                    if kind == 'assignment':
                        require(not c, 'observer helper update unsupported')
                        for part in text.split(','):
                            m = re.fullmatch(r'([A-Za-z_]\w*)\s*=\s*(0|false)', part.strip())
                            require(m is not None and m[1] in CLOCKS | SEQ, 'observer update grammar unsupported')
                    if kind == 'synchronisation':
                        m = re.fullmatch(r'([A-Za-z_]\w*)\?', text)
                        require(m is not None, 'observer must receive, never send')
                        require(m[1] in channels and channels[m[1]] == {'urgent': False, 'broadcast': True}, 'observer binary/urgent input')
                        sync_receives += 1
                else:
                    # Production may call exact void recorder helpers whose hidden
                    # effects do not influence a retained result or branch.
                    require(not (tokens(text) & HIDDEN), 'direct hidden dependency in production edge: ' + name)
                    if r & HIDDEN:
                        require(kind == 'assignment', 'transitive hidden enabling dependency: ' + name)
                        helper_sites.append({**record, 'helpers': sorted(c), 'hidden_effects': sorted(w & HIDDEN)})
                    production_sites.append({**record, 'kind': kind, 'read_identifiers': sorted(r), 'writes': sorted(w), 'helpers': sorted(c)})
            if observer:
                observer_edges.append(record)
        for lid, edges in outgoing.items():
            require(len(edges) == 2, 'committed exit must be complementary pair')
            require(all(set(e['labels']) == {'guard'} for e in edges), 'committed exit has side effects/sync')
            require(all(e['target'] not in {locs[i].findtext('name') for i in committed} for e in edges), 'committed cycle')
            guards = [re.fullmatch(r'([A-Za-z_]\w*)\s*(<=|>)\s*([A-Za-z_]\w*)', e['labels']['guard']) for e in edges]
            require(all(g is not None for g in guards), 'unsupported committed exit partition')
            require({g[2] for g in guards} == {'<=', '>'} and len({(g[1], g[3]) for g in guards}) == 1, 'committed exit gap/overlap')
            require(guards[0][1] in CLOCKS, 'committed exit clock is retained')
            require(re.search(r'\bconst\s+int\s+' + re.escape(guards[0][3]) + r'\s*=\s*\d+\s*;', remainder) is not None, 'deadline must be integer constant')
            committed_exits.append({'template': name, 'location': locs[lid].findtext('name'), 'edges': edges})
    qreads, qwrites, qcalls = effects(query, funcs)
    require(not qwrites and not (qreads & HIDDEN), 'query not retained-state predicate')
    removed_instances = [i for i in order if bindings[i] in observer_names]
    require(not (tokens(query) & set(removed_instances)), 'query refers to erased observer')
    require('deadlock' not in tokens(query), 'deadlock is not a projected state predicate')
    return {
        'evidence_kind': ['mathematical_argument', 'static_validation'],
        'execution_status': 'not_applicable', 'property_verdict': 'not_applicable',
        'acceptance_status': 'pending_independent_review',
        'counts': {'original_processes': 51, 'removed_observers': 22, 'retained_processes': 29,
                   'global_helpers': len(funcs), 'observer_edges': len(observer_edges),
                   'broadcast_receive_edges': sync_receives, 'committed_locations': len(committed_exits)},
        'hidden_variables': sorted(HIDDEN), 'retained_recorders': ['u0_mac_c_obs_ack', 'u0_sdn_c_obs_rec'],
        'removed_instances': removed_instances, 'retained_order': [i for i in order if i not in removed_instances],
        'observer_edges': observer_edges, 'committed_exit_certificate': committed_exits,
        'production_sites': production_sites, 'hidden_helper_callsites': helper_sites,
        'function_dependencies': {n: {'reads': sorted(effects(f['body'], funcs, (n,))[0]),
                                     'writes': sorted(effects(f['body'], funcs, (n,))[1]),
                                     'calls': sorted(effects(f['body'], funcs, (n,))[2])} for n, f in funcs.items()},
        'query': query.strip(), 'query_helpers': sorted(qcalls),
    }


def erase(root, certificate):
    reduced = copy.deepcopy(root)
    removed = set(certificate['removed_instances'])
    for t in list(reduced.findall('template')):
        if 'Obs' in t.findtext('name'):
            reduced.remove(t)
    system = clean(reduced.findtext('system'))
    lines = [line for line in system.splitlines() if not any(re.match(r'\s*' + re.escape(i) + r'\s*=', line) for i in removed) and not line.strip().startswith('system ')]
    lines.append('system ' + ', '.join(certificate['retained_order']) + ';')
    reduced.find('system').text = '\n'.join(lines) + '\n'
    # Retain all global declarations, even hidden recorder state, verbatim.
    # Only locations/templates/bindings disappear; surviving behavior is unchanged.
    for queries in reduced.findall('queries'):
        reduced.remove(queries)
    ET.indent(reduced, space='  ')
    return b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(reduced, encoding='utf-8') + b'\n'
