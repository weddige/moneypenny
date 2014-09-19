# -*- coding: UTF-8 -*-
import logging

import re

import aiml
from moneypenny.handler import HandlerType


log = logging.getLogger(__name__)


class Aiml(metaclass=HandlerType):
    regex = re.compile('(.*)', re.I)
    kernel = aiml.Kernel()

    @staticmethod
    def postregister(handlers):
        from moneypenny.conf import settings

        log.debug('Reregister handler')
        me = Aiml()
        handlers.unregister(Aiml)
        handlers.register(me, prio=handlers.LOWPRIO)
        log.info('Load AIML')
        me.kernel.learn(settings['aimlbot']['file'])
        me.kernel.setBotPredicate('name', settings['aimlbot']['name'])

    def __call__(self, event, conversation=None):
        match = self.regex.match(event['body'])
        event.reply(self.kernel.respond(match.group(1), conversation.jid)).send()
