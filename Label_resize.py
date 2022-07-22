from operator import index
import os

import numpy as np
import SimpleITK as sitk
from skimage.transform import resize

path=r'D:\BaiduNetdiskDownload\DongyingData\DongyingBrain_SegLabel'
MrImages=sitk.ReadImage("D:/pythonScripts/nonRigidRegistration/moving/aligned_norm.nii.gz")
MrIamgeData=sitk.GetArrayFromImage(MrImages)
names=os.listdir(path)

for index, name in enumerate(names):

    file_path=os.path.join(path,name)
    image=sitk.ReadImage(file_path)
    imageData=sitk.GetArrayFromImage(image)

    #ct图像resize
    labelImageData = resize(imageData, MrIamgeData.shape,\
        order=3, mode='symmetric', preserve_range=True)
    labelImageData[labelImageData>0.1]=1
    ctImages=sitk.GetImageFromArray(labelImageData)

    sitk.WriteImage(ctImages,os.path.join('D:\\BaiduNetdiskDownload\\DongyingData\\Label_resize',name))

    print("done")
    print(index)
