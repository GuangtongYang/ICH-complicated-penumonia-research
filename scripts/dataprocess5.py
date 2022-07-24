'''将出血量相似的放到一块 生成表格'''
import numpy as np
import pandas as pd
from requests import head

data_path=r''
data=pd.read_csv(data_path,header=None,sep=' ',names=['F/B','L/B','L/F','L/All','F/All','fluid','brain','lesion','0',\
    '1','2','3','4','5','6',\
    '7','8','9','10','11',\
    '12','13','14','15','16',\
        '17','18','19','20','21','22','23','24',\
        '25','26','27','28','29','30','31',\
            '32','33','34','35','label'])

data.head()

my_data=data.sort_values('lesion')
my_data.head()

my_data.to_csv('',index=True,header=True)

