######################################################################
######################################################################
######                                                           #####
######  Import and parse XML Files containing meccg dream cards  #####
######                                                           #####
######################################################################
######################################################################

import os
from pathlib import Path
import re
from lxml import etree
from itertools import groupby
import pandas as pd
import numpy as np
from unidecode import unidecode

################################
# Get XML Files for processing #
################################

# XMLFiles = [file for file in os.listdir('XML Files') if re.findall('_',file) != []]
XMLFiles = [file for file in os.listdir('XML Files') if file.endswith('.xml')]

assert len(XMLFiles) > 0, "No Files in Listed Directory" 

######################################################
# Change & to &amp; in order to make xml files valid #
######################################################

for file in XMLFiles:    
    with open(Path('XML Files',file), 'r+',encoding = 'UTF-8') as f:
        text = f.read()
        text = re.sub('& ', '&amp; ', text)
        f.seek(0)
        f.write(text)
        f.truncate()

######################################
# Dictionary of prefixes:[filepaths] #
######################################

# Setup

# Key function
def prefix(string: str):
    return string[0: string.index('_')]

# Dictionary
FilesDict = {key: list(value) for key, value in groupby(XMLFiles, prefix)}


#################
#################
### Parse XML ###
#################
#################

'''
'rb' opens file as reading + binary, meaning that the bytes in the file 
are not automatically decoded.  
This is necessary, because we can't pass a decoded file using etree.fromstring
'''

# Get column names from XML, with the first column name manually inputted as the card set
column_names = ['Set']

for filelist in FilesDict.values():
    for file in filelist:
        # root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ISO-8859-1'))
        root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))

        # Grab keys 
        for i in root.iterchildren():
            for j in i:
                for key in j.keys():
                    if key not in column_names:
                        column_names.append(key)

        for i in root[0].iterchildren():
            for j in i:
                if j.get("key") not in column_names:
                    column_names.append(j.get("key"))
            
# return values for multiple keys at once.
def dict_return(dict,*keys):
    values = []
    for i in keys:
        values.append(dict.get(i))
    return values


############################################################################
# Loop through xml generating list of lists where each sub-list is a card. #
#               Values for unused attributes marked as none.               #
############################################################################

dict_sets = {prfx:[] for prfx in {prefix(i) for i in XMLFiles}}

cards=[]

for setkey in FilesDict:
    for file in FilesDict[setkey]:
        root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='UTF-8'))
        # root = etree.fromstring(open(Path(os.getcwd(),'XML Files',file),'rb').read(),parser=etree.XMLParser(encoding='ascii//TRANSLIT'))
        for i in root[0].iterchildren():
                # We want the first field to be the set
                card = ['Set',setkey]
                for key,value in zip(i.keys(),i.values()): 
                    #for value in i.values():
                    card.append(key)
                    card.append(value)
                card = [card[i:i+2] for i in range(0, len(card), 2)] 
                for j in i.iterchildren():
                    card.append((j.values()))
                #print(card)    
                dct = dict(card)
                # print(dict_return(dct,*column_names))
                # print(key) 
                # dict_sets[setkey].append(dict_return(dct,*column_names))
                cards.append(dict_return(dct,*column_names))



####################################
# put list of lists into dataframe #
####################################

# Capitalize column names
column_names = [i.capitalize() for i in column_names]

# Create df
df_xml = pd.DataFrame(cards,columns=column_names)

# Change text of graphics to conform with actual file names.
df_xml['Graphics'] = df_xml.apply(\
    lambda x:
    unidecode(x['Graphics']),
    axis=1)

df_xml['Graphics'] = df_xml.apply(\
    lambda x:
    re.sub('[^a-zA-Z0-9.]','',x['Graphics']),
    axis = 1)

# df_xml['Graphics']=df_xml['Graphics'].str.replace('-','')
# df_xml['Graphics']=df_xml['Graphics'].str.replace('''''','')
# df_xml['Graphics']=df_xml['Graphics'].str.replace('\'','')


#######################
# Import Lackey Files #
#######################

df_lackey = pd.DataFrame()

for file in os.listdir('Lackey Files'):
    df_lackey=df_lackey.append(pd.read_csv(Path('Lackey Files',file),sep='\t',encoding = 'ISO-8859-1'))


###########################################
# Rename df_xml fields to match df_lackey #
###########################################
df_xml.rename(inplace=True,
            columns={
                    'Home_site': 'HomeSite'
                    , 'Sp': 'SP'
                    , 'Graphics': 'Imagefile'
                    , 'Mp': 'MP'
                    , 'Site_path': 'SitePath'
                    , 'Draw_opp': 'OpponentDraw'
                    , 'Cp': 'Corruption'
                    }
)                     

#################################
# Add missing columns to df_xml #
#################################

df_xml['GI'] = np.NaN
df_xml['Magic'] = np.NaN

####################################
# Remove extraneous df_xml columns #
####################################

for i in set(df_xml.columns.values) - set(df_lackey.columns.values):
    del df_xml[i]

#############################################
# Check that both dfs have the same columns #
#############################################

assert sorted(df_xml.columns.values) == sorted(df_lackey.columns.values), 'DataFrames contain different columns'

###############################################
# Rearrange df_xml columns to match df_lackey #
###############################################

df_xml = df_xml[df_lackey.columns.values]

###############
# Combine dfs #
###############

df_allsets = pd.concat([df_xml,df_lackey])

###############################
# Replace blank Text with '-' #
###############################
############################
# Convert unicode to ansii #
############################

for column in ['Name','Imagefile','Text','HomeSite','Race','Region']:
    df_allsets[column].where(df_allsets[column] != '', other = '-', inplace = True)
    # df_allsets[column].where(df_allsets[column] != '' ,other = '-', inplace = True)
    df_allsets[column].fillna(value = '-',inplace = True)
    df_allsets[column] = df_allsets[column].astype('string')
    df_allsets[column] = df_allsets.apply(\
        lambda x:
        unidecode(x[column]),
        axis = 1)

# print('after', chr(10),df_allsets[['Name','Text']].loc[df_allsets.Text != ''].head(3))

############################################################################
# For duplicate names within df append number to name to ensure uniqueness #
############################################################################

# Assign arbitrary rank within each group of identical names
df_allsets['NameRank'] = df_allsets.groupby('Name').cumcount() + 1


# Append rank to Name where rank > 1
df_allsets['Name'] = \
    df_allsets.apply(lambda x:
    x['Name'] + str(x['NameRank']) if x['NameRank'] > 1
    else x['Name'],
    axis = 1)

del df_allsets['NameRank']

######################################################
# Fix regions types for mislabeled regions using csv #
######################################################

# Import fixes into df
df_region_fix = pd.read_csv('Fixed_Regions.csv')

# Merge fixes with df
df_allsets = pd.merge(df_allsets,df_region_fix,on = 'Name', how = 'left',suffixes=('','_fix'))

# Update class field
df_allsets.Class.where(df_allsets.Class_fix.isnull(),other = df_allsets.Class_fix, inplace = True)

# Remove Class_fix field
del df_allsets['Class_fix']


#########################
# Miscellaneous cleanup #
#########################

df_allsets.Name.loc[df_allsets.Name == 'Caves of ulund'] = 'Caves of Ulund'
df_allsets.Region.loc[df_allsets.Name.isin(
    ['Old Forest','Old Forest1','Old Forest2','Old Forest (M)']
    )] = 'Cardolan'


####################
# Export df to csv #
####################

df_allsets.to_csv('Complete_Spoiler.csv', index = False)

