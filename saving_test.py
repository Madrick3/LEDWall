#%%
from matplotlib.backends.backend_pdf import PdfPages
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
fig, ax1 = plt.subplots()
#Data represent one panel, random color
data1 = np.random.rand(10, 10)*100
ax1.imshow(data1, cmap=cmap, norm=norm)
# draw gridlines
ax1.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax1.set_xticks(np.arange(0, 10, 1));
ax1.set_yticks(np.arange(0, 10, 1));
ax1.set_title("First Grid: ")
second=plt.show()

# create discrete colormap #2
#Data represent one panel, random color
data2 = np.random.rand(10, 10)*100
fig, ax2 = plt.subplots()
ax2.imshow(data2, cmap=cmap, norm=norm)
# draw gridlines
ax2.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax2.set_xticks(np.arange(0, 10, 1));
ax2.set_yticks(np.arange(0, 10, 1));
ax2.set_title("Second Grid: ")
first=plt.show()

#Create Overlapping Grid of two grids
#CombineData
data3=data2+data1
fig, ax3 = plt.subplots()
ax3.imshow(data3, cmap=cmap, norm=norm)
# draw gridlines
ax3.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax3.set_xticks(np.arange(0, 10, 1));
ax3.set_yticks(np.arange(0, 10, 1));
ax3.set_title("Compare Grid: ")
plt.savefig('grid.png', bbox_inches="tight")
ax3.imshow(data3, cmap=cmap, norm=norm)
compare=plt.show()



# %%
