# -*- coding: UTF-8 -*-
import logging
import configparser

import sleekxmpp
from moneypenny import conf
from moneypenny.conf import settings, handlers, HandlerNotFoundError


log = logging.getLogger(__name__)


class Conversation:
    persistent = False
    handler = None

    def __init__(self, jid):
        self.jid = jid
        filename = settings['conversation']['file'].format(jid)
        self._data = configparser.ConfigParser()
        self._data.read(filename)
        if not self._data.has_section(jid):
            self._data.add_section(jid)

    def __getitem__(self, key):
        return self._data[self.jid][key]

    def __setitem__(self, key, value):
        self._data[self.jid][key] = value
        f = open(settings['conversation']['file'].format(self.jid), 'w+')
        self._data.write(f)
        f.close()

    def handle(self, client, event):
        if self.persistent:
            if hasattr(self, 'history'):
                self.history.append(event)
            else:
                self.history = [event, ]
        if self.handler:
            handler = self.handler
            self.handler = None
            handler(event, self)
        else:
            try:
                handlers.get_handler(event['body'])(event, self)
            except HandlerNotFoundError:
                event.reply('Does not compute').send()
                log.info('No handler found for "%s".' % event['body'])

    @property
    def client(self):
        return conf.client


class Moneypenny(sleekxmpp.ClientXMPP):
    _conversations = dict()

    def __init__(self, *args, **kwargs):
        _jid = settings['moneypenny']['user']
        if 'ressource' in settings['moneypenny']:
            _jid = _jid + '/' + settings['moneypenny']['ressource']

        super(Moneypenny, self).__init__(_jid, settings['moneypenny']['password'])

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        # Singelton like acess:
        conf.client = self

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        log.info('Session start for %s' % self.boundjid)

    def message(self, event):
        if event['type'] in ('chat', 'normal'):
            self.conversation(event['from'].bare).handle(self, event)

    def conversation(self, jid):
        log.info('Request conversation for {0}.'.format(jid))
        if jid not in self._conversations:
            self._conversations[jid] = Conversation(jid)
        return self._conversations[jid]
