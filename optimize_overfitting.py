# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 17:53:51 2016

@author: Sandra
"""

from bayes import *
from copy import deepcopy

def check_predition():
    emails, genders = load_data("data\\male_dataset.txt","data\\female_dataset.txt") 
    f = open(os.path.join(os.pardir, "data\\check_prediction_path.txt"),"a")
    emails_copy = []
    genders_copy = []
    ok = [0,0,0,0,0]
    for k in [0, 1, 2, 3, 4]:
        
        i = 0
        
        for email in emails:
            
            #trebalo bi obrisati email iz emails  
            index = emails.index(email)
            emails_copy = deepcopy(emails)
            genders_copy = deepcopy(genders)
            emails_copy = emails_copy[:index] + emails_copy[index+1 :]
            real_gender = genders[index]
            genders_copy = genders_copy[:index] + genders_copy[index+1 :] 
            bag_of_words, words_count, emails_count = fit(emails_copy, genders_copy)
            p = predict(email, bag_of_words, words_count, emails_count,k)
            
            if p[real_gender + "_probability"] > 0.5:
                f.write("{0}. marked gender: {1:6}, male prob: {2:10}, female prob: {3:10}, OK!!!\n".format(i,real_gender, p["male_probability"], p["female_probability"]))   
                ok[k] += 1
            else:
                f.write("{0}. marked gender: {1:6}, male prob: {2:10}, female prob: {3:10}\n".format(i,real_gender, p["male_probability"], p["female_probability"]))                
            i += 1
    f.close()
    return ok, i
    
if __name__ == '__main__':
    ok, i = check_predition()
    print("velicina dataset-a: ", i)
    for k in [0,1,2,3,4]:
        print("k={0} prosli test: {1}".format(k,ok[k]))