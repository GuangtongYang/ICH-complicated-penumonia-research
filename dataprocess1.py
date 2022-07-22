'''根据肺炎轻重把分区数据分类'''
import os
import SimpleITK as sitk

bad_path=r'D:\BaiduNetdiskDownload\BrainData\bad_copy'
medium_path=r'D:\BaiduNetdiskDownload\BrainData\medium_copy'
slight_path=r'D:\BaiduNetdiskDownload\BrainData\slight'
none_path=r'D:\BaiduNetdiskDownload\BrainData\none'

file=open('./output/analysis_percent.txt','r')
name_list=file.readlines()
file.close()
fw=open('./output/LesionAera_Lung.txt','a')

for lung_name in os.listdir(bad_path):
    lung_name=lung_name.split('.')[0]
    for i,name in enumerate(name_list):
        name=name.split('.')[0]
        if name==lung_name:
            fw.write("3 "+name_list[i])
            break

for lung_name in os.listdir(medium_path):
    lung_name=lung_name.split('.')[0]
    for i,name in enumerate(name_list):
        name=name.split('.')[0]
        if name==lung_name:
            fw.write("2 "+name_list[i])
            break


for lung_name in os.listdir(slight_path):
    lung_name=lung_name.split('.')[0]
    for i,name in enumerate(name_list):
        name=name.split('.')[0]
        if name==lung_name:
            fw.write("1 "+name_list[i])
            break


for lung_name in os.listdir(none_path):
    lung_name=lung_name.split('.')[0]
    for i,name in enumerate(name_list):
        name=name.split('.')[0]
        if name==lung_name:
            fw.write("0 "+name_list[i])
            break

fw.close()
    
            
    


print(77+101+47+19)
