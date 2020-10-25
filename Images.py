###########################################################################
# Combine each playable card's image into a single image for each region. #
###########################################################################

import cv2 as cv
import pandas as pd
import os
import json
from pathlib import Path
import numpy as np
from PIL import Image
from PIL import ImageDraw
from math import ceil

# #! Okay for now.  Not worth spending more time on until final spoilers are obtained.
# # Have list of images in dataframe by set.  Want to compare to list of images in Set folders.
# # Make a comparable sets
# for dfset in cards.Set.unique():
#     df_set = set(cards.Imagefile.loc[cards.Set == dfset])
#     images_set = set(os.listdir('Images/'+dfset))
#     print(dfset,chr(10),df_set-images_set,chr(10),chr(10))

##################
# Import spoiler #
##################
cards = pd.read_csv('Complete_Spoiler.csv')

################################################
# Load dictionary with region:[playable cards] #
################################################
with open('dict_regions.json','r') as f:
    d_regions = json.load(f)


##############################################################
# Function that converts list of cards to list of Imagefiles #
##############################################################

def fetch_image_paths(cardlist):
    imagelist = []
    for card in cardlist:
        pth = Path('Images',cards.Set.loc[cards.Name == card].item(),cards.Imagefile.loc[cards.Name == card].item())
        imagelist.extend([pth])
    return list(set(imagelist))


###################################
# Catch missing image files/paths #
###################################
def catch_noimage(fpath,handler_path):
    '''
    Handles cases where filepath does not exist.
    '''
    try:
        return PIL.Image.open(fpath)
    except FileNotFoundError:
        print('FileNotFoundError:',fpath)
        img = PIL.Image.open(handler_path)
        draw = ImageDraw.Draw(img)
        draw.text((0, 295),str(fpath),(255,255,255))
        return img


#TODO Address regions with no playable cards.
#TODO Add transparent placeholder cards to ensure each row is of the same length

def h_images(imagelist, n_horizontal):
    '''
    Concatenates a list of image paths horizontally into list of 
    k n length images
    '''
    placeholder = Path('Images','metw-back.jpg')
    if len(imagelist) == 0:
        output_list = [PIL.Image.open(placeholder)]
    else:
        output_list = []
        h_arrays = []
        k = ceil(len(imagelist) / n_horizontal)
        n = min(n_horizontal,len(imagelist))
        # n that doesn't decrease by counter
        n_static = n 
        temp = []
        while k > 0:
            # print('start')
            while len(imagelist) > 0 and n > 0:
                temp.extend([imagelist.pop(0)])
                n = n - 1
            while len(temp) < n_static:
                temp.extend([placeholder])
                # print(len(temp))
            #     print('inner')
            # print('outer')
            imgs = [ catch_noimage(i,placeholder) for i in temp ]
            # imgs = [i.putalpha(255) for i in imgs]
            # print(imgs)
            imgs_comb = np.hstack(imgs)
            h_arrays.append(imgs_comb)
            n = n_horizontal
            temp = []
            k = k - 1
            # return imgs
            # print('stop')
        output_list = [PIL.Image.fromarray(img) for img in h_arrays]
    return output_list

def v_images(h_images_output):
    '''
    Takes the h_images output and v_stacks the combined horizontal images.
    '''
    v_imgs = np.vstack(h_images_output)
    output_image = PIL.Image.fromarray(v_imgs)
    return output_image

##########################################
# Create combined images for each region #
##########################################
#! All mp resources

cards_per_row = 5
# size_reduce_percent = 1

for i in d_regions:
    img = v_images(h_images(fetch_image_paths(d_regions[i]),cards_per_row))
    size_reduce_percent = min(1,590/(img.size[1]*0.3))
    img = img.resize(tuple(int(i*size_reduce_percent) for i in img.size))
    img.save(Path('Images','All', i + '.jpg').absolute())
