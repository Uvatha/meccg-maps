from bokeh.models.annotations import Tooltip
import pandas as pd

from pathlib import Path

############################## File Paths ########################################

## File path for file with region names and x/y coordinates.
#LocList_FilePath = r"C:\Users\Me3\Desktop\MECCG\LocList.xlsx".replace("\\", "/")

## File path for map image.
MapImg_FilePath = Path(r"C:\Users\Me3\Desktop\MECCG\Images\Maps\DC Map Hartwig (regions).jpg")

## File path for test card image.
Card_ImgFilePath = Path(r"C:\Users\Me3\Desktop\MECCG\AttackLord.jpg")

##################################################################################

from PIL import Image

image = Image.open(MapImg_FilePath)
# image.show()


sites = pd.read_csv('LocList.csv')
sites['imgs'] = sites.Region.apply(lambda x: str(Path('Images','All',str(x)+'.jpg')))
sites['desc'] = 'Desc'
sites['fonts'] = '<i>italics</i>'

len(sites.Region)

# sites['imgs'] = 
# sites.Region.apply(lambda x: str(x) + '.jpg')

# sites.imgs

# sites['Region']

scaling_factor = 2

max_x = int(1253*scaling_factor)
max_y = int(1185*scaling_factor)


sites['x'] = sites['x']*scaling_factor
sites['y'] = sites['y']*scaling_factor

from bokeh.plotting import figure, output_file, show

# output to static HTML file
output_file("MECCG_Map.html")

#########
# Hover #
#########


TOOLTIPS = """
<html>
<head>
    <div>
        <div>
            <img
                style=";position: fixed;left:0;top:0;"
                src="@imgs"
                background-color: transparent
                border = "0"
            ></img>
        </div>
    </div>
</head>
</html>
"""


p = figure(plot_width=max_x, plot_height=max_y, tooltips=TOOLTIPS)

p.axis.visible = False
p.grid.visible = False
help(p.background)

# add a circle renderer with a size, color, and alpha
p.background_fill_alpha = 0.5

p.image_url(url=['DC Map Hartwig (regions).jpg'], x=0, y=0, w=max_x, h=max_y, anchor="bottom_left", alpha = 1)

p.circle('x','y', size=100, color="brown", alpha=0, source=sites)
# p.square(sites['x-1'],sites['y-1'], size=8, color="navy", alpha=1)

# show the results
show(p)

save(p)




# TOOLTIPS = """
#     <div>
#         <div>
#             <img
#                 src="@imgs" height="42" alt="@imgs" width="42"
#                 style="float: left; margin: 0px 15px 15px 0px;"
#                 border="2"
#             ></img>
#         </div>
#         <div>
#             <span style="font-size: 17px; font-weight: bold;">@desc</span>
#             <span style="font-size: 15px; color: #966;">[$index]</span>
#         </div>
#         <div>
#             <span>@fonts{safe}</span>
#         </div>
#         <div>
#             <span style="font-size: 15px;">Location</span>
#             <span style="font-size: 10px; color: #696;">($x, $y)</span>
#         </div>
#     </div>
# """






















# import plotly.graph_objects as go
# import plotly.express as px
# fig = px.scatter(Sites, x="x", y="y",hover_name="Region")#, hover_data=Sites["region"])
# #fig.show()

# fig.update_layout(
#      yaxis = dict(
#           scaleanchor = "x",
#           scaleratio = 1
#      ),
#      xaxis = dict(
#          #range=(0, Sites.y.max()),
#          #range=(0, 100),
#          constrain='domain'
#      )
# )

# fig.update_layout(
#     autosize=False,
#     width=1200,
#     height=1200,
#     margin=go.layout.Margin(
#         l=0,
#         r=0,
#         b=100,
#         t=30,
#         pad=0
#     )
# )

# # Add images
# fig.add_layout_image(
#         go.layout.Image(
#             source=Image.open(MapImg_FilePath),
#             xref="x",
#             yref="y",
#             x=0,
#             y=Sites.y.max(),
#             sizex=Sites.x.max(),
#             sizey=Sites.y.max(),
#             #sizing="stretch",
#             opacity=1,
#             layer="below")
# )

# # Set templates
# fig.update_layout(#template="plotly_white",
#                   xaxis_showgrid=False,
#                   yaxis_showgrid=False)

# fig.update_xaxes(showticklabels=False,
#                  showline=False,
#                  title=''
#                )

# fig.update_yaxes(showticklabels=False,
#                  showline=False,
#                  title=''
#                 )

# fig.update_xaxes(range=[0,Sites.x.max()])
# fig.update_yaxes(range=[0,Sites.y.max()])

# from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# # Copied from stack overflow
# ax = fig.add_subplot(111)

# xybox = (50., 50.)

# ab = AnnotationBbox(image, (0,0), xybox=xybox, xycoords='data',
#         boxcoords="offset points",  pad=0.3,  arrowprops=dict(arrowstyle="->"))

# line, = ax.plot(x,y, ls="", marker="o")

# ###############
# # Hover event #
# ###############
# def hover(event):
#     # if the mouse is over the scatter points
#     if line.contains(event)[0]:
#         # find out the index within the array from the event
#         ind, = line.contains(event)[1]["ind"]
#         # get the figure size
#         w,h = fig.get_size_inches()*fig.dpi
#         ws = (event.x > w/2.)*-1 + (event.x <= w/2.) 
#         hs = (event.y > h/2.)*-1 + (event.y <= h/2.)
#         # if event occurs in the top or right quadrant of the figure,
#         # change the annotation box position relative to mouse.
#         ab.xybox = (xybox[0]*ws, xybox[1]*hs)
#         # make annotation box visible
#         ab.set_visible(True)
#         # place it at the position of the hovered scatter point
#         ab.xy =(x[ind], y[ind])
#         # set the image corresponding to that point
#         image.set_data(arr[ind,:,:])
#     else:
#         #if the mouse is not over a scatter point
#         ab.set_visible(False)
#     fig.canvas.draw_idle()

