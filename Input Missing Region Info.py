
###################################################################################################
# Used to enter region type information for regions that have incorrect data in the spoiler file. #
###################################################################################################

import pandas as pd
import re

#################
# df of spoiler #
#################
cards = pd.read_csv('complete_spoiler.csv')

#####################
# Series of regions #
#####################
regions = cards.Name.loc[(cards.Type.str.contains('region',case = False))\
    | (cards.Class.str.contains('region',case = False))]

regions = [re.sub('\d','',i) for i in regions]


df_regions = cards[['Name','Class']].loc[cards.Name.isin(regions)]

################################################
# Find regions for which we need to input type #
################################################

valid_region_types = ['{w}', '{c}', '{b}', '{s}', '{f}', '{d}']

df_regions_fix = df_regions.loc[~df_regions.Class.isin(valid_region_types)]

##################################
# Input the correct region types #
##################################

for i in df_regions_fix.Name:
    df_regions_fix.Class.loc[df_regions_fix.Name == i] = input(f'Enter region type for {i}')


#################
# Export to csv #
#################
df_regions_fix.to_csv('Fixed_Regions.csv', index = False)