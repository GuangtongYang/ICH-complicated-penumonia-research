'''根据概率图得出脑区'''

import SimpleITK as sitk
import pandas as pd
import numpy as np


bad_sum_image=sitk.ReadImage('')
bad_sum_data=sitk.GetArrayFromImage(bad_sum_image)

medium_sum_image=sitk.ReadImage('')
medium_sum_data=sitk.GetArrayFromImage(medium_sum_image)

slight_sum_image=sitk.ReadImage('')
slight_sum_data=sitk.GetArrayFromImage(slight_sum_image)

none_sum_image=sitk.ReadImage('')
none_sum_data=sitk.GetArrayFromImage(none_sum_image)

mr_35_image=sitk.ReadImage('')
mr_35_data=sitk.GetArrayFromImage(mr_35_image)

bad_output_dict={}
for i in range(1,36):
    bad_output_dict.setdefault(i,0.0)

# for key_grey in bad_output_dict.keys():
#     aera=np.where(mr_35_data==key_grey)
#     count=0
#     #print(aera[0].shape)
#     aera_sum=aera[0].shape[0]
#     for index_z,index_y,index_x in zip(aera[0],aera[1],aera[2]):
#         #print(standardData[index_z][index_y][index_x])
#         num=bad_sum_data[index_z][index_y][index_x]
#         if num!=0:
#             bad_output_dict[key_grey]+=(bad_sum_data[index_z][index_y][index_x])
#             count+=1
#     bad_output_dict[key_grey]/=count

# print(sorted(bad_output_dict.items(),key=lambda x:x[1],reverse=True))

my_aera=np.where(none_sum_data>0.3)
for index_z,index_y,index_x in zip(my_aera[0],my_aera[1],my_aera[2]):
    num=mr_35_data[index_z][index_y][index_x]
    for grey in range(1,35):
        if num==grey:
            bad_output_dict[grey]+=1
print(sorted(bad_output_dict.items(),key=lambda x:x[1],reverse=True))






















