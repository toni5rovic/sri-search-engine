# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:42:11 2020

@author: Toni
"""

class WordDictionary:
    def __init__(self):
        self.dict = {}
    
    def add_word(self, word):
        if word not in self.dict:
            word_id = hash(word)
            self.dict[word] = word_id
            return word_id
        else:
            return self.dict[word]
   
    def get_word_id(self, word):
        return self.dict.get(word)  