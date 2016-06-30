# coding=utf-8

from joblib import Parallel, delayed
from os.path import realpath, normpath, basename
from Utilidades.pipelines import *
from Procesadores.clasificadores import *
from Procesadores.importador import *
from Procesadores.vectorizador import *


def trabajadorDisperso(object, vectorizer, classifier, prefix, label):
    pipe = pipelineDisperso(object, vectorizer, classifier)
    name = guardarModelo(pipe, prefix, label)
    evaluarModelo(pipe, object, name)


def trabajadorDenso(object, vectorizer, classifier, prefix, label):
    pipe = pipelineDenso(object, vectorizer, classifier)
    name = guardarModelo(pipe, prefix, label)
    evaluarModelo(pipe, object, name)


def trabajadorConstructor(dataset, vectorizador, clasificador, prefijo, label):
    modelo = pipelineDenso(dataset,vectorizador, clasificador)
    name = guardarModelo(modelo, prefijo, label)


def benchmark(datasetPath, stopwordPath, threads, **args):
    stopwordPath = realpath(stopwordPath)
    datasetPath = realpath(datasetPath)
    prefix = basename(normpath(datasetPath)) + '_'

    print 'Cargando clasificador...'

    if args.has_key('clasificador'):
        if args['clasificador'] == 'NB':
            clf = nuevoNaiveBayes()
            worker = trabajadorDenso
            prefix += 'NB_'
        elif args['clasificador'] == 'SVC':
            clf = nuevoSVC()
            worker = trabajadorDisperso
            prefix += 'SVC_'
        elif args['clasificador'] == 'LinearSVC':
            clf = nuevoLinearSVC()
            worker = trabajadorDisperso
            prefix += 'LinearSVC_'
        elif args['clasificador'] == 'MaxEnt':
            clf = nuevoMaxEnt()
            worker = trabajadorDisperso
            prefix += 'MaxEnt_'
        elif args['clasificador'] == 'DT':
            clf = nuevoDecisionTree()
            worker = trabajadorDisperso
            prefix += 'DecTree_'
        elif args['clasificador'] == 'RF':
            clf = nuevoRandomForest()
            worker = trabajadorDisperso
            prefix += 'RandFor_'
        else:
            clf = nuevoNaiveBayes()
            worker = trabajadorDenso
            prefix += 'NB_'
            print 'ADVERTENCIA: Clasificador no válido, se usará Naive-Bayes'
    else:
        clf = nuevoNaiveBayes()
        worker = trabajadorDenso
        prefix += 'NB_'
        print 'ADVERTENCIA: Clasificador no especificado, se usará Naive-Bayes'

    print 'Creando vectorizadores de palabras...'

    tests_TO = []
    tests_BTO = []
    tests_TF = []
    tests_TFIDF = []

    labels_TO = []
    labels_BTO = []
    labels_TF = []
    labels_TFIDF = []

    v01, p01 = word_vectorizer2(scoreType='TO')
    v02, p02 = word_vectorizer2(scoreType='TO', stopwordPath=stopwordPath)
    v03, p03 = word_vectorizer2(scoreType='TO', stemming='spanish')
    v04, p04 = word_vectorizer2(scoreType='TO', stemming='spanish', stopwordPath=stopwordPath)

    v05, p05 = word_vectorizer2(scoreType='BTO')
    v06, p06 = word_vectorizer2(scoreType='BTO', stopwordPath=stopwordPath)
    v07, p07 = word_vectorizer2(scoreType='BTO', stemming='spanish')
    v08, p08 = word_vectorizer2(scoreType='BTO', stemming='spanish', stopwordPath=stopwordPath)

    v09, p09 = word_vectorizer2(scoreType='TF')
    v10, p10 = word_vectorizer2(scoreType='TF', stopwordPath=stopwordPath)
    v11, p11 = word_vectorizer2(scoreType='TF', stemming='spanish')
    v12, p12 = word_vectorizer2(scoreType='TF', stemming='spanish', stopwordPath=stopwordPath)

    v13, p13 = word_vectorizer2(scoreType='TFIDF')
    v14, p14 = word_vectorizer2(scoreType='TFIDF', stopwordPath=stopwordPath)
    v15, p15 = word_vectorizer2(scoreType='TFIDF', stemming='spanish')
    v16, p16 = word_vectorizer2(scoreType='TFIDF', stemming='spanish', stopwordPath=stopwordPath)

    tests_TO.append(v01)
    tests_TO.append(v02)
    tests_TO.append(v03)
    tests_TO.append(v04)

    labels_TO.append(p01)
    labels_TO.append(p02)
    labels_TO.append(p03)
    labels_TO.append(p04)

    tests_BTO.append(v05)
    tests_BTO.append(v06)
    tests_BTO.append(v07)
    tests_BTO.append(v08)

    labels_BTO.append(p05)
    labels_BTO.append(p06)
    labels_BTO.append(p07)
    labels_BTO.append(p08)

    tests_TF.append(v09)
    tests_TF.append(v10)
    tests_TF.append(v11)
    tests_TF.append(v12)

    labels_TF.append(p09)
    labels_TF.append(p10)
    labels_TF.append(p11)
    labels_TF.append(p12)

    tests_TFIDF.append(v13)
    tests_TFIDF.append(v14)
    tests_TFIDF.append(v15)
    tests_TFIDF.append(v16)

    labels_TFIDF.append(p13)
    labels_TFIDF.append(p14)
    labels_TFIDF.append(p15)
    labels_TFIDF.append(p16)

    print 'Cargando dataset...'
    res = importarDirectorio(datasetPath)

    print 'Ejecutando benchmark...'

    if threads >= 4:
        jobs = 4
        print 'Usando 4 threads'
    elif threads <= 0:
        jobs = -1
        print 'Usando todos los threads disponibles'
    else:
        jobs = threads
        print 'Usando '+ `jobs` + ' threads'

    Parallel(n_jobs=jobs)(delayed(worker)(res, vector, clf, prefix, label) for vector, label in zip(tests_TO, labels_TO))
    Parallel(n_jobs=jobs)(delayed(worker)(res, vector, clf, prefix, label) for vector, label in zip(tests_BTO, labels_BTO))
    Parallel(n_jobs=jobs)(delayed(worker)(res, vector, clf, prefix, label) for vector, label in zip(tests_TF, labels_TF))
    Parallel(n_jobs=jobs)(delayed(worker)(res, vector, clf, prefix, label) for vector, label in zip(tests_TFIDF, labels_TFIDF))

    print 'Benchmark finalizado!'


