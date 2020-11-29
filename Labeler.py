################################
# Use regex to label resources #
################################

#TODO Incorporate named regions (e.g. Eriador, Northern Wastes, Sunlands)
#TODO Use list of alignment restricted cards

#! Exclude Give --> Playable or Against --> Playable

'''
Deep regions (e.g. Deep Wilderness) are treated as regular Wilderness
Free- hold with space
'''

import pandas as pd
import re
from pathlib import Path
import json

def labeler_output(Alignment):
# Alignment = 'Hero'

    ################
    # Import cards #
    ################

    cards = pd.read_csv('Complete_Spoiler.csv')

    ##########################################################
    # Add field with full file path for image for future use #
    ##########################################################

    cards['fullpath'] = cards.apply(lambda x: str(Path('Images','Sets',x['Set'],x['png_path'])), axis = 1)

    ################################################################
    # Narrow down population to resources with non-zero MP values. #
    ################################################################
    mpr = cards[['fullpath','Primary','MPs','Text','Alignment']].\
        loc[(~cards.MPs.fillna('').isin(['(0)','0','-','missing'])) & \
            (cards.Primary.str.contains('resource', case = False))
        ]


    ##########################################
    # Narrow down MPR to specified alignment #
    ##########################################

    #TODO Allow for cross-alignment resources for given lord type (e.g. Elf: Minion Rings)
    #TODO Allow lord players to use minion even mp cards.
    #? Lord players can use minion even mp cards? Yes

    # Dict of alignment
    alignment_resources_dict = {'Hero': ['Hero','Dual'],
                                'Minion':['Minion','Dual'],
                                'Fallen-wizard':['Hero','Minion','Dual','Fallen/Lord','Fallen-wizard'],
                                'Balrog':['Minion','Dual','Balrog'],
                                'Elf-lord':['Hero','Dual','Elf-lord','Lord'],
                                'Dwarf-lord':['Hero','Dual','Dwarf-lord','Lord'],
                                'Atani-lord':['Hero','Dual','Atani-lord','Lord'],
                                'Dragon-lord':['Minion','Dual','Dragon-lord','Lord','Grey']
                                }

    mpr = mpr.loc[mpr.Alignment.isin(alignment_resources_dict[Alignment])]

    ########################################
    # Find cards with playable in the text #
    ########################################

    ply = mpr[['fullpath','Text']].loc[(cards.Text.str.contains('play', case = False))]


    #################################################################
    #         Manually remove image values from dictionary.         #
    # Should be a last resort if adjusting the regex or other logic #
    #                         doesn't work.                         #
    #################################################################

    def manual_override_remove(dict,key,image):
        try:
            d_m_ind = dict[key].index(image) 
            del dict[key][d_m_ind]
        except ValueError:
            print('')    



    ###########################
    # Make dict values unique #
    ###########################
    def dict_unique(dict):
        for key,value in dict.items():
            dict[key] = list(set(dict[key]))

    #####################
    # Series of regions #
    #####################
    #! 
    regions = cards.NameEN.loc[(cards.Primary.str.contains('region',case = False))\
        | (cards.Secondary.str.contains('region',case = False))]


    # regions = [re.sub('\d','',i) for i in regions]
    ###################
    # Series of sites #
    ###################
    #!
    sites = cards.NameEN.loc[(cards.Primary.str.contains('site',case = False))\
        | (cards.Primary.str.contains('site', case = False))]
        
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
        for name,text in zip(ply.fullpath,ply.Text):
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
        for name,text in zip(ply.fullpath,ply.Text):
            if all([\
                bool(re.search(f'(?<=[Pp]lay)[^.]*{region}',text))\
            ,\
                ~bool(re.search(f'(?<=other than)[^.]*{region}',text))+2\
            ]):
                names.append(name)
        d_regions[region] = names


    # Add Dungeon
    d_regions['Dungeon'] = []

    ##############################
    # Map regions to region type #
    ##############################

    # List of regex for region types
    reg_region_types = \
    {
    '\[b\]':'Border-land',\
    '\[c\]':'Coastal Sea',\
    '\[d\]':'Dark-domain',\
    '\[f\]':'Free-domain',\
    '\[s\]':'Shadow-land',\
    '\[w\]':'Wilderness',\
    'Border-land':'Border-land',\
    '[Cc]oast':'Coastal Sea',\
    'Dark-domain':'Dark-domain',\
    'Free-domain':'Free-domain',\
    'Shadow-land':'Shadow-land',\
    '[Ww]ilderness':'Wilderness',\
    '[Dd]esert':'Desert',\
    '[Mm]ountain':'Mountain',
    '[Jj]ungle':'Jungle',
    '[j]':'Jungle'
    }
    # {
    # '\[b\]':'[b]',\
    # '\[c\]':'[c]',\
    # '\[d\]':'[d]',\
    # '\[f\]':'[f]',\
    # '\[s\]':'[s]',\
    # '\[w\]':'[w]',\
    # 'Border-land':'[b]',\
    # '[Cc]oast':'[c]',\
    # 'Dark-domain':'[d]',\
    # 'Free-domain':'[f]',\
    # 'Shadow-land':'[s]',\
    # '[Ww]ilderness':'[w]',\
    # '[Dd]esert':'[e]',\
    # '[Mm]ountain':'[m]'
    # }



    # Dict to retrieve regiontype for each region.  region:regiontype
    cards = cards.set_index('NameEN')

    rtypes = \
    {region:\
        # cards.RType_Short.get(region, 'missing')\
        cards.RType_Long.loc[cards.Primary == 'Region'].get(region, 'missing')\
            for region in d_regions.keys()} 

    cards = cards.reset_index()
    # del cards['index']

    ################################################
    # Manually add rtypes for regions with no card #
    ################################################
    #TODO Need to deal with mountain regions since they are also labeled as wilderness.

    # rtypes['Under-deeps'] = 'Under-deeps'
    # rtypes['Special'] = 'Special'
    # rtypes['Dungeon'] = 'Dungeon'

    # del rtypes['-']

    ################################################################
    # Need to extend d_regions with cards playable by region type. #
    ################################################################
    # todo make dict of cards playable by region type to connect to d_regions via rtypes

    d_regiontypes = {}

    for regiontype,code in reg_region_types.items():
        names = []
        for name,text in zip(ply.fullpath,ply.Text):
            if all([\
                bool(re.search(f'(?<=[Pp]lay)[^.]*{regiontype}',text))\
            ,\
                ~bool(re.search(f'(?<=other than)[^.]*{regiontype}',text))+2\
            ]):
                names.append(name)
        d_regiontypes[code] = names


    # # Remove Blue Mountain Dwarves from region: mountain
    # try:
    #     d_m_ind = d_regiontypes['[m]'].index('metw_bluemountaindwarves.jpg') 
    #     del d_regiontypes['[m]'][d_m_ind]
    # except ValueError:
    #     print('')

    d_regiontypes
    #############################
    # ######################### #
    # # Playable by site type # #
    # ######################### #
    #############################


    #// TODO Check Ruins & Lairs next to [R] 
    # There are cases where Ruins & Lairs appears and [R] is not present and vice versa.
    #! Need to check for name and symbol separately for site types

    # cards.loc[cards.Text.str.contains('Ruins And Lairs')]
    # cards.loc[cards.Text.str.contains('Ruins & Lairs \[R\]')].count()
    # cards.loc[cards.Text.str.contains('\[R\]')].count()

    # cards.Site.unique()

    # TODO Map sites into Dragon's Lair/non-Dragon's Lair/NA
    # ! Need to have site type in region type as well as just site type.

    #TODO Need to deal with cases where playable at a haven applies to other kinds of havens.

    reg_site_types = {'Ruins & Lairs':'Ruins & Lairs',
                'Ruins and Lairs':'Ruins & Lairs',
                '\[R\]':'Ruins & Lairs',
                'Border-hold':'Border-hold',
                '\[B\]':'Border-hold',    
                'Shadow-hold':'Shadow-hold',
                '\[S\]':'Shadow-hold', 
                'Dark-hold':'Dark-hold',
                '\[D\]':'Dark-hold',
                'Free-hold':'Free-hold',
                '\[F\]':'Free-hold',
                'Haven':'Haven',
                'Darkhaven':'Darkhaven',
                'Lordhaven':'Lordhaven',
                'Elf-hold':'Elf-hold',
                'Wizardhaven':'Wizardhaven',
                'Lordhaven':'Lordhaven',
                'Dragon\'s Lair':'Dragon\'s Lair',
                'Dragon\'s lair':'Dragon\'s Lair',
                'Dragon\'s lair':'Dragon\'s Lair',
                'non-Dragon\'s Lair':'non-Dragon\'s Lair',
                'Dwarf-hold':'Dwarf-hold',
                'Elf-hold':'Elf-hold',
                'Atani-hold':'Atani-hold',
                'Man-hold':'Man-hold',
                'Under-deeps' : 'Under-deeps'
                }


    #############################################
    # Dictionary of site_type: [playable cards] #
    #############################################

    #TODO Deal with sitetype in regiontype separately, 
    #TODO because regiontype alone should catch most cases.
    #! Need to correct for...
    # Wizardhaven other than...



    d_sitetypes = {}

    for sitetype,code in reg_site_types.items():
        names = []
        for name,text in zip(ply.fullpath,ply.Text):
            if all([\
                bool(re.search(f'(?<=[Pp]lay)[^.]*{sitetype}',text))\
            ,\
                ~bool(re.search(f'(?<=in a)[^.]*{sitetype}',text))
            ,\
                ~bool(re.search(f'(?<=other than)[^.]*{sitetype}',text))+2\
            ]):
                names.append(name)
        d_sitetypes[code] = names


    # Find cards that need to be excluded from d_sitetypes
    d_sitetypes_n = {}

    for sitetype,code in reg_site_types.items():
        names = []
        for name,text in zip(ply.fullpath,ply.Text):
            if any([
            #     bool(re.search(f'(?<=[Pp]lay)[^.]*{sitetype}[^.]*(?= in)',text))
            \
                bool(re.search(f'(?<=[Nn]ot [Pp]lay)[^.]*{sitetype}',text))
            ,\
                bool(re.search(f'(?<=[Pp]lay)[^.]*non-{sitetype}',text))\
            ,\
                bool(re.search(f'(?<=other than)[^.]*{sitetype}',text))\
            ]):
                names.append(name)
        d_sitetypes_n[code] = names

    # Delete cards that need to be excluded
    # for stype,playable in d_sitetypes_n.items():
    for stype in d_sitetypes_n.keys():
        for card in d_sitetypes_n[stype]:
            # print(stype,card,ind)
            try:
                ind = d_sitetypes[stype].index(card) 
            except ValueError:
                continue
            del d_sitetypes[stype][ind]


    ###########################################################
    # Delete Under-deeps playable cards from other site types #
    ###########################################################

    for sitetype, playable in d_sitetypes.items():
        if sitetype == 'Under-deeps':
            continue
        else:
            d_sitetypes[sitetype] = list(set(playable) - set(d_sitetypes['Under-deeps']))


    ###########################################################
    # Make site tables that has site information by alignment #
    ###########################################################
    #TODO Sites for specific lords
    #TODO Turn all of these dfs into a function that creates dict of dfs

    def alignment_sites():
        alignment_only_sites = cards[['NameEN','Site','Alignment','Region','fullpath']].loc[(cards.Alignment == Alignment)\
                                &(cards.Primary == 'Site')]

        sites = cards[['NameEN','Site','Alignment','Region','fullpath']].loc[(cards.Alignment.isin(alignment_list_dict[Alignment]))
                            & (cards.Primary == 'Site')
                            & ~(cards.NameEN.isin(alignment_only_sites.NameEN))]

        sites = sites.append(alignment_only_sites)

        sites['Alignment'] = Alignment  
        return sites
    alignment_list_dict = {
                        'Hero':['Hero','Dual'],
                        'Minion':['Minion','Dual'],
                        'Fallen-wizard':['Hero','Dual'],
                        'Elf-lord':['Hero','Dual'],
                        'Dwarf-lord':['Hero','Dual'],
                        'Atani-lord':['Hero','Dual'],
                        'Balrog':['Minion','Dual'],
                        'War-lord':['Minion','Dual']
    }


    alignment_sites = alignment_sites()


    #TODO Consider only including sitetype playable in regiontype/named area (aka Eriador)
    # Can also just restrict by uniqueness
    #TODO Add playable in special sitetype (e.g. Dragon's Lair)


    #########################
    # Playable in territory #
    #########################

    terr_list = ['Northern Waste', 'Eriador', 'Wilderland', 'Mirkwood', 'Greater Gondor', 'Gondor', 'Mordor', 'Sundering Seas', 'Great Central Plains', 'Sun-lands', 'Harnendor', 'Bellakar', 'Sirayn', 'Bay of Ormal', 'Uttersouth', 'Ardor', 'Dominion of the Seven']

    d_territories = {}

    for territory in terr_list:
        names = []
        for name,text in zip(ply.fullpath,ply.Text):
            if all([\
                bool(re.search(f'(?<=[Pp]lay)[^.]*{territory}',text))\
            ,\
                ~bool(re.search(f'(?<=other than)[^.]*{territory}',text))+2\
            ,\
                ~bool(re.search(f'(?<=not be in )[^.]*{territory}',text))+2\
            ]):
                names.append(name)
        d_territories[territory] = names

    # Need territories as region names
    # and region types as region names

    d_territories

    ##############################################
    # Import dict with territory:region mappings #
    ##############################################
    with open('dict_territories.json') as json_file: 
        dict_territory_regions = json.load(json_file) 

    dict_territory_regions
    ############################################################
    # Transform territory:[playable] dict to region:[playable] #
    ############################################################
    dict_territories_regions_playable = {}

    for territory,regions in dict_territory_regions.items():
        for region in regions:
            dict_territories_regions_playable[region] = d_territories[territory]

    ############################################################
    # Transform regiontype:[playable] dict to region:[playable] #
    ############################################################
    dict_regiontype_regions_playable = {}

    for region in d_regions.keys():
        dict_regiontype_regions_playable[region] = d_regiontypes.get(rtypes.get(region,''),'')


    # dict_regiontype_regions_playable
    ############################################################
    # Transform sitetype:[playable] dict to region:[playable] #
    ############################################################
    #TODO Low priority.  Need to account for special sitetypes (Dragon's Lair, Dwarf-hold, etc...)
    # dict of region:[sitetypes]
    d_region_sitetype = {}

    for region in d_regions.keys():
        d_region_sitetype[region] = list(set(cards.Site.loc[(cards.Region == region) & (cards.Primary == 'Site')]))

    # region:[playable]
    dict_sitetype_regions_playable = {region:[] for region in d_regions}

    for region, sitetypes in d_region_sitetype.items():
        for sitetype in sitetypes:
            dict_sitetype_regions_playable[region].extend(d_sitetypes[sitetype])


    #########################################################################
    # Remove territory specific cards from dict_regiontype_regions_playable #
    #########################################################################
    dict_intersection = {}
    dict_subtract = {}
    all_territory_playable_set = []

    for i in dict_territories_regions_playable.values():
        all_territory_playable_set.extend(i)

    all_territory_playable_set = set(all_territory_playable_set)

    for region,playable in dict_regiontype_regions_playable.items():
        dict_regiontype_regions_playable[region] = list(set(playable) - all_territory_playable_set)


    ################################################################################################
    # Remove territory specific + region specific cards from regions that are not the correct type #
    ################################################################################################

    # for region,playable in dict_territories_regions_playable.items():
    #     set(playable).intersection(set(dict_regiontype_regions_playable.get(region,'')))
    #     # dict_territories_regions_playable[region] = set(playable).intersection(set(dict_regiontype_regions_playable.get(region,'')))

    # # both
    # # For a given region copy cards in both

    # # need the set that are in both + the set that are only in territories

    # d_regiontypes
    # territory --> region --> regiontype 

    # set(dict_territories_regions_playable[]).intersection(set(dict_regiontype_regions_playable.get(region,'')))

    # dict_territories_regions_playable

    #########################################################
    # Put regiontype playable cards back into d_regiontypes #
    #########################################################

    d_regiontypes = {regiontype:[] for regiontype in d_regiontypes.keys()}

    for region,playable in dict_regiontype_regions_playable.items():
        d_regiontypes.get(rtypes[region],[]).extend(playable)

    for regiontype,playable in d_regiontypes.items():
        d_regiontypes[regiontype] = list(set(d_regiontypes[regiontype]))


    ################################################################################################
    # Remove territory specific + region specific cards from regions that are not the correct type #
    ################################################################################################

    dict_intersection = {}
    dict_subtract = {}
    all_regiontype_playable_set = []
    # all_regiontype_playable_set = set([all_regiontype_playable_set.extend([i]) for i in dict_regiontype_regions_playable.values()])

    for i in dict_regiontype_regions_playable.values():
        all_regiontype_playable_set.extend(i)

    all_regiontype_playable_set = set(all_regiontype_playable_set)

    for region,playable in dict_territories_regions_playable.items():
        # print(region,chr(10),dict_regiontype_regions_playable.get(region,''),chr(10),'playable',chr(10),playable,chr(10),chr(10))
        
        diff = set(playable)-all_regiontype_playable_set
        intersect = set(playable).intersection(set(dict_regiontype_regions_playable.get(region,'')))
        dict_territories_regions_playable[region] = list(diff | intersect)

    ############################################################################################################
    # Remove territory specific + site specific cards from regions that do not contain the relevant site types #
    ############################################################################################################

    dict_intersection = {}
    dict_subtract = {}
    all_sitetype_playable_set = []
    # all_sitetype_playable_set = set([all_sitetype_playable_set.extend([i]) for i in dict_regiontype_regions_playable.values()])

    for i in dict_sitetype_regions_playable.values():
        all_sitetype_playable_set.extend(i)

    all_sitetype_playable_set = set(all_sitetype_playable_set)

    for region,playable in dict_territories_regions_playable.items():
        
        diff = set(playable)-all_sitetype_playable_set
        intersect = set(playable).intersection(set(dict_sitetype_regions_playable.get(region,'')))
        dict_territories_regions_playable[region] = list(diff | intersect)



    #########################################
    # Extend d_regions with territory cards #
    #########################################

    for region in d_regions.keys():
        d_regions[region].extend(dict_territories_regions_playable.get(region,''))

    ############################################################################
    # Convert dict_regiontype_regions_playable back into regiontype:[playable] #
    ############################################################################
    # TODO ^


    # Need to add regions with no cards
    # In the future, consider replacing Under-deeps with site's adjacent region
    #!
    # for i in ['Under-deeps','Special','Misty Mountains - Southern Spur',\
    # for i in ['Under-deeps','Special','Misty Mountains - Southern Spur',\
    #     'Misty Mountains - Northern Spur','Grey Mountains','Dungeon','Old Forest']:#,\
    #     # 'Misty Mountains -- Northern Spur']:
    #     # 'Misty Mountains -- Northern Spur','Anorien/Ithilien','-']:
    #     try:
    #         d_regions[i]
    #     except:
    #         d_regions[i] = []

    # # TODO Need to fix Misty Moutnains -- Northern Spur wherever it occurs.
    # # Need to add Garrison at Cair Andros to Anorien and Ithilien
    # d_regions['Anorien'].extend(['Garrison at Cair Andros'])
    # d_regions['Ithilien'].extend(['Garrison at Cair Andros'])

    #######################################################################
    # Remove territory specific cards from dict_sitetype_regions_playable #
    #######################################################################

    for region,playable in dict_sitetype_regions_playable.items():
        dict_sitetype_regions_playable[region] = list(set(playable) - set(dict_territories_regions_playable.get(region,'')))

    ##########################
    # Put sites into regions #
    ##########################

    # Create site:region dict
    d_site_region = \
    {site:region for site,region in zip(
        d_sites.keys(),
        [cards.Region.loc[(cards.NameEN == card) & (cards.Primary == 'Site')].unique().item() for card in d_sites.keys()]
        )
    }

    # Extend d_regions with cards playable by site.
    for site,region in d_site_region.items():
        d_regions[region].extend(d_sites[site])

    # Prevents erro
    #!
    # d_regions['-'] = [] 


    ############################################
    # Manually remove mistakenly flagged cards #
    ############################################

    manual_override_remove(d_regiontypes,'Mountain','Images\\Sets\\MEDM\\medm_necklaceofgirion.jpg')
    manual_override_remove(d_regiontypes,'Mountain','Images\\Sets\\METW\\metw_bluemountaindwarves.jpg')
    manual_override_remove(d_regiontypes,'Wilderness','Images\\Sets\\METI\\meti_entwives.jpg')
    manual_override_remove(d_regiontypes,'Dark-domain','Images\\Sets\\METI\\meti_entwives.jpg')
    manual_override_remove(d_regiontypes,'Shadow-land','Images\\Sets\\METI\\meti_entwives.jpg')
    manual_override_remove(d_regiontypes,'Wilderness','Images\\Sets\\MEFB\\mefb_elvesoftaurromen.jpg')
    manual_override_remove(d_regiontypes,'Shadow-land','Images\\Sets\\MEFB\\mefb_erynlasgalen.jpg')
    manual_override_remove(d_regiontypes,'Shadow-land','Images\\Sets\\MEKN\\mekn_annayulma.jpg')
    manual_override_remove(d_sitetypes,'Haven','Images\\Sets\\MEKN\\mekn_annayulma.jpg')
    manual_override_remove(d_regions,'Harondor','Images\\Sets\\MEWR\\mewr_crownofearnur.jpg')
    manual_override_remove(d_regions,'Ithilien','Images\\Sets\\MEWR\\mewr_crownofearnur.jpg')
    manual_override_remove(d_regions,'Southern Rhovanion','Images\\Sets\\MEWR\\mewr_crownofearnur.jpg')
    manual_override_remove(d_sitetypes,'Border-hold','Images\\Sets\\MESL\\mesl_hwanin.jpg')
    manual_override_remove(d_sitetypes,'Border-hold','Images\\Sets\\MEWR\\mewr_harnendorcontested.jpg')

    ######################################
    # Site images per region output dict #
    ######################################
    dict_sites_output = {region:[] for region in alignment_sites.Region.unique()}

    for region in dict_sites_output.keys():
        for image in alignment_sites.fullpath.loc[alignment_sites.Region == region]:
            dict_sites_output[region].extend([image])


    ##############################
    # Playable cards output dict #
    ##############################
    d_output = d_regions
    d_output.update(d_sitetypes)
    d_output.update(d_regiontypes)

    dict_unique(d_output)


    ###################################
    # Convert Paths in dict to string #
    ###################################
    return d_output, dict_sites_output
