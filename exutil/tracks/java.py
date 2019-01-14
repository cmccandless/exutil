from glob import glob
import os
import subprocess

from .track import Track, task


class Java(Track):
    def get_deliverables(self, exercise, opts=None):
        # exercise_name = exercise.replace('-', ' ').title().replace(' ', '')
        solution_file_pattern = os.path.join(
            exercise, 'src', 'main', 'java', '*.java'
        )
        return glob(solution_file_pattern)

    @task('testing')
    def test(self, exercise, verbose=False):
        args = ['gradle', 'test']
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Java
