import os
import subprocess

from .track import Track, task


class CSharp(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        exercise_name = exercise.replace('-', ' ').title().replace(' ', '')
        solution_file_name = '{}.cs'.format(exercise_name)
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('testing')
    def test(self, exercise, verbose=False, **kwargs):
        args = ['dotnet', 'test']
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = CSharp
