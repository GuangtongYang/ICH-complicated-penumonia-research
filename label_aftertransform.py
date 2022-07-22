'''对变化后得label寻找分区 主要改变阈值 '''

import SimpleITK as sitk
import numpy as np
import os

path=r'D:\BaiduNetdiskDownload\DongyingData\labeloutput'
names = os.listdir(path)

standard=sitk.ReadImage('./moving/aligned_seg35.nii.gz')
standardData=sitk.GetArrayFromImage(standard)

for i,name in enumerate(names):
    # if i==1:
    #     break
    labelImage_after=sitk.ReadImage(os.path.join(path,name))
    labelData_after=sitk.GetArrayFromImage(labelImage_after)
    #print(labelData.shape)

    lalel_aera=np.where(labelData_after>0.6)


    lesion_aera=set()
    print(type(lesion_aera))
    for index_z,index_y,index_x in zip(lalel_aera[0],lalel_aera[1],lalel_aera[2]):
        #print(standardData[index_z][index_y][index_x])
        lesion_aera.add(standardData[index_z][index_y][index_x])

    print(lesion_aera)


    analysis_file=open(r'D:\pythonScripts\nonRigidRegistration\output\analysis_0.6.txt','a')
    analysis_file.write(name+':'+str(lesion_aera)+'\n')
    analysis_file.close()
