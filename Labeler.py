################################
# Use regex to label resources #
################################

#! Exclude Give --> Playable or Against --> Playable

'''
Deep regions (e.g. Deep Wilderness) are treated as regular Wilderness
Free- hold with space
'''

import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
from itertools import groupby

################
# Import cards #
################

cards = pd.read_csv('Complete_Spoiler.csv')

################################################################
# Narrow down population to resources with non-zero MP values. #
################################################################
mpr = cards[['Name','Type','MP','Text']].\
    loc[(~cards.MP.fillna('').isin(['(0)','0',''])) & \
        (cards.Type.str.contains('resource', case = False))
    ]

#########################################
# Find cards with playable in the title #
#########################################

ply = mpr[['Name','Text']].loc[cards.Text.str.contains('play', case = False)]

#####################
# Series of regions #
#####################
regions = cards.Name.loc[(cards.Type.str.contains('region',case = False))\
    | (cards.Class.str.contains('region',case = False))]

regions = [re.sub('\d','',i) for i in regions]

###################
# Series of sites #
###################
sites = cards.Name.loc[(cards.Type.str.contains('site',case = False))\
    | (cards.Class.str.contains('site', case = False))]
    
sites = [re.sub(' \(.*\)','',i) for i in sites]
sites = [re.sub('\d','',i) for i in sites]
sites = set(sites)

###########################################
# ####################################### #
# # Dictionary of site:[Playable Cards] # #
# ####################################### #
###########################################
# Can remove any clause below and just replace with the [Pp]lay regex.

d_sites = {}

for site in sites:
    names = []
    for name,text in zip(ply.Name,ply.Text):
        if any([
            all([\
            bool(re.search(f'(?<=[Pp]layable)[^.]*{site}',text)),\
            ~bool(re.search(f'(?<=other than)[^.]*{site}',text))+2\
            ]),
            all([\
            bool(re.search(f'(?<=[Pp]lay)[^.]*{site}',text)),\
            ~bool(re.search(f'(?<=other than)[^.]*{site}',text))+2\
            ])
           ]):
            names.append(name)
    d_sites[site] = names


##############################################
# ########################################## #
# # Dictionary of region: [Playable Cards] # #
# ########################################## #
##############################################

d_regions = {}

for region in regions:
    names = []
    for name,text in zip(ply.Name,ply.Text):
        if all([\
            bool(re.search(f'(?<=[Pp]lay)[^.]*{region}',text))\
        ,\
            ~bool(re.search(f'(?<=other than)[^.]*{region}',text))+2\
        ]):
            names.append(name)
    d_regions[region] = names

# Need to add regions with no cards
# In the future, consider replacing Under-deeps with site's adjacent region
for i in ['Under-deeps','Special','Misty Mountains - Southern Spur',\
    'Misty Mountains - Northern Spur','Grey Mountains','Dungeon','Old Forest',\
    'Misty Mountains -- Northern Spur']:
    # 'Misty Mountains -- Northern Spur','Anorien/Ithilien','-']:
    try:
        d_regions[i]
    except:
        d_regions[i] = []

# TODO Need to fix Misty Moutnains -- Northern Spur wherever it occurs.
# Need to add Garrison at Cair Andros to Anorien and Ithilien
d_regions['Anorien'].extend(['Garrison at Cair Andros'])
d_regions['Ithilien'].extend(['Garrison at Cair Andros'])

##########################
# Put sites into regions #
##########################

# Create site:region dict
d_site_region = \
{site:region for site,region in zip(
    d_sites.keys(),
    [cards.Region.loc[cards.Name == card].item() for card in d_sites.keys()]
    )
}

# Extend d_regions with cards playable by site.
for site,region in d_site_region.items():
    d_regions[region].extend(d_sites[site])

##############################
# Map regions to region type #
##############################

# List of regex for region types
reg_region_types = \
{'[\[{]b[\[{]':'{b}',\
'[[{]c[\]{]':'{b}',\
'[[{]d[\]{]':'{d}',\
'[[{]f[\]{]':'{f}',\
'[[{]s[\]{]':'{s}',\
'[[{]w[\]{]':'{w}',
'Border-land':'{b}',\
'[Cc]oast':'{c}',\
'Dark-domain':'{d}',\
'Free-domain':'{f}',\
'Shadow-land':'{s}',\
'Wilderness':'{w}',\
#* '[[{]m[\]{]', ## No cards contain [m] or {m} so far.
'mountain':'mountain'}

