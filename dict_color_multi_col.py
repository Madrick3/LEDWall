#%%
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import array as arr

#Array of data
dict_data={}
dict_data["data1"]=[0,1,0,0,1,0,0,1,1,0,0]
dict_data["data2"]=[0,0,0,0,1,1,0,1,0,0,1]
dict_data["data3"]=[1,1,1,1,1,1,1,1,1,1]
dict_data["data4"]=[0,0,0,0,0,0,0,0,0,0]
dict_data["data5"]=[1,0,1,0,1,0,1,0,1,0]
dict_data["data6"]=[0,1,0,0,1,0,0,1,1,0,0]
dict_data["data7"]=[0,0,0,0,1,1,0,1,0,0,1]
dict_data["data8"]=[1,1,1,1,1,1,1,1,1,1]
dict_data["data9"]=[0,0,0,0,0,0,0,0,0,0]
dict_data["data10"]=[1,0,1,0,1,0,1,0,1,0]

#Assign colors to array based on data provided
dict_colors={}
dict_colors["colors1"]=[]
dict_colors["colors2"]=[]
dict_colors["colors3"]=[]
dict_colors["colors4"]=[]
dict_colors["colors5"]=[]
dict_colors["colors6"]=[]
dict_colors["colors7"]=[]
dict_colors["colors8"]=[]
dict_colors["colors9"]=[]
dict_colors["colors10"]=[]

j=1
x=1

while j<=(10):
    x=0
    color_def=[]
    data=dict_data[("data"+str(j))]
    while x<10:
        if data[x]==0:
            color_def.append('w')
        if data[x]==1:
            color_def.append('k')
        x=x+1
        colors_org.append(colors)
    dict_colors[("colors"+str(j))]=color_def
    j=j+1

h=1
colorlog=[]
while h<=(10):
    data=dict_colors[("colors"+str(h))]
    colorlog.append(data)
    h=h+1

#Display colors
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')
info = ax.table(cellColours=colorlog, loc='centered')
plt.savefig('data_grid.png', bbox_inches="tight")
plt.show()

# %%
