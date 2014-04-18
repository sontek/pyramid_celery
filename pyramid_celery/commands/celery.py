from __future__ import absolute_import, print_function
import sys

from celery.bin.celery import CeleryCommand
from celery.app import default_app
from pyramid.paster import bootstrap


class CommandMixin(object):
    preload_options = ()

    def setup_app_from_commandline(self, argv):
        if len(argv) < 2:
            print >> sys.stderr, 'No configuration file specified.'
            sys.exit(1)
        bootstrap(argv[1])
        self.app = default_app
        return argv[:1] + argv[2:]

class pworker(CommandMixin, CeleryCommand):
    pass


def main():
    # Fix for setuptools generated scripts, so that it will
    # work with multiprocessing fork emulation.
    # (see multiprocessing.forking.get_preparation_data())
    if __name__ != "__main__":
        sys.modules["__main__"] = sys.modules[__name__]

    pworker(app=default_app).execute_from_commandline()
