import pandas as pd
import numpy as np
import string

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

#### Data_set
pd.set_option('display.max_columns', 12)
df = pd.read_csv('data/ks-projects-201801.csv')

### Research
plt.subplot(221, title='Main category')
df['main_category'].value_counts().plot.bar()
plt.subplot(222, title='Currency')
df['currency'].value_counts().plot.bar()
plt.subplot(223, title='Country')
df['country'].value_counts().plot.bar()
plt.subplot(224, title='State')
df['state'].value_counts().plot.bar()
plt.show()

### Data preparation
categorical_columns = ['main_category', 'country', 'currency']
df = pd.get_dummies(df, columns=categorical_columns)
df = df.drop(columns=['ID', 'name', 'pledged', 'usd pledged', 'usd_pledged_real', 'category'], axis=1)
df['launched'] = pd.to_datetime(df['launched'])
df['deadline'] = pd.to_datetime(df['deadline'])
df['duration_days'] = df['deadline'].subtract(df['launched'])
df['duration_days'] = df['duration_days'].astype('timedelta64[D]')
df = df.drop(columns=['launched', 'deadline'])
#print(df['duration_days'])
print(df.shape)
#print(df['goal'])
#print(df.isnull().any())

#####outliers
df['goal'].plot(kind='box')
plt.show()

#ax = sns.boxplot(x=df['goal'].to_frame())
#df['goal'].to_frame()

X = df.drop(columns=['state'], axis=1)
y = df['state']

sc = preprocessing.StandardScaler()
X = pd.DataFrame(sc.fit_transform(X.values), index=X.index, columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)



#### 1. KNN,  - Mateusz

#### 2. Random Forest - Lila

#### 3. SVM - Jakub

#### 4. XGBoost