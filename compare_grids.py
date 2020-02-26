#%%
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#Data represent one panel, random color
data1 = np.random.rand(10, 10)*100
# create discrete colormap
cmap = colors.ListedColormap(['white', 'black'])
bounds = [0,10,20]
norm = colors.BoundaryNorm(bounds, cmap.N)


# create discrete colormap grid #1
fig, ax = plt.subplots()
#Data represent one panel, random color
data1 = np.random.rand(10, 10)*100
ax.imshow(data1, cmap=cmap, norm=norm)
# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(0, 10, 1));
ax.set_yticks(np.arange(0, 10, 1));
ax.set_title("First Grid: ")
second=plt.show()

# create discrete colormap #2
#Data represent one panel, random color
data2 = np.random.rand(10, 10)*100
fig, ax = plt.subplots()
ax.imshow(data2, cmap=cmap, norm=norm)
# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(0, 10, 1));
ax.set_yticks(np.arange(0, 10, 1));
ax.set_title("Second Grid: ")
first=plt.show()

#Create Overlapping Grid of two grids
#CombineData
data3=data2+data1
fig, ax = plt.subplots()
ax.imshow(data3, cmap=cmap, norm=norm)
# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(0, 10, 1));
ax.set_yticks(np.arange(0, 10, 1));
ax.set_title("Compare Grid: ")
plt.show()


# %%
