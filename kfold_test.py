
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, make_scorer, precision_score, \
    roc_auc_score, roc_curve,accuracy_score,\
        classification_report,recall_score

from logisticregression import confusion_matrix_scorer

data_path=r'D:\pythonScripts\nonRigidRegistration\output\fluid_LesionAera_label_ml.txt'
data=pd.read_csv(data_path,header=None,sep=' ',names=['F/B','L/B','L/F','L/All','F/All','fluid','brain','lesion','0',\
    '1','2','3','4','5','6',\
    '7','8','9','10','11',\
    '12','13','14','15','16',\
        '17','18','19','20','21','22','23','24',\
        '25','26','27','28','29','30','31',\
            '32','33','34','35','label'])


# data.describe()
data=data.drop('0',axis=1)
# for i, label in enumerate(data['label']):
#     if label==3:
#         data=data.drop(index=i,axis=0)

#print(data['fluid'])
data.head()

tprs=[]
aucs=[]
mean_fpr=np.linspace(0,1,100)
#X=data.iloc[:,8:-1]#分区特征
#X=data.iloc[:,0:8]#出血特征
X=data.iloc[:,0:-1]#分区特征+出血特征
y=data.iloc[:,-1]

# for i in range(1,36):
#     X[str(i)][X[str(i)]>=0.5]=1
#     X[str(i)][X[str(i)]<0.5]=0

X.head()

#y[y>2]=2
#y[y==2]=1

#y[y==2]=1
#y[y==3]=2
#y[y>0]=1 #二分类 有无肺炎
y[y==1]=0#二分类  无轻 中重
y[y>1]=1
y.head()

y.describe()
auc=[]
acc=[]
se=[]
sp=[]
PPV=[]
NPV=[]
pipe = Pipeline(steps=[ ('std',StandardScaler()),
                       ('clf', LogisticRegression(solver='liblinear',\
                       penalty='l1',C=0.01,multi_class='auto'))])

pipe1 = Pipeline(steps=[ (('std'),StandardScaler()),
                        
                       ('clf', svm.SVC(kernel='linear',C=0.01,probability=True)),
                       ])

pipe2 = Pipeline(steps=[ (('std'),StandardScaler()),
                       ('clf', RandomForestClassifier(max_depth=8))])

X_train,X_test,Y_trian,y_test=train_test_split(X,y,test_size=0.2)

