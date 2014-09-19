# -*- coding: UTF-8 -*-
import logging

import re

from moneypenny.handler import HandlerType
from moneypenny.conf.scheduler import *
from pywcl.scheduler.utils import minutely
from pywcl.scheduler import Task


log = logging.getLogger(__name__)


class Pong(metaclass=HandlerType):
    ''' Syntax: pingme [not] '''
    regex = re.compile(r'pingme( not)?', re.I)
    tasks = dict()

    def __call__(self, event, conversation):
        self.conversation = conversation
        if 'not' in event['body']:
            scheduler.cancel(self.tasks[event['from'].bare])
            event.reply('I won\'t ping you.').send()
        else:
            log.info('I will ping {0}'.format(event['from'].full))
            self.tasks[event['from'].bare] = scheduler.schedule(self.ping, event['from'].full)
            event.reply('I will ping you.').send()

    @staticmethod
    def postregister(handlers):
        handlers.unregister(Pong)
        handlers.register(Pong())

    @Task(due=minutely())
    def ping(self, me):
        log.info('Ping {0}'.format(me))
        self.conversation.client.send_message(mto=me, mbody='Ping?')

