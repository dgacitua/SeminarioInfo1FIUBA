# coding=utf-8

import codecs
import tidylib
import xml.etree.ElementTree as ET
from genericpath import exists
from os import listdir, makedirs
from os.path import isfile, join, realpath, splitext


xstr = lambda s: s or ''


def obtenerCodificacion(s):
    return (type(s), s)


def procesarArchivoXML(path):
    tree = ET.parse(path)
    return tree.getroot()


def procesarStringXML(string):
    return ET.fromstring(string)


def importarMuchoCine(path, newPath):
    data = []
    target = []
    target_names = ['neg', 'pos']
    filenames = []

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    for file in onlyfiles:
        route = realpath(join(path, file))
        filename = splitext(file)[0]

        with open(route, 'r') as myfile:
            temp1 = myfile.read()
            temp2 = tidylib.tidy_document(temp1, {'input_xml': True, 'output_xml': True})[0]

        root = ET.XML(temp2)

        rank = int(root.get('rank'))
        summary = xstr(root.find('summary').text)
        body = xstr(root.find('body').text)

        if rank <=2 or rank >=4:
            if rank <= 2:
                sentiment = 'neg'
                rankTarget = 0
            elif rank >= 4:
                sentiment = 'pos'
                rankTarget = 1
            else:
                sentiment = 'neu'
                rankTarget = 3

            content1 = (summary + ' ' + body)
            content2 = content1.encode('utf-8')

            data.append(content2)
            target.append(rankTarget)
            filenames.append(filename)

            newFilePath = join(newPath,sentiment)

            if not exists(newFilePath):
                makedirs(newFilePath)

            newFile = open(join(newFilePath,filename),'w')
            newFile.write(content2)
            newFile.close()

    ret = {'data': data, 'filenames': filenames, 'target': target, 'target_names': target_names}

    return ret
