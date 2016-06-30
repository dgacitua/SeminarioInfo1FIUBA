# coding=utf-8

from Utilidades.DenseTransformer import DenseTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict
from sklearn.externals import joblib

def pipelineDenso(object, vectorizer, classifier):
    data = object.data
    target = object.target
    labels = object.target_names

    dt = DenseTransformer()

    pipe = Pipeline([('vect', vectorizer),
                    ('dense', dt),
                    ('clf', classifier)])
    pipe.fit(data, target)

    return pipe


def pipelineDisperso(object, vectorizer, classifier):
    data = object.data
    target = object.target
    labels = object.target_names

    pipe = Pipeline([('vect', vectorizer),
                    ('clf', classifier)])
    pipe.fit(data, target)

    return pipe


def guardarModelo(pipe, prefix, label):
    nombre = prefix + label
    joblib.dump(pipe, "Modelos/" + nombre)
    print "Modelo guardado: " + nombre
    return nombre


def cargarModelo(filePath):
    pipe = joblib.load(filePath)
    print "Modelo cargado: " + filePath
    return pipe


def evaluarModelo(pipe, object, name):
    data = object.data
    target = object.target
    labels = object.target_names

    pred = cross_val_predict(pipe, data, target, cv=10, n_jobs=1)

    print "Resultados para " + name
    print confusion_matrix(target, pred)
    print classification_report(target, pred, target_names=labels, digits=5)


def predecirModelo(pipe, object, name):
    data = object.data
    target = object.target
    labels = object.target_names

    pred = pipe.predict(data)

    print "Resultados para " + name
    print confusion_matrix(target, pred)
    print classification_report(target, pred, target_names=labels, digits=5)