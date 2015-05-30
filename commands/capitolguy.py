""" 
Copyright (c) Mike Shultz 2015


VoteSmart IRC bot API query commands module
"""

import random
from string import Template

from commands.StandardCommand import StandardCommand

from votesmart import votesmart, VotesmartApiError

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

offices = {
    530: 'Administrator of the Environmental Protection Agency',
    529: 'Director of the Office of Management & Budget',
    1: 'President',
    55: 'U.S. Attorney General',
    56: 'U.S. Secretary of Agriculture',
    57: 'U.S. Secretary of Commerce',
    58: 'U.S. Secretary of Defense',
    59: 'U.S. Secretary of Education',
    60: 'U.S. Secretary of Energy',
    61: 'U.S. Secretary of Health and Human Services',
    62: 'U.S. Secretary of Homeland Security',
    63: 'U.S. Secretary of Housing and Urban Development',
    64: 'U.S. Secretary of Labor',
    65: 'U.S. Secretary of State',
    69: 'U.S. Secretary of the Interior',
    66: 'U.S. Secretary of Transportation',
    67: 'U.S. Secretary of Treasury',
    68: 'U.S. Secretary of Veterans Affairs',
    2: 'Vice President',
    5: 'U.S. House',
    6: 'U.S. Senate',
    491: 'Chief Judge of the U.S. Court of Appeals',
    494: 'Chief Judge of the U.S. District Court',
    490: 'Judge of the U.S. Court of Appeals',
    493: 'Judge of the U.S. District Court',
    492: 'Senior Judge of the U.S. Court of Appeals',
    495: 'Senior Judge of the U.S. District Court',
    497: 'Solicitor General',
    77: 'U.S. Associate Justice of the Supreme Court',
    76: 'U.S. Chief Justice of the Supreme Court',
    4: "Lieutenant Governor",
    31: "Director of the Department of Revenue",
    33: "Education Secretary",
    34: "Insurance Commissioner",
    35: "Labor Commissioner",
    36: "Land Commissioner",
    44: "Secretary of State",
    11: "Agriculture Commissioner",
    14: "Chief Financial Officer",
    16: "Commissioner of Agriculture",
    17: "Commissioner of Agriculture and Forestry",
    18: "Commissioner of Agriculture and Industry",
    23: "Commissioner of Schools and Public Lands",
    24: "Commissioner of State Lands",
    37: "Public Service Commissioner",
    38: "Public Utilities Commissioner",
    39: "Railroad Commissioner",
    40: "Revenue Director",
    41: "Secretary of Agriculture",
    42: "Secretary of Education",
    43: "Secretary of Education and Cultural Affairs",
    45: "Secretary of the Commonwealth",
    46: "State Mine Inspector",
    47: "State School Superintendent",
    48: "State Superintendent of Public Instruction",
    49: "State Superintendent of Schools",
    50: "Superintendent of Education",
    51: "Superintendent of Public Instruction",
    333: "Superintendent, Department of Education",
    334: "Taxation Director",
    335: "Transportation Director",
    336: "Utilities and Transportation Commission",
    52: "Tax Commissioner",
    54: "Treasurer and Insurance Commissioner",
    271: "Public Utilities Commission Chair",
    272: "Public Utilities Commission Vice-Chair",
    26: "Comptroller",
    27: "Comptroller of the Treasury",
    30: "Director of the Department of Education",
    8: "State House",
    9: "State Senate",
    79: "Justice of the Supreme Court",
    81: "Judge of the Appellate Court",
    167: "Director of Budget and Finance",
    168: "Director of Business and Industry",
    169: "Director of Department of Agriculture",
    170: "Director of Department of Education",
    172: "Director of Division of Revenue",
    173: "Director of Education",
    174: "Director of Finance",
    175: "Director of Finance and Administration",
    176: "Director of Health and Human Services",
    177: "Director of Insurance",
    178: "Director of Labor",
    179: "Director of Labor Licensing and Regulation",
    181: "Director of Mining and Reclamation Division",
    182: "Director of Parks, Recreation and Tourism",
    183: "Director of Public Safety",
    184: "Director of Revenue",
    185: "Director of Revenue and Taxation",
    186: "Director of Social Services",
    187: "Director of State Housing Authority",
    188: "Director of State Planning Office",
    190: "Director of the Board of Agriculture",
    191: "Director of the Bureau of Land Management",
    192: "Director of the Department for Public Health",
    82: "Director of the Department of Administration",
    193: "Director of the Department of Administration (Finance and Administration Cabinet)",
    194: "Director of the Department of Administrative Services",
    195: "Director of the Department of Agriculture",
    196: "Director of the Department of Civil Rights",
    197: "Director of the Department of Commerce",
    198: "Director of the Department of Community Health",
    199: "Director of the Department of Consumer and Business Services",
    200: "Director of the Department of Economic and Community Development",
    201: "Director of the Department of Elections",
    202: "Director of the Department of Employment, Training and Rehabilitation",
    203: "Director of the Department of Environmental Quality",
    204: "Director of the Department of Finance",
    205: "Director of the Department of Fish, Wildlife and Parks",
    206: "Director of the Department of Health",
    207: "Director of the Department of Health and Human Services",
    208: "Director of the Department of Health and Welfare",
    209: "Director of the Department of Human Services",
    210: "Director of the Department of Insurance",
    211: "Director of the Department of Labor",
    212: "Director of the Department of Labor and Economic Growth",
    213: "Director of the Department of Labor and Industrial Relations",
    214: "Director of the Department of Labor and Training",
    215: "Director of the Department of Land Conservation and Development",
    216: "Director of the Department of Lands",
    217: "Director of the Department of Management and Budget",
    218: "Director of the Department of Military and Veterans Affairs",
    219: "Director of the Department of Natural Resources",
    220: "Director of the Department of Personnel and Administration",
    221: "Director of the Department of Protective and Regulatory Services",
    223: "Director of the Department of Public Safety",
    224: "Director of the Department of Public Safety Standards and Training",
    225: "Director of the Department of State Employer",
    226: "Director of the Department of Transportation",
    227: "Director of the Department of Treasury",
    228: "Director of the Department of Veterans' Affairs",
    229: "Director of the Division of Special Revenue",
    230: "Director of the Elections Enforcement Commission",
    231: "Director of the Finance Authority",
    232: "Director of the Human Services Department",
    233: "Director of the Office of Homeland Security and Preparedness",
    234: "Director of the Office of the State Budget",
    235: "Director of the State Board of Land",
    236: "Director of the State Department of Conservation and Natural Resources",
    189: "Director of Transportation",
    237: "Elections Division Director",
    239: "Emergency Management Agency Director",
    241: "Executive Director Natural Resources Commission",
    242: "Executive Director of the Department of Housing and Community Affairs",
    243: "Executive Director of the Workers' Compensation Board",
    245: "Finance Director",
    248: "Inspector General",
    249: "Insurance Director",
    262: "President of Public Utilities Commission",
    259: "Natural Resources and Conservation Director",
    258: "Natural Resources Director",
    260: "Office of Homeland Security Director",
    263: "President of the Board of Public Utilities",
    264: "President of the State Board of Education",
    266: "Public Health and Human Services Director",
    268: "Public Service Commission Chair",
    332: "Superintendent of the Insurance Department",
    32: "Education Commissioner",
    3: "Governor",
    12: "Attorney General",
    7: "State Assembly",
    83: "Administrator of the Office of State Lands",
    85: "Agriculture Director",
    91: "Board of Education Chair",
    92: "Budget Director",
    93: "Chair of Board of Elections",
    94: "Chair of Elections Commission",
    95: "Chair of Licensing and Regulation Commission",
    96: "Chair of Public Service Commission",
    97: "Chair of Public Utilities Commission",
    98: "Chair of Rail Development Commission",
    99: "Chair of the Public Utilities Commission",
    100: "Chair of the Railroad Commission",
    101: "Chair of the Transport Commission",
    102: "Chairman of Board of Education",
    103: "Chairman of the Department of Agriculture",
    104: "Chairman of the Department of Land and Natural Resources",
    105: "Chairman of the State Board of Elections",
    106: "Chairman of the Tax Commission",
    107: "Chief Business Officer of Office for Economic Development",
    108: "Chief Executive Officer of Finance Authority",
    109: "Chief of the Office of Economic Growth",
    112: "Commission on Indian Affairs",
    330: "State Courts Administrator",
    331: "State Mine Inspector (Office of Mine Safety and Licensing)",
    19: "Commissioner of Education",
    20: "Commissioner of Elections",
    21: "Commissioner of Public Lands",
    25: "Commissioner of the General Land Office",
    28: "Controller",
    29: "Corporation Commissioner",
    86: "Trustee, Office of Hawaiian Affairs",
    462: "Executive Director of the Department of Revenue",
    464: "Executive Council",
    463: "Executive Director of Environmental Quality",
    161: "Comptroller General",
    162: "Comptroller of Public Accounts",
    460: "Comissioner of State Board of Elections",
    163: "Coordinator of Indian Affairs",
    164: "Corporation Commission Chairman",
    165: "Corporation Commission Vice-Chairman",
    274: "School Superintendent",
    261: "Ombudsman",
    53: "Treasurer",
    80: "Chief Judge of the Appellate Court",
    447: "Commissioner of Agriculture and Commerce",
    180: "Director of Labor and Industrial Relations",
    78: "Chief Justice of the Supreme Court",
    445: "Legislative Post Auditor",
    466: "Director of the Office of the State Employer",
    467: "Judge of the Supreme Court",
    470: "Vice Chief Justice of the Supreme Court",
    471: "Deputy Chief Justice of the Supreme Court",
    475: "Senior Associate Justice of the Supreme Court",
    476: "Senior Associate Judge of the Appellate Court",
    477: "Associate Chief Justice of the Supreme Court",
    478: "Presiding Judge of the Appellate Court",
    469: "Presiding Justice of the Supreme Court",
    468: "Associate Justice of the Supreme Court",
    479: "Vice Presiding Judge of the Appellate Court",
    480: "Director of the Department of Energy, Labor and Economic Growth",
    484: "Public Service Commission Vice Chair",
    485: "Executive Director of the Workforce Commission",
    487: "Executive Director of Indian Affairs",
    488: "Director of the Public Utilities Commission",
    496: "State Board of Education",
    13: "Auditor",
    489: "Chairperson of the Labor and Industry Review Commission",
    498: "Senior Justice of the Supreme Court",
    277: "Secretary of Administration",
    278: "Secretary of Administration and Finance",
    279: "Secretary of Aging",
    280: "Secretary of Agriculture and Forestry",
    281: "Secretary of Banking",
    282: "Secretary of Commerce",
    283: "Secretary of Commerce and Tourism",
    284: "Secretary of Commerce and Trade",
    285: "Secretary of Community and Economic Development",
    286: "Secretary of Conservation and Natural Resources",
    287: "Secretary of Department of Natural Resources and Environmental Control",
    288: "Secretary of Energy and Environmental Affairs",
    289: "Secretary of Energy, Minerals and Natural Resources",
    290: "Secretary of Environment and Natural Resources",
    291: "Secretary of Environmental Protection",
    292: "Secretary of Finance",
    293: "Secretary of Finance and Administration",
    294: "Secretary of Game, Fish and Parks",
    295: "Secretary of General Services",
    296: "Secretary of Health",
    297: "Secretary of Health and Environment",
    298: "Secretary of Health and Human Services",
    299: "Secretary of Health and Mental Hygiene",
    300: "Secretary of Health and Social Services",
    301: "Secretary of Housing and Economic Development",
    302: "Secretary of Human Services",
    303: "Secretary of Labor",
    304: "Secretary of Labor and Industry",
    305: "Secretary of Labor and Workforce Development Agency",
    306: "Secretary of Legislative Affairs",
    307: "Secretary of Natural Resources",
    308: "Secretary of Planning and Policy",
    309: "Secretary of Public Safety",
    310: "Secretary of Public Welfare",
    311: "Secretary of Revenue",
    312: "Secretary of Revenue & Regulation",
    313: "Secretary of Taxation and Revenue",
    314: "Secretary of Technology",
    320: "Secretary of the Agency of Commerce and Community Development",
    244: "Executive Secretary of Board of Commissioners for Public Lands",
    322: "Secretary of the Agency of Natural Resources",
    323: "Secretary of the Budget",
    324: "Secretary of the Department of Agriculture",
    325: "Secretary of the Department of Health and Hospitals",
    326: "Secretary of the Department of Revenue",
    327: "Secretary of the Education Cabinet",
    328: "Secretary of the Environment",
    315: "Secretary of Transportation",
    316: "Secretary of Transportation and Construction",
    317: "Secretary of Veterans Affairs",
    318: "Secretary of Veterans' Services",
    319: "Secretary of Wildlife and Parks",
    456: "Secretary of Food and Agriculture",
    459: "Secretary of Business, Housing, and Transportation",
    15: "Clerk of Courts",
    110: "Clerk of Courts",
    111: "Clerk of the Supreme Court",
    88: "Auditor and Inspector",
    87: "Auditor General",
    89: "Auditor of Accounts",
    90: "Auditor of Public Accounts",
    269: "Public Service Commissioner, President",
    273: "Revenue Commissioner",
    166: "Corporation Commissioner (Public Utilities)",
    141: "Commissioner of Public Safety",
    142: "Commissioner of Taxation and Finance",
    238: "Elementary and Secondary Education Commissioner",
    240: "Environmental Management Commissioner",
    246: "Financial Regulation Commissioner",
    247: "Higher Education Commissioner",
    250: "Insurance and Safety Fire Commissioner",
    254: "Labor and Industries Commissioner",
    255: "Labor and Industry Commissioner",
    256: "Labor and Industry Review Commissioner",
    251: "Labor Commissioner (Department of Labor)",
    252: "Labor Commissioner (Labor and Industry)",
    265: "Public Health Commissioner",
    267: "Public Safety Commissioner",
    84: "Agricultural Commissioner",
    113: "Commissioner of Administration",
    114: "Commissioner of Administrative and Financial Services",
    115: "Commissioner of Agriculture and Consumer Services",
    116: "Commissioner of Agriculture and Industries",
    117: "Commissioner of Agriculture and Markets",
    118: "Commissioner of Banking and Finance",
    119: "Commissioner of Commerce",
    120: "Commissioner of Commerce and Insurance",
    121: "Commissioner of Conservation",
    122: "Commissioner of Corrections",
    123: "Commissioner of Defense, Veterans and Emergency Management",
    124: "Commissioner of Economic and Community Development",
    125: "Commissioner of Environment and Conservation",
    126: "Commissioner of Environmental Protection",
    127: "Commissioner of Environmental Quality",
    128: "Commissioner of Finance",
    129: "Commissioner of General Land Office",
    130: "Commissioner of Health",
    131: "Commissioner of Health and Human Services",
    132: "Commissioner of Health and Social Services",
    133: "Commissioner of Inland Fisheries and Wildlife",
    134: "Commissioner of Insurance",
    135: "Commissioner of Labor",
    136: "Commissioner of Labor and Industries",
    137: "Commissioner of Labor and Workforce",
    138: "Commissioner of Marine Resources",
    140: "Commissioner of Professional and Financial Regulation",
    146: "Commissioner of the Department of Administration",
    147: "Commissioner of the Department of Administrative Services",
    159: "Commissioner of Finance and Administration",
    148: "Commissioner of the Department of Banking",
    149: "Commissioner of the Department of Banking and Insurance",
    150: "Commissioner of the Department of Banking, Insurance, Securities, and Health Care Administration",
    151: "Commissioner of the Department of Environmental Protection",
    152: "Commissioner of the Department of Health",
    153: "Commissioner of the Department of Health and Senior Services",
    154: "Commissioner of the Department of Human Services",
    156: "Commissioner of the Department of Personnel",
    157: "Commissioner of the Department of Transportation",
    158: "Commissioner of the Department of Veterans' Affairs",
    160: "Commissioner of the Office of Administration",
    143: "Commissioner of Transportation",
    145: "Commissioner of Veterans Affairs",
    144: "Commissioner of Veteran's Affairs",
    486: "Commissioner of Management and Budget",
    517: "Board of Education",
    518: "Chair of the State Board of Education",
    521: "Secretary of the Labor Cabinet",
    522: "Secretary of the Cabinet for Health and Family Services",
    524: "Secretary of the Energy and Environmental Cabinet",
    139: "Commissioner for Natural Resources",
    253: "Secretary of Labor, Licensing, and Regulation",
    525: "Governor's Council",
    526: "Treasurer and Reciever General",
    519: "Secretary of the Department of Natural Resources",
    155: "Commissioner of the Department of Labor and Workforce Development",
    276: "Secretary of Labor and Workforce Development",
    222: "Director of the Department of Public Health",
    528: "Public Regulation Commission",
    499: "Director of the Department of Agriculture and Rural Development",
    500: "Director of the Department of Technology, Management and Budget",
    505: "Secretary of Workforce Solutions",
    504: "Director of the Government Accountability Board",
    503: "Chair of Utilities and Transportation Commission",
    502: "Secretary of Health and Human Resources",
    501: "Director of the Department of Natural Resources and Environment",
    506: "Director of the Department of Family and Protective Services",
    507: "Chair of the Civil Service Commission",
    512: "Commissioner of the Department of Energy and Environmental Protection",
    513: "Commissioner of Human Rights",
    514: "Commissioner of the Bureau of Mediation Services",
    515: "Judge of the Court of Criminal Appeals",
    516: "Presiding Judge of the Court of Criminal Appeals",
    523: "Executive Director of the Office of Mine Safety and Licensing",
    531: "Director of the Department of Labor and Industries",
    532: "Commissioner of the Department of Forests, Parks & Recreation",
    533: "Secretary of the Agency of Agriculture, Food, and Markets",
    321: "Secretary of the Agency of Human Services",
    10: "Adjutant General",
    534: "Commissioner of the Department of Agriculture and Food",
    536: "Chair of the State Parks and Recreation Board",
    537: "State Parks and Recreation Board",
    538: "Chair of the Office of Hawaiian Affairs",
    539: "Executive Director of the Department of Regulatory Agencies",
    540: "Executive Director of Health and Environment",
    22: "Commissioner of Revenue",
    542: "State Board of Equalization",
}

