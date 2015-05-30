""" 
Copyright (c) Mike Shultz 2015


VoteSmart IRC bot API query commands module
"""

import random
from string import Template

from commands.StandardCommand import StandardCommand

from votesmart import votesmart

states = {
    'NA': 'National',
    'AS': 'American Samoa',
    'FL': 'Florida',
    'MI': 'Michigan',
    'MO': 'Missouri',
    'MT': 'Montana',
    'ID': 'Idaho',
    'DC': 'District of Columbia',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IN': 'Indiana',
    'MN': 'Minnesota',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'IA': 'Iowa',
    'IL': 'Illinois',
    'NC': 'North Carolina',
    'NY': 'New York',
    'PA': 'Pennsylvania',
    'OH': 'Ohio',
    'AK': 'Alaska',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'KS': 'Kansas',
    'AZ': 'Arizona',
    'OR': 'Oregon',
    'AL': 'Alabama',
    'ND': 'North Dakota',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TX': 'Texas',
    'TN': 'Tennessee',
    'UT': 'Utah',
    'WV': 'West Virginia',
    'WY': 'Wyoming',
    'WI': 'Wisconsin',
    'OK': 'Oklahoma',
    'NE': 'Nebraska',
    'WA': 'Washington',
    'NH': 'New Hampshire',
    'ME': 'Maine',
    'MD': 'Maryland',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'MA': 'Massachusetts',
    'VT': 'Vermont',
    'GU': 'Guam',
    'PR': 'Puerto Rico',
    'VI': 'Virgin',
    'KY': 'Kentucky',
    'VA': 'Virginia',
    'NJ': 'New Jersey',
    'MS': 'Mississippi',
    'LA': 'Louisiana',
}
states_rev_up = {v.upper(): k for k, v in states.items()}
state_codes = [(k) for k,v in states.items()]

translate = {
    'senators': Template("$state has $fact senators."),
    'usCircuit': Template("$state part of the $fact U.S. Circuit Court of Appeals."),
    'ltGov': Template("$state $fact have a leutenant governor."),
    'lowerLegis': Template("$state's lower legislative body is called the $fact."),
    'flower': Template("$state's state flower is the $fact."),
    'area': Template("$state's total area is $fact"),
    'upperLegis': Template("$state's upper legislative body is called the $fact"),
    'termLength': Template("$state's term length is $fact."),
    'bicameral': Template("Bicameral: $fact."),
    'capital': Template("$state's state capital is named $fact."),
    'nickName': Template("$state is also known as $fact."),
    'bird': Template("$state's state bird is the $fact."),
    'highPoint': Template("$state's highest point is $fact."),
    'termLimit': Template("$state's term limit is $fact."),
    'lowPoint': Template("$state's lowest point is $fact."),
    'primaryDate': Template("$state's primary is held on  $fact."),
    'statehood': Template("$state officially became a state on $fact."),
    'reps': Template("$state has $fact representatives."),
    'motto': Template("$state's motto is \"$fact.\""),
    'population': Template("$state has a population of $fact."),
    'tree': Template("$state's official tree is the $fact."),
    'generalDate': Template("$state has its general election on $fact."),
    'largestCity': Template("$state's largest city is $fact."),
}
# facts/state attrs you want to ignore
ignore = ['name', 'stateId', 'billUrl', 'voterReg', 'voteUrl', 'rollUpper', 'rollLower', 'stateType', ]

class statefact(StandardCommand): 
    """ Show a super fun fact about a state! """

    def resolveStateCode(self, name):
        for k,v in states.items(): 
            if v.upper() == name.upper(): 
                return k
        return False

    def cleanFacts(self, facts):

        if type({}) == type(facts):
            # remove fact fields without any data.
            for k,v in facts.items():
                if not v:
                    del(facts[k])

        return facts

    def getRandomFact(self, state):
        votesmart.apikey = self.conf['votesmart-api-key']
        state_data = votesmart.state.getState(state.upper())
        state_dict = self.cleanFacts(state_data.__dict__)
        return random.choice(state_dict.items())

    def handleCommand(self, args = None): 
        """ Share a random fact about a state that was had from the Vote
            Smart API """

        if self.conf['debug']:
            print 'args %s - %s' % (self.args, args)

        state = (self.args or args).strip()

        if state.upper() in states:
            fact = self.getRandomFact(state)
            return translate[fact[0]].substitute(state = str(state), fact = str(fact[1]))
        elif state.upper() in states_rev_up:
            if self.conf['debug']:
                print "Matched a state name! (%s)" % self.resolveStateCode(state)
            fact = self.getRandomFact(self.resolveStateCode(state))
            return translate[fact[0]].substitute(state = str(state), fact = str(fact[1]))
        else:
            return "I don't know anything about this state... hmm..."