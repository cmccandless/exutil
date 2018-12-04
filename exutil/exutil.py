from __future__ import print_function
import argparse
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import json
import sys
from glob import glob
from importlib import import_module
import os

from . import tracks  # NOQA; needed for dynamic import below
from .tracks.argparse_ext import (
    ExtendAction,
)

VERSION = '0.4.1'
opts = None
track = None


DEFAULT_CONFIG = {
    'track': 'python'
}


def print(*args, **kwargs):
    kwargs = dict(kwargs)
    kwargs['flush'] = kwargs.get('flush', True)
    return builtins.print(*args, **kwargs)


def get_config_file():
    filename = '.exutil'
    if os.path.isfile(filename):
        return filename
    filepath = os.path.abspath(os.path.join('~', filename))
    if os.path.isfile(filepath):
        return filepath
    return None


def get_config(config_file=None):
    if config_file is None:
        config_file = get_config_file()
    if config_file is not None:
        with open(config_file) as f:
            return json.load(f)
    return DEFAULT_CONFIG


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
    parser.add_argument('-c', '--config', help='config file')
    parser.add_argument('-i', '--ignore', action=ExtendAction, default=[])
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        help='test timeout (tracks: Python)'
    )
    parser.add_argument(
        '--track',
        type=lambda s: s.lower(),
        choices=('bash', 'python'),
        help=' ',
    )
    parser.add_argument(
        'command',
        action=ExtendAction,
        help=','.join(sorted(tracks.Track()))
    )
    parser.add_argument('exercise', action=ExtendAction, nargs='+')
    opts = parser.parse_args(args)
    config = get_config(opts.config)
    for attr, config_value in config.items():
        if getattr(opts, attr, None) is None:
            setattr(opts, attr, config_value)
    track_module = import_module(
        '.' + opts.track,
        package='exutil.tracks'
    )
    track = track_module.Track()
    commands = [
        c for c in map(track.find_best, opts.command)
        if c is not None
    ]
    do_download = track.download in commands
    if do_download:
        commands.remove(track.download)
        if 'next' in opts.exercise:
            track.download('next')
            opts.exercise.remove('next')
    for pattern in opts.exercise:
        if do_download:
            track.download(pattern)
        for ex in glob(pattern):
            ex = ex.strip('/')
            if ex in opts.ignore:
                continue
            for command in commands:
                ret = command(ex, opts=opts)
                if ret not in {None, 0}:
                    sys.exit(ret)


if __name__ == '__main__':
    main()
