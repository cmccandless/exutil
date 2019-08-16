import os
import subprocess

from .track import Track, task


class Bash(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        solution_file_name = '{}.ps1'.format(exercise.title().replace('-', ''))
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('testing')
    def test(self, exercise, verbose=False, **kwargs):
        args = ['bin/run-test.sh', exercise]
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Bash
