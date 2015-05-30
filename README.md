# capitolguy
Proof of concept of an IRC bot that utilizes the [Vote Smart API](https://votesmart.org/share/api).

## Getting started

You can always get help by running `python capitolguy.py --help`

    usage: capitolguy.py [-h] [--nick N] [--server SERVER] [--port PORT] C [C ...]

    Handle requests for querying Vote Smart data.

    positional arguments:
      C                IRC channel(s) to join.

    optional arguments:
      -h, --help       show this help message and exit
      --nick N         Nickname the bot should use, if available.
      --server SERVER  IRC server to connect to.
      --port PORT      IRC server's port to connect to.

### Configure

Copy config.ini.tpl to config.ini.

    cp config.ini.tpl config.ini

Edit the configuration as  you see fit.

### Run

Run the IRC daemon.  

    python capitolguy.py --nick CapitolDude --server irc.freenode.net '#mycoolchannel' '#anotherchannel' &

## Commands

You can run these commands in the IRC channel and the bot will respond(unless they were removed from `config.ini`).

### !sayhi

Command that makes the bot announce itself.

    <mikeshultz> !sayhi
    <VoteSmartBot> Hello, I am Capitol Guy!

### !repeat

Stupid command to repeat whatever you tell it.

    <mikeshultz> !repeat I'm a little teapot!
    <VoteSmartBot> I'm a little teapot!

### !statefact

Command to query the Vote Smart API for a random state fact.  It can accept codes(MT) or name(montana), but they *do* need to be spelled properly.

    <mikeshultz> !statefact Maine
    <VoteSmartBot> Maine's highest point is Mt. Katahdin, 5,268 ft.
