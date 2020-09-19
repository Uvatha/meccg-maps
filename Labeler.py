################################
# Use regex to label resources #
################################

'''
Also look up "played" and other variations in addition to playable
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

ply = mpr[['Name','Text']].loc[cards.Text.str.contains('Playable', case = False)]

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


##########################
# Put sites into regions #
##########################

d_site_region = \
{site:region for site,region in zip(
    d_sites.keys(),
    [cards.Region.loc[cards.Name == card].item() for card in d_sites.keys()]
    )
}

# cards.loc[(cards.Region == '-') & (cards.Name.isin(sites))]

for site,region in d_site_region.items():
    d_regions[region].extend(d_sites[site])



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