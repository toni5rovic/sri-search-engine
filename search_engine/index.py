# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:55:23 2020

@author: Toni
"""
import os 
import math

from timeit import default_timer as timer
from index_info import IndexInfo
from log_info import LogInformation

class Index:
    def __init__(self, stemmer_output, w_dict, f_dict, index_folder, export_log=False):
        self.word_dictionary = w_dict
        self.file_dictionary = f_dict
        self.stemmer_output = stemmer_output
        self.dictionary = {}
        self.norm_per_file = {}
        self.export_log = export_log
        self.index_output_folder = index_folder
    
    def create_index(self):
        '''This method creates the index structure and 
        calculates all the necessary values
        '''
        start = timer()
        self.process_files()
        self.calculate_tf()
        self.calculate_weights()
        self.calculate_normalized_weights()
        end = timer()

        time_needed = end - start
        if self.export_log == True:
            log_file = os.path.join(self.index_output_folder, "log.txt")
            log = LogInformation(log_file)
            log.time_needed = str(time_needed)
            log.memory_usage = log.getsize(self)
            log.export_log()
    
    def add_word(self, file_id, word):
        '''This method adds the word to the word dictionary if 
        it is not already there. If it is there already, then the 
        file is added.
        '''
        word_id = self.word_dictionary.add_word(word)
        if word_id in self.dictionary:
            entry = self.dictionary.get(word_id)
            entry.add_file(file_id)
        else:
            entry = IndexInfo(self.word_dictionary)
            entry.add_file(file_id)
            self.dictionary[word_id] = entry
        
    def process_files(self):
        'This method processes all the files from the stemmer output.'
        for file in os.listdir(self.stemmer_output):
            file_name = os.fsdecode(file)
            full_path = os.path.join(self.stemmer_output, file_name)
            
            with open(full_path, 'r') as file_:
                token_list = file_.readlines()
                
            token_list = list(map(lambda x: x.replace('\n', ''), token_list))
            
            for token in token_list:
                file_id = self.file_dictionary.add_file(full_path)
                self.add_word(file_id, token)
            
    def calculate_tf(self):
        'This method calculates the term frequencies.'
        maximum_frequency_per_file = self.get_max_frequencies()
     
        for word_id, index_info in self.dictionary.items():
            for file_id, word_file_pair in index_info.dictionary.items():
                word_file_pair.tf = index_info.get_frequency(file_id) / maximum_frequency_per_file[file_id] 
                
    def get_max_frequencies(self):
        '''This method returns dictioanry with key: file_id, and the value:
        max frequency of the file.
        '''
        max_frequency_per_file = {}
        for word_id, index_info in self.dictionary.items():
            for file_id, word_file_pair in index_info.dictionary.items():
                if file_id in max_frequency_per_file:
                    current_max = max_frequency_per_file[file_id]
                    if (word_file_pair.frequency > current_max):
                        max_frequency_per_file[file_id] = word_file_pair.frequency
                else:
                    max_frequency_per_file[file_id] = word_file_pair.frequency
        
        return max_frequency_per_file
    
    def calculate_weights(self):
        'This method calculates weights for all words in all files.'
        self.calculate_idfs()
        for word_id, index_info in self.dictionary.items():
            for file_id, word_file_pair in index_info.dictionary.items():
                #word_file_pair.w = word_file_pair.tf * idfs[word_id]
                word_file_pair.w = word_file_pair.tf * self.dictionary[word_id].idf
            
    
    def calculate_idfs(self):
        'This method calculates the idfs and stores them'
        num_of_files = self.file_dictionary.get_num_of_files()
        for word_id, index_info in self.dictionary.items():
            num_of_files_per_word = len(index_info.dictionary)
            self.dictionary[word_id].idf = math.log2((1 + num_of_files) / (1 + num_of_files_per_word)) + 1
        
    def calculate_normalized_weights(self):
        'This method calculated the normalized weights and stores them'
        self.get_norm_per_file()
        
        for word_id, index_info in self.dictionary.items():
            for file_id, word_file_pair in index_info.dictionary.items():
                word_file_pair.wn = word_file_pair.w / self.norm_per_file[file_id]
            
    def get_norm_per_file(self):
        '''This method calculates the square roots of sums of all the squared weights
        of the words found in a given file. Also, this method stores these values
        in the dictionary.'''
        self.norm_per_file = {}        
        for word_id, index_info in self.dictionary.items():
            for file_id, word_file_pair in index_info.dictionary.items():
                if file_id not in self.norm_per_file:
                    self.norm_per_file[file_id] = 0
                
                self.norm_per_file[file_id] += pow(word_file_pair.w, 2)
        
        for file_id, value in self.norm_per_file.items():
            self.norm_per_file[file_id] = math.sqrt(self.norm_per_file[file_id])
        
    def export(self, output_path):
        file_hook = open(output_path, 'w', encoding='utf-8')
        file_hook.write(str(len(self.dictionary)))
        file_hook.write('\n')
        
        for word_id, index_info in self.dictionary.items():
            file_hook.write('\n')
            file_hook.write("Word: " + str(word_id))
            file_hook.write('\n')
            
            index_info.export(file_hook)
            file_hook.write("------------------------")
        
        file_hook.close()