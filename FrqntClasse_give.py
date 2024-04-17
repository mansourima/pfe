import pandas as pd
from sklearn.metrics import roc_curve, auc
from dbconnection import db
from pandas._libs.tslibs.offsets import YearBegin
#from pandas.core.generic import DataFrame
from sklearn.svm import SVC
from datetime import datetime
import constants
import pickle
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree
from sklearn import neighbors
import xgboost as Xgb
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier,StackingClassifier
from sklearn.model_selection import learning_curve
#Confusion Matrx
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix,make_scorer
from numpy.ma.extras import average
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
 #Local_outlier_factor
from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import seaborn as sns
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, ExtraTreesClassifier, VotingClassifier,BaggingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import RobustScaler,MinMaxScaler,StandardScaler

from sklearn.model_selection import StratifiedKFold,ShuffleSplit
import numpy as np
import sys
from sklearn.tree import *
import time
import matplotlib.pyplot as plt
import cmath
from imblearn.over_sampling import SMOTE
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

print("-----Give---------------------------")
resultCollectionFile = db.Give_Fdbck_Train
cursor = resultCollectionFile.find()
df = pd.DataFrame(list(cursor))
df.to_csv('The_Give_Train.csv', index=False)
df = pd.read_csv('The_Give_Train.csv')
most_frequent_classes = []

    
for document in resultCollectionFile.find():
        trip_given_class = document.get("trip_given_class", {})
        class_count = {}
        for class_id, class_name in trip_given_class.items():
            # Incrémenter le compte de la classe
            class_count[class_name] = class_count.get(class_name, 0) + 1
        most_frequent_class = max(class_count, key=class_count.get)
        most_frequent_classes.append(most_frequent_class)

print(most_frequent_classes)
df['most_frequent'] = most_frequent_classes
df.info()

print("-----Got---------------------------")

resultCollectionFile = db.Got_Fdbck_Train
cursor = resultCollectionFile.find()
df = pd.DataFrame(list(cursor))
df.to_csv('The_Got_Train.csv', index=False)
df = pd.read_csv('The_Got_Train.csv')
most_frequent_classes = []

    
for document in resultCollectionFile.find():
        trip_got_class = document.get("trip_got_class", {})
        class_count = {}
        for class_id, class_name in trip_got_class.items():
            # Incrémenter le compte de la classe
            class_count[class_name] = class_count.get(class_name, 0) + 1
        most_frequent_class = max(class_count, key=class_count.get)
        most_frequent_classes.append(most_frequent_class)

print(most_frequent_classes)
df['most_frequent'] = most_frequent_classes
df.info()