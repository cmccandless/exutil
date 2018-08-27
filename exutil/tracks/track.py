import os
import shutil
import subprocess as sp
import sys
from contextlib import contextmanager
from functools import wraps
from io import StringIO


def terminal(*args):
    print(' '.join(args))
    sp.check_call(args)


def exercism(*args):
    terminal('exercism', *args)


def git(*args):
    terminal('git', *args)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


@contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def task(action):
    def _dec(function):
        @wraps(function)
        def _wrapper(self, target, *args, opts=None, **kwargs):
            if isinstance(target, Track):
                target = args[0]
            print(f'{action.title()} {target}...', end='')
            try:
                if opts.verbose:
                    print()
                    function(self, target, *args, **kwargs)
                else:
                    with capture():
                        function(self, target, *args, **kwargs)
                print('Done')
            except sp.CalledProcessError as e:
                sys.stdout.flush()
                if e.output is None:
                    print('Failed')
                else:
                    print(e.output.decode().strip())
                sys.exit(e.returncode)
            except SystemExit as e:
                print('Failed')
                sys.exit(e.code)
        return _wrapper
    return _dec


class Track(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.commands = [
            self.migrate,
            self.test,
            self.restore,
            self.checkin,
            self.submit,
        ]

    def __iter__(self):
        return (c.__name__ for c in self.commands)

    def find_best(self, command):
        matches = [
            c for c in self.commands
            if c.__name__.startswith(command)
        ]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) == 0:
            print(f"Unknown command '{command}'")
        else:
            print(f"Ambigious command '{command}'; choose from the following:")
            for match in matches:
                print(f'  {match.__name__}')
        sys.exit(1)

    def get_deliverables(self, exercise, opts=None):
        raise NotImplementedError()

    @task('migrating')
    def migrate(self, exercise, *args, **kwargs):
        if os.path.isfile(os.path.join(exercise, '.solution.json')):
            print(f'{exercise} has already been migrated')
            return
        exercism('download', '-t', 'python', '-e', exercise)
        src_dir = '{}-2'.format(exercise)
        if os.path.isdir(src_dir):
            print(f'Copying {src_dir}/*->{exercise}')
            copytree(src_dir, exercise)
            print(f'Removing {src_dir}/')
            shutil.rmtree(src_dir)
        for filepath in self.get_deliverables(exercise, **kwargs):
            print(f'Restoring {filepath}')
            globals()['git'](
                'checkout',
                '--',
                filepath
            )

    @task('submitting')
    def submit(self, exercise, opts=None):
        return exercism('submit', *self.get_deliverables(exercise))

    @task('testing')
    def test(self, exercise, opts=None):
        raise NotImplementedError()

    @task('restoring')
    def restore(self, exercise, opts=None):
        print(f'Removing {exercise}/')
        shutil.rmtree(exercise)
        git('checkout', '--', exercise)

    @task('checking in')
    def checkin(self, exercise, opts=None):
        git('add', exercise)
