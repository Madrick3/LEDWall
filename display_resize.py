#%%
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
import numpy as np

#Resize the Image
filename=input('Enter file name: ')
img1 = Image.open(filename)

#Show Image Side by Side
columns = 2
rows = 1
fig=plt.figure(figsize=(10,10))
fig.add_subplot(1, 2, 1)
plt.imshow(img1)
plt.show()

img1.thumbnail((300,400), Image.ANTIALIAS)
fig.add_subplot(1, 2, 2)
plt.imshow(img1)
plt.show()

# %%
