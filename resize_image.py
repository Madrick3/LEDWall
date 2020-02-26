#%%
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
import numpy as np

#Resize the Image
filename=input('Enter file name: ')
img = Image.open(filename)
img.thumbnail((400,300), Image.ANTIALIAS)
img.show()

# %%
