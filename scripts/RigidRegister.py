#%%
from unicodedata import name
import SimpleITK as sitk
import numpy as np
from sklearn.utils import resample
from skimage.transform import resize
import os

path=r''
output_path=r''
labeloutput_path=r''
label_path=r''
MrImages=sitk.ReadImage("")
standard=sitk.ReadImage('')
standardData=sitk.GetArrayFromImage(standard)
MrIamgeData=sitk.GetArrayFromImage(MrImages)
names=os.listdir(path)

p1=sitk.GetDefaultParameterMap('translation')   
p1['WriteResultImage']=['false']
p2=sitk.GetDefaultParameterMap('affine')   
p2['WriteResultImage']=['false']
p3=sitk.GetDefaultParameterMap('bspline')
p3['WriteResultImage']=['false']

for i,ctname in enumerate(names):
    if i==1:
        break
    # if i==240: 
    #     break
    ctImages=sitk.ReadImage(os.path.join(path,ctname))

    labelImage=sitk.ReadImage(os.path.join(label_path,ctname))
    labelData=sitk.GetArrayFromImage(labelImage)

    ctImageData=sitk.GetArrayFromImage(ctImages)


    #%%
    #先进行刚性配准  对齐

    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(MrImages)
    elastixImageFilter.SetMovingImage(ctImages)

    elastixImageFilter.SetParameterMap(p1)
    elastixImageFilter.AddParameterMap(p2)
    elastixImageFilter.AddParameterMap(p3)
    
    elastixImageFilter.Execute()
    elastixImageFilter.PrintParameterMap()

    resultImage = elastixImageFilter.GetResultImage()
    transformParameterMap = elastixImageFilter.GetTransformParameterMap()

    result=sitk.GetArrayFromImage(resultImage)
    #sitk.WriteImage(resultImage,os.path.join(output_path,ctname))

    print(result.shape)

    # %%
    labelTransformer=sitk.TransformixImageFilter()
    labelTransformer.SetTransformParameterMap(transformParameterMap)
    print(transformParameterMap)
    labelTransformer.SetMovingImage(labelImage)
    labelTransformer.LogToConsoleOn()
    labelTransformer.Execute()
    labelImage_after=labelTransformer.GetResultImage()
    #sitk.WriteImage(labelImage_after,os.path.join(labeloutput_path,ctname))
    # %%
    labelData_after=sitk.GetArrayFromImage(labelImage_after)
    print(labelData.shape)

    lalel_aera=np.where(labelData_after>0.5)


    lesion_aera=set()
    print(type(lesion_aera))
    for index_z,index_y,index_x in zip(lalel_aera[0],lalel_aera[1],lalel_aera[2]):
        #print(standardData[index_z][index_y][index_x])
        lesion_aera.add(standardData[index_z][index_y][index_x])

    print(lesion_aera)

    
    #analysis_file=open(r'D:\pythonScripts\nonRigidRegistration\output\analysis.txt','a')
    #analysis_file.write(ctname+':'+str(lesion_aera)+'\n')
    #analysis_file.close()
    print(str(i)+' done')
    

print('done')
# %%
