# -*- coding: UTF-8 -*-
import logging

_logger = logging.getLogger(__name__)
_handlers = set()


class HandlerType(type):
    def __init__(cls, name, bases, attrs):
        super(HandlerType, cls).__init__(name, bases, attrs)
        _logger.info('Register %s' % cls)
        _handlers.add(cls)
