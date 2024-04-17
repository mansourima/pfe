import pandas as pd
from dbconnection import db
from sklearn.svm import SVC
import constants
import pickle
from imblearn.combine import SMOTETomek


def log_reg_given():
    print("-------------------------------------------------")
    """resultCollectionFile = db.Give_Fdbck_Train
    cursor = resultCollectionFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('Give_Train.csv', index=False)"""
    df1 = pd.read_csv('Give_most_1.csv')
    df2 = pd.read_csv('Give_most_3.csv')

    data = pd.concat([df1, df2], axis=0)

    df = data[data['trip_nbr']>1]
    X=df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                 constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]].values
    y= df.giving_feedback_classifier_int.values

    smote = SMOTETomek()
    X_resampled, y_resampled = smote.fit_resample(X, y) 
    clf = SVC(gamma=100, C=1000)

    clf.fit(X_resampled,y_resampled)
    print("Score d'entrainement de svm pour given: ", clf.score(X_resampled,y_resampled))

    filename = "svm_give"
    save_given_reg = pickle.dump(clf, open(filename, 'wb'))

def log_reg_got():

    print("-------------------------------------------------------------------")
    """resultCollectionFile = db.Got_Fdbck_Train
    cursor = resultCollectionFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('Got_Train.csv', index=False)"""
    df1 = pd.read_csv('Give_most_1.csv')
    df2 = pd.read_csv('Give_most_3.csv')

    data = pd.concat([df1, df2], axis=0)

    df = data[data['trip_nbr']>1]
    X=df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                 constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]].values
    y= df.most_frequent.values

    smote = SMOTETomek()
    X_resampled, y_resampled = smote.fit_resample(X, y) 
    clf = SVC(gamma=100, C=1000)

    clf.fit(X_resampled,y_resampled)
    print("Score d'entrainement de svm pour got ", clf.score(X_resampled,y_resampled))
    filename = "svm_got"
    save_got_reg = pickle.dump(clf, open(filename, 'wb'))

log_reg_given()
log_reg_got()
