""" 
Copyright (c) Mike Shultz 2015


VoteSmart IRC bot base commands module
"""

from commands.StandardCommand import StandardCommand

class repeat(StandardCommand): 
    """ Repeat what is said """

    commandName = 'repeat'

    def handleCommand(self, args = None): 
        """ Repeat what was said to you """
        if self.conf['debug']:
            print 'args %s - %s' % (self.args, args)
        say = self.args or args
        return say.strip()

class sayhi(StandardCommand): 
    """ Repeat what is said """

    def handleCommand(self, msg = None): 
        """ Repeat what was said to you """
        return "Hello, I am Capitol Guy!"
