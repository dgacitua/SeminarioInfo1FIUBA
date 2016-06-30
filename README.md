# Programa de Benchmarks (Análisis de Sentimientos)

Creado por *Daniel Gacitúa Vásquez*

## Introducción

Este programa fue creado como aplicación práctica para el Trabajo Práctico Final de la asignatura **Seminario de Ingeniería Informática I** de la **Facultad de Ingeniería de la Universidad de Buenos Aires**, respecto a la temática de Minería de Datos y el Análisis de Sentimientos en el Idioma Español.

El Trabajo Práctico puede ser consultado en el siguiente link: https://drive.google.com/open?id=0B6aw-J5t480CcUpZQTJZQzM0VFk

## Requisitos del Programa (Dependencias)

- Python 2.7
- Scikit Learn
- NLTK y sus Snowball Stemmers
- Tweepy

## Ejecutar el Programa

El programa se ejecuta en la terminal. De la siguiente manera podemos ver la ayuda:
```sh
$ cd SeminarioInfo1FIUBA
$ python main.py -h
```
```
usage: main.py [-h] [-b] [-g] [-p] [-d PATH] [-s PATH] [-m PATH]
               [-c CLASSIFIER] [-t [THREADS]]

Programa para procesar datasets mediante Análisis de Sentimientos binario

optional arguments:
  -h, --help       show this help message and exit
  -b, --benchmark  Ejecuta el marco de prueba de Clasificadores y Procesadores
                   (Etapa Uno)
  -g, --generate   Crea los modelos necesarios para la Clasificación Fuera de
                   Dominio (Etapa Dos)
  -p, --predict    Predice la clase de un Dataset en base a un Modelo ya
                   creado
  -d PATH          Ruta al directorio donde está el Dataset
  -s PATH          Ruta al archivo donde están las Stopwords
  -m PATH          Ruta al archivo donde está el Modelo guardado
  -c CLASSIFIER    Clasificador a utilizar en el marco de prueba (--benchmark)
  -t [THREADS]     Número de hilos de ejecución (threads) a utilizar
```

Para ejecutar Benchmarks (Etapa Uno del Trabajo Práctico), introducimos el siguiente comando:
```sh
$ python main.py -b -d Datasets/muchocine -s Datasets/spanishStopWords.txt -c NB -t 4
```

Para generar Modelos para la Etapa Dos del Trabajo Práctico, introducimos el siguiente comando:
```sh
$ python main.py -g -d Datasets/muchocine -s Datasets/spanishStopWords.txt
```

Para realizar predicciones con un Modelo ya creado, ejecutamos el siguiente comando:
```sh
$ python main.py -p -d Datasets/muchocine -m Modelos/muchocine_MaxEnt_TFIDF_NoStem_NoStopwords
```

El formato de salida de una predicción es el siguiente:
```
Resultados para muchocine_MaxEnt_TFIDF_NoStem_NoStopwords
[[14871  2762]
 [ 8059 26749]]
             precision    recall  f1-score   support

        neg    0.64854   0.84336   0.73323     17633
        pos    0.90641   0.76847   0.83176     34808

avg / total    0.81970   0.79365   0.79863     52441
```
Primero se indica el nombre del modelo, luego su matriz de confusión y finalmente los resultados puntuados de la evaluación (en Precision, Recall y F1-score).

## Notas del Programa

- Se recomienda leer el Trabajo Práctico base para entender los conceptos clave para el funcionamiento del programa.
- Los clasificadores disponibles (para el parámetro *-c*) son: **NB**, **SVC**, **MaxEnt**, **DT** y **RF**.
- Se pueden usar Rutas Absolutas o Relativas para el acceso a archivos (parámetros *-d*, *-s* y *-m*).
- Los Modelos generados se guardan automáticamente en la carpeta **Modelos**.
- Se recomienda guardar los Datasets en la carpeta **Datasets**.
- Es importante conservar todos los archivos que genera cada modelo, si falta una parte, el modelo no se puede reutilizar.
- Los datasets de entrada deben tener el siguiente formato:
  - Una carpeta con el nombre del dataset
  - Dentro de ella dos carpetas: **neg** y **pos**, en cada una de ellas se ingresarán las entradas negativas y positivas
  - Cada entrada debe ser un archivo de texto plano independiente codificado en UTF-8 (da igual el nombre y la extensión).
- Se ofrecen los siguientes datasets de ejemplo (con el formato antes indicado):
  - [muchocine](https://drive.google.com/open?id=0B6aw-J5t480CUlllcVRkUzM2blE) por *Dr. Fermín L. Cruz Mata*
  - [androidapps](https://drive.google.com/open?id=0B6aw-J5t480Cc0Jra3dyemIxRU0) por *Luciana Dubiau*
  - [restaurante](https://drive.google.com/open?id=0B6aw-J5t480CRE9mTWQ0QzRadFk) por *Luciana Dubiau*

## Licencias

El programa recién descrito se encuentra bajo Licencia MIT. Los datasets de ejemplo son propiedad de sus dueños y se distribuyen respetando sus licencias respectivas.

Copyright (c) 2016 Daniel Gacitúa Vásquez

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.