# -*- coding: utf-8 -*-
"""
Created on Sat Jul 02 18:31:45 2016

@author: Sandra
"""
from __future__ import print_function
import math
from parsing2 import *

def load_data():
    # TODO 1: ucitati podatke iz data/train.tsv datoteke
    # rezultat treba da budu dve liste, texts i sentiments
    emails, genders = [], []
    
    parse_file("D:\\F\\treca godina\\sesti semestar\\ORI\\data\\musko.mbox","male_dataset.txt")
    parse_file("D:\\F\\treca godina\\sesti semestar\\ORI\\data\\zensko.mbox","female_dataset.txt")
          
    f = open("male_dataset.txt", 'r')
    lines = f.readlines()
    f.close()
    email = ""
    separator = "=================================="
    for i,line in enumerate(lines):
        if separator in line:
            emails.append(email)
            genders.append("male")            
            email = ""
        else:
            email += line
            
            
    f = open("female_dataset.txt", 'r')
    lines = f.readlines()
    f.close()
    email = ""
    for i,line in enumerate(lines):
        if separator in line:
            emails.append(email)
            genders.append("female")            
            email = ""
        else:
            email += line
        

    return emails, genders
    


def tokenize(text):
    text = preprocess(text)
    # TODO 3: implementirana tokenizacija teksta na reci
    # rezultat treba da bude lista reci koje se nalaze u datom tekstu
    words = text.split(' ')

    return words
    
    

def count_words(text):
    # Ako smo vec prosledili listu, nije potrebna tokenizacija
    if isinstance(text, list):
        words = text
    else:
        words = tokenize(text)
        
    # TODO 4: implementirano prebrojavanje reci u datom tekstu
    # rezultat treba da bude mapa, ciji kljucevi su reci, a vrednosti broj ponavljanja te reci u datoj recenici
    words_count = {}
    for word in words:
        if words_count.has_key(word):
            words_count[word] += 1
        else:
            words_count[word] = 1
            
    return words_count
    
    

def fit(emails, genders):
    # inicijalizacija struktura
    bag_of_words = {}               # bag-of-words za sve recenzije
    words_count = {'male': {},       # isto bag-of-words, ali posebno za pozivitne i negativne recenzije
                   'female': {}}
    emails_count = {'male': 0.0,      # broj tekstova za pozivitne i negativne recenzije
                   'female': 0.0}

    # TODO 5: proci kroz sve recenzije i sentimente i napuniti gore inicijalizovane strukture
    # bag-of-words je mapa svih reci i broja njihovih ponavljanja u celom korpusu recenzija
    
    for email, gender in zip(emails, genders):
        email_dict = count_words(email)
        
        for word, count in email_dict.iteritems():
            # Iteriramo kroz svaku rijec za dati tekst i dodajemo u listu svih rijeci
            if bag_of_words.has_key(word):
                bag_of_words[word] += count
            else:
                bag_of_words[word] = count
            
            # Dodajemo rijec u odgovarajuci rjecnik - pozitivnih ili negativnih recenzija    
            if words_count[gender].has_key(word):
                words_count[gender][word] += count
            else:
                words_count[gender][word] = count
        
        # Uvecamo broj pozitivnih ili negativnih recenzija
        emails_count[gender] += 1
    
    return bag_of_words, words_count, emails_count
    
    
    
    
def predict(email, bag_of_words, words_count, emails_count):
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
        word_p = bag_of_words[word] / num_of_words
        
        for gender in p_words.keys():
            if words_count[gender].has_key(word) and words_count[gender][word] > 0:
                # P(rec|pol)
                word_if_gender_p[gender] = words_count[gender][word] / num_of_words_in_corpus[gender]
                # suma logaritama: log( P(rec|pol) / P(rec))
                p_words[gender] += math.log(word_if_gender_p[gender] / word_p)
    
    
    score_pos = math.exp(p_words['male'] + math.log(p_gender['male']))
    score_neg = math.exp(p_words['female'] + math.log(p_gender['female']))
        
 
    return {'male': score_pos, 'female': score_neg}
    
    
if __name__ == '__main__':
    # ucitavanje data seta
    emails, genders = load_data()

    # izracunavanje / prebrojavanje stvari potrebnih za primenu Naivnog Bayesa
    bag_of_words, words_count, emails_count = fit(emails, genders)

    # recenzija
    email = 'Vezbe iz C++ su u nedelju, dodjite. Branko'

    # klasifikovati sentiment recenzije koriscenjem Naivnog Bayes klasifikatora
    predictions = predict(email, bag_of_words, words_count, emails_count)
    
    print('-'*30)
    print('Email: {0}'.format(email))
    print('Score(male): {0}'.format(predictions['male']))
    print('Score(female): {0}'.format(predictions['female']))
