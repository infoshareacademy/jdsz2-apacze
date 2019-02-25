import pandas as pd
import numpy as np
import string

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import BallTree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

#### Data_set
pd.set_option('display.max_columns', 12)
df = pd.read_csv('data/ks-projects-201801.csv')

### Research
# plt.subplot(221, title='Main category')
# df['main_category'].value_counts().plot.bar()
# plt.subplot(222, title='Currency')
# df['currency'].value_counts().plot.bar()
# plt.subplot(223, title='Country')
# df['country'].value_counts().plot.bar()
# plt.subplot(224, title='State')
# df['state'].value_counts().plot.bar()
#plt.show()

### Data preparation
categorical_columns = ['main_category', 'country', 'currency']
df = pd.get_dummies(df, columns=categorical_columns)
df = df.drop(columns=['ID', 'name', 'pledged', 'goal', 'usd pledged', 'usd_pledged_real', 'category'], axis=1)
df['launched'] = pd.to_datetime(df['launched'])
df['deadline'] = pd.to_datetime(df['deadline'])
df['duration_days'] = df['deadline'].subtract(df['launched'])
df['duration_days'] = df['duration_days'].astype('timedelta64[D]')
df = df.drop(columns=['launched', 'deadline'])
#print(df['duration_days'])
print(df.shape)
#print(df['goal'])
#print(df.isnull().any())

#####boxplot outliers
#df['usd_goal_real'].plot(kind='box', logy=True)
#plt.show()

####
X = df.drop(columns=['state'], axis=1)

df.state = pd.Categorical(df.state)
df['state'] = df.state.cat.codes
y = df['state']

sc = preprocessing.StandardScaler()
X = pd.DataFrame(sc.fit_transform(X.values), index=X.index, columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

# scorer to compare results
scorer = make_scorer(mean_squared_error)
kfold = KFold(n_splits=5, random_state=11)

#### 0. Logistic regresion
logreg = LogisticRegression(solver='lbfgs', multi_class='auto', n_jobs=-1).fit(X_train, y_train)
y_pred = logreg.predict(X_test)
acc_log = accuracy_score(y_test, y_pred)
print('Logistic regresion:\t',acc_log)

#### Logistic regression plot
# plt.figure(figsize=(8, 8))
# plt.title('LOGIT')
# plt.scatter(y_pred, y_test, linewidth=2)
# plt.ylabel('y')
# plt.xlabel('x')
# plt.show()

#### 1. KNN,  - Mateusz

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
acc_knn = round(knn.score(X_test, y_test) * 100, 2)
print(acc_knn)

#### 2. Random Forest - Lila

#### 3. SVM - Jakub

#### 4. XGBoost


def run_xgboost_analysis():

    a = [2, 3, 4, 5, 6, 7, 8, 9, 12, 15]
    b = [0.09, 1.0, 1.1]
    c = [50, 100, 150, 200, 250, 300, 320, 350, 400]
    max_scr = 100000000000000
    max_dep = 0
    max_len = 0
    max_n_est = 0
    for i in a:
        for j in b:
            for k in c:

                clf_xgbr = XGBRegressor(max_depth=i, learning_rate=j, n_estimators=k)
                #
                results = cross_val_score(clf_xgbr, X_train, y_train, cv=kfold, scoring=scorer)
                #
                res_med = np.median(results)
                if res_med < max_scr:
                    max_dep = i
                    max_len = j
                    max_n_est = k
                    max_scr = res_med

    return max_scr, max_dep, max_len, max_n_est


# max_scr_1, max_dep_1, max_len_1, max_n_est_1 = run_xgboost_analysis()
# print('Best score is {0}, for parameters depth {1}, learning rate {2}, n_estimators {3}'.format(max_scr_1, max_dep_1, max_len_1, max_n_est_1))











