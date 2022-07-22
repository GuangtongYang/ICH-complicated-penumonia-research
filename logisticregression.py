
from cProfile import label
import pip
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn import metrics,tree
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
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, make_scorer

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


#X=data.iloc[:,8:-1]#分区特征
#X=data.iloc[:,0:8]#出血特征
X=data.iloc[:,0:-1]#分区特征+出血特征
y=data.iloc[:,-1]
# for i in range(1,36):
#     X[str(i)][X[str(i)]>=0.1]=1
#     X[str(i)][X[str(i)]<0.1]=0
X.head()

#y[y>2]=2
#y[y==2]=1

#y[y==2]=1
#y[y==3]=2
y[y>0]=1 #二分类 有无肺炎
#y[y==1]=0
#y[y>1]=1
y.head()

y.describe()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

pipe = Pipeline(steps=[ ('std',StandardScaler()),
                    
                       ('clf', LogisticRegression(solver='liblinear',\
                       penalty='l1',C=1,multi_class='auto'))])

pipe1 = Pipeline(steps=[ (('std'),StandardScaler()),
                        
                       ('clf', svm.SVC(kernel='linear',C=0.1)),
                       ])

pipe2 = Pipeline(steps=[ (('std'),StandardScaler()),
                       ('clf', RandomForestClassifier(max_depth=7))])

pipe3 = Pipeline(steps=[ (('std'),StandardScaler()),
                       ('clf', KNeighborsClassifier(n_neighbors=4))])

pipe4 = Pipeline(steps=[ (('std'),StandardScaler()),
                       ('clf', tree.DecisionTreeClassifier())])

# pipe.fit(X_train,y_train)
# pipe.score(X_test,y_test)
def confusion_matrix_scorer(clf, X, y):
    y_pred = clf.predict(X)
    cm = confusion_matrix(y, y_pred)
    return {'tn': cm[0, 0], 'fp': cm[0, 1],
        'fn': cm[1, 0], 'tp': cm[1, 1]}

scoring_binary={'auc':'roc_auc','acc':'accuracy',\
    'sensitivity':'recall','PPV':'precision',\
        }
scores = cross_validate(pipe, X, y, cv=10, return_train_score=True,\
    return_estimator=True,scoring=scoring_binary)
my_confusion_matrix=cross_validate(pipe, X, y, cv=10, return_train_score=False,\
    return_estimator=True,scoring=confusion_matrix_scorer)
#scores = cross_val_score(pipe1, X, y, cv=5)
#print(np.mean(scores['test_score']))
print(scores.keys())
df_scores = pd.DataFrame(scores)
df_scores

TP=my_confusion_matrix['test_tp']
TN=my_confusion_matrix['test_tn']
FP=my_confusion_matrix['test_fp']
FN=my_confusion_matrix['test_fn']

auc=scores['test_auc']
acc=scores['test_acc']
#Specificity or true negative rate
my_specificity=TN/(TN+FP)
#sensitivity. recall
my_sensitivity=scores['test_sensitivity']
#precision
my_precision=scores['test_PPV']
#Negative predictive value
my_npv=TN/(TN+FN)

print('二分类 有无 ')
print(X.shape)
print(scores['estimator'][0])
print('auc:             %s'%np.mean(auc))
print('acc:             %s'%np.mean(acc))
print('sensitivity:     %s'%np.mean(my_sensitivity))
print('specificity:     %s'%np.mean(my_specificity))
print('PPV:             %s'%np.mean(my_precision))
print('NPV              %s'%np.mean(my_npv))

df_scores
