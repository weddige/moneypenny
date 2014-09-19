# -*- coding: UTF-8 -*-
import logging

import seth

from moneypenny.core.moneypenny import Moneypenny


class MoneypennyDaemon(seth.Daemon):
    def shutdown(self):
        logging.info('Shutdown.')
        self.client.disconnect(wait=True)

    def run(self):
        self.client = Moneypenny()
        if self.client.connect():
            logging.info('Start listening.')
            self.client.process(block=True)
            logging.info('STOP')
        else:
            logging.error('Could not connect.')
