from pyramid_celery.commands import CommandMixin
from celery.bin.celerybeat import BeatCommand as BaseBeatCommand
from celery.bin.base import Command


class BeatCommand(CommandMixin, BaseBeatCommand):
    preload_options = tuple(BaseBeatCommand.preload_options
            [len(Command.preload_options):])



def main():
    return BeatCommand().execute_from_commandline()
