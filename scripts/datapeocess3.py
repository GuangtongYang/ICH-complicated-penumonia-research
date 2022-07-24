'''计算出血的量 脑脊液的量 脑实质的量'''

import SimpleITK as sitk
import numpy as np
import os
import re

file_path=r''
file_names=os.listdir(file_path)

referenece_file=open(r'','r')
referenece_names=referenece_file.readlines()
referenece_file.close()

fw=open(r'','r')
patient_data_lists=fw.readlines()
fw.close()

lesion_file_path=r''


output_file=open('','a')

'''1 {28: 0.08317898636134029, 20: 0.0001528022697331742}'''
for i,reference in enumerate(referenece_names):
    # if i==1:
    #     break
    reference=re.search(r' .+.nii',reference).group()[1:]
    print(reference)

    image=sitk.ReadImage(os.path.join(file_path,reference))

    fluid_data=sitk.GetArrayFromImage(image)
    brain_data=sitk.GetArrayFromImage(image)

    #脑脊液 fluid
    fluid_data[fluid_data<3]=0
    fluid_data[fluid_data>8]=0
    fluid_index=np.where(fluid_data)
    fluid_number=fluid_index[0].shape[0]

    #脑实质 brain
    brain_data[brain_data<25]=0
    brain_data[brain_data>44]=0
    brain_index=np.where(brain_data)
    brain_number=brain_index[0].shape[0]


    #出血的量
    lesion_iamge=sitk.ReadImage(os.path.join(lesion_file_path,reference+'.gz'))
    lesion_data=sitk.GetArrayFromImage(lesion_iamge)
    lesion_index=np.where(lesion_data)
    lesion_num=lesion_index[0].shape[0]

    '''fluid  brain  lesion_num  aera_percent label'''
    output_file.write(str(fluid_number/brain_number)+' '+str(lesion_num/brain_number)+' '+\
        str(lesion_num/fluid_number)+' '+
        str(lesion_num/(brain_number+fluid_number))+' '+\
            str(fluid_number/(brain_number+fluid_number))+' '+\
                str(fluid_number)+' '+str(brain_number)+' '\
            +str(lesion_num)+' '+patient_data_lists[i])
output_file.close()


