################################
# Use regex to label resources #
################################

'''
Deep regions (e.g. Deep Wilderness) are treated as regular Wilderness
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

#######################################
# Dictionary of site:[Playable Cards] #
#######################################
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

##########################################
# Dictionary of region: [Playable Cards] #
##########################################

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
    'Misty Mountains -- Northern Spur','Anorien/Ithilien','-']:
    try:
        d_regions[i]
    except:
        d_regions[i] = []

# TODO Need to fix Misty Moutnains -- Northern Spur wherever it occurs.

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
[r'[\[{]b[\[{]',\
'[[{]c[\]{]',\
'[[{]d[\]{]',\
'[[{]f[\]{]',\
'[[{]s[\]{]',\
'[[{]w[\]{]',\
#* '[[{]m[\]{]', ## No cards contain [m] or {m} so far.
'mountain']

# Dict to retrieve regiontype for each region.  region:regiontype

cards = cards.set_index('Name')

rtypes = \
{region:\
    cards.Class.get(region, 'missing')\
        for region in d_regions.keys()} 

# rtypes

cards = cards.reset_index()
# del cards['index']















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