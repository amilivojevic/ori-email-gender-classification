# -*- coding: utf-8 -*-
"""
Created on Sat Jul 02 18:31:45 2016

@author: Sandra
"""
from __future__ import print_function
import math
from numpy import inf
from parsing2 import *
from feature2_word_length import fit2, predict2

def load_data(male_data, female_data):
    emails = []
    genders = []
    f = open(os.path.join(os.pardir, male_data), 'r')
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
            
            
    f = open(os.path.join(os.pardir, female_data), 'r')
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

def generate_dataset():
    # TODO 1: ucitati podatke iz data/train.tsv datoteke
    # rezultat treba da budu dve liste, texts i sentiments
    
    parse_file("D:\\F\\treca godina\\sesti semestar\\ORI\\data\\musko.mbox","data\\male_dataset.txt")
    parse_file("D:\\F\\treca godina\\sesti semestar\\ORI\\data\\zensko.mbox","data\\female_dataset.txt")
    
    return load_data("data\\male_dataset.txt","data\\female_dataset.txt")
    


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
    
def predict(email, bag_of_words, words_count, emails_count, k = 0):
    words = tokenize(email)                 # tokenizacija teksta
    #counts = count_words(words)            # prebrojavanje reci u tekstu
    
    # broj reci u muskom/zenskom korpusu
    num_of_words_in_corpus = {"male": 0.0, "female": 0.0}
    for gender in words_count:
        num_of_words_in_corpus[gender] += float(sum(words_count[gender].values()))
    
    # broj svih reci u svim mailovima
    num_of_words = float(sum(num_of_words_in_corpus.values()))
 
    # TODO 6: implementiran Naivni Bayes klasifikator za sentiment teksta (recenzije)
    score_female, score_male = 0.0, 0.0
    
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
        if bag_of_words.has_key(word):
            # P(rec)
            word_p = bag_of_words[word] / num_of_words
        
        for gender in p_words.keys():
            if words_count[gender].has_key(word) and words_count[gender][word] > 0:
                # P(rec|pol) = #pojavljivanje te reci u m ili z mailovima + k /  #br reci u m ili z korpusu + k * #br reci u m ili z korpusu
                word_if_gender_p[gender] = (words_count[gender][word] + k) / (num_of_words_in_corpus[gender] + k*len(words_count[gender]))
                #print("word_if_gender_p[{0}] = {1}   word = {2}".format(gender,word_if_gender_p[gender],word))
                # suma logaritama: log( P(rec|pol) / P(rec))
                p_words[gender] += math.log(word_if_gender_p[gender]  / word_p)
                #print("math.log(word_if_gender_p[gender] = {0}   word = {1}".format(math.log(word_if_gender_p[gender]),word))
                 
    #print("p_words['female'] = {0}  ".format(p_words['female']))
    score_male = math.exp(p_words['male'] + math.log(p_gender['male']))
    score_female = math.exp(p_words['female'] + math.log(p_gender['female']))

    male_probability = score_male/(score_female+score_male)
    female_probability = score_female/(score_female+score_male)
 
    return {'male': score_male, 'female': score_female, 'male_probability':male_probability, 'female_probability': female_probability}
    

def detect_overfitting(bag_of_words,words_count):
    male_word_overfitting = {}
    
    for word in bag_of_words.keys():
        #print("word: ",word)
        # P(rec|male) / P(rec|female)
        if words_count["female"].has_key(word) and words_count["female"][word] > 0:
            if words_count["male"].has_key(word) and words_count["male"][word]>0:
                male_word_overfitting[word] = float(words_count["male"][word]) / float(words_count["female"][word])
                #print("words_count[male][{0}] = {1}, words_count[female][{0}] = {2}".format(word,words_count["male"][word], words_count["female"][word]))                
                #print("male_word_overfitting[{0}] = {1}".format(word,male_word_overfitting[word]))
            else:
                male_word_overfitting[word] = 0
                #if male_word_overfitting[word] == 0:
                    #print("{0}, u muskim: {1}, u zenskim: {2}, ratio: {3}".format(word,0, words_count["female"][word], 0))

        else:
            male_word_overfitting[word] = inf
            
        
    return male_word_overfitting
        
        
        
    
if __name__ == '__main__':
    # ucitavanje data seta (sa i bez generisanjem)
    emails, genders = generate_dataset()
    #emails, genders = load_data("data\\male_dataset.txt","data\\female_dataset.txt")

    # izracunavanje / prebrojavanje stvari potrebnih za primenu Naivnog Bayesa
    bag_of_words, words_count, emails_count = fit(emails, genders)

    # recenzija
    #email = 'Vezbe iz C++ su u nedelju, dodjite. Branko'
    email = 'Devojke, sta radite u ponedeljak? Kada vam je ispit? Dragana'

    # klasifikovati sentiment recenzije koriscenjem Naivnog Bayes klasifikatora
    predictions = predict(email, bag_of_words, words_count, emails_count)
    
    print('-'*30)
    print('Email: {0}'.format(email))
    print('Score(male): {0}'.format(predictions['male']))
    print('Score(female): {0}'.format(predictions['female']))
    print('Probability(male): {0}'.format(predictions['male_probability']))
    print('Probability(female): {0}'.format(predictions['female_probability']))
    
    # klasifikovati sentiment recenzije koriscenjem Naivnog Bayes klasifikatora
    predictions = predict(email, bag_of_words, words_count, emails_count, 1)
    print('-'*30)
    print('Laplasova estimacija')
    print('Score(male): {0}'.format(predictions['male']))
    print('Score(female): {0}'.format(predictions['female']))
    print('Probability(male): {0}'.format(predictions['male_probability']))
    print('Probability(female): {0}'.format(predictions['female_probability']))
        
    
    bag_of_words, words_count, emails_count = fit2(emails, genders)
    # klasifikovati sentiment recenzije koriscenjem Naivnog Bayes klasifikatora
    predictions = predict2(email,bag_of_words, words_count, emails_count)
    
    print('-'*30)
    print('Email: {0}'.format(email))
    print('Score(male): {0}'.format(predictions['male']))
    print('Score(female): {0}'.format(predictions['female']))
    
    

