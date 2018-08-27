from __future__ import print_function
import argparse
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import sys
from glob import glob
from importlib import import_module

from . import tracks  # NOQA; needed for dynamic import below
from .tracks.argparse_ext import (
    ExtendAction,
)

VERSION = '0.2.4'
opts = None
track = None


def print(*args, **kwargs):
    kwargs = dict(kwargs)
    kwargs['flush'] = kwargs.get('flush', True)
    return builtins.print(*args, **kwargs)


def main(args=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {} using Python {}'.format(
            VERSION,
            '.'.join(map(str, sys.version_info))
        )
    )
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-i', '--ignore', action=ExtendAction, default=[])
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        help='test timeout (tracks: Python)'
    )
    parser.add_argument('--track', default='python')
    parser.add_argument(
        'command',
        action=ExtendAction,
        help=','.join(sorted(tracks.Track()))
    )
    parser.add_argument('exercise', action=ExtendAction, nargs='+')
    opts = parser.parse_args(args)
    track_module = import_module(
        '.' + opts.track,
        package='exutil.tracks'
    )
    track = track_module.Track()
    for pattern in opts.exercise:
        for ex in glob(pattern):
            if ex in opts.ignore:
                continue
            for command in opts.command:
                command = track.find_best(command)
                ret = command(ex, opts=opts)
                if ret not in {None, 0}:
                    sys.exit(ret)


if __name__ == '__main__':
    main()
