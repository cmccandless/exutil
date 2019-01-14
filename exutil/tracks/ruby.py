import os
import subprocess

from .track import Track, task


class Ruby(Track):
    def get_deliverables(self, exercise, opts=None):
        solution_file_name = '{}.rb'.format(exercise.replace('-', '_'))
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('testing')
    def test(self, exercise, opts=None, verbose=False):
        test_file_name = '{}_test.rb'.format(exercise.replace('-', '_'))
        args = ['ruby', test_file_name]
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Ruby
