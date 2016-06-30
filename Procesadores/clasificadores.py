# coding=utf-8

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KernelDensity
from sklearn.linear_model import LogisticRegression


def nuevoNaiveBayes():
    return GaussianNB()


def nuevoSVC():
    return SVC(kernel='linear')


def nuevoLinearSVC():
    return LinearSVC()


def nuevoDecisionTree():
    return DecisionTreeClassifier()


def nuevoRandomForest():
    return RandomForestClassifier()


def nuevoMaxEnt():
    return LogisticRegression()