# -*- coding: UTF-8 -*-
import logging

import re

from moneypenny.handler import HandlerType


log = logging.getLogger(__name__)


class Conversation(metaclass=HandlerType):
    ''' Syntax: SET [VAR] = [VAL] | GET [VAR]
        Writes and reads data to session'''
    regex = re.compile('(SET +(?P<set_var>\w+) *[= ] *(?P<val>.*))|(GET +(?P<get_var>\w+))', re.I)

    def __init__(self, event, conversation):
        match = self.regex.match(event['body'])
        if match.group('set_var'):
            conversation.persistent = True
            conversation[match.group('set_var')] = match.group('val')
            event.reply('%s="%s"' % (match.group('set_var'), match.group('val'))).send()
        elif match.group('get_var'):
            try:
                event.reply('%s="%s"' % (match.group('get_var'), conversation[match.group('get_var')])).send()
            except KeyError:
                event.reply('{0}=None'.format(match.group('get_var'))).send()
        else:
            log.error('RegEx not working with "{0}"'.format(event['body']))
