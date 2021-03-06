# -*- coding: utf-8 -*-
"""AI/ML/WEEK7_Task1_feature_elimination_E18CSE037.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1beyVucfeTFb8Gs9icnpyw3p76igjU7yX

# Task 1: Feature Selection Schemes

In this assignment you will understand Feature selection techniques

###Forward Selection: 
Forward selection is an iterative method in which we start with having no feature in the model. In each iteration, we keep adding the feature which best improves our model till an addition of a new variable does not improve the performance of the model.

###Backward Elimination: 
In backward elimination, we start with all the features and removes the least significant feature at each iteration which improves the performance of the model. We repeat this until no improvement is observed on removal of features.

###Recursive Feature elimination: 
It is a greedy optimization algorithm which aims to find the best performing feature subset. It repeatedly creates models and keeps aside the best or the worst performing feature at each iteration. It constructs the next model with the left features until all the features are exhausted. It then ranks the features based on the order of their elimination.

##Dataset
The dataset is available at "data/bank-full.csv" in the respective challenge's repo.
The dataset can be obtained from:
https://www.kaggle.com/vinicius150987/bank-full-machine-learning

#Features (X)
##Input variables:
# bank client data:
1. age (numeric)
2. job : type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')
3. marital : marital status (categorical: 'divorced','married','single','unknown'; note: 'divorced' means divorced or widowed)
4. education (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown')
5. default: has credit in default? (categorical: 'no','yes','unknown')
6. housing: has housing loan? (categorical: 'no','yes','unknown')
7. loan: has personal loan? (categorical: 'no','yes','unknown')
# related with the last contact of the current campaign:
8. contact: contact communication type (categorical: 'cellular','telephone')
9. month: last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec')
10. day_of_week: last contact day of the week (categorical: 'mon','tue','wed','thu','fri')
11. duration: last contact duration, in seconds (numeric). Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no'). Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.
# other attributes:
12. campaign: number of contacts performed during this campaign and for this client (numeric, includes last contact)
13. pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)
14. previous: number of contacts performed before this campaign and for this client (numeric)
15. poutcome: outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success')
# social and economic context attributes
16. emp.var.rate: employment variation rate. quarterly indicator (numeric)
17. cons.price.idx: consumer price index. monthly indicator (numeric)
18. cons.conf.idx: consumer confidence index. monthly indicator (numeric)
19. euribor3m: euribor 3 month rate. daily indicator (numeric)
20. nr.employed: number of employees. quarterly indicator (numeric)

##Output variable (desired target):
21. y. has the client subscribed a term deposit? (binary: 'yes','no')

#### Objective
- To apply different feature selection approaches such as Forward Selection, Backward Elimination and recursive feature elimination for feature selection in Logistic Regression Algorithm.


#### Tasks
- Download and load the data (csv file)
- Process the data 
- Split the dataset into 70% for training and rest 30% for testing (sklearn.model_selection.train_test_split function)
- Train Logistic Regression
- Apply feature selection techniques
- Train the models on the feature reduced datasets
- Compare their accuracies and print feature subset

#### Further Fun
- Perform feature selection with other schemes in the Sklearn: https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_selection|

#### Helpful links
- pd.get_dummies() and One Hot Encoding: https://queirozf.com/entries/one-hot-encoding-a-feature-on-a-pandas-dataframe-an-example
- Feature Scaling: https://scikit-learn.org/stable/modules/preprocessing.html
- Train-test splitting: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- Feature selection in ML: https://machinelearningmastery.com/feature-selection-machine-learning-python/
- Feature selection in sklearn: https://scikit-learn.org/stable/modules/feature_selection.html
- Use slack for doubts: https://join.slack.com/t/deepconnectai/shared_invite/zt-givlfnf6-~cn3SQ43k0BGDrG9_YOn4g
"""

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from sklearn import preprocessing

banking =  pd.read_csv("/content/bank-full.csv")

banking.columns

banking.dtypes

banking.head(6)

banking.describe()

banking.shape

banking.rename(columns={"y":"Action"},inplace = True)

banking.Action.value_counts()

sns.heatmap(banking.isnull(),yticklabels = False, cbar = False , cmap ='RdYlGn')

new_data =  banking.select_dtypes(include='object')

#checking the number of unique categories in each column
for i in new_data.columns:
  print(i,';',len(set(i)),'labels')

