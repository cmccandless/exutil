import os
import pytest
import subprocess

from .track import Track, task


class Python(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        solution_file_name = '{}.py'.format(exercise.replace('-', '_'))
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('linting')
    def lint(self, exercise, verbose=False, **kwargs):
        # solution_file_name = '{}.sh'.format(exercise.replace('-', '_'))
        args = ['flake8']
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0

    @task('testing')
    def test(self, exercise, opts=None, verbose=False, **kwargs):
        args = ['-x', exercise]
        if verbose:
            args.insert(0, '-v')
        if opts is not None and opts.timeout is not None:
            args.extend(('--timeout', opts.timeout))
        ret = pytest.main(args)
        return ret


Track = Python
