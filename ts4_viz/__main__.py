import argparse
import json
import sys
import os

from graphviz_stuff import setup

from cmd_stuff import MsgVizualizerShell


def create_arg_parser():
    # Creates and returns the ArgumentParser object

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'ts4JSONDump',
        help='Path to the .json dum file.',
        default='msg_data.json',
    )
    parser.add_argument(
        '--outputFile',
        help='Path to the .gv output file.',
        default='result.gv',
    )
    return parser


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if not os.path.exists(parsed_args.ts4JSONDump):
       print("input file does not exists")

    with open(parsed_args.ts4JSONDump, 'r') as f:
        data = json.load(f)

    setup(
        filename=parsed_args.outputFile,
        _data = data
    )

    MsgVizualizerShell(data).cmdloop()
