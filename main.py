# -*- coding: utf-8 -*-

import argparse
from Utilidades.benchmarks import *
from Utilidades.twitter import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programa para procesar datasets mediante Análisis de Sentimientos binario')

    parser.add_argument('-b', '--benchmark', action='store_true', help='Ejecuta el marco de prueba de Clasificadores y Procesadores (Etapa Uno)')
    parser.add_argument('-g', '--generate', action='store_true', help='Crea los modelos necesarios para la Clasificación Fuera de Dominio (Etapa Dos)')
    parser.add_argument('-p', '--predict', action='store_true', help='Predice la clase de un Dataset en base a un Modelo ya creado')

    parser.add_argument('-d', metavar='PATH', help='Ruta al directorio donde está el Dataset')
    parser.add_argument('-s', metavar='PATH', help='Ruta al archivo donde están las Stopwords')
    parser.add_argument('-m', metavar='PATH', help='Ruta al archivo donde está el Modelo guardado')
    parser.add_argument('-c', metavar='CLASSIFIER', help='Clasificador a utilizar en el marco de prueba (--benchmark)')
    parser.add_argument('-t', nargs='?', const=4, default=4, type=int, metavar='THREADS', help='Número de hilos de ejecución (threads) a utilizar')

    args = parser.parse_args()

    if args.benchmark==True:
        if args.d and args.s and args.c:
            datasetPath = args.d
            sw_path = args.s
            classifier = args.c
            threads = args.t
            print 'Ejecutando Benchmark con ' + datasetPath + ', con las Stopwords ' + sw_path + ', el Clasificador ' + classifier + ' y ' + `threads` + ' hilos de ejecución'
            benchmark(datasetPath, sw_path, threads, clasificador=classifier)
        else:
            print 'ERROR! Se necesita un Dataset, un Archivo de Stopwords y un Clasificador'
    elif args.generate==True:
        if args.d and args.s:
            datasetPath = args.d
            sw_path = args.s
            print 'Creando Modelos con ' + datasetPath + ' y las Stopwords ' + sw_path
            crearModelos(datasetPath, sw_path)
        else:
            print 'ERROR! Se necesita un Dataset y un Archivo de Stopwords'
    elif args.predict==True:
        if args.d and args.m:
            datasetPath = args.d
            model_path = args.m
            print 'Realizando predicciones en ' + datasetPath + ' con el Modelo ' + model_path
            prediccion(datasetPath, model_path)
        else:
            print 'ERROR! Se necesita un Dataset y un Modelo Guardado'
    else:
        print 'ERROR! No se ha indicado una acción válida'
