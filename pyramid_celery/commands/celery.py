from __future__ import absolute_import, print_function
import sys

from celery.bin.celery import CeleryCommand
from celery.app import default_app

from . import CommandMixin

class pworker(CommandMixin, CeleryCommand):
    pass


def main():
    # Fix for setuptools generated scripts, so that it will
    # work with multiprocessing fork emulation.
    # (see multiprocessing.forking.get_preparation_data())
    if __name__ != "__main__":
        sys.modules["__main__"] = sys.modules[__name__]

    pworker(app=default_app).execute_from_commandline()
