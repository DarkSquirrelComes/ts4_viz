from copy import deepcopy
import json
import graphviz

global FILENAME
FILENAME = None
global data
data = None
global g
g: graphviz.Digraph = None
global excluded_fields
excluded_fields = []


def setup(filename=None, _data=None):
    global FILENAME
    global data
    if _data:
        data = _data
    if FILENAME:
        FILENAME = filename
    build_graph()

def parent_id(msg, msgs):
    if msg['msg_type'] == 'external_call':
        return 'OFF-CHAIN-CALLER'
    res = -1
    for m in msgs:
        if m['id'] < msg['id'] and m['dst'] == msg['src']:
            res = m['id']
    return res if res != -1 else 'UNKNOWN'

def build_graph():
    global g
    global data
    if g:
        g.clear()
    g = graphviz.Digraph('G', filename=FILENAME)
    g.attr(compound='true')

    # g.node('OFF-CHAIN')

    addresses = set(map(lambda m: 'OFF-CHAIN' if m['dst'] in ('', None) else m['dst'], data['allMessages']))
    addresses_with_no_nick = addresses.copy()

    for addr, nick in data['nicknames'].items():
        with g.subgraph(name='cluster' + nick) as nick_s:
            nick_s.attr(compound='true')
            nick_s.attr(label=nick)
            for a in addresses:
                addresses_with_no_nick.discard(a)
                if addr == a:
                    with nick_s.subgraph(name='cluster' + a) as s:
                        s.attr(rankdir="TB")
                        s.attr(compound='true')
                        s.attr(label=a)
                        last_msg_id = None
                        for msg in data['allMessages']:
                            if msg['dst'] == a:
                                s.node(str(msg['id']), _prettyfy_msg(msg))
                                if last_msg_id:
                                    s.edge(last_msg_id, str(msg['id']), style='invis')
                                last_msg_id = str(msg['id'])
    with g.subgraph(name='clusterOFF-CHAIN') as s:
        s.attr(label='OFF-CHAIN')
        s.attr(compound='true')
        for msg in data['allMessages']:
            if msg['dst'] in ('', None):
                s.node(str(msg['id']), _prettyfy_msg(msg))
        s.node('OFF-CHAIN-CALLER')
    g.node('UNKNOWN')


    for msg in data['allMessages']:
        g.edge(
            tail_name=str(parent_id(msg, data['allMessages'])),
            head_name=str(msg['id']),
        )

    g.save()

def _simplify_addr(addr: str):
    if addr is None:
        return None

    return addr[:5] + '...' + addr[-3:]

def _prettyfy_msg(msg, copy=True):
    if copy:
        msg = deepcopy(msg)
    for key, val in msg.items():
        if _is_addr(val):
            msg[key] = _simplify_addr(val)
        elif isinstance(val, str) and len(val) > 10:
            msg[key] = val[:9] + '...'
        if isinstance(val, dict):
            _prettyfy_msg(val, False)
    return json.dumps(msg, indent=2).replace('\n', '\l')

def _is_addr(s):
    if not isinstance(s, str):
        return False
    if len(s) != 66 or s[1] != ':':
        return False
    return True