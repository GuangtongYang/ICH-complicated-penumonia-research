'''画热力图'''
from cv2 import setIdentity
from matplotlib import markers
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import SimpleITK as sitk


mr_image=sitk.ReadImage('')
mr_data=sitk.GetArrayFromImage(mr_image)

bad_sum_image=sitk.ReadImage('')
bad_sum_data=sitk.GetArrayFromImage(bad_sum_image)
print(bad_sum_data.shape)
my_data=bad_sum_data+mr_data

fig=plt.figure()
ax = fig.add_subplot(1,1,1)

#ax.set( title='Statistical model of bleeding volume')
#sns.set(font_scale=1.5)

#sns.pointplot(my_data[:,80,:])
sns.heatmap(data=bad_sum_data[:,80,:],cmap='RdBu_r',\
    xticklabels=False,yticklabels=False)

plt.rc('font',family='Times New Roman',size=12)
plt.plot()