class statefact(StandardCommand): 
    """ Show a super fun fact about a state! """

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
            return statefact.translate[fact[0]].substitute(state = str(state), fact = str(fact[1]))
        elif state.upper() in states_rev_up:
            if self.conf['debug']:
                print "Matched a state name! (%s)" % self.resolveStateCode(state)
            fact = self.getRandomFact(self.resolveStateCode(state))
            return statefact.translate[fact[0]].substitute(state = str(state), fact = str(fact[1]))
        else:
            return "I don't know anything about this state... hmm..."

class districtbyzip(StandardCommand):
    """ Show districts for a zip code """

    def handleCommand(self, args = None):
        """ Get districts for a zip """

        if self.conf['debug']:
            print 'args %s - %s' % (self.args, args)

        votesmart.apikey = self.conf['votesmart-api-key']
        districts = []

        try:
            if '-' in self.args:
                if self.conf['debug']:
                    print "I've got a 9-digit zip here."
                zip5, zip4 = self.args.split('-')
            elif type(0) == type(int(self.args)):
                if self.conf['debug']:
                    print "I've got a 5-digit zip here."
                zip5 = self.args
                zip4 = None
        except ValueError:
            return "Invalid zip code."

        districts = votesmart.district.getByZip(zip5, zip4=zip4)

        if self.conf['debug']:
            for d in districts:
                print dir(d)

        districts_string = ''
        district_count = 0
        for d in districts:
            if d.officeId != '6':
                district_count += 1
                districts_string += '%s District %s; ' % (offices.get(int(d.officeId)), d.name)

        return "I found %s districts for %s: %s.  More Information: https://votesmart.org/search?q=%s" % (district_count, self.args, str(districts_string.strip('; ')), self.args)

