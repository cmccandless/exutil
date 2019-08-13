import os
import subprocess

from .track import task
from .csharp import CSharp


class FSharp(CSharp):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        exercise_name = exercise.replace('-', ' ').title().replace(' ', '')
        solution_file_name = '{}.fs'.format(exercise_name)
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('linting')
    def lint(self, exercise, verbose=False, **kwargs):
        exercise_name = exercise.replace('-', ' ').title().replace(' ', '')
        solution_file_name = '{}.fs'.format(exercise_name)
        args = ['dotnet-fsharplint', '-sf', solution_file_name]
        kwargs = dict(cwd=exercise)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = FSharp
