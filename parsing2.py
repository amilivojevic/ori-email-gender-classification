# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:54:17 2016

@author: Sandra
"""

import re, string, math

path = "D:\\F\\treca godina\\sesti semestar\\ORI\\data\\musko.mbox"
#path = "D:\\F\\treca godina\\sesti semestar\\ORI\\PROJEKAT\\proba.txt"

def parse_file(path,dataset_path):
    f = open(path, 'r')
    f2 = open(dataset_path,"a")
    lines = f.readlines()
    f.close()
    i = 0     
    plain = False
    plainContentType = False
    headerWrote = False
    
    
    
    for i,line in enumerate(lines):
        #print line
        if plainContentType:
            #samo na pocetku, da se ispise zaglavlje poruke
            if not headerWrote:
                print "***NOVA PORUKA:"
                f2.write("==================================")
                f2.writelines("\n")
                f2.writelines("\n")
                headerWrote = True
                
            #ako je stigao do From ili do html-a, zavrsi poruku
            if line.startswith(">") or "From" in line or ("--" in line and "Content-Type: text/html;" in lines[i+2]) or ("--" in line and "Content-Type: text/html;" in lines[i+1]) or (("--" in line and "Content-Type: image/jpeg;" in lines[i+1])) or ("Content-Disposition: attachment;" in lines[i+1]):
                plain = False
                plainContentType = False
                headerWrote = False
            else:
                #ako nije stigao do kraja
                if len(line)>1 and not any([line.startswith(s) for s in ["This is a copy of a message sent to","X-","=20","Date: ","Content","--",">"]]) and not any([s in line for s in ["You received this email because","To change or turn off email notifications","charset","format=flowed","2013/","2012/","2011/","https:/","http:"]]): 
                        f2.write(line)                    
                        print line
                        
            
        if line.startswith("--"):
            plain = True
        
        if plain and "Content-Type: text/plain;" in line:
            plainContentType = True
    
    
    f2.write("\n==================================")
    f2.close()
    
def preprocess(text):
    # preprocesiranje teksta
    # - izbacivanje znakova interpunkcije
    # - svodjenje celog teksta na mala slova
    # ubacivanje slova c,s,z,s,dj umesto č,ć,ž,š,đ
    # rezultat treba da bude preprocesiran tekst
    serbian_letters_map = [("=C5=BE","z"),("=BE","z"),("=C4=87","c"),("=E6","c"),("=C4=8C","c"),("=C4=8D","c"),("=E8","c"),("=C5=A0","s"),("=C5=A1","s"),("=B9","s"),("=A9","s"),("=F0","dj"),("=D0","dj")]
    for k,v in serbian_letters_map:
        text = text.replace(k,v)
        
    text = text.lower()
    text = re.sub('[^a-zA-Z]+', ' ', text).strip()
    print text
    return text

            
parse_file(path,"datasetprobni.txt")
preprocess("odr=C5=BEavanja laboratorijskih ve=C5=BEbi.")