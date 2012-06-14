from pyramid_celery.commands import CommandMixin
from celery.bin.celeryev import EvCommand as BaseEvCommand
from celery.bin.base import Command


class EvCommand(CommandMixin, BaseEvCommand):
    preload_options = tuple(BaseEvCommand.preload_options
            [len(Command.preload_options):])



def main():
    return EvCommand().execute_from_commandline()
