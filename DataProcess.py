from cProfile import label
import random
from re import X 
from tkinter import Label
import SimpleITK as sitk
import numpy as np
from skimage.transform import resize

'''根据脑出血分割区域在原图中去掉分割区域'''
'''以便更好地配准'''

image=sitk.ReadImage(r'D:\BaiduNetdiskDownload\DongyingData\CtImage_resize_norm_unbone\001_cheng_xiaoxiang.nii')
imageData=sitk.GetArrayFromImage(image)
imageData.shape


Label=sitk.ReadImage(r"D:\BaiduNetdiskDownload\DongyingData\Label_resize\001_cheng_xiaoxiang.nii.gz")
LabelData=sitk.GetArrayFromImage(Label)
LabelData=np.array(LabelData)
z=np.any(LabelData,axis=(1,2))
start_slice, end_slice = np.where(z)[0][[0, -1]]



'''划定一个区域，将里面的值提出来作为出血区域的补充'''
for index in range(start_slice,end_slice+1):
    label_x,label_y=np.where(LabelData[index,:,:])
    for i in range(20):    
        x_randomPixel=random.randint(100,200)
        y_randomPixel=random.randint(100,200)
        SupplyAreaData=imageData[index,x_randomPixel:\
                                x_randomPixel+50,\
                                y_randomPixel:y_randomPixel+50]
        if np.var(SupplyAreaData)>1:
            supplyData=np.array([0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.32,0.34,0.36])
            continue
        elif x_randomPixel+50 in label_x or  y_randomPixel+50 in label_y:
            supplyData=np.array([0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.32,0.34,0.36])
            continue
        elif np.sum(SupplyAreaData)==0:
            supplyData=np.array([0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.32,0.34,0.36])
            continue
        else:
            print(np.var(SupplyAreaData))
            supplyData=np.array([0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.32,0.34,0.36])
            break       
    for x_index in range(0,label_x.shape[0]):
        imageData[index,label_x[x_index],label_y[x_index]]=supplyData[random.randint(0,\
                                                        supplyData.shape[0]-1)]
        #imageData[index,x[:],y[:]]=  supplyData[random.randint(0,supplyData.shape[0]-1)]

#ct图像resize
MrImages=sitk.ReadImage("./moving/aligned_norm.nii.gz")
MrIamgeData=sitk.GetArrayFromImage(MrImages)
ctImageData = resize(imageData, MrIamgeData.shape,\
     order=3, mode='symmetric', preserve_range=True)
ctImages=sitk.GetImageFromArray(ctImageData)
LabelData = resize(LabelData, MrIamgeData.shape,\
     order=3, mode='symmetric', preserve_range=True)
label=sitk.GetImageFromArray(LabelData)
#sitk.WriteImage(label,'./label/001_cheng_xiaoxiang_norm.nii')
sitk.WriteImage(ctImages,'./fixed/001_cheng_xiaoxiang_process.nii')



