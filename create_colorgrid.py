#%%
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#Data represent one panel, random color
data = np.random.rand(10, 10)*100

# create discrete colormap
cmap = colors.ListedColormap(['white', 'black'])
bounds = [0,10,20]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(0, 10, 1));
ax.set_yticks(np.arange(0, 10, 1));

plt.show()

# %%
