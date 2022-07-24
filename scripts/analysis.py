from optparse import Values
import os
import SimpleITK as sitk
from cv2 import setIdentity
import numpy as np
import re

image=sitk.ReadImage('')
imagedata=sitk.GetArrayFromImage(image)
labeloutput_path=r''
names=os.listdir(labeloutput_path)

#读包含哪些分区的文件
file = open('./output/analysis.txt','r')
lesion_aera_list=file.readlines()
file.close()

#建立一个字典存储标准分区各区域所占的像素点数
standard_dict={}
for i in range(0,36):
    aera_count=np.where(imagedata==i)
    standard_dict.setdefault(i,aera_count[0].shape[0])
print(standard_dict)
#values=standard_dict.values()
#print(sum(values)==imagedata.shape[0]*imagedata.shape[1]*imagedata.shape[2])

for index_outputlabel,name in enumerate(names):
    if index_outputlabel<240:
        continue
    # if index_outputlabel==240:
    #     break
    
    #读取变换后的label
    label_afterTransform=sitk.ReadImage(os.path.join(labeloutput_path,name))
    label_after_data=sitk.GetArrayFromImage(label_afterTransform)
    label_loc=np.where(label_after_data>0.5)#元组  zyx

    #读取这个label所占的脑区
    lesion_aera=lesion_aera_list[index_outputlabel]
    lesion=re.search(r'{.+}',lesion_aera).group()
    lesion=lesion[1:len(lesion)-1]
    print(lesion)
    lesion_list=lesion.split(',')

        
    #建议一个字典存储百分比
    my_lesion_percent_dict={}
    for aera in lesion_list:
         my_lesion_percent_dict.setdefault(int(aera),0)
    for index_z,index_y,index_x in zip(label_loc[0],label_loc[1],label_loc[2]):
        for aera in lesion_list:
            aera=aera.lstrip()
            if imagedata[index_z][index_y][index_x] == int(aera):
                my_lesion_percent_dict[int(aera)]+=1
    my_keys=my_lesion_percent_dict.keys()
    print(my_keys)

    for key in my_keys:
        my_lesion_percent_dict[key]=my_lesion_percent_dict[key]/standard_dict[key]
    print(my_lesion_percent_dict)
    file_output=open('./output/analysis_percent.txt','a')
    file_output.write(name+str(my_lesion_percent_dict)+'\n')
    file_output.close()
    my_lesion_percent_dict.clear()




    
    
        






