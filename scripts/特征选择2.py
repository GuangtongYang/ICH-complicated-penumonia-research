#%%
#多变量特征选择
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import pearsonr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.metrics import confusion_matrix, make_scorer, mutual_info_score, precision_score, \
    roc_auc_score, roc_curve,accuracy_score,\
        classification_report,recall_score

data_path=r''
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
y[y>1]=1 #二分类 有无肺炎
#y[y==1]=0#二分类  无轻 中重
y[y>1]=1
y.head()

#print(X.columns.values)
X=StandardScaler().fit_transform(X)#标准化
#归一化
# for i in X.columns.values:
#     min=np.min(X[i])
#     max=np.max(X[i])
#     X[i]=(X[i]-min)/(max-min)


#print(X)
names=data.columns.values


# for i in X.columns.values:
#     corr=X[i].corr(y)
#     if corr > 0.3:
#         print(i+':'+str(corr))
auc=[]
acc=[]
se=[]
sp=[]
PPV=[]
NPV=[]
importances=[]
pipe = Pipeline(steps=[ ('std',StandardScaler()),
                       ('clf', LogisticRegression(solver='liblinear',\
                       penalty='l1',C=0.001,multi_class='auto'))])


pipe1 = Pipeline(steps=[ (('std'),StandardScaler()),
                        
                       ('clf', svm.SVC(kernel='linear',C=0.0001,probability=True)),
                       ])

pipe2 = Pipeline(steps=[ (('std'),StandardScaler()),
                       ('clf', RandomForestClassifier(max_depth=3))])



skf=StratifiedKFold(n_splits=10)


my_fold=0
mean_tpr = 0.0              # 用来记录画平均ROC曲线的信息
mean_fpr = np.linspace(0, 1, 100)

for train_index,test_index in skf.split(X,y):

    X_train=X.loc[train_index]
    X_test=X.loc[test_index]

    pipe1.fit(X_train,y[train_index])

    y_pred=pipe1.predict(X_test)
    probas_=pipe1.predict_proba(X_test)
    probas_trian=pipe1.predict_proba(X_train)
    #print(probas_[:,1])
    #print(pipe['clf'].coef_)
    #importances.append(abs(pipe2['clf'].coef_))
    #概率调整
    # fpr_svm, tpr_svm, thresholds_svm = roc_curve(y[train_index], probas_trian[:,1])
    # optimal_idx_svm = np.argmax(tpr_svm - fpr_svm)#tpr和fpr差异最大
    # optimal_threshold_svm = thresholds_svm[optimal_idx_svm]
    # y_pred_after_adjust = np.copy(probas_[:,1])
    # y_pred_after_adjust[y_pred_after_adjust>=optimal_threshold_svm] = 1
    # y_pred_after_adjust[y_pred_after_adjust<optimal_threshold_svm] = 0
    #print(y_pred_binary)
    #print(probas_[:,1])

    #print(y_pred)
    #print(optimal_threshold_svm)
    #print(fpr_svm)
    #print(tpr_svm)

    acc.append(accuracy_score(y[test_index],y_pred=y_pred))
    auc.append(roc_auc_score(y[test_index],y_score=probas_[:,1]))
    se.append(recall_score(y[test_index],y_pred=y_pred))
    PPV.append(precision_score(y[test_index],y_pred=y_pred))
    tn, fp, fn, tp = confusion_matrix(y[test_index], y_pred).ravel()
    sp.append(tn/(tn+fp))
    NPV.append(tn/(tn+fn))

    fpr,tpr,thresholds=roc_curve(y[test_index],y_score=probas_[:,1])
    #print(fpr.shape)
    mean_tpr += np.interp(mean_fpr, fpr, tpr)   # 插值函数 interp(x坐标,每次x增加距离,y坐标)  累计每次循环的总值后面求平均值
    mean_tpr[0] = 0.0 

    #plt.plot(fpr,tpr,lw=1,label='ROC fold {0} (auc = {1:.2f})'.format(my_fold, auc[-1]))
    my_fold+=1

print('二分类 中重、无轻 ')
print(X.shape)
print(pipe1['clf'])
print('auc:             %s'%np.mean(auc))
print('acc:             %s'%np.mean(acc))
print('sensitivity:     %s'%np.mean(se))
print('specificity:     %s'%np.mean(sp))
print('PPV:             %s'%np.mean(PPV))
print('NPV              %s'%np.mean(NPV))

# %%
