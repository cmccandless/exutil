import os
import pytest
import subprocess

from .track import Track, task


class Julia(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        solution_file_name = '{}.jl'.format(exercise)
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    # @task('linting')
    # def lint(self, exercise, verbose=False, **kwargs):
    #     # solution_file_name = '{}.sh'.format(exercise.replace('-', '_'))
    #     args = ['flake8']
    #     kwargs = dict(cwd=exercise)
    #     if not verbose:
    #         kwargs['stderr'] = subprocess.DEVNULL
    #         kwargs['stdout'] = subprocess.DEVNULL
    #     subprocess.check_call(args, **kwargs)
    #     return 0

    @task('testing')
    def test(self, exercise, opts=None, verbose=False, **kwargs):
        test_file_name = 'runtests.jl'
        args = ['julia', test_file_name]
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Julia
