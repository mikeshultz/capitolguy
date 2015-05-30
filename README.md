# capitolguy
Proof of concept of an IRC bot that utilizes the Vote Smart API.

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