from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
new_data_encoded = new_data.apply(lb.fit_transform)
new_data_nonobject = banking.select_dtypes(exclude = ["object"])
banking1 = pd.concat([new_data_nonobject,new_data_encoded], axis = 1)

banking1.head()

banking1.shape

"""# K Best Features"""

from sklearn.feature_selection import SelectKBest
from scipy.stats import chi2 
from sklearn.feature_selection import f_classif

X = banking1.iloc[:,0:16]
y = banking1['Action']

X.shape

Kbest = SelectKBest(f_classif, k=3)
kfit = Kbest.fit(X,y)

scores = pd.DataFrame({'Scores':kfit.scores_})
columns = pd.DataFrame({'Features':X.columns})

# Train logistic regression model with subset of features from K Best
FeatureScores=pd.concat([columns,scores],axis=1)
FeatureScores=FeatureScores.sort_values(by='Scores',ascending=False)
FeatureScores

# Train logistic regression model with subset of features from K Best
k=10
X=FeatureScores.iloc[0:k,0]
X
K_Best_DataFrame=banking1[X]
K_Best_DataFrame

#Splitting the Dataset into 70% training and 30% Testing Set
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(K_Best_DataFrame,y,test_size=0.3,random_state=42)

#Printing the Shape of X_train,X_test,y_train,y_test
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.linear_model import LogisticRegression

lr=LogisticRegression()
lr.fit(K_Best_DataFrame,y)

#Accuracy on Training and Testing Set
from sklearn.metrics import accuracy_score
print("----------LOGISTIC REGRESSION----------")
y_lr_train=lr.predict(X_train)
print("Accuracy of Training Split :",accuracy_score(y_train,y_lr_train))
y_lr_pred=lr.predict(X_test)
print("Accuracy of Test Split :",accuracy_score(y_test,y_lr_pred))

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

from sklearn.linear_model import LogisticRegression,SGDClassifier, RidgeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import f1_score,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

"""# Forward Selection"""

# Train a logistic regression model here

X_f = banking1.iloc[:,0:16]
y_f = banking1['Action']

X_f_train,X_f_test,y_f_train,y_f_test=train_test_split(X_f,y_f,test_size=0.3,random_state=8)

f_model = LogisticRegression()

f_model.fit(X_f_train, y_f_train)

X_f_train_shape = X_f_train.shape
X_f_train_type  = type(X_f_train)
y_f_train_shape = y_f_train.shape
y_f_train_type  = type(y_f_train) 
print(f'X: Type-{X_f_train_type}, Shape-{X_f_train_shape}')
print(f'y: Type-{y_f_train_type}, Shape-{y_f_train_shape}')
assert (X_f_train.shape[0]==y_f_train.shape[0] and X_f_test.shape[0]==y_f_test.shape[0]), "Check your splitting carefully"
print(X_f_train.shape)
print(X_f_test.shape)
print(y_f_train.shape)
print(y_f_test.shape)

# Print the absolute weights of the model and sort them in ascending order
coefficients = pd.DataFrame(f_model.coef_)
coefficients=coefficients.T
columns = pd.DataFrame(X_f_train.columns)
FeatureScores=pd.concat([columns,coefficients],axis=1)
FeatureScores.columns=['Columns','Coefficients']
FeatureScores
# Convert in positive values
rows=FeatureScores.shape[0]
for g in range(rows):
  if(FeatureScores.iloc[g,1]<0):
    FeatureScores.iloc[g,1]=-FeatureScores.iloc[g,1]
  else:
    continue
FeatureScores
#sorting them in descending order
FeatureScores=FeatureScores.sort_values(by='Coefficients',ascending=False)
FeatureScores

C=FeatureScores.iloc[:,0]
C

FE_Features=X_f_train[C]
FE_Features_test=X_f_test[C]

# Run a for loop where each time you train a new model by adding features (from no of features 1 to n) 
# with highest weights (based on absolute weight from initial model)
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
training_f_accuracy=[]
testing_f_accuracy=[]
rows,columns=FE_Features.shape
print(columns)
for m in range(1,columns+1):
   Add_Features=FE_Features.iloc[:,:m]
   lr_f=LogisticRegression()
   lr_f.fit(Add_Features,y_f_train)
  #  print("----------LOGISTIC REGRESSION----------")
   y_lr_f_train=lr_f.predict(Add_Features)
   training_f_accuracy.append(accuracy_score(y_f_train,y_lr_f_train))
   y_lr_f_pred=lr_f.predict(FE_Features_test.iloc[:,:m])
   testing_f_accuracy.append(accuracy_score(y_f_test,y_lr_f_pred))

