import os
import pytest

from .track import Track, task


class Python(Track):
    def get_deliverables(self, exercise, opts=None):
        solution_file_name = '{}.py'.format(exercise.replace('-', '_'))
        solution_file_path = os.path.join(exercise, solution_file_name)
        return [solution_file_path]

    @task('testing')
    def test(self, exercise, opts=None):
        args = ['-x', exercise]
        if opts is not None and opts.timeout is not None:
            args.extend(('--timeout', opts.timeout))
        print(' '.join(['pytest', *args]))
        ret = pytest.main(args)
        return ret


Track = Python
