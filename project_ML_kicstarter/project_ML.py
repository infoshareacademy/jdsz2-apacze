import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
pd.set_option('display.max_columns', 12)

df = pd.read_csv('data\ks-projects-201801.csv')
categorical_columns = ['category', 'main_category', 'country', 'currency']
df = pd.get_dummies(df, columns=categorical_columns)
df = df.drop(columns=['ID', 'name', 'pledged', 'usd pledged', 'usd_pledged_real', 'usd_goal_real'],axis=1)

X = df.drop(columns=['state'],axis=1)
y = df[['state']]
#### 1. Preprocessing
print(X.shape)
print(X.head(5))

