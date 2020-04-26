# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 01:16:50 2020

@author: Toni
"""
from pickle import dump, load
import os, sys

class Exporter:
    def __init__(self):
        self.word_dictionary_filename = "word_dictionary.bin"
        self.file_dictionary_filename = "file_dictionary.bin"
        self.index_filename = "index.bin"

    def export_objects(self, folderpath, word_dictionary, file_dictionary, index):
        'This method exports index, file dictionary and word dictionary'
        with open(os.path.join(folderpath, self.word_dictionary_filename), "wb") as file:
            dump(word_dictionary, file)
        with open(os.path.join(folderpath, self.file_dictionary_filename), "wb") as file:
            dump(file_dictionary, file)
        with open(os.path.join(folderpath, self.index_filename), "wb") as file:
            dump(index, file)
            
    def import_objects(self, folderpath):
        'This method improts objects from files and returns them'
        with open(os.path.join(folderpath, self.word_dictionary_filename), "rb") as file:
            word_dictionary = load(file)
        with open(os.path.join(folderpath, self.file_dictionary_filename), "rb") as file:
            file_dictionary = load(file)
        with open(os.path.join(folderpath, self.index_filename), "rb") as file:
            index = load(file)
        return word_dictionary, file_dictionary, index