###########################################################################
# Combine each playable card's image into a single image for each region. #
###########################################################################

#// TODO Save images as png and set alpha to 0 for placeholder.

import pandas as pd
from pathlib import Path
import numpy as np
from PIL import Image
from PIL import ImageDraw
from math import ceil
import os
import Labeler 


def combined_images(alignment):
    ##################
    # Import spoiler #
    ##################
    cards = pd.read_csv('Complete_Spoiler.csv')

    # ################################################
    # # Load dictionary with region:[playable cards] #
    # ################################################
    # with open('dict_regions.json','r') as f:
    #     d_regions = json.load(f)

    d_regions,d_sites_regions = Labeler.labeler_output(alignment)


    ######################
    # Create directories #
    ######################
    def create_alignment_directories(alignment):
        try:
            os.mkdir('Images/' + alignment)
        except FileExistsError:
            print(f'{alignment} directory already exists')
        try:
            os.mkdir(f'Images/{alignment}/Sites')
        except FileExistsError:
            print('')


    ###################################
    # Catch missing image files/paths #
    ###################################
    def catch_noimage(fpath,handler_path):
        '''
        Handles cases where filepath does not exist.
        '''
        try:
            img = Image.open(fpath)
            img.putalpha(255)
            return img
        except FileNotFoundError:
            print('FileNotFoundError:',fpath)
            img = Image.open(handler_path)
            img.putalpha(0)
            # draw = ImageDraw.Draw(img)
            # draw.text((0, 295),str(fpath),(255,255,255))
            return img


    #TODO Address regions with no playable cards.
    #TODO Add transparent placeholder cards to ensure each row is of the same length

    def h_images(imagelist, n_horizontal):
        '''
        Concatenates a list of image paths horizontally into list of 
        k n length images
        '''
        placeholder = Path('Images','metw-back.png')
        

        if len(imagelist) == 0:
            output_list = [catch_noimage('bloopity-doop',placeholder)] # Done to apply alpha value to avoid error.  Shouldn't be necessary, but update can wait.
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
                    temp.extend(['flipity floo'])
                    # print(len(temp))
                #     print('inner')
                # print('outer')
                imgs = [catch_noimage(i,placeholder) for i in temp]
                imgs = [img.resize((420,590)) for img in imgs]
                # imgs = [i.putalpha(255) for i in imgs]
                # print(imgs)
                imgs_comb = np.hstack(imgs)
                h_arrays.append(imgs_comb)
                n = n_horizontal
                temp = []
                k = k - 1
                # return imgs
                # print('stop')
            output_list = [Image.fromarray(img) for img in h_arrays]
            # output_list = [img.convert('L') for img in output_list]
        return output_list

    def v_images(h_images_output):
        '''
        Takes the h_images output and v_stacks the combined horizontal images.
        '''
        # print(h_images_output)
        v_imgs = np.vstack(h_images_output)
        # print(v_imgs)
        output_image = Image.fromarray(v_imgs)
        return output_image


    ###########################
    # Create required folders #
    ###########################
    create_alignment_directories(alignment)


    #########################################################
    # Dictionary for cards per row based on number of cards #
    #########################################################

    regions_cards_per_row_dict = {0:1, 1:1, 2:2, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3, 10:4, 11:4, 12:4}
    sites_cards_per_row_dict = {0:1, 1:1, 2:1, 3:1, 4:1}
    ##########################################
    # Create combined images for each region #
    ##########################################
    #! All mp resources

    # cards_per_row = 5
    # size_reduce_percent = 1

    for i,j in d_regions.items():

        # img = h_images(j,regions_cards_per_row_dict.get(len(j),5))
        img = v_images(h_images(j,regions_cards_per_row_dict.get(len(j),5)))

        # size_reduce_percent = min(1,590/(img.size[1]*0.3))

        # img = img.resize(tuple(int(i*size_reduce_percent) for i in img.size))

        img.save(Path('Images',alignment, i + '.png').absolute())



    # ###############################################
    # # Create combined site images for each region #
    # ###############################################

    # cards_per_row = 2
    # size_reduce_percent = 1

    for i,j in d_sites_regions.items():

        img = v_images(h_images(j,sites_cards_per_row_dict.get(len(j),2)))

        # size_reduce_percent = min(1,590/(img.size[1]*0.3))
        # size_reduce_percent = min(1,590/(img.size[1]))

        # img = img.resize(tuple(int(i*size_reduce_percent) for i in img.size))

        img.save(Path('Images',alignment, 'Sites', i + '.png').absolute())



# combined_images('Hero')

# # It seems rfft2 on a 3 channel image returns a 2 channel result. PIL only supports 3 channel or 1 channel images. So either operate on a grey scale image:

# # i = i.convert('L')

# png = Image.open('Images/metw-back.png')
# jpg = Image.open('Images/metw-back.jpg')

# png.putalpha(0)

# j_hstack = np.hstack([jpg,jpg])
# p_hstack = np.hstack([png,png])


# h_images(['Images/metw-back.jpg','Images/metw-back.jpg'],2)
# ph = h_images(['Images/mtw-back.png','Images/metw-back.png','Images/metw-back.png','Images/metw-ack.png'],2)

# v_images(ph)
