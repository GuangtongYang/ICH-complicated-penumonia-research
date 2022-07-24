'''将出血区域相加'''
import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
leison_bad_names=os.listdir(r'')
leison_medium_names=os.listdir(r'')
leison_slight_names=os.listdir(r'')
lesion_none_names=os.listdir(r'')

label_output_path=r''

refer_image=sitk.ReadImage(os.path.join(label_output_path,leison_bad_names[0].split('.gz')[0]))
for i,file_name in enumerate(leison_bad_names):
    # if i==2:
    #     break
    file_name=file_name.split('.gz')[0]

    label_after_trans=sitk.ReadImage(os.path.join(label_output_path,file_name))
    label_after_trans_data=sitk.GetArrayFromImage(label_after_trans)
    label_after_trans_data[label_after_trans_data>0.5]=1
    label_after_trans_data[label_after_trans_data<0.5]=0

    if i==0:
        final_data=np.zeros(label_after_trans_data.shape)
  
    final_data+=label_after_trans_data
    #print(np.sum(label_after_trans_data))

#print(0.5*len(leison_medium_names))
final_data=final_data/len(leison_bad_names)
#final_data[final_data<0.5*len(leison_bad_names)]=0
final_image=sitk.GetImageFromArray(final_data)
final_image.SetOrigin(refer_image.GetOrigin())
final_image.SetDirection(refer_image.GetDirection())
sitk.WriteImage(final_image,'')



