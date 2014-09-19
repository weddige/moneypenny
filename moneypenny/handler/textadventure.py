# -*- coding: UTF-8 -*-
import logging
import zlib
import pickle

import re
from copy import copy

from adventure.game import Game
from adventure import load_advent_dat
from moneypenny.handler import HandlerType
from moneypenny.conf import settings


log = logging.getLogger(__name__)


def _make_suspend(game, path):
    _path = copy(path)
    self = game  # ignore propper binding

    def suspend(verb, obj=None):
        savefile = open(_path, 'wb')
        r = self.random_generator  # must replace live object with static state
        self.random_state = r.getstate()
        f = self.i_suspend
        try:
            del self.random_generator
            del self.i_suspend
            del self.t_suspend
            savefile.write(zlib.compress(pickle.dumps(self), 9))
        finally:
            self.random_generator = r
            self.i_suspend = f
            self.t_suspend = f
            savefile.close()
        self.write('Game saved')

    return suspend


class Adventure(metaclass=HandlerType):
    regex = re.compile('adventure (?P<cmd>start|continue)', re.I)

    def __init__(self, event, conversation):
        match = self.regex.match(event['body'])
        if not match:
            if Adventure in conversation.data:
                game = conversation.data[Adventure]
                words = re.findall('\w+', event['body'])
                event.reply(game.do_command(words).strip()).send()
                if not game.is_finished:
                    conversation.handler = Adventure
            else:
                log.warn('An adventure session was lost.')
                event.reply('You have to start an adventure first.').send()
        elif match.group('cmd') == 'start':
            game = Game()
            load_advent_dat(game)
            savefile = settings['textadventure']['file'].format(conversation.jid)
            game.i_suspend = _make_suspend(game, savefile)
            game.t_suspend = game.i_suspend
            game.start()
            conversation.handler = Adventure
            event.reply(game.output.strip()).send()
            conversation.data[Adventure] = game
        else:
            savefile = settings['textadventure']['file'].format(conversation.jid)
            game = Game.resume(savefile)
            game.i_suspend = _make_suspend(game, savefile)
            game.t_suspend = game.i_suspend
            event.reply('GAME RESTORED').send()
            conversation.handler = Adventure
            conversation.data[Adventure] = game
