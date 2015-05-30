""" 
Copyright (c) Mike Shultz 2015


IRC bot that utilizes the Vote Smart API
"""
__version__ = "0.1.1"

import sys, importlib, re, argparse, ConfigParser

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# handle config
config = ConfigParser.ConfigParser()
config.read('config.ini')
CONFIG = {}

# general app config
if config.get('Main', 'debug') == 'true': 
    CONFIG['debug'] = True
else:
    CONFIG['debug'] = False

# config for capitolguy
CONFIG ['votesmart-api-key'] = config.get('VoteSmart', 'key')

parser = argparse.ArgumentParser(description = 'Handle requests for querying Vote Smart data.')
parser.add_argument('channel', metavar = 'C', nargs = '+', help = 'IRC channel(s) to join.')
parser.add_argument('--nick', metavar = 'N', dest = 'nick', type = str, default='VoteSmartBot', help = 'Nickname the bot should use, if available.')
parser.add_argument('--server', dest = 'server', default = 'irc.freenode.net', help = 'IRC server to connect to.')
parser.add_argument('--port', dest = 'port', default = 6667, help = 'IRC server\'s port to connect to.')
parser.add_argument('--name', dest = 'name', default = 'The Capitol Guy', help = 'Bot\'s "Real Name"')

args = parser.parse_args()
if CONFIG['debug']:
    print args

commands = {}

# import command modules
for m in config.items('Commands'):
    module = m[0]
    commandsToImport = config.get('Commands', module)
    for c in commandsToImport.split(','):
        classToImport = c.strip()
        __import__('commands.' + module)
        commands[classToImport] = getattr(sys.modules['commands.' + module], classToImport)

class CapitolGuy(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = args.nick
    realname = args.name
    versionName = 'capitolguy'
    versionNum = __version__
    sourceURL = 'https://github.com/mikeshultz/capitolguy'
    
    def connectionMade(self):
        irc.IRCClient.realname = 'The Capitol Guy'
        irc.IRCClient.connectionMade(self)
        
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        
    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        for c in self.factory.channel:
            self.join(c)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        # ello

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        if CONFIG['debug']:
            print "<%s> %s" % (user, msg)
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I am the Capitol Guy!" % user
            self.msg(channel, msg)

        if msg.startswith("!"): 
            commandString = re.compile(r"""^\!([\d\w]+)[\b]*([\d\w _\-'\\/\.\!\?\+=\^\%]*)""")
            res = re.match(commandString, msg)
            if res:
                if CONFIG['debug']:
                    print 'Running command %s' % res.group(1)

                """ If it's a bunk command, forget about it. """
                try:
                    cmd = commands[res.group(1)](CONFIG, msg)
                    self.msg(channel, cmd.handleCommand())
                except KeyError: 
                    if CONFIG['debug']:
                        print "%s is not a known command." % res.group(1)
                    else:
                        pass

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        if CONFIG['debug']:
            print 'Action performed by %s' % user
        user = user.split('!', 1)[0]
        if CONFIG['debug']:
            print "* %s %s" % (user, msg)

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        if CONFIG['debug']:
            print "%s is now known as %s" % (old_nick, new_nick)

class CapitolGuyFactory(protocol.ClientFactory):
    """A factory for CapitolGuy.
    """

    def __init__(self, args):
        self.channel = args.channel

    def buildProtocol(self, addr):
        p = CapitolGuy()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "ERROR: connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # create factory protocol and application
    guy = CapitolGuyFactory(args)
    reactor.connectTCP(args.server, args.port, guy)
    reactor.run()