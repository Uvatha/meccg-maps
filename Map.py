import pandas as pd
import re
from pathlib import Path

def map_html(Alignment):

    #TODO Figure out how to change plot tab title
    # Iron Hills != Dorwinion
    # Dorwinion != Taur Romen
    # Dune Sea != Moria
    

    host_url = 'https://meccg-images.s3.amazonaws.com/'


    sites = pd.read_csv('LocList.csv')

    #! Online Version
    sites['imgs'] = sites.Region.apply(lambda x: host_url + Alignment +'/' + str(x)+'.png')
    sites['imgs'] = sites['imgs'].str.replace(' ','+')
    
    sites['site_imgs'] = sites.Region.apply(lambda x: host_url + Alignment +'/Sites/' + str(x)+'.png')
    sites['site_imgs'] = sites['site_imgs'].str.replace(' ','+')
    
    # # #! Local Version
    # sites['imgs'] = sites.Region.apply(lambda x: 'Images/' + Alignment +'/' + str(x)+'.png')
    # sites['site_imgs'] = sites.Region.apply(lambda x: 'Images/' + Alignment +'/Sites/' + str(x)+'.png')
    

    sites['desc'] = 'Desc'
    sites['fonts'] = '<i>italics</i>'


    scaling_factor = 1.5

    max_x = int(1253*scaling_factor)
    max_y = int(1185*scaling_factor)


    sites['x'] = sites['x']*scaling_factor
    sites['y'] = sites['y']*scaling_factor

    from bokeh.plotting import figure, output_file, show

    # output HTML file
    output_file(Alignment+"_Map.html")

    #########
    # Hover #
    #########


    TOOLTIPS = """
    <html>
    <head>
    <style>
    img {}
    </style>
        <div>
            <div>
                <img
                    style="position: fixed;
                        left:0;
                        top:0;
                        max-width:50%;
                        max-height:100%"
                    src="@imgs"
                    background-color: transparent
                    border = "0"
                ></img>
                <img
                    style="position: fixed;
                        right:0;
                        top:0;
                        max-height:100%"
                    src="@site_imgs"
                    background-color: transparent
                    border = "0"
                ></img>
                <p> @Region </p>
            </div>
        </div>
    </head>
    </html>
    """

    p = figure(plot_width=max_x, plot_height=max_y, tooltips=TOOLTIPS)

    p.axis.visible = False
    p.grid.visible = False

    # add a circle renderer with a size, color, and alpha
    p.background_fill_alpha = 0.5

    p.image_url(url=[host_url + 'DC+Map+Hartwig+(regions).jpg'], x=0, y=0, w=max_x, h=max_y, anchor="bottom_left", alpha = 1)

    p.circle('x','y', size=37, color="brown", alpha=0, source=sites)

    # show the results
    show(p)

    #####################
    # Adjust plot title #
    #####################
    with open(Path(Alignment+"_Map.html"), 'r+',encoding = 'UTF-8') as f:
        text = f.read()
        text = re.sub('<title>Bokeh Plot</title>', f'<title>{Alignment} Map</title>', text)
        f.seek(0)
        f.write(text)
        f.truncate()