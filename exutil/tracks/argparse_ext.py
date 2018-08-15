import argparse
import re

RGX_LIST = re.compile('[ ,;]')


class ExtendAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ExtendAction, self).__init__(option_strings, dest, **kwargs)

    def __parse__(self, value):
        return value

    def __extend__(self, namespace, value):
        current = getattr(namespace, self.dest)
        if current is None:
            current = []
        parsed = RGX_LIST.split(value)
        current.extend(map(self.__parse__, parsed))
        setattr(namespace, self.dest, current)

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            for value in values:
                self.__extend__(namespace, value)
        else:
            self.__extend__(namespace, values)
