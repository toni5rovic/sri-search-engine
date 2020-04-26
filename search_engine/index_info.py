# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:59:26 2020

@author: Toni
"""

from word_file_pair import WordFilePair

class IndexInfo:
    def __init__(self, word_dictionary):
        #self.word_dictionary = word_dictionary
        self.dictionary = {}
        self.idf = 0
    
    def add_file(self, file_id):
        '''This method adds file_id to the dictionary if it doesn\'t exist
        and sets the frequency to 1. If it already exists, frequency is incremented.
        '''
        if file_id not in self.dictionary:
            word_file_pair = WordFilePair()
            word_file_pair.frequency = 1
            self.dictionary[file_id] = word_file_pair
        else:
            word_file_frequency = self.dictionary[file_id]
            word_file_frequency.frequency += 1
    
    def get_frequency(self, file_id):
        'This method returns the frequency for the given file_id'
        word_file_pair = self.dictionary.get(file_id)
        return word_file_pair.frequency
    
    def export(self, file_hook):
        file_hook.write("\n")
        file_hook.write("IDF: " + str(self.idf))
        for file_id, word_file_pair in self.dictionary.items():
            file_hook.write("\t" + str(file_id) + "\n")
            self.dictionary[file_id].export(file_hook)
            file_hook.write("\n")