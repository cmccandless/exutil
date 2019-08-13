# from glob import glob
import os
import subprocess

from .track import Track, task


class Javascript(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        solution_file_name = '{}.js'.format(exercise)
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('linting')
    def lint(self, exercise, verbose=False, **kwargs):
        args = [
            'eslint',
            '--config', os.path.join(os.getcwd(), '.eslintrc.json'),
            '*.js'
        ]
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0

    @task('testing')
    def test(self, exercise, verbose=False, **kwargs):
        args = ['npm', 'test']
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Javascript
