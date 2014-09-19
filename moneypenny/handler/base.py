# -*- coding: UTF-8 -*-
import datetime

import re

from moneypenny.handler import HandlerType


class Uptime(metaclass=HandlerType):
    ''' uptime
    Return uptime of Jabberbot.'''
    regex = re.compile(r'uptime', re.I)
    __start = datetime.datetime.now()

    def __init__(self, event, conversation=None):
        d = datetime.datetime.now() - self.__start
        if d.days > 1:
            result = '%s Tage ' % d.days
        elif d.days == 1:
            result = '1 Tag '
        else:
            result = ''
        hours, remainder = divmod(d.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        result += '%s:%s:%s' % (hours, minutes, seconds)
        event.reply(result).send()


class Echo(metaclass=HandlerType):
    ''' echo [MSG]
    Return [MSG]'''

    regex = re.compile(r'echo (?P<msg>.*)', re.I)

    def __init__(self, event, conversation=None):
        match = self.regex.match(event['body'])
        event.reply(match.group('msg')).send()


class Help(metaclass=HandlerType):
    ''' help
    Return help text for all loaded modules.'''
    regex = re.compile(r'help', re.I)

    def __init__(self, event, conversation=None):
        from moneypenny.conf import handlers

        result = 'Help:'
        for handler in handlers._registered_handlers:
            name = handler.__name__ if hasattr(handler, '__name__') else handler.__class__.__name__
            help = handler.__doc__ or 'No help avaiable.'
            result += '\n{0}:\t{1}'.format(name, help)
        event.reply(result).send()

