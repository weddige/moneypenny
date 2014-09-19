# -*- coding: UTF-8 -*-
import configparser
import logging

import os
import imp

from moneypenny.handler import _handlers


log = logging.getLogger(__name__)
client = None
project_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class _Settings(configparser.ConfigParser):
    def __init__(self):
        super(_Settings, self).__init__(interpolation=configparser.ExtendedInterpolation())
        conffiles = (
            os.path.expanduser('~/.moneypenny/config'),
            '/etc/moneypenny/config',
            os.path.join(project_dir, 'config'),
        )
        self.read(conffiles)
        self.add_section('runtime')
        self.set('runtime', 'project_dir', project_dir)
        logging.basicConfig(level=getattr(logging, self['logging']['level']))
        logging.getLogger('sleekxmpp').setLevel(logging.WARNING)


class HandlerNotFoundError(Exception):
    pass


class _Handlers:
    LOWPRIO = 1
    NOPRIO = 0
    HEIGHTPRIO = -1

    _registered_handlers = {}

    def __init__(self):
        root = os.path.join(project_dir, 'handler')
        if settings.has_option('moneypenny', 'handler'):
            modules = settings.get('moneypenny', 'handler').strip().split(',')
        else:
            modules = [
                os.path.splitext(file_name)[0]
                for file_name in os.listdir(root)
                if os.path.splitext(file_name)[1] == '.py'
            ]
        for module_name in modules:
            try:
                module = imp.load_source(module_name, os.path.join(root, module_name + '.py'))
            except Exception as e:
                logging.info(e)
        self._registered_handlers = {h: 0 for h in _handlers}
        for handler in _handlers:
            if hasattr(handler, 'postregister'):
                handler.postregister(self)

    def get_handler(self, msg):
        for handler in sorted(self._registered_handlers, key=lambda h: self._registered_handlers[h]):
            if handler.regex.match(msg):
                return handler
        raise HandlerNotFoundError()

    def register(self, handler, prio=0):
        self._registered_handlers[handler] = prio

    def unregister(self, handler):
        del self._registered_handlers[handler]

settings = _Settings()
handlers = _Handlers()
