# coding=utf-8

import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.snowball import SpanishStemmer


englishStem = EnglishStemmer()
spanishStem = SpanishStemmer()
regexPattern = re.compile(r'([^\s\w]|_)+')


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    text = regexPattern.sub('', text)
    tokens = word_tokenize(text)
    return tokens


def stem_tokenize(text):
    text = regexPattern.sub('', text)
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, spanishStem)
    return stems


def spanish_tokenize(text):
    text = regexPattern.sub('', text)
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, spanishStem)
    return stems


def english_tokenize(text):
    text = regexPattern.sub('', text)
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, englishStem)
    return stems


def get_vectorizer(isStemming, **kwargs):
    if kwargs.has_key('stopwordPath'):
        # Reading stopwords
        with open(kwargs.get('stopwordPath')) as f:
            sw = f.read().splitlines()

        if (isStemming):
            return CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=stem_tokenize, stop_words=sw)
        else:
            return CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=tokenize, stop_words=sw)
    else:
        if (isStemming):
            return CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=stem_tokenize)
        else:
            return CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=tokenize)


def word_vectorizer(isScore, isStemming, **kwargs):
    params = {"strip_accents": 'unicode', "max_features": 1500}

    if isScore:
        vect = TfidfVectorizer()

        if kwargs.has_key('scoreType'):
            # Setting Score Type
            if kwargs['scoreType'] == 'TF':
                params["use_idf"] = False
            elif kwargs['scoreType'] == 'TF-IDF':
                params["use_idf"] = True
    else:
        vect = CountVectorizer()

        if kwargs.has_key('isBinary'):
            # Setting Binary Frequency
            if kwargs['isBinary']:
                params["binary"] = True
            else:
                params["binary"] = False

    if kwargs.has_key('stopwordPath'):
        # Reading stopwords
        with open(kwargs.get('stopwordPath')) as f:
            sw = f.read().splitlines()
        params["stop_words"] = sw

    if isStemming:
        params["tokenizer"] = stem_tokenize
    else:
        params["tokenizer"] = tokenize

    #print params
    vect.set_params(**params)

    return vect


def word_vectorizer2(**args):
    params = {"strip_accents": 'unicode'}
    prefijo = ''

    # Establecer ponderación de las palabras vectorizadas
    if args.has_key('scoreType'):
        if args['scoreType'] == 'TFIDF':
            vector = TfidfVectorizer()
            params["use_idf"] = True
            prefijo += args.get('scoreType') + '_'
        elif args['scoreType'] == 'TF':
            vector = TfidfVectorizer()
            params["use_idf"] = False
            prefijo += args.get('scoreType') + '_'
        elif args['scoreType'] == 'BTO':
            vector = CountVectorizer()
            params["binary"] = True
            prefijo += args.get('scoreType') + '_'
        elif args['scoreType'] == 'TO':
            vector = CountVectorizer()
            params["binary"] = False
            prefijo += args.get('scoreType') + '_'
        else:
            vector = CountVectorizer()
            params["binary"] = False
            prefijo += args.get('scoreType') + '_'
            print 'ADVERTENCIA: Tipo de ponderación no válido, se usará TO'
    else:
        vector = CountVectorizer()
        params["binary"] = False
        prefijo += 'TO_'
        print 'ADVERTENCIA: Tipo de ponderación no especificado, se usará TO'

    # Establecer tamaño del conjunto de palabras
    if args.has_key('maxFeatures'):
        params["max_features"] = args.get('maxFeatures')
    else:
        params["max_features"] = 1500
        #print 'ADVERTENCIA: No se especifica un máximo de conjunto de palabras, se usarán 1500'

    # Establecer stemming
    if args.has_key('stemming'):
        if args['stemming'] == 'spanish':
            params["tokenizer"] = spanish_tokenize
            prefijo += 'SpanishStem_'
        elif args['stemming'] == 'english':
            params["tokenizer"] = english_tokenize
            prefijo += 'EnglishStem_'
        else:
            params["tokenizer"] = tokenize
            prefijo += 'NoStem_'
            print 'ADVERTENCIA: Stemmer no válido, no se realizará stemming'
    else:
        params["tokenizer"] = tokenize
        prefijo += 'NoStem_'

    # Establecer conjunto de stopwords (opcional)
    if args.has_key('stopwordPath'):
        # Reading stopwords
        with open(args.get('stopwordPath')) as f:
            sw = f.read().splitlines()
        params["stop_words"] = sw
        prefijo += 'Stopwords'
    else:
        prefijo += 'NoStopwords'

    # print params

    vector.set_params(**params)

    return vector, prefijo


# def vectorizer1(object):
#     cv = CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=tokenize)
#     X_train_counts = cv.fit_transform(object.data)
#     X_words = object.target
#     X_labels = object.target_names
#
#     return X_train_counts, X_words, X_labels
#
#
# def vectorizer2(object, stopwords):
#     fsw = open(stopwords, 'r')
#     sw = fsw.readlines()
#     fsw.close()
#
#     cv = CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=tokenize, stop_words=sw)
#     X_train_counts = cv.fit_transform(object.data)
#     X_words = object.target
#     X_labels = object.target_names
#
#     return X_train_counts, X_words, X_labels
#
#
# def vectorizer3(object):
#     cv = CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=stem_tokenize)
#     X_train_counts = cv.fit_transform(object.data)
#     X_words = object.target
#     X_labels = object.target_names
#
#     return X_train_counts, X_words, X_labels
#
#
# def vectorizer4(object, stopwords):
#     fsw = open(stopwords, 'r')
#     sw = fsw.readlines()
#     fsw.close()
#
#     cv = CountVectorizer(strip_accents='unicode', max_features=1500, tokenizer=stem_tokenize, stop_words=sw)
#     X_train_counts = cv.fit_transform(object.data)
#     X_words = object.target
#     X_labels = object.target_names
#
#     return X_train_counts, X_words, X_labels