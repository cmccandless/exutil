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
import logging

from . import tracks  # NOQA; needed for dynamic import below
from .tracks.argparse_ext import (
    ExtendAction,
)

VERSION = '0.5.0'
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
        try:
            with open(config_file) as f:
                return json.load(f)
        except json.decoder.JSONDecodeError as e:
            logging.error('.exutil format error: ' + str(e))
            sys.exit(1)
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
    parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
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
    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif opts.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
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
    init_script = getattr(opts, "init_script", None)
    ignore = set(getattr(opts, 'non_exercises', []))
    if do_download:
        commands.remove(track.download)
        if 'next' in opts.exercise:
            ret = track.download(
                'next',
                verbose=opts.verbose,
                init_script=init_script
            )
            if ret not in {None, 0}:
                sys.exit(ret)
            opts.exercise.remove('next')
    for pattern in opts.exercise:
        if do_download:
            ret = track.download(
                pattern,
                verbose=opts.verbose,
                init_script=init_script
            )
            if ret not in {None, 0}:
                logging.error('Download failed!')
                sys.exit(ret)
        exercises = [
            path for path in glob(pattern)
            if path.rstrip('/') not in ignore
        ]
        if not exercises:
            print('exercise {} not found'.format(pattern))
            sys.exit(1)
        for ex in exercises:
            ex = ex.strip('/')
            if (
                not os.path.isdir(ex) or
                (
                    not (
                        os.path.isfile(os.path.join(ex, '.solution.json')) or
                        os.path.isfile(os.path.join(
                            ex, '.exercism', 'metadata.json'
                        ))
                    ) and
                    track.migrate not in commands
                )
            ):
                logging.error('{} is not an exercise'.format(ex))
                continue
            if ex in opts.ignore:
                continue
            for command in commands:
                ret = command(ex, opts=opts)
                if ret not in {None, 0}:
                    sys.exit(ret)


if __name__ == '__main__':
    main()
