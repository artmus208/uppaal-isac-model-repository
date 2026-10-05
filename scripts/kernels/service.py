"""Fixed-model premise audit; never invokes a verifier."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEPENDENCY = HERE
spec = importlib.util.spec_from_file_location('receipt_premises', DEPENDENCY / 'receipt.py')
receipt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receipt)
require, norm, compact = receipt.require, receipt.norm, receipt.compact
APP, JOB = receipt.APP, receipt.JOB
TERMINALS = {'Rejected', 'Completed', 'ServiceFailed', 'ServiceTimeout', 'Cancelled'}
TRACKED = {'c82_service_age', 'c82_sample_age', 'u0_app_c_admission',
           'c82_fifo_rank', 'c82_enqueued', 'c82_dispatched', 'c82_sampled',
           'u0_mac_queue_q', 'c82_tx_age'}
MODEL = receipt.MODEL


def sha(data):
    return hashlib.sha256(data).hexdigest()


def direct(code, symbols):
    names = '|'.join(re.escape(s) for s in sorted(symbols))
    return set(re.findall(r'\b(' + names + r')\s*(?:=(?!=)|\+\+|--|[-+*/%&|^]=)',
                          receipt.uncomment(code)))


def written(code, funcs, symbols, stack=()):
    result = direct(code, symbols)
    for name in receipt.calls(code, funcs):
        require(name not in stack, 'recursive helper unsupported')
        result |= written(funcs[name].split('{', 1)[1][:-1], funcs, symbols, stack+(name,))
    return result


def snapshot(root):
    """Full semantic capsule (coordinates/nails excluded); fixed after review."""
    result = {'global_declaration': sha(norm(root.findtext('declaration')).encode()),
              'system': norm(root.findtext('system')), 'templates': {}}
    for t in root.findall('template'):
        require(all(x.tag in {'name','declaration','parameter','location','init','transition'}
                    for x in t), 'unsupported template element')
        name = t.findtext('name')
        require(name not in result['templates'], 'duplicate template')
        loc = [{'id': l.get('id'), 'name': l.findtext('name'),
                'labels': [(x.get('kind'), norm(x.text)) for x in l.findall('label')],
                'committed': l.find('committed') is not None,
                'urgent': l.find('urgent') is not None} for l in t.findall('location')]
        value = {'declaration': norm(t.findtext('declaration')),
                 'parameter': norm(t.findtext('parameter')), 'locations': loc,
                 'init': t.find('init').get('ref'),
                 'edges': [{k: norm(v) if isinstance(v, str) else v for k,v in e.items()}
                           for e in receipt.edges(root) if e['template'] == name]}
        result['templates'][name] = sha(json.dumps(value, sort_keys=True).encode())
    return result


def scalar(decl, name):
    matches = re.findall(r'\b' + re.escape(name) + r'\s*=\s*(\d+)\b', decl)
    require(len(matches) == 1, 'unique scalar constant required: '+name)
    return int(matches[0])


def node_map(t):
    return {l.findtext('name'): l for l in t.findall('location')}


def sites(es, symbol, funcs):
    return {(e['template'], e['index']) for e in es
            if symbol in written(e.get('assignment', ''), funcs, TRACKED)}


def analyze(root, capsule):
    """Called directly by mutations; outer full-byte gates are not used here."""
    ts = {t.findtext('name'): t for t in root.findall('template')}
    require(len(ts) == len(root.findall('template')), 'duplicate template')
    es = receipt.edges(root)
    funcs, _ = receipt.functions(root.findtext('declaration'))
    decl = receipt.uncomment(root.findtext('declaration'))
    constants = {n: scalar(decl, n) for n in
                 ['u0_bus_T_mac_tick', 'c82_D_service', 'u0_app_D_admission',
                  'u0_bus_D_bus', 'u0_mac_queue_K', 'u0_phy_D_sense']}
    require(constants == {'u0_bus_T_mac_tick':5, 'c82_D_service':40,
                          'u0_app_D_admission':15, 'u0_bus_D_bus':1,
                          'u0_mac_queue_K':4, 'u0_phy_D_sense':5}, 'changed timing/capacity constants')
    ae = [e for e in es if e['template'] == APP]
    se = [e for e in es if e['template'] == 'SharedLoad']
    al = node_map(ts[APP])
    sl = node_map(ts['SharedLoad'])
    require(al['ServiceIdle'].get('id') == ts[APP].find('init').get('ref'), 'APP initialization')
    require(ae[2]['source'] == 'RequestReady' and ae[2]['target'] == 'RequestPending',
            'emission graph')
    require('c82_emit_request' in receipt.calls(ae[2].get('assignment',''), funcs), 'emission helper')
    require('u0_app_c_admission=0' in compact(ae[2]['assignment']), 'emission admission reset')
    post, todo = set(), ['RequestPending']
    while todo:
        source = todo.pop()
        if source in post:
            continue
        post.add(source)
        todo.extend(e['target'] for e in ae if e['source'] == source)
    require(post == TERMINALS | {'RequestPending','Accepted','AcceptedDegraded'}, 'post-emission escape')
    require(not any(e['source'] in TERMINALS for e in ae), 'terminal not absorbing')
    inv = {n: compact('&&'.join(x.text or '' for x in al[n].findall("label[@kind='invariant']")))
           for n in post-TERMINALS}
    require(inv == {'RequestPending':'u0_app_c_admission<=u0_app_D_admission',
                    'Accepted':'c82_service_age<=c82_D_service',
                    'AcceptedDegraded':'c82_service_age<=c82_D_service'}, 'APP clock bounds')
    # Complete transitive closure of writers of the timing/rank stage variables.
    required_sites = {'c82_service_age':{(APP,2)}, 'u0_app_c_admission':{(APP,2)},
        'c82_sample_age':{(receipt.PHY,25)}, 'c82_sampled':{(receipt.PHY,25)},
        'c82_enqueued':{('SharedLoad',5)},
        'c82_fifo_rank':{('SharedLoad',1),('SharedLoad',5)},
        'c82_dispatched':{('SharedLoad',1)},
        'u0_mac_queue_q':{('SharedLoad',1),('SharedLoad',5),('SharedLoad',6)},
        'c82_tx_age':{(JOB,6)}}
    for symbol, wanted in required_sites.items():
        require(sites(es,symbol,funcs) == wanted, 'writer closure: '+symbol)
    for e in es:
        for label in ['guard','select','synchronisation']:
            require(not written(e.get(label,''),funcs,TRACKED), 'side effects outside update')
    require('c82_service_age=0' in compact(funcs['c82_emit_request']), 'service reset')
    require('c82_sample_age=0' in compact(funcs['c82_store_measurement']), 'sample reset')
    pe = [e for e in es if e['template']==receipt.PHY][25]
    require('!c82_sampled' in receipt.conjuncts(pe['guard']), 'one-shot measurement guard')
    require('c82_active' in receipt.conjuncts(se[5]['guard']) and
            '!c82_enqueued' in receipt.conjuncts(se[5]['guard']) and
            'u0_mac_queue_q<u0_mac_queue_K' in receipt.conjuncts(se[5]['guard']), 'one-shot insertion guard')
    require('u0_mac_queue_q++;c82_fifo_rank=u0_mac_queue_q;c82_enqueued=true;' in
            compact(funcs['c82_insert_result']), 'post-increment FIFO rank')
    service = compact(funcs['c82_mac_service'])
    require('if(c82_fifo_rank==1){c82_fifo_rank=0;c82_dispatched=true;' in service,
            'dispatch at rank one')
    require('elsec82_fifo_rank--;' in service, 'unit rank decrement')
    require('u0_mac_queue_q=(u0_mac_queue_q>u0_mac_queue_K?u0_mac_queue_q:' in
            compact(se[1]['assignment']), 'absorbing overflow in aggregate update')
    require('server==0&&c82_active&&c82_enqueued&&!c82_dispatched' in service and
            'u0_mac_queue_q<=u0_mac_queue_K&&c82_fifo_rank>0' in service, 'service eligibility')
    require([e['index'] for e in se if 'c82_mac_service' in receipt.calls(e.get('assignment',''),funcs)]
            == [1], 'unique service decision')
    require(compact(se[1]['assignment']).startswith('c82_mac_service(server),'), 'service before aggregate update')
    require(compact(se[0]['guard']) == 'tick==u0_bus_T_mac_tick' and
            'tick==u0_bus_T_mac_tick' in receipt.conjuncts(se[1]['guard']), 'epoch guards')
    require('server:int[-1,0]' == compact(se[1]['select']), 'optional server choice')
    require(compact(se[1]['assignment']).endswith('tick=0'), 'decision clock reset')
    require([(e['index'],sorted(direct(e.get('assignment',''),{'tick'}))) for e in se
             if direct(e.get('assignment',''),{'tick'})] == [(1,['tick'])], 'sole tick writer')
    require(compact(ts['SharedLoad'].findtext('declaration')).startswith('clocktick;'), 'ordinary tick clock')
    require(sl['Wait'].get('id') == ts['SharedLoad'].find('init').get('ref'), 'epoch initialization')
    require(compact(sl['Wait'].findtext("label[@kind='invariant']"))=='tick<=u0_bus_T_mac_tick', 'epoch invariant')
    require(all(sl[n].find('committed') is not None for n in ['Sample_1','Publish_0','Offer_0']),
            'zero-time decision cycle')
    shape = [(e['source'], e['target']) for e in se]
    require(shape == [('Wait','Sample_1'),('Sample_1','Publish_0'),('Publish_0','Offer_0'),
                      ('Offer_0','Wait'),('Offer_0','Wait'),('Wait','Wait'),('Wait','Wait')], 'service graph')
    success = [e for e in ae if e['target']=='Completed']
    require(len(success)==4 and all('c82_sample_age<5' in receipt.conjuncts(e['guard'])
                                    for e in success), 'strict freshness entrances')
    for e in success:
        require('c82_result_delivery?' == compact(e.get('synchronisation','')), 'actual success delivery')
    jl = node_map(ts[JOB])
    je = [e for e in es if e['template']==JOB]
    require(compact(jl['Transmitting'].findtext("label[@kind='invariant']")) ==
            'c82_tx_age<=u0_bus_D_bus', 'bounded attempted transport')
    require('c82_tx_age=0' in compact(je[6]['assignment']), 'attempt transport reset')
    require(je[6]['source']=='Queued' and je[6]['target']=='Transmitting' and
            je[7]['source']=='Transmitting' and je[7]['target']=='Done', 'attempt delivery graph')
    actual = snapshot(root)
    require(actual == capsule, 'reviewed full semantic capsule changed')
    writers = [{**e,'writes':sorted(written(e.get('assignment',''),funcs,TRACKED))} for e in es
               if written(e.get('assignment',''),funcs,TRACKED)]
    return {'templates':len(ts), 'transitions_scanned':len(es), 'helpers_scanned':len(funcs),
            'constants':constants, 'post_emission_locations':sorted(post),
            'terminals':sorted(TERMINALS), 'nonterminal_invariants':inv,
            'writer_sites':writers, 'tick_writer':se[1],
            'success_entrances':success, 'rank_cap_earliest_time_only':1,
            'evidence_kind':'static_validation', 'model_checking_verdict':None,
            'mathematical_acceptance':'pending_independent_review'}


def age(rank, enqueue=0, phase=0, skipped=0, launch=0, transport=0, period=5):
    require(isinstance(rank,int) and rank>=1, 'positive integer rank')
    require(isinstance(skipped,int) and skipped>=0, 'nonnegative integer skips')
    vals = list(map(Fraction,[enqueue,phase,launch,transport,period]))
    require(all(x>=0 for x in vals) and vals[-1]>0, 'nonnegative latencies; positive period')
    return sum(vals[:4]) + (rank-1+skipped)*vals[-1]


def rational_examples():
    cases = [dict(rank=1,phase='7/2',transport=1),
             dict(rank=1,phase=4,transport=1),
             dict(rank=1,phase='9/2',transport=1),
             dict(rank=2),dict(rank=3),dict(rank=4),dict(rank=1,skipped=1),
             dict(rank=1,enqueue=1,phase=2,launch=1,transport=1)]
    return [{'input':c,'receipt_age':str(age(**c)),'strict_fresh':age(**c)<5,
             'evidence':'rational_contract_example_not_full_model_trace'} for c in cases]
