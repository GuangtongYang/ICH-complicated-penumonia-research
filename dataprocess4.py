import re

import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
from matplotlib.pyplot import bar, bar_label
from nbformat import write

''' 分析轻中重型肺炎脑区分布'''

bad_lesion_aera_dict={}
medium_lesion_aera_dict={}
slight_lesion_aera_dict={}
none_lesion_aera_dict={}
for i in range(0,36):
    bad_lesion_aera_dict.setdefault(str(i),0)
    medium_lesion_aera_dict.setdefault(str(i),0)
    slight_lesion_aera_dict.setdefault(str(i),0)
    none_lesion_aera_dict.setdefault(str(i),0)
'''0 011_hou_wanming.nii{26: 0.026107784431137725, 20: 0.002271385090628265, 29: 0.0010314595152140279}'''

file=open('./output/LesionAera_lung.txt','r')
patient_data_list=file.readlines()
file.close()



for i,patient_data in enumerate(patient_data_list):
    # if i==1:
    #     break
    label=patient_data.split(' ')[0]
    if label == '3':
        #重度
        lesion_aera_list=re.findall(r'\d*:',patient_data)
        for leison_aera in lesion_aera_list:
            leison_aera=leison_aera.split(':')[0]
            bad_lesion_aera_dict[leison_aera]+=1

    if label == '2':
        #中度
        lesion_aera_list=re.findall(r'\d*:',patient_data)
        for leison_aera in lesion_aera_list:
            leison_aera=leison_aera.split(':')[0]
            medium_lesion_aera_dict[leison_aera]+=1

    if label == '1':
        #轻度
        lesion_aera_list=re.findall(r'\d*:',patient_data)
        for leison_aera in lesion_aera_list:
            leison_aera=leison_aera.split(':')[0]
            slight_lesion_aera_dict[leison_aera]+=1

    if label == '0':
        #无
        lesion_aera_list=re.findall(r'\d*:',patient_data)
        for leison_aera in lesion_aera_list:
            leison_aera=leison_aera.split(':')[0]
            none_lesion_aera_dict[leison_aera]+=1
#print(bad_lesion_aera_dict)

label_list=[]
bad_list=[]
medium_list=[]
slight_list=[]
none_list=[]
for i in range(1,36):
    label_list.append(str(i))
    bad_list.append(bad_lesion_aera_dict[str(i)]/19)
    medium_list.append(medium_lesion_aera_dict[str(i)]/47)
    slight_list.append(slight_lesion_aera_dict[str(i)]/77)
    none_list.append(none_lesion_aera_dict[str(i)]/101)


#print(bad_list)
fig=plt.figure()


rects_bad=plt.bar(x=range(27,35),height=bad_list[27:35],width=0.2,\
            alpha=0.8,color='red',label='severe')
rects_mediium=plt.bar(x=[i +0.2 for i in range(27,35)],height=medium_list[27:35],width=0.2,\
            alpha=0.8,color='blue',label='medium')
rects_slight=plt.bar(x=[i +0.4 for i in range(27,35)],height=slight_list[27:35],width=0.2,\
            alpha=0.8,color='green',label='slight')
rects_none=plt.bar(x=[i+0.6 for i in range(27,35)],height=none_list[27:35],width=0.2,\
            alpha=0.8,color='grey',label='none')                   
plt.ylim(0,1.2)
plt.ylabel('Proportion ')

plt.xticks([i+0.4  for i in range(27,35)],label_list[27:35])
#plt.xlabel('Brain anatomy partitioning')
#plt.title('lesion aera statistical data')

plt.legend(loc='upper right')

# for rect in rects_mediium:
#    height = rect.get_height()
#    plt.text(rect.get_x() + rect.get_width() / 2, height+0.02, '%.2f'%height, ha="center", va="bottom")
# for rect in rects_bad:
#    height = rect.get_height()
#    plt.text(rect.get_x() + rect.get_width() / 2, height+0.02, '%.2f'%height, ha="center", va="bottom")  
# for rect in rects_slight:
#    height = rect.get_height()
#    plt.text(rect.get_x() + rect.get_width() / 2, height+0.02, '%.2f'%height, ha="center", va="bottom")  
# for rect in rects_none:
#     height = rect.get_height()
#     plt.text(rect.get_x() + rect.get_width() / 2, height+0.02, '%.2f'%height, ha="center", va="bottom") 
plt.show()

# print(bad_lesion_aera_dict)
# print(medium_lesion_aera_dict)
# print(slight_lesion_aera_dict)
# print(none_lesion_aera_dict)
# fw=open(r'./output/lesion_aeras_statistics.txt','a')
# fw.write('bad\n')
# fw.write(str(bad_lesion_aera_dict))
# fw.write('medium\n')
# fw.write(str(medium_lesion_aera_dict))
# fw.write('slight\n')
# fw.write(str(slight_lesion_aera_dict))
# fw.write('none\n')
# fw.write(str(none_lesion_aera_dict))
# fw.close()
