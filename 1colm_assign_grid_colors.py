#%%
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import array as arr

#Array of data
data=arr.array('f',[0,1,0,0,1,0,0,1,1,0,0])

#Assign colors to array based on data provided
colors=[]
j=1
while j<(10):
    if data[j]==0:
        colors.append('w')
    if data[j]==1:
        colors.append('k')
    j=j+1



#Display colors
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')
table = ax.table(cellColours=colors,loc='center')



plt.show()

# %%

