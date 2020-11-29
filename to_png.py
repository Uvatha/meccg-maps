import os
from PIL import Image
from pathlib import Path


for set in os.listdir('Images/Sets'):
    for img in os.listdir(Path('Images/Sets',set)):
        jpg = Image.open(Path('Images/Sets',set,img))
        jpg.save(Path('Images/Sets',set,img[0:-4] + '.png'))


img = Image.open(Path('Images','metw-back.jpg'))

img.save(Path('Images','metw-back.png'))