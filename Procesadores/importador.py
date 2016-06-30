# coding=utf-8

import arff
from sklearn.datasets import load_files
from os.path import realpath, normpath, basename


def importarArff(filePath):
    with open(filePath, 'r') as myfile:
        text = myfile.read()

    obj = arff.loads(text)
    return obj


def importarDirectorio(dirPath):
    dirPath = realpath(dirPath)
    name = basename(normpath(dirPath))
    obj = load_files(dirPath, encoding='utf-8')
    print 'Dataset cargado: ' + name
    return obj