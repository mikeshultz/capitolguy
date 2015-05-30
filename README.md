![Logo](https://votesmart.org/static/images/subpages/share/capitol_guy_blue_trans.gif)
# capitolguy
Proof of concept of an IRC bot that utilizes the [Vote Smart API](https://votesmart.org/share/api).

## Getting started

You can always get help by running `python capitolguy.py --help`

    usage: capitolguy.py [-h] [--nick N] [--server SERVER] [--port PORT]
                         [--name NAME]
                         C [C ...]

    Handle requests for querying Vote Smart data.

    positional arguments:
      C                IRC channel(s) to join.

    optional arguments:
      -h, --help       show this help message and exit
      --nick N         Nickname the bot should use, if available.
      --server SERVER  IRC server to connect to.
      --port PORT      IRC server's port to connect to.
      --name NAME      Bot's "Real Name"

### Configure

Copy config.ini.tpl to config.ini.

    cp config.ini.tpl config.ini

Edit the configuration as  you see fit.

### Run

Run the IRC daemon.  

    python capitolguy.py --nick CapitolDude --server irc.freenode.net '#mycoolchannel' '#anotherchannel' &

## Commands

You can run these commands in the IRC channel and the bot will respond(unless they were removed from `config.ini`).

### Base Commands

#### !sayhi

Command that makes the bot announce itself.

    <mikeshultz> !sayhi
    <VoteSmartBot> Hello, I am The Capitol Guy! I'm a government and elections transparency bot for #votesmart.  Do let them know if I'm acting strangely.

#### !repeat

Stupid command to repeat whatever you tell it.

    <mikeshultz> !repeat I'm a little teapot!
    <VoteSmartBot> I'm a little teapot!

### Vote Smart Specific Commands

#### !bill

Command that provides minimal data on a bill including a link to the page on votesmart.org for more information.

    <mikeshultz> !bill HR 3361
    <CapitolGuy> USA FREEDOM Act(HR 3361).  More information: https://votesmart.org/bill/18243
    <CapitolGuy> (HR 3361).  More information: https://votesmart.org/bill/18243

#### !candidatesearch

Command to search for a candidate by last name.

    <mikeshultz> !candidatesearch Rubio
    <CapitolGuy> Marco Rubio: https://votesmart.org/candidate/1601

#### !districtbyzip

Command that will provide the districts for a particular 5-digit or 9-digit USPS Zip code.

    <mikeshultz> !districtbyzip 19403-2801
    <CapitolGuy> I found 3 districts for 19403-2801: U.S. House District 6; State House District 150; State Senate District 44.  More Information: https://votesmart.org/search?q=19403-2801

#### !officialsearch

Command to search for office holders by last name.

    <mikeshultz> !officialsearch Obama
    <CapitolGuy> President Barack Obama II: https://votesmart.org/candidate/9490
    <CapitolGuy> Senator Erin Oban: https://votesmart.org/candidate/152042

#### !statefact

Command to query the Vote Smart API for a random state fact.  It can accept codes(MT) or name(montana), but they *do* need to be spelled properly.

    <mikeshultz> !statefact Maine
    <VoteSmartBot> Maine's highest point is Mt. Katahdin, 5,268 ft.