# Dict to retrieve regiontype for each region.  region:regiontype
domain = cards.Text.loc[cards.Text.str.contains('domain',case = False)]
cards = cards.set_index('Name')

rtypes = \
{region:\
    cards.Class.get(region, 'missing')\
        for region in d_regions.keys()} 

cards = cards.reset_index()
# del cards['index']

###############################################################################
# Fangorn appears as a region name and hazard.  Need to specify regions type. #
###############################################################################

rtypes['Fangorn'] = '{w}'

################################################
# Manually add rtypes for regions with no card #
################################################
# ! Some of these regions do have cards, and should be dealt with through the 
# ! master file.  This is fine for now, though.

rtypes['Under-deeps'] = 'Under-deeps'
rtypes['Special'] = 'Special'
rtypes['Dungeon'] = 'Dungeon'
rtypes['Old Forest'] = '{w}'
rtypes['Misty Mountains - Southern Spur'] = 'mountain' # Use mountain instead of {m} because that's how it appears on actual cards.
rtypes['Misty Mountains - Northern Spur'] = 'mountain'
rtypes['Misty Mountains -- Northern Spur'] = 'mountain'
rtypes['Grey Mountains'] = '{w}'

del rtypes['Anorien/Ithilien']
del rtypes['-']


################################################################
# Need to extend d_regions with cards playable by region type. #
################################################################
# todo make dict of cards playable by region type to connect to d_regions via rtypes

d_regiontypes = {}

for regiontype,code in reg_region_types.items():
    names = []
    for name,text in zip(ply.Name,ply.Text):
        if all([\
            bool(re.search(f'(?<=[Pp]lay)[^.]*{regiontype}',text))\
        ,\
            ~bool(re.search(f'(?<=other than)[^.]*{regiontype}',text))+2\
        ]):
            names.append(name)
    d_regiontypes[code] = names

# d_regiontypes

# # Extend d_regions with d_regiontypes and rtypes
# for i in 
# :

# rtypes # Region:RegionType
# d_regions # Region:Playable List
# d_regiontypes # RegionType:Region


# ply.to_clipboard(index=False)


#############################
# ######################### #
# # Playable by site type # #
# ######################### #
#############################

# TODO Map sites into Dragon's Lair/non-Dragon's Lair/NA
# ! Need to have site type in region type as well as just site type.

reg_site_types = {'Ruins & Lairs':'{R}',
              'Ruins and Lairs':'{R}',
              'Ruins And Lairs':'{R}',
              '[[{]R[}]]':'{R}',
              'Border-hold':'{B}',
              '[[{]B[}]]':'{B}',    
              'Shadow-hold':'{S}',
              '[[{]S[}]]':'{S}', 
              'Dark-hold':'{D}',
              '[[{]D[}]]':'{D}',
              'Free-hold':'{F}',
              '[[{]F[}]]':'{F}',
              'Dragon\'s Lair':'Dragon\'s Lair',
              'non-Dragon\'s Lair':'non-Dragon\'s Lair',
              'Dwarf-hold':'Dwarf-hold',
              'Elf-hold':'Elf-hold',
              'Atani-hold':'Atani-hold',
              'Man-hold':'Man-hold'
            }

# TODO If card is tagged using sitetype in regiontype than exclude from just site type.
#// Combine regiontype and region names.  Actually not necessary because region names have already been captured.
# TODO Incorporate geographic areas like Eriador, Mirkwood, Northern Wastes etc...

# Region names and region types

d_sitetypes = {}

#TODO Produce dictionary of site type + region type: [Playable Cards]
#TODO Then map each region to list of site types.
#TODO Then map each region:[Playable Cards] 

for sitereg,sitetype in reg_site_types.items():
    for regioneg,regiontype in reg_region_types.values():
    
temp = 
pd.DataFrame.from_dict(d_regions)

import json

def remove_dict_dups(dictionary):
    for i in dictionary.keys():
        dictionary[i]=list(set(dictionary[i]))

remove_dict_dups(d_regions)


jsn = json.dumps(d_regions)

f = open('dict_regions.json','w')
f.write(jsn)
f.close()

json.loads(open('dict_regions.json'))

help(json.load)

type(json.load(open('dict_regions.json','r')))

rtypes['Special']

