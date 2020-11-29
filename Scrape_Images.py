from imageio import imread, imsave
import os
import pandas as pd
from time import sleep

###################
# Read in spoiler #
###################

df = pd.read_json('cards-dc.json')


######################################################
# Function for adding prefix for  cards with erratum #
######################################################
# Repalce NaNs with 0

df.erratum.fillna(0, inplace = True)

def erratum_prefix(erratum):
    if erratum == 1:
        return 'dce-'
    else:
        return ''


##########################################
# Create image url and save path columns #
##########################################


df['ImageURL'] = 'https://www.cardnum.net/img/cards/' + df.Set + '/' + df.erratum.apply(erratum_prefix) + df.ImageName
df['SavePath'] = 'Images/Sets/' + df.Set + '/' + df.ImageName

#################################
# Create set folders for images #
#################################


for set in df.Set.unique():
    os.mkdir('Images/Sets/' + set)


########################
# Read and save images #
########################

#! Setting quality and dpi for save isn't working.

for url,path in zip(df.ImageURL,df.SavePath):
    sleep(3)
    try:
        image = imread(url)
        imsave(path, image, quality = 100, dpi = (401,401))
    except AttributeError:
        print('Faulty URL!',url)

