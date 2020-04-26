# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 20:02:25 2020

@author: Toni
"""

import sys

class Metadata:
    def __init__(self):
        self.time_needed = ""
        
        # Practice 1
        self.num_of_files = 0
        self.num_of_tokens = 0
        self.avg_tokens_per_file = 0.0
        self.p1_words_frequency = {}
        
        # Practice 2
        self.num_of_words_after_removing_stopwords = 0
        self.min_num_of_words = sys.maxsize
        self.max_num_of_words = 0
        self.avg_num_of_words_per_file = 0
        self.top_5_frequent_words_before = {}
        self.top_5_frequent_words_after = {}
        self.p2_words_frequency = {}
        
        # Practice 3
        self.num_of_words_after_stemming = 0
        self.min_words_stemming = sys.maxsize
        self.max_words_stemming = 0
        self.avg_words_stemming = 0.0
        self.top_5_frequent_words_after_stemming = {}
        self.p3_words_frequency = {}
    
    def practice1_metadata(self, token_list):
        for word in token_list:
            if word not in self.p1_words_frequency:
                self.p1_words_frequency[word] = 1
            else:
                self.p1_words_frequency[word] += 1
                
        self.num_of_tokens += len(token_list)
    
    def practice2_metadata(self, token_list):
        if (len(token_list) < self.min_num_of_words):
            self.min_num_of_words = len(token_list)
        
        if (len(token_list) > self.max_num_of_words):
            self.max_num_of_words = len(token_list)
        
        for word in token_list:
            if word not in self.p2_words_frequency:
                self.p2_words_frequency[word] = 1
            else:
                self.p2_words_frequency[word] += 1
        
        self.num_of_words_after_removing_stopwords += len(token_list)
                
    def practice3_metadata(self, token_list):
        if (len(token_list) < self.min_words_stemming):
            self.min_words_stemming = len(token_list)
        
        if (len(token_list) > self.max_words_stemming):
            self.max_words_stemming = len(token_list)
        
        for word in token_list:
            if word not in self.p3_words_frequency:
                self.p3_words_frequency[word] = 1
            else:
                self.p3_words_frequency[word] += 1
                
        self.num_of_words_after_stemming += len(token_list)
    
    def sort_dictionary(self, dictionary):
        sorted_dict = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
        return sorted_dict
    
    def final_metadata(self):
        sorted_p1_words = self.sort_dictionary(self.p1_words_frequency)
        self.top_5_frequent_words_before = sorted_p1_words[:5]
        sorted_p2_words = self.sort_dictionary(self.p2_words_frequency)
        self.top_5_frequent_words_after = sorted_p2_words[:5]
        sorted_p3_words = self.sort_dictionary(self.p3_words_frequency)
        self.top_5_frequent_words_after_stemming = sorted_p3_words[:5]
        
        #self.num_of_tokens = len(self.p1_words_frequency)
        #self.num_of_words_after_removing_stopwords = len(self.p2_words_frequency)
        #self.num_of_words_after_stemming = len(self.p3_words_frequency)
        
    def print_metadata(self):
        print("--- Practice 1 ---")
        print("Files: " + str(self.num_of_files))
        print("Tokens: " + str(self.num_of_tokens))
        print("Average tokens per file: " + str(self.avg_tokens_per_file))
        
        print("\n")
        print("--- Practice 2 ---")
        print("Number of words before removing stopwords: " + str(self.num_of_tokens))
        print("Number of words after removing stopwords: " + str(self.num_of_words_after_removing_stopwords))
        print("Min number of words in a file: "+ str(self.min_num_of_words))
        print("Average number of words: " + str(self.avg_num_of_words_per_file))
        print("Max number of words: " + str(self.max_num_of_words))
        print("Top 5 words before:")
        print(self.top_5_frequent_words_before)
        print("Top 5 words after:")
        print(self.top_5_frequent_words_after)
        
        print("\n")
        print("--- Practice 3 ---")
        print("Number of words before stemming: " + str(self.num_of_words_after_removing_stopwords))
        print("Number of words after stemming: " + str(self.num_of_words_after_stemming))
        print("Min number of words in a file: " + str(self.min_words_stemming))
        print("Average number of words: " + str(self.avg_words_stemming))
        print("Max number of words: " + str(self.max_words_stemming))
        print("Top 5 words before stemming:")
        print(self.top_5_frequent_words_after)
        print("Top 5 words after stemming:")
        print(self.top_5_frequent_words_after_stemming)
        
        print("------------------")
        print("Time needed: " + self.time_needed)