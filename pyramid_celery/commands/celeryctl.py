from __future__ import absolute_import

from pyramid_celery.commands import CommandMixin
from celery.bin.celery import CeleryCommand as BaseCeleryCtl


class CeleryCtl(CommandMixin, BaseCeleryCtl):
    commands = BaseCeleryCtl.commands.copy()
    option_list = BaseCeleryCtl.option_list[len(BaseCeleryCtl.preload_options):]


def main():
    return CeleryCtl().execute_from_commandline()
