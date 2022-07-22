import numpy as np
import os
import pandas as pd
import re

'''
格式化数据
name 1 2 3 4 ... 35  label 

1 016_zhang_rongxin.nii{28: 0.08317898636134029, 20: 0.0001528022697331742}
'''
file=open('./output/LesionAera_Lung.txt','r')
data_list=file.readlines()
file.close()

output_file=open('./output/LesionAera_label_ml.txt','a')


output_data_list=['0']*36

for i,my_data in enumerate(data_list):

    patient_name=re.search(r' .+{',my_data).group()[0:-1]
    print(patient_name[0:-1])

    label=my_data[0]
    name=re.search(r' .+{',my_data).group()[1:-1]
    for my_index in range(0,36):
        num=re.search(str(my_index)+r': \d.\d*',my_data)
        if num!=None:
            num=num.group()
            #格式 10: 0.9805
            output_data_list[my_index]=num.split(' ')[1]
        else:
            output_data_list[my_index]='0'
    #output_file.write(patient_name+' ')
    for output in output_data_list:
        output_file.write(output+' ')
    output_file.write(label+'\n')
    print(output_data_list)
output_file.close()
    







