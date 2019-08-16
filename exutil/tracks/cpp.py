import os
import subprocess

from .track import Track, task


class Cpp(Track):
    def get_deliverables(self, exercise, opts=None, **kwargs):
        exercise_name = exercise.replace('-', '_').lower()
        solution_file_name = '{}.cpp'.format(exercise_name)
        solution_file_path = os.path.join(exercise, solution_file_name)
        header_file_name = '{}.h'.format(exercise_name)
        header_file_path = os.path.join(exercise, header_file_name)
        return [solution_file_path, header_file_path]

    def cmake(self, exercise, cwd='.', verbose=False):
        args = ['cmake', '-G', 'Unix Makefiles', '..']
        kwargs = dict(cwd=cwd)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)

    @task('testing')
    def test(self, exercise, verbose=False, **kwargs):
        cwd = os.path.join(exercise, '.build')
        os.makedirs(cwd, exist_ok=True)
        self.cmake(exercise, cwd=cwd, verbose=verbose)
        args = ['make']
        kwargs = dict(cwd=cwd)
        if not verbose:
            kwargs['stderr'] = subprocess.DEVNULL
            kwargs['stdout'] = subprocess.DEVNULL
        subprocess.check_call(args, **kwargs)
        return 0


Track = Cpp
