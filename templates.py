""" 
Copyright (c) Mike Shultz 2015


Message templates.
"""

import random
from string import Template

direct_message_responses = [
    Template("Indeed, $user, indeed."),
    Template("Indubitably, my dear $user."),
    Template("The time is now $time."),
    Template("I hate $day..."),
    Template("$user: You can get commands by sending me a private message."),
    Template("$user: You can take a peak under my clothing at https://github.com/mikeshultz/capitolguy"),
]
def dm_response(*args, **kwargs):
    t = random.choice(direct_message_responses)
    return t.safe_substitute(**kwargs)