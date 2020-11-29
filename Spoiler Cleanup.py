##################
# Spoile cleanup #
##################

import os
from pathlib import Path
from itertools import groupby
import pandas as pd
import numpy as np
from unidecode import unidecode
import json

##################
# Import Spoiler #
##################

spoiler = pd.read_json('cards-dc.json')

            
###############################
# Replace blank Text with '-' #
###############################
############################
# Convert unicode to ansii #
############################

for column in spoiler.columns.values:
    spoiler[column].where(spoiler[column] != '', other = '-', inplace = True)
    spoiler[column].fillna(value = '-',inplace = True)
    spoiler[column] = spoiler[column].astype('string')
    spoiler[column] = spoiler.apply(\
        lambda x:
        unidecode(x[column]),
        axis = 1)

####################################################
#  Add region type columns for use in Labeler.py   #
# Change double and triple regions types to single #
####################################################

#short
dict_short = {old:('[' + old[0]).lower() + ']' for old in spoiler.RPath.unique()}

dict_short['Double Wilderness'] = '[w]'
dict_short['Triple Wilderness'] = '[w]'
dict_short['Double Coastal Sea'] = '[c]'
dict_short['Triple Coastal Sea'] = '[c]'
dict_short['Desert'] = '[e]'
dict_short['Double Desert'] = '[e]'

spoiler['RType_Short'] = spoiler.RPath.map(dict_short)

#long
dict_long  = {old:old for old in spoiler.RPath.unique()}
 
dict_long ['Double Wilderness'] = 'Wilderness'
dict_long ['Triple Wilderness'] = 'Wilderness'
dict_long ['Double Coastal Sea'] = 'Coastal Sea'
dict_long ['Triple Coastal Sea'] = 'Coastal Sea'
dict_long ['Triple Coastal Seas'] = 'Coastal Sea'
dict_long ['Double Desert'] = 'Desert'

spoiler['RType_Long'] = spoiler.RPath.map(dict_long)

#########################
# Miscellaneous cleanup #
#########################

# Sudu Cull has multiple regions designated
spoiler.Region.loc[spoiler.NameEN == 'Sudu Cull'] = 'Dune Sea'
spoiler.RPath.loc[spoiler.NameEN == 'Dorwinion'] = 'Border-land'
spoiler.RType_Long.loc[spoiler.NameEN == 'Dorwinion'] = 'Border-land'



####################################
# Add regions with no region cards #
####################################


def missing_region(region_name,rtype_short,rtype_long):
    global spoiler

    region_dict = {column:['missing'] for column in spoiler.columns.values}
    
    region_dict['Primary'] = ['Region']
    region_dict['Secondary'] = ['region']
    region_dict['NameEN'] = [region_name]
    region_dict['RType_Short'] = [rtype_short]
    region_dict['RType_Long'] = [rtype_long]

    region_df = pd.DataFrame.from_dict(region_dict)
    spoiler = spoiler.append(region_df)


missing_region('Belegaer','[c]','Coastal Sea')
missing_region('Sea of Silence','[c]','Coastal Sea')


#####################
# Add png ImageName #
#####################
spoiler['png_path'] = spoiler.ImageName.str.replace('.jpg','.png')

#########################################################
# Add fields for territories, dragon's lair, and holds. #
#########################################################
spoiler.NameEN.loc[]

territory_dict = {
                  'Northern Waste': ['Dor Bendor', 'Dragon Gap', 'East Bay of Forochel', 'Ekkaia', 'Everdalf', 'Forochel', 'Forovirkain', 'Gondalf', 'Grey Mountains', 'Hûb Uichel', 'Illuin (see below)', 'Lindalf', 'Lhûgdalf', 'Minheldolath', 'Narthalf', 'Rast Losnaeth', 'Talath Oiohelka', 'Talath Uichel', 'Thorenaer', 'Withered Heath','Ekkaia','West Bay of Forochel','East Bay of Forochel','Sea of Silence','Helkear'],
                  'Eriador': ['Angmar', 'Arthedain', 'Cardolan', 'Dunland', 'Enedhwaith', 'High Pass', 'Hollin', 'Lindon', 'Misty Mountains - Northern Spur', 'Misty Mountains - Southern Spur', 'Númeriador', 'Old Forest', 'Redhorn Gate', 'Rhudaur', 'The Shire','Eriadoran Coast'],
                  'Wilderland': ['Anduin Vales', 'Brown Lands', 'Dagorlad', 'Dorwinion', 'Eorstan', 'Fangorn', 'Grey Mountains', 'Grey Mountain Narrows', 'Gundabad', 'Iron Hills', 'Mirkwood (see below)', 'Northern Rhovanion', 'Sea of Rhûn', 'Southern Rhovanion', 'Wold & Foothills', 'Heart of Mirkwood', 'Southern Mirkwood', 'Western Mirkwood', 'Woodland Realm'],
                  'Mirkwood': ['Heart of Mirkwood', 'Southern Mirkwood', 'Western Mirkwood', 'Woodland Realm'],
                  'Greater Gondor': ['Andrast', 'Gap of Isen', 'Harondor', 'Old Pûkel-land', 'Old Pûkel Gap', 'Rohan', 'Anfalas', 'Anórien', 'Belfalas', 'Ithilien', 'Lamedon', 'Lebennin', 'Mouths of the Anduin'],
                  'Gondor': ['Anfalas', 'Anórien', 'Belfalas', 'Ithilien', 'Lamedon', 'Lebennin', 'Mouths of the Anduin'],
                  'Mordor': ['Chelkar', 'Ered Lithui', 'Gorgoroth', 'Horse Plains', 'Imlad Morgul', 'Khand', 'Nuriag', 'Nurn', 'Udûn'],
                  'Sundering Seas': ['Andrast Coast', 'Bay of Belfalas', 'Bay of Drel Drêl', 'Bay of Felaya', 'Coast of Harad', 'Elven Shores', 'Eriadorian Coast', 'Hyarnustar Coast', 'Kurryan Bay', 'Mardruak Cape', 'Methran Cape', 'The Sundering Seas', 'West Bay of Forochel'],
                  'Great Central Plains': ['Chey Sart', 'Ered Harmal', 'Forrhûn', 'Harrhûn', 'Heb Aaraan', 'Lotan', 'Kykurian Kyn', 'Nûrad', 'Orgothraath', 'Relmether', 'Taur Rómen'],
                  'Sun-lands': ['Arysis', 'Bay of Tulwang', 'Bozisha-Miraz', 'Dune Sea', 'Erim Póa', 'Harshandatt', 'Isfahan', 'Lurmsakûn', 'Mirror of Fire', 'Né Tava', 'Siakan', 'Suza Sumar', 'Seznebab', 'Tulwang', 'Zajantak', 'Chelkar', 'Harondor', 'Harzurzan', 'Hyarmenfalas', 'Pezarsan', 'Bellazen', 'Felaya', 'Kes Arik', 'Mardruak', 'Chennacatt', 'Isra', 'Kirmlesra'], 
                  'Harnendor': ['Chelkar', 'Harondor', 'Harzurzan', 'Hyarmenfalas', 'Pezarsan'],
                  'Bellakar': ['Bellazen', 'Felaya', 'Kes Arik', 'Mardruak'],
                  'Sirayn': ['Chennacatt', 'Isra', 'Kirmlesra'], 
                  'Bay of Ormal': ['Ammu Baj', 'Bulchyades', 'Chy', 'Clyan', 'East Bay of Ormal', 'Ered Ormal', 'Harshandatt', 'Kirmlesra', 'Kythor', 'Lyneria', 'Olyas Kriis', 'Ormal Shores of Ormal', 'Sakal an-Khâr', 'Sára Bask', 'West Bay of Ormal', 'Zhûrgor'],  
                  'Uttersouth': ['Bosiri', 'Sakal-an-Khâr', 'Shores of Maquatostoth', 'Straight of Tumag', 'Tumag', 'Yellow Mountains', 'Zurghôr', 'Dûshera', 'Gan', 'Geshaan', 'Koronandë', 'Koros Bay', 'Hathor', 'Mûmakan', 'Mûmakan Coasts', 'Tâliran', 'Tantûrak', 'Tuktan', 'Ûsakan', 'Ûsakan Bay', 'Mûlambûr'],
                  'Ardor': ['Dûshera', 'Gan', 'Geshaan', 'Koronandë', 'Koros Bay', 'Hathor', 'Mûmakan', 'Mûmakan Coasts', 'Tâliran', 'Tantûrak', 'Tuktan', 'Ûsakan', 'Ûsakan Bay'],
                  'Dominion of the Seven': ['Cleft of Goats', 'Curinshiban', 'Drêl', 'Elorna', 'Hyarn', 'Mag', 'Mirëdor', 'Pel', 'Pel Bight', 'Yellow Mountains – Western Spur']
                  }

####################
# Convert to utf-8 #
####################

for key in territory_dict.keys():
    for item in enumerate(territory_dict[key]): 
        territory_dict[key][item[0]] = unidecode(territory_dict[key][item[0]])


#################################
# Export territory_dict to json #
#################################

jsn = json.dumps(territory_dict)

f = open('dict_territories.json','w')
f.write(jsn)
f.close()

############################################
# Create boolean fields for each territory #
############################################

for key in territory_dict.keys():
    spoiler[key] = 0
    spoiler[key].loc[spoiler.Region.isin(territory_dict[key])] = 1
    spoiler[key].loc[spoiler.NameEN.isin(territory_dict[key])] = 1

####################
# Export df to csv #
####################

spoiler.to_csv('Complete_Spoiler.csv', index = False)
