# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:10:49 2020

@author: Toni
"""
import re
from nltk import TreebankWordTokenizer

class NormalizationTokenization:
    def __init__(self):
        self.letters_mappings = { u"á" : "a", 
                                  u"é" : "e", 
                                  u"í" : "i",
                                  u"ó" : "o",
                                  u"ú" : "u",
                                  u"ñ" : "n",
                                  u"ü" : "u" }
        self.tokenizer = TreebankWordTokenizer()
        
    def letter_without_accent(self, letter):
        'This method returns the version of a letter without accent'
        if letter in self.letters_mappings:
            return self.letters_mappings[letter]
        else:
            return letter
    
    def normalize(self, text):
        '''This method returns normalized version of the text.
        It removes all disallowed characters and makes the text lower case'''
        text = text.lower()
        mapIterator = map(lambda letter: self.letter_without_accent(letter), text)
        text = "".join(mapIterator)
        
        regex = r'[^a-zA-Z0-9\s\_\-\n]'
        text = re.sub(regex, '', text)
        return text
    
    def tokenize(self, text):
        'This method returns the text diveded to tokens'
        return self.tokenizer.tokenize(text)
    
    def process_text(self, text):
        '''This method is the main method of this class. 
        It processes the text and returns the result'''
        normalized_text = self.normalize(text)
        token_list = self.tokenize(normalized_text)
        return token_list