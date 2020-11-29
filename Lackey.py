import pandas as pd


##################
# Import spoiler #
##################

lky = pd.read_csv('Complete_Spoiler.csv')


##########################
# Choose columns to keep #
##########################

lky.columns.values

columns = ['NameEN','Set','ImageName','Primary','Secondary','Race','Alignment','Rarity','MPs','Specific'
            ,'Skill','Mind','Direct','General','Prowess','Body','Corruption','Home','Unique'
            ,'RPath','Site','Playable','GoldRing','GreaterItem','MajorItem','MinorItem','Information'
            ,'Palantiri','Scroll','Hoard','Gear','Haven','Stage','Strikes','erratum','ice_errata','dreamcard','Text'
            ]

############################################
# Create dictionary to adjust column names #
############################################

col_dict = {a:a for a in columns}

col_dict['NameEN'] = 'Name'
col_dict['Site'] = 'SiteType'
col_dict['RPath'] = 'RegionType/Path'
col_dict['ImageName'] = 'Imagefile'


####################
# Update dataframe #
####################

lky = lky[columns]

lky.rename(columns = col_dict, inplace =  True)

######################################
# Export to tab delimited text files #
######################################

for set in lky.Set.unique():
    lky.loc[lky.Set == set].to_csv(set + '.txt',sep = '\t', index = False)


pd.DataFrame(lky.Set.unique()).to_csv('setlist.txt',sep = '\t', index = False)

len(lky.Set.unique())

i = 0
for col in lky.columns.values:
    print('COLUMN'+str(i)+':"'+col+'"\t1')
    i = i+1


len(lky.Set.unique())
