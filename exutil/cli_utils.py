import subprocess as sp


def terminal(*args):
    print(' '.join(args))
    sp.check_call(args, stderr=sp.STDOUT)


def exercism(*args):
    return terminal('exercism', *args)


def git(*args):
    return terminal('git', *args)
