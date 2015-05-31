""" 
Copyright (c) Mike Shultz 2015


VoteSmart IRC bot base commands module
"""

import re

""" Exceptions """
class BotException(Exception): pass

class StandardCommand():

    command = None
    args = None
    message = ''

    def __init__(self, conf, user, msg):
        "huh"
        self.conf = conf
        self.user = user
        self.message = msg
        self.parseCommand(msg)

    def parseCommand(self, msg):
        commandString = re.compile(r"""^\!([\d\w]+)[\b]*([\d\w _\-'\\/\.\!\?\+=\^\%]*)""")
        res = re.match(commandString, msg)
        if res:
            print "I'm handling this command!"

            self.command = res.group(1)
            self.args = res.group(2).strip()
        
            print 'Command: %s' % self.command
            print 'Arg(s): %s' % self.args

    def handleCommand(self, args = None): 
        """ Parse args, handle command, and perform the action.
        """