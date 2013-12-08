from __future__ import absolute_import

from pyramid_celery.commands import CommandMixin
try:
    from celery.bin.celerybeat import BeatCommand as BaseBeatCommand
except ImportError:
    from celery.bin.celery import beat as BaseCeleryCtl

from celery.bin.base import Command


class BeatCommand(CommandMixin, BaseBeatCommand):
    preload_options = tuple(BaseBeatCommand.preload_options
            [len(Command.preload_options):])



def main():
    return BeatCommand().execute_from_commandline()
