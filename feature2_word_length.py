# -*- coding: utf-8 -*-
"""
Created on Sun Jul 03 15:42:11 2016

@author: Sandra
"""

from __future__ import print_function
import math
from parsing2 import *

def tokenize(text):
    text = preprocess(text)
    # TODO 3: implementirana tokenizacija teksta na reci
    # rezultat treba da bude lista reci koje se nalaze u datom tekstu
    words = text.split(' ')

    return words

def calculate_words_length(text):
    # Ako smo vec prosledili listu, nije potrebna tokenizacija
    if isinstance(text, list):
        words = text
    else:
        words = tokenize(text)

    words_length = {}    
    
    for word in words:
        length = len(word)
        if words_length.has_key(length):
            words_length[length] += 1
        else:
            words_length[length] = 1
            
    return words_length
    
    
def fit2(emails, genders):
        
    # inicijalizacija struktura
    bag_of_words = {}               # bag-of-words za sve emailove
    words_length = {'male': {},       # isto bag-of-words, ali posebno za muske i zenske emialove
                   'female': {}}
    emails_count = {'male': 0.0,      # broj muskih i zenskih emailova
                   'female': 0.0}
    
    for email, gender in zip(emails, genders):
        length_dict = calculate_words_length(email)
        
        for length, count in length_dict.iteritems():
            # Iteriramo kroz duzine reci za dati mail i dodajemo u listu svih duzina
            if bag_of_words.has_key(length):
                bag_of_words[length] += count
            else:
                bag_of_words[length] = count
            
            # Dodajemo rijec u odgovarajuci rjecnik - pozitivnih ili negativnih recenzija    
            if words_length[gender].has_key(length):
                words_length[gender][length] += count
            else:
                words_length[gender][length] = count
        
        # Uvecamo broj pozitivnih ili negativnih recenzija
        emails_count[gender] += 1
    
    return bag_of_words, words_length, emails_count    
    
    
def predict2(email, bag_of_words, words_count, emails_count):
    words = tokenize(email)                 # tokenizacija teksta
    #counts = count_words(words)            # prebrojavanje reci u tekstu
    
    # broj reci u muskom/zenskom korpusu
    num_of_words_in_corpus = {"male": 0.0, "female": 0.0}
    for gender in words_count:
        num_of_words_in_corpus[gender] += float(sum(words_count[gender].values()))
    
    # broj svih reci u svim mailovima
    num_of_words = float(sum(num_of_words_in_corpus.values()))
 
    # TODO 6: implementiran Naivni Bayes klasifikator za sentiment teksta (recenzije)
    score_pos, score_neg = 0.0, 0.0
    
    # P(pol) = #m ili z mailovi / #svi mailovi
    p_gender = {"male": 0.0, "female": 0.0}
    # broj svih emailova
    all_mails_count = emails_count["male"] + emails_count["female"]
    # P(male)
    p_gender["male"] = emails_count["male"] / all_mails_count
    # P(female)
    p_gender["female"] = emails_count["female"] / all_mails_count
    
    
    p_words = {"male": 0.0, "female":0.0}
    word_if_gender_p = {"male": 0.0, "female":0.0}
    for word in words:
        # P(rec)
        word_len = len(word)
        word_p = bag_of_words[word_len] / num_of_words
        
        for gender in p_words.keys():
            if words_count[gender].has_key(word_len) and words_count[gender][word_len] > 0:
                # P(rec|pol)
                word_if_gender_p[gender] = words_count[gender][word_len] / num_of_words_in_corpus[gender]
                # suma logaritama: log( P(rec|pol) / P(rec))
                p_words[gender] += math.log(word_if_gender_p[gender] / word_p)
    
    
    score_pos = math.exp(p_words['male'] + math.log(p_gender['male']))
    score_neg = math.exp(p_words['female'] + math.log(p_gender['female']))
        
 
    return {'male': score_pos, 'female': score_neg}
    