class candidatesearch(StandardCommand):
    """ Show candidates by last namesearch """

    def handleCommand(self, args = None):
        """ Get candidates with a levenstein search"""

        if self.conf['debug']:
            print 'args %s - %s' % (self.args, args)

        votesmart.apikey = self.conf['votesmart-api-key']
        candidates = None

        try:
            candidates = votesmart.candidates.getByLevenstein(self.args)
            message = ''
            total = 0
        except VotesmartApiError as e:
            message = str(e.message)

        if candidates:
            for c in candidates:
                
                if total < 5:
                    name = (c.preferredName + ' ' + c.lastName + ' ' + c.suffix).strip()
                    message += '\n%s: https://votesmart.org/candidate/%s' % (str(name), str(c.candidateId))
                elif total == 5:
                    message += '\nThere were too many results for me to display.  For more information, try https://votesmart.org/search?q=%s' % self.args
                
                total += 1

        return message

class officialsearch(StandardCommand):
    """ Show officials by last namesearch """

    def handleCommand(self, args = None):
        """ Get officials with a levenstein search"""

        if self.conf['debug']:
            print 'args %s - %s' % (self.args, args)

        votesmart.apikey = self.conf['votesmart-api-key']
        officials = None

        try:
            officials = votesmart.officials.getByLevenstein(self.args)
            message = ''
            total = 0
        except VotesmartApiError as e:
            message = str(e.message)

        if officials:
            for c in officials:
                
                if total < 5:
                    name = (c.title + ' ' + c.preferredName + ' ' + c.lastName + ' ' + c.suffix).strip()
                    message += '\n%s: https://votesmart.org/candidate/%s' % (str(name), str(c.candidateId))
                elif total == 5:
                    message += '\nThere were too many results for me to display.  For more information, try https://votesmart.org/search?q=%s' % self.args
                
                total += 1

        return message