# # add callback for mouse moves
# fig.canvas.mpl_connect('motion_notify_event', hover) 


























# ## Read test spoiler file
# spoiler = pd.read_csv(Spoiler_FilePath, "\t").dropna(subset=["Name"])

# # Need Dataframe with region/imagefile.
# # To get image file we need a list of regions.  List of regions will be used to obtain list of image files to be concatenated.

# # With spoiler df add column that is a list of regions.
# # With df column, split into cardimage/region pairs

# """
# Site after "playable at"

# Sites in region types

# """

# ## Playable at specific site
# # Find the word after "playable at," check it against a list of sites, find the site's region.  Want to return a dataframe of cardname/region.
# # spoiler['test']=spoiler.Text.split("playable at",1)[1]
# # spoiler['test']=spoiler.apply(lambda x: x['Text'].split("playable at",1)),axis=1)



# # print(find_all(strtest.lower(),'playable'))
# # for i in find_all(strtest.lower(),'playable'):
# #     print(strtest[i+12:i+20])

# strtest = "this card is playable at Moria.  Also playable at Lorien.  Also addtional text. Playable at hufflepuff"

# SiteTypes = [
#     "Hero Site",
#     "Minion Site",
#     "Hero Minion Site",
#     "Dwarf-lord Site",
#     "Elf-lord Site",
#     "Atani-lord Site",
#     "Fallen-wizard Site",
# ]

# sitelist = list(spoiler[spoiler.Type.isin(SiteTypes)].Name.unique())

# # for i in sitelist:
# #     print(i.find('M'))

# # values1)) & (df_a['car'].isin(values2)))]

# sitelist = pd.DataFrame(
#     spoiler[
#         ~(spoiler.Name.str.contains("\(*\)", regex=True))
#         & (spoiler.Type.isin(SiteTypes))
#     ].Name.unique(),
#     columns=["Name"]
# )

# #########################################################
# # Find index for matches with Name in card text from sitelist.  Check if "playable at" comes before in card text.  Return card name if it does.

# #Step 1, find index for a site name match.

# #retrieves rows from spoiler df where Moria is in text.
# spoiler[spoiler.Text.fillna('').str.contains('Moria')]

# # Function that finds the index of all instances of substring within a string and returns them in a list.
# def find_all(string, substring):
#     """
#     Function: Returning all the index of substring in a string. Not case sensitive.
#     Arguments: String and the search string
#     Return:Returning a list
#     """
#     length = len(substring)
#     c = 0
#     indexes = []
#     while c < len(string):
#         if string[c : c + length].lower() == substring.lower() and c != '':
#             indexes.append(c)
#         c = c + 1
#     return indexes 


# #all resources
# #print(spoiler[spoiler.Type.fillna('').str.contains('resource',case=False)].Text)

# ################################################################################################################

# index_list=[]

# # 
# for i,text in enumerate(spoiler[spoiler.Type.str.contains('|'.join(['Resource','character','item']),case=False,na=False )].Text):
#     if find_all(str(i),'Moria') != []:
#         index_list.append(find_all(str(i),'Moria')+[i])
#         #index_list.insert(i,'extend')
                
# index_list

# len(index_list)

# help(index_list.append)

# #################################################################################################################
# # Unique words after "playable at"


# print(Source)
# #################################################################################################################


# def find_index_list(column,substrings: list) -> list:
#     """
#     Looks through column and returns a list with rownum,substring,and index within text.
#     """
#     index_list=[]
#     for i in substrings:
#         for j in enumerate(column):
#             if find_all(str(j),i) != []:
#                 index_list.append([j[0],i,find_all(str(j),i)])
#     return index_list


# len(find_index_list(spoiler.Text,['playable at']))

# #####################################################################################################
# # Find distributions of substrings after "playable at"

# post_playable_at = []

# for i in spoiler[spoiler.Type.fillna('').str.contains('([R,r]esource)|([C,c]haracter)|([I,i]tem)')].Text.fillna(''):
#     for j in re.finditer(f'(?<=[P,p]layable at\W)\w+\'?\w*[\s,-,\']?\w*[\s,-,\']?\w*',i):
#         post_playable_at.append(j.group())

# len(post_playable_at)
# print(post_playable_at)


# pcounts=pd.DataFrame(post_playable_at,columns=['Text']).Text.value_counts()

# spoiler[spoiler.Text.fillna('').str.contains('[P,p]layable at sites in Gondor')].to_clipboard()

# #####################################################################################################

# #
# def find_index_list(column,substrings):
#     index_list=[]
#     for i in substrings:
#         for j in enumerate(column):
#             if find_all(str(j),i) != []:
#                 index_list.append([j[0],i,find_all(str(j),i)])
#     return index_list

# # add filters for spoiler.Text vvvvvv
# # find_index_list(spoiler.Text,sitelist.Name)





# ########################################################################################################
# ## Open Image
# from PIL import Image

# image = Image.open(Background_ImgFilePath)
# image.show()
# ########################################################################################################


# """
# General Needs

#  Output needed: CardName | Playable in a list of regions.

#  We can identify regions by:
#    Site Name, Region Type, Site Type, Site Type in Region Type


#  """
 

    
    
# spoiler[spoiler.Type.fillna('').str.contains('([I,i]tem)|([C,c]haracter)|([R,r]esource)')]

# #########################################################################################################################
