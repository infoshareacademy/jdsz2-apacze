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
from sklearn.linear_model import LogisticRegression
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
categorical_columns = ['category', 'main_category', 'country', 'currency']
df = pd.get_dummies(df, columns=categorical_columns)
df = df.drop(columns=['ID', 'name', 'pledged', 'usd pledged', 'usd_pledged_real', 'backers'], axis=1)
df['launched'] = pd.to_datetime(df['launched'])
df['deadline'] = pd.to_datetime(df['deadline'])
df['duration_days'] = df['deadline'].subtract(df['launched'])
df['duration_days'] = df['duration_days'].astype('timedelta64[D]')
print(df.shape)
print(df.columns)



#### 2.
#X = df.drop(columns=['state'],axis=1)
#y = df[['state']