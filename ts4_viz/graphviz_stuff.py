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

def build_graph():
    global g
    global data
    if g:
        g.clear()
    g = graphviz.Digraph('G', filename=FILENAME)

    g.node('OFF-CHAIN')

    for addr, nick in data['nicknames'].items():
        g.node(name=addr[2:], label= f'{_simplify_addr(addr)}\n({nick})')


    for msg in data['allMessages']:
        g.edge(
            tail_name=(msg['src'] or '__OFF-CHAIN')[2:],
            head_name=(msg['dst'] or '__OFF-CHAIN')[2:],
            label=_prettyfy_msg(msg),
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
        if isinstance(val, dict):
            _prettyfy_msg(val, False)
    return json.dumps(msg, indent=2).replace('\n', '\l')

def _is_addr(s):
    if not isinstance(s, str):
        return False
    if len(s) != 66 or s[1] != ':':
        return False
    return True