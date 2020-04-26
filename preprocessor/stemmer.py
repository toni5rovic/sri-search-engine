# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:10:55 2020

@author: Toni
"""

from nltk.stem import SnowballStemmer

class Stemmer:
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish', ignore_stopwords=True)
        self.letters_mappings = { "a" : [u"á"], 
                                  "e" : [u"é"], 
                                  "i" : [u"í"],
                                  "o" : [u"ó"],
                                  "u" : [u"ú", u"ü"],
                                  "n" : [u"ñ"] }
        
    def get_stems(self, tokens):
        'This method returns the stems of all the tokens in the list. '
        stems = []
        for token in tokens:
            stem = self.stem(token)
            stems.append(stem)
            
        return stems
    
    def stem(self, token):
        '''This method stems one token. Firstly, it creates all the accented
        versions of the token, and then stems each one, choosing the shortest
        for the result.
        '''
        token_versions = self.get_versions(token)
        min_stem = self.stemmer.stem(token_versions[0])
        for version in token_versions:
            current_stem = self.stemmer.stem(version)
            if (len(current_stem) < len(min_stem)):
                min_stem = current_stem
        
        return min_stem
    
    def get_versions(self, token):
        '''This method returns versions of the token. The versions are created
        by replacing all the vowels and the letter _n_ with its accented versions.'''
        versions = []
        versions.append(token)
        index = 0
        for letter in token:
            if letter in self.letters_mappings:
                accented_letter_list = self.letters_mappings[letter]
                for letter_with_accent in accented_letter_list:
                    version = token[:index] + letter_with_accent + token[(index+1):]
                    versions.append(version)
            index += 1
            
        return versions
