import cmd
from copy import deepcopy

import ts4_viz.graphviz_stuff as gs


class MsgVizualizerShell(cmd.Cmd):
    intro = 'Welcome to the shell.\n'
    prompt = '(vizualize) '
    file = None

    def __init__(self, data, *args, **kwargs) -> None:
        self._original_data = deepcopy(data)
        self._data = [deepcopy(data)]
        self._index = 0
        super().__init__(*args, **kwargs)


    #---- FILTER MESSAGES ----#

    def do_filter_messages_by_index(self, arg):
        '''filter_messages_by_index optional(start_index) finish_index'''
        try:
            args = list(map(int, arg.split()))
            assert 1 <= len(args) <= 2
        except:
            print('wrong args number')
            return
        rng = set(range(*args))
        # print(rng)
        pred = lambda msg: msg['id'] in rng
        data = self._peek_data()
        data['allMessages'] = list(filter(pred, data['allMessages']))
        self._push_data(data)
        gs.setup(_data=deepcopy(data))

    def do_exclude_offchain_messages(self, _):
        '''exclude events and external calls'''
        self._exclude_msgs_by_predicate(
            lambda msg: msg['msg_type'] not in ('event', 'external_call')
        )
        gs.setup(_data=self._peek_data())

    def do_exclude_onchain_messages(self, _):
        '''exclude all messages except events and external calls'''
        self._exclude_msgs_by_predicate(
            lambda msg: msg['msg_type'] in ('event', 'external_call')
        )
        gs.setup(_data=self._peek_data())

    def do_exclude_msgs_with_type(self, arg: str):
        '''types are call, external_call, event'''
        arg = arg.strip()
        self._exclude_msgs_by_predicate(
            lambda msg: msg['msg_type'] != arg
        )
        gs.setup(_data=self._peek_data())

    def do_exclude_msgs_with_name(self, arg):
        '''filter by method\'s name'''
        arg = arg.strip()
        self._exclude_msgs_by_predicate(
            lambda msg: msg['name'] != arg
        )
        gs.setup(_data=self._peek_data())

    def do_exclude_msgs_by_predicate(self, arg):
        '''supports python lambda functions, for example
        exclude_msgs_by_predicate lambda msg: msg["name"] in ("ping", "pong")
        exclude_msgs_by_predicate lambda msg: 10 < msg["timestamp"] < 1000
        exclude_msgs_by_predicate lambda msg: msg["dst"].startswith("0dfe") and msg["name"] != "ping"
        '''

        arg = arg.strip()
        p = eval(arg)

        def pred(x):
            try:
                return not p(x)
            except:
                return True

        self._exclude_msgs_by_predicate(pred)
        gs.setup(_data=self._peek_data())


    # ---- FILTER CONTRACTS ----#

    def do_exclude_address(self, arg: str):
        '''also supports addresses as prefixes, for example
        exclude_address 0:abc
        exclude_address dfe
        '''
        arg = arg.strip()
        if not arg.startswith('0:'):
            arg = '0:' + arg
        self._exclude_addrss_by_predicate(
            lambda addr: addr.startswith(arg)
        )
        self._exclude_msgs_by_predicate(
            lambda msg: not ((msg['src'] or '').startswith(arg) or (msg['dst'] or '').startswith(arg))
        )
        gs.setup(_data=self._peek_data())

    def do_exclude_nickname(self, arg):
        arg = arg.strip()
        self._exclude_msgs_by_predicate(
            lambda msg: msg['name'] != arg
        )
        gs.setup(_data=self._peek_data())

    def do_exclude_all_except_address_and_its_neighbours(self, arg):
        arg = arg.strip()
        self._exclude_msgs_by_predicate(
            lambda msg: msg['name'] != arg
        )
        gs.setup(_data=self._peek_data())


    # ---- VIEW SETTINGS ----#
    # def do_restore_default_view_settings(self, ):
    #     pass

    # def do_simplify_view(self, ):
    #     pass

    # def do_dont_show_msg_features(self, ):
    #     pass

    # def do_show_msg_features(self, ):
    #     pass


    #---- HISTORY MANIPULATION ----#

    def do_undo(self, _):
        if self._index > 0:
            self._index -= 1
            gs.setup(_data=self._peek_data())

    def do_redo(self, _):
        if self._index + 1 < len(self._data):
            self._index -= 1
            gs.setup(_data=self._peek_data())

    def do_reset_default(self, _):
        self._push_data(self._original_data)
        gs.setup(_data=self._peek_data())


    #---- TECHNICAL ----#

    def do_exit(self, _):
        exit()

    def _peek_data(self):
        return deepcopy(self._data[self._index])

    def _peek_previous(self):
        if self._index > 0:
            return deepcopy(self._data[self._index - 1])
        else:
            return deepcopy(self._original_data)

    def _push_data(self, data):
        self._index += 1
        try:
            self._data[self._index] = deepcopy(data)
        except:
            self._data.append(deepcopy(data))
            self._index = len(self._data) - 1
        gs.setup(_data=self._peek_data())

    def _exclude_msgs_by_predicate(self, pred):
        data = self._peek_data()
        data['allMessages'] = list(filter(
            pred,
            data['allMessages'],
        ))
        self._push_data(data)

    def _exclude_addrss_by_predicate(self, pred):
        data = self._peek_data()
        res = {}

        for addr, nick in data['nicknames'].items():
            if not pred(addr):
                res[addr] = nick
        data['nicknames'] = res
        self._push_data(data)
