from operator import index
import os

import numpy as np
import SimpleITK as sitk
from skimage.transform import resize

path=r''
MrImages=sitk.ReadImage("")
MrIamgeData=sitk.GetArrayFromImage(MrImages)
names=os.listdir(path)

for index, name in enumerate(names):

    file_path=os.path.join(path,name)
    ctimage=sitk.ReadImage(file_path)
    imageData=sitk.GetArrayFromImage(ctimage)

    #归一化
    imageData[imageData>106]=0
    imageData[imageData<0]=0
    imageData=(imageData-np.min(imageData))/(np.max(imageData)-np.min(imageData))

    #ct图像resize
    ctImageData = resize(imageData, MrIamgeData.shape,\
        order=3, mode='symmetric', preserve_range=True)
    ctImages=sitk.GetImageFromArray(ctImageData)

    sitk.WriteImage(ctImages,os.path.join('',name))

    print("done")
    print(index)




