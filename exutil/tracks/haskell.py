from glob import glob
import os
import subprocess

from .track import Track, task


class Haskell(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        solution_file_pattern = os.path.join(
            exercise, 'src', '*.hs'
        )
        return glob(solution_file_pattern)

    @task('linting')
    def lint(self, exercise, verbose=False, **kwargs):
        args = ['hlint', 'src']
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0

    @task('testing')
    def test(self, exercise, verbose=False, **kwargs):
        args = ['stack', 'test']
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Haskell