cards['Name'].get('Strider','missing')

cards.set_index('Name').Class.get('Dunland','missing')

cards.Class.loc[cards.Name == 'Dunland']


cards.Region.index.loc[cards.Name == 'Lorien']



cards.Class.loc[cards.Name == 'nothere']

help(cards.get)

cards.get(cards.Name)

#! Have to deal with regions with no region type due to lack of a 
#! card like Misty Mountains.




'''

Goal: Find cards playable in a region type

Output: Dict of regiontype: [Playable cards]

Execute by looking for Play.* followed by region type in same sentence.

Notes:

Will "other than" be an issue?

With site we need to avoid the pattern Play.* other than site.
With region, though, the pattern would more likely be Play.* regiontype other than.

# ? Any cases where regiontype and other are in the same sentence? 
# Just Peaceful Coexistence

# TODO List of cards to be dealt with manually: Peaceful Coexistence, Entwives


# ? In Eriador, Mirkwood, etc...

'''

# ply.Name.loc[(ply.Text.str.contains('[Oo]ther'))\
#             &(ply.Text.str.contains('[\[{]f[}\]]'))]







# for i in rtypes:
#     print(i, chr(10),\
#         # ply.Name.loc[(ply.Text.str.contains('[Nn]on'))\
#         ply.Name.loc[(ply.Text.str.contains('other'))\
#         & (ply.Text.str.contains(i))]
#     )


#// rtypes = {cards.Class.loc[cards.Name == nameiter].item() for nameiter in cards.Name.loc[cards.Type == 'Region']}

#// for i in ['[b]','[c]','[d]','[f]','[s]','[w]']:
#//     rtypes.add(i)

for i in ['Border-land','Coastal Sea','Dark-domain','Free-domain',]

fullt = 

brack = set(cards.Name.loc[cards.Text.str.contains('Mountain')])

fullt

fullt-brack




rtypes

######################################
# Find cards playable by region type #
######################################


'''
Region types in cards are going to be text (or not).  Region types 
'''

r1 = '{c}{c}'
r2 = '\[c\]\[c\]'
r3 = '{cc}'
r4 = '\[cc\]'

print(ply.Name.loc[ply.Text.str.contains(r2)],chr(10))
print(ply.Name.loc[ply.Text.str.contains(r3)],chr(10))
print(ply.Name.loc[ply.Text.str.contains(r4)],chr(10))
print(ply.Name.loc[ply.Text.str.contains(r1)],chr(10))


cards.Name.loc[(cards.Text.str.contains('deep',case = False)) \
    & ~(cards.Text.str.contains('under',case = False))\
    & ~(cards.Text.str.contains('sulfur',case = False))\
    & ~(cards.Text.str.contains('pukel',case = False))\
    & ~(cards.Text.str.contains('under',case = False))\
    & ~(cards.Text.str.contains('mine',case = False))]



ply.Name.loc[((ply.Text.str.contains(r1))
    | (ply.Text.str.contains('\[w\]')))\
        & ply.Text.str.contains('wilderness', case = False)]



ply.Name.loc[ply.Text.str.contains('wilderness', case = False)]




d_rtypes = {}

for region in regions:
    names = []
    for name,text in zip(ply.Name,ply.Text):
        if all([\
            bool(re.search(f'(?<=[Pp]lay)[^.]*{region}',text))\
        ,\
            ~bool(re.search(f'(?<=other than)[^.]*{region}',text))+2\
        ]):
            names.append(name)
    d_rtypes[region] = names


#############################################
# Find card playable by site type in region #
#############################################


# d_sites['Old Forest']
# d_regions['Cardolan']


# d_sites['Under-deeps']

# cards.Region.loc[cards.Name == 'The Under-grottos']

# cards.Region.loc[cards.Name == 'Tom\'s House']
# cards.Region.loc[cards.Name == 'Old Forest']

# d_regions['Cardolan']
# d_sites['Old Forest']

# {a:b for a,b in d_site_region.items()}

# d_regions

# {value:key for key,value in t.items()}
# sorted(t.keys())
# t

# cards.Region.loc[cards.Name == 'Caves of Ulund']

# cards.loc[cards.Name == 'Caves of ulund']



# Lorien, The Wind-deeps, Iron Hill Dwarf-hold

# cards.loc[cards.Name == 'Grey Havens']

# tdict['Lorien']

# cards.