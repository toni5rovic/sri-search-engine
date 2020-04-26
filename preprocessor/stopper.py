# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 23:45:28 2020

@author: Toni
"""
import os.path

class Stopper:
    def __init__(self):
        self.letters_mappings = { u"á" : "a", 
                                  u"é" : "e", 
                                  u"í" : "i",
                                  u"ó" : "o",
                                  u"ú" : "u",
                                  u"ñ" : "n",
                                  u"ü" : "u" }
        self.stopwords_file_1 = "spanishSmart.txt"
        self.stopwords_file_2 = "spanishST.txt"
        self.stopwords = []
    
    def letter_without_accent(self, letter):
        'This method returns version of a letter without accent'
        if letter in self.letters_mappings:
            return self.letters_mappings[letter]
        else:
            return letter
        
    def load_stopwords(self, stopwords_folder):
        'This method loads two lists of stopwords and joins them'
        ### first file
        full_path = os.path.join(stopwords_folder, self.stopwords_file_1)
        with open(full_path, 'r', encoding='utf8') as file:
            content = file.read()
        
        # replacing all accented letters with their versions without accent
        content = ''.join(map(lambda letter: self.letter_without_accent(letter), content))
        # list of words
        file_1_stopwords = content.split('\n')
        
        ### second file
        full_path = os.path.join(stopwords_folder, self.stopwords_file_2)
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = ''.join(map(lambda letter: self.letter_without_accent(letter), content))
        file_2_stopwords = content.split('\n')
        
        all_stopwords = file_1_stopwords + file_2_stopwords
        all_stopwords = list(set(all_stopwords))
        self.stopwords = all_stopwords
        
    def remove_stopwords(self, tokens):
        'This method removes stopwords from the list of tokens'
        # removing stopwords from token list
        tokens_without_stopwords = []
        for token in tokens: 
            if token not in self.stopwords:
                tokens_without_stopwords.append(token)
        return tokens_without_stopwords