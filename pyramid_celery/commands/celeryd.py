from __future__ import absolute_import

import sys
from pyramid_celery.commands import CommandMixin
try:
    from celery.bin.celeryd import WorkerCommand as BaseWorkerCommand
except ImportError:
    # Celery >=3.1
    from celery.bin.celery import worker as BaseWorkerCommand

try:
    from celery.concurrency.processes.forking import freeze_support
except ImportError:  # pragma: no cover
    freeze_support = lambda: True  # noqa


class WorkerCommand(CommandMixin, BaseWorkerCommand):
    preload_options = ()


def main():
    # Fix for setuptools generated scripts, so that it will
    # work with multiprocessing fork emulation.
    # (see multiprocessing.forking.get_preparation_data())
    if __name__ != "__main__":
        sys.modules["__main__"] = sys.modules[__name__]
    freeze_support()
    worker = WorkerCommand()
    worker.execute_from_commandline()