# Print the accuracies of all the models trained and names of the features used for each time
for m in range(1,columns+1):
   Add_Features=FE_Features.iloc[:,:m]
   print("Iteration ",m)
   print()
   print("Column Names",Add_Features.columns)
   print()
   print("Training Accuracy",training_f_accuracy[m-1])
   print()
   print("Testing Accuracy",testing_f_accuracy[m-1])
   print()
   print()
   print()

# Find a feature subset number where accuracy is maximum and number of features is minimum at the same time

"""# Backward Elimination"""

X = banking1.iloc[:,0:16]
y = banking1['Action']

# Train a logistic regression model here
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=42)

lr = LogisticRegression()

lr.fit(X_train,y_train)

# Print the absolute weights of the model and sort them in descending order

print(lr.coef_)

X

weights= []
for i in lr.coef_[0]:
    print(i)
    weights.append(abs(i))

w={}
for i in range (len(X_f.columns)):
    w[X_f.columns[i]]=weights[i]
w

fin = sorted(w.items(), key=lambda x: x[1])
fin

# Run a for loop where each time you train a new model by removing features (from no of features n to 1) 
# with lowest weights (based on absolute weight from initial model) 
feature_subset=[]
accuracy_test=[]
accuracy_train=[]

for i in range(0,len(fin)):
    features=[]
    for j in range(i,len(fin)):
        features.append(fin[j][0])
    feature_subset.append(features) 
    X_present=X[features] 
    X_train, X_test, y_train, y_test = train_test_split(X_present, y, test_size=0.33,random_state=42)
    print(X_train.shape)
    logistic=LogisticRegression()
    logistic.fit(X_train,y_train)
    res_y=logistic.predict(X_test)
    accuracy_test.append(accuracy_score(y_test, res_y))
    res_y=logistic.predict(X_train)    
    accuracy_train.append(accuracy_score(y_train, res_y))
    
# print(feature_subset)

# Print the accuracies of all the models trained and names of the features used for each tim
print("No Of Features","\t","Test Accuracy","\t","Train Accuracy")
for i in range (len(feature_subset)):
    print(len(feature_subset[i]),"\t",accuracy_test[i],"\t",accuracy_train[i])

# Find a feature subset number where accuracy is maximum and number of features is minimum at the same time

"""# Recursive Feature Elimination. 
Recursive Feature Elimination (RFE) as its title suggests recursively removes features, builds a model using the remaining attributes and calculates model accuracy.
"""

X = banking1.iloc[:,0:16]
y = banking1.iloc[:,16]
logit = LogisticRegression()

X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.3, random_state = 10)

from sklearn.svm import SVR

rfe = RFE(estimator=logit, step=1)
rfe = rfe.fit(X,y)

cols = pd.DataFrame(X.columns)
ranking = pd.DataFrame(rfe.ranking_)

rankings_of_features = pd.concat([cols,ranking],axis = 1)

rankings_of_features

rankings_of_features.columns = ["head","rank"]

rankings_of_features

print(rankings_of_features.nlargest(5,'rank'))
#remember this gives wrong results

rankings_of_features.sort_values(by='rank')

#replace your X_train,X_test with new training data(the one which contains most impactful features)
X_trainRFE = rfe.transform(X_train)
X_testRFE = rfe.transform(X_test)

model = logit.fit(X_trainRFE,y_train)

from sklearn import metrics
from sklearn.model_selection import cross_val_score

logit.predict(X_testRFE)

score = logit.score(X_testRFE, y_test)
print(score)

"""# RFE using cross validation"""

rfecv = RFECV(estimator=logit, step=1, cv=5, scoring='accuracy')
rfecv = rfecv.fit(X_trainRFE,y_train)

rfecv.grid_scores_

X_train_rfecv = rfecv.transform(X_trainRFE)
X_test_rfecv = rfecv.transform(X_testRFE)

model = logit.fit(X_train_rfecv,y_train)

logit.predict(X_test_rfecv)

logit.score(X_test_rfecv,y_test)
print(score)