import pandas as pd
from dbconnection import db
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


def log_reg_given():

    print("-------------------------------------------------------------------")
    resultCollectionFile = db.Give_Fdbck_Train
    cursor = resultCollectionFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('The_Give_Train_1.csv', index=False)
    df = pd.read_csv('The_Give_Train_1.csv')
    #df2 = pd.read_csv('The_Give_Train.csv')
    data = df[df["trip_nbr"] > 1]
    #data = df2[df2["trip_nbr"] > 1]

    #data = pd.concat([data1, data2], axis=0)

    nombre_de_tuples = len(data)
    print("le nombre de tuple:",nombre_de_tuples)
    #print(df.info())
    X=data[["trip_nbr","max_variance",constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                 constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]].values
    y= data.giving_feedback_classifier_int.values
    #"trip_nbr","max_variance",
    smote = SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y) 
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X_resampled)
    

    train_X,test_X, train_Y,test_Y = train_test_split(X_scaled, y_resampled, test_size=0.2, random_state=42)

    #train_X,test_X, train_Y,test_Y = train_test_split(X, y, test_size=0.3, random_state=42)

    classifiers = [
       SVC(C=1000,gamma=100),#]#,gamma=100 C=100 
       KNeighborsClassifier(),
       DecisionTreeClassifier(),
       LogisticRegression(),
       RandomForestClassifier(),
       GaussianNB(),

       AdaBoostClassifier(),
       ExtraTreesClassifier(),
       #VotingClassifier()]
       MLPClassifier(),
       GradientBoostingClassifier()]

    for clf in classifiers:
            clf_name = clf.__class__.__name__
            clf.fit(train_X, train_Y)
            #print("Support Vector Machine Training Score for Given Feedback Classifier Score is ", clf.score(train_X, train_Y))
            # Perform predictions on test data
            y_pred = clf.predict(test_X)
            accuracy = metrics.accuracy_score(test_Y, y_pred)
            print(clf_name," = ",accuracy)
            report = classification_report(test_Y, y_pred)
            #print("Classification Report:")
            #print(report)

    print("Model Training Complete")
    

def log_reg_got():

    print("-------------------------------------------------------------------")
    resultCollectionFile = db.Got_Fdbck_Train
    cursor = resultCollectionFile.find()
    dateStr = datetime.now()
    resultStr = str(dateStr)
    resultStr = resultStr.replace(" ", "")
    df = pd.DataFrame(list(cursor))
    df.to_csv('The_Got_Train_1.csv', index=False)
    df = pd.read_csv('The_Got_Train_1.csv')
    data = df[df["trip_nbr"] > 1]
    nombre_de_tuples = len(data)
    print("le nombre de tuple:",nombre_de_tuples)
    #print(df.info())
    X=data[["trip_nbr","max_rating_with_variance",constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                 constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]].values
    y= data.got_feedback_classifier_int.values

    smote = SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y) 
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X_resampled)
    

    train_X,test_X, train_Y,test_Y = train_test_split(X_scaled, y_resampled, test_size=0.2, random_state=42)

    #train_X,test_X, train_Y,test_Y = train_test_split(X, y, test_size=0.3, random_state=42)

    classifiers = [
       SVC(C=1000,gamma=100),#]#,gamma=100 C=100 
       KNeighborsClassifier(),
       DecisionTreeClassifier(),
       LogisticRegression(),
       RandomForestClassifier(),
       GaussianNB(),

       AdaBoostClassifier(),
       ExtraTreesClassifier(),
       #VotingClassifier()]
       MLPClassifier(),
       GradientBoostingClassifier()]

    for clf in classifiers:
            clf_name = clf.__class__.__name__
            clf.fit(train_X, train_Y)
            #print("Support Vector Machine Training Score for Got Feedback Classifier Score is ", clf.score(train_X, train_Y))
            # Perform predictions on test data
            y_pred = clf.predict(test_X)
            accuracy = metrics.accuracy_score(test_Y, y_pred)
            print(clf_name," = ",accuracy)
            report = classification_report(test_Y, y_pred)
            #print("Classification Report:")
            #print(report)

    print("Model Training Complete")


log_reg_given()
log_reg_got()