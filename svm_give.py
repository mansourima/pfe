import pandas as pd
from pandas.core.api import DataFrame
from sklearn.exceptions import DataDimensionalityWarning
from sklearn.metrics import roc_curve, auc
from dbconnection import db
from imblearn.combine import SMOTETomek
from pandas._libs.tslibs.offsets import YearBegin
#from pandas.core.generic import DataFrame
from sklearn.svm import SVC
from xgboost import XGBClassifier
from datetime import datetime
import constants
import seaborn as sn  
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
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
from matplotlib import pyplot as plt

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


df1 = pd.read_csv('Give_most_1.csv')
df2 = pd.read_csv('Give_most_3.csv')

data = pd.concat([df1, df2], axis=0)

data = data[data['trip_nbr']>1]
X=data[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                 constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]].values
y= data.giving_feedback_classifier_int.values
#counter_before = Counter(y)
#y = df'giving_feedback_classifier_int']] most_frequent
#"trip_nbr","max_variance",
smote = SMOTETomek()
X_resampled, y_resampled = smote.fit_resample(X, y) 
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_resampled)
#counter_after = Counter(y_resampled)

train_X,test_X, train_Y,test_Y = train_test_split(X_scaled, y_resampled, test_size=0.2, random_state=42)
    #train_Y = np.array(train_Y) - 1 
    #test_Y = np.array(test_Y) - 1

classifiers = [
       SVC(gamma=100,C=1000),]#,gamma=100 C=100 
       #KNeighborsClassifier(),]
       #DecisionTreeClassifier(),
       #LogisticRegression(),
       #RandomForestClassifier(),]
       #GaussianNB(),

       #AdaBoostClassifier(),]
       #ExtraTreesClassifier(),]
       #XGBClassifier()]
       #VotingClassifier()]
       #MLPClassifier(),
       #GradientBoostingClassifier()]

for clf in classifiers:
            clf_name = clf.__class__.__name__
            clf.fit(train_X, train_Y)
            y_pred = clf.predict(test_X)
            accuracy = metrics.accuracy_score(test_Y, y_pred)
            print(clf_name," = ",accuracy*100)
            report = classification_report(test_Y, y_pred)
            #print("Classification Report:")
            print(report)
            cm = confusion_matrix(test_Y, y_pred)
            print(cm)

"""plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.bar(counter_before.keys(), counter_before.values())
plt.title('Distribution des classes avant SMOTETomek')

plt.subplot(1, 2, 2)
plt.bar(counter_after.keys(), counter_after.values())
plt.title('Distribution des classes après SMOTETomek')

plt.tight_layout()
plt.show()"""

def dessiner_matrice_confusion(class_name,cm,column):
        #labels = [class_name, 'not ' + class_name]

       # Créer un DataFrame à partir de la matrice de confusion
        #df_cm = pd.DataFrame(cm, index=labels, columns=labels)
        df_cm = pd.DataFrame(cm, index=column, columns=column)
       # Afficher la matrice de confusion avec les classes prédites et réelles
        plt.figure(figsize=(8, 6))
        sn.set(font_scale=1.4)  # pour la taille des labels
        sns.heatmap(df_cm, annot=True, fmt='d', cmap='Blues', cbar=False, square=True,
            xticklabels=column,
            yticklabels= column)
        plt.xlabel('Classe Réelle')
        plt.ylabel('Classe Prédite')#, rotation=0, labelpad=40, ha='right')
        plt.title('Matrice de Confusion ')#-{}' .format(column))#, pad=20, y=1.08)
        plt.show()

dessiner_matrice_confusion('giving_feedback_classifier', cm, ['Safety', 'punctuality', 'friendliness', 'comfortibility', 'Chatty'])





