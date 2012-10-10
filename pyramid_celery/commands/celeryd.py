import sys
from pyramid_celery.commands import CommandMixin
from pyramid.paster import bootstrap
from celery.bin import celeryd
from billiard import freeze_support
from pyramid_celery.app import app
from celery.bin.celeryd import WorkerCommand as BaseWorkerCommand

worker = celeryd.WorkerCommand(app=app)

class WorkerCommand(CommandMixin, BaseWorkerCommand):
    options = list(worker.get_options() + worker.preload_options)

    def handle(self, *args, **options):
        print "IN HANDLE"
        bootstrap(self.config_file)
        worker.run(*args, **options)

def main():
    # Fix for setuptools generated scripts, so that it will
    # work with multiprocessing fork emulation.
    # (see multiprocessing.forking.get_preparation_data())
    if __name__ != "__main__":
        sys.modules["__main__"] = sys.modules[__name__]
    freeze_support()

    worker = WorkerCommand()
    worker.execute_from_commandline()
