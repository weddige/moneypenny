# -*- coding: UTF-8 -*-
import logging

import re
import random

from moneypenny.handler import HandlerType


log = logging.getLogger(__name__)


class Dice(metaclass=HandlerType):
    regex = re.compile(r'(\d*)(W|D)(\d+)', re.I)

    def __init__(self, event, conversation=None):
        match = self.regex.match(event['body'])
        if match.group(1) == '':
            n = 1
        else:
            n = int(match.group(1))
        result = ''
        r = int(match.group(3))
        if n > 10000:
            event.reply('Does not compute.').send()
        else:
            log.info('Throw %s %s-sided dice.' % (n, r))
            for i in range(n):
                result += '%s ' % random.randint(1, r)
            event.reply(result).send() 
