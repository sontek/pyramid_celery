from pyramid_celery.commands import CommandMixin
from celery.bin.celeryctl import celeryctl as BaseCeleryCtl
from celery.bin.celeryctl import help as BaseHelp


class Help(BaseHelp):
    option_list = BaseHelp.option_list[len(BaseCeleryCtl.preload_options):]


class CeleryCtl(CommandMixin, BaseCeleryCtl):
    commands = BaseCeleryCtl.commands.copy()
    commands['help'] = Help
    option_list = BaseCeleryCtl.option_list[len(BaseCeleryCtl.preload_options):]



def main():
    return CeleryCtl().execute_from_commandline()
