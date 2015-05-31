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
    """ Announce myself """

    def handleCommand(self, msg = None): 
        """ Repeat what was said to you """
        return "Hello, I am The Capitol Guy! I'm a government and elections transparency bot for #votesmart.  Do let them know if I'm acting strangely."

class commands(StandardCommand):
    """ Give instructions on how to get comamnds, or if a nick is 
        defined, send it to a specific user.
    """
    def handleCommand(self, msg = None): 
        """ Command help """
        # TODO: Can we get this to dynamicaly generate?
        return "%s: Command is not implemented." % self.user