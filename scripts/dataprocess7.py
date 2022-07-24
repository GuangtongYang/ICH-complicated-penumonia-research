'''以出血量为x轴，肺炎分型为y轴画图'''
from matplotlib import markers
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


data_path=r''
data=pd.read_csv(data_path,header=None,sep=' ',names=['F/B','L/B','L/F','L/All','F/All','fluid','brain','lesion','0',\
    '1','2','3','4','5','6',\
    '7','8','9','10','11',\
    '12','13','14','15','16',\
        '17','18','19','20','21','22','23','24',\
        '25','26','27','28','29','30','31',\
            '32','33','34','35','label'])
bad_data=data.copy()
medium_data=data.copy()
slight_data=data.copy()
none_data=data.copy()

# my_data=data.sort_values('lesion')
# my_data.head()

for i, label in enumerate(bad_data['label']):
    if label!=3:
        bad_data=bad_data.drop(index=i,axis=0)
bad_data.describe()

for i, label in enumerate(medium_data['label']):
    if label!=2:
        medium_data=medium_data.drop(index=i,axis=0)
medium_data.describe()

for i, label in enumerate(slight_data['label']):
    if label!=1:
        slight_data=slight_data.drop(index=i,axis=0)
slight_data.describe()

for i, label in enumerate(none_data['label']):
    if label!=0:
        none_data=none_data.drop(index=i,axis=0)
none_data.describe()





fig=plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set( title='Statistical model of bleeding volume',
         ylabel='Brain hemorrhage/tissue')
# ax.scatter(bad_data['F/B'],bad_data['label'],color='red',marker='+',label='severe')
# ax.scatter(medium_data['F/B'],medium_data['label'],color='green',marker='v',label='medium')
# ax.scatter(slight_data['F/B'],slight_data['label'],color='blue',marker='*',label='mild')
# ax.scatter(none_data['F/B'],none_data['label'],color='black',marker='.',label='none')
# ax.legend(loc='lower right')
# ax.boxplot([bad_data['L/All'],medium_data['L/All'],slight_data['L/All'],none_data['L/All']],\
#     labels=['severe','medium','slight','none'],\
#         showmeans=True,patch_artist = True,\
#             boxprops={'color':'blue','facecolor':'white'})
sns.heatmap()

plt.show()