def prediccion(datasetPath, modelPath):
    modelPath = realpath(modelPath)
    name = basename(normpath(modelPath))

    print 'Cargando dataset...'
    res = importarDirectorio(datasetPath)

    print 'Cargando modelo'
    pipe = cargarModelo(modelPath)

    print 'Ejecutando predicción...'
    predecirModelo(pipe, res, name)

    print 'Evaluación terminada!'


def crearModelos(datasetPath, stopwordPath):
    datasetPath = realpath(datasetPath)
    name = basename(normpath(datasetPath)) + '_'

    print 'Cargando dataset...'
    res = importarDirectorio(datasetPath)

    tests = []
    labels = []
    classifiers = []
    names = []

    v1, p1 = word_vectorizer2(scoreType='TFIDF')
    v2, p2 = word_vectorizer2(scoreType='TFIDF', stemming='spanish', stopwordPath=stopwordPath)

    tests.append(v1)
    tests.append(v2)
    tests.append(v1)
    tests.append(v2)

    labels.append(p1)
    labels.append(p2)
    labels.append(p1)
    labels.append(p2)

    cl1 = nuevoSVC()
    cl2 = nuevoMaxEnt()

    classifiers.append(cl1)
    classifiers.append(cl1)
    classifiers.append(cl2)
    classifiers.append(cl2)

    name1 = name + 'SVC_'
    name2 = name + 'MaxEnt_'

    names.append(name1)
    names.append(name1)
    names.append(name2)
    names.append(name2)

    Parallel(n_jobs=4)(delayed(trabajadorConstructor)(res, vector, clf, n, label) for vector, label, clf, n in zip(tests, labels, classifiers, names))