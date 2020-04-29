# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:46:28 2020

@author: Toni
"""
import os
import math

from query_word_info import QueryWordInfo
from preprocessor import Preprocessor

class QueryHandler:
    def __init__(self, rootPath, index, word_dict, file_dict):
        self.dictionary = {}
        self.norm_for_query = -1
        self.similarities = {}
        self.similarities_to_show = {}
        self.index = index
        self.preprocessor = Preprocessor(rootPath=rootPath)
        
        self.word_dictionary = word_dict
        self.file_dictionary = file_dict
        self.time_needed = None
        self.number_of_results = 0
        
    def print_idfs(self):
        for word_id, index_info in self.index.dictionary.items():
            print("IDF: " + str(index_info.idf))
    
    def sort_dictionary(self, dictionary):
        sorted_dict = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
        return sorted_dict

    def process_query(self, query, max_number_of_docs, PRF = True):
        if PRF == False:
            return self.process_query_default(query, max_number_of_docs)
        
        return self.process_query_with_PRF(query, max_number_of_docs)

    def process_query_with_PRF(self, query, max_number_of_docs):
        N_files = 5
        N_terms = 5

        similarities_first_run = self.process_query_default(query, max_number_of_docs)
        sorted_first_run = self.sort_dictionary(similarities_first_run)
        similarities_first_run = dict(sorted_first_run[:N_files])

        new_query = query
        for file_id, _ in similarities_first_run.items():
            top_words = self.get_top_words(file_id, N_terms)
            for word, _ in top_words.items():
                new_query += " " + word
        print(new_query)
        
        self.similarities = {}
        self.similarities_to_show = {}
        similarities_second_run = self.process_query_default(new_query, max_number_of_docs)
        return similarities_second_run

    def get_top_words(self, file_id, num_of_top_words):
        all_words = {}
        for word_id, index_info in self.index.dictionary.items():
            word_file_pair = index_info.dictionary.get(file_id)
            if word_file_pair != None:
                # in word_dictionary pairs are word:id
                word = next(key for key, value in self.word_dictionary.dict.items() if value == word_id)
                all_words[word] = word_file_pair.frequency
        
        sorted_words = self.sort_dictionary(all_words)
        return dict(sorted_words[:num_of_top_words])

    def process_query_default(self, query, max_number_of_docs):
        tokens = self.preprocessor.preprocess_text(query)
        
        self.fill_dictionary(tokens)
        
        self.calculate_tfs()
        self.calculate_weights()
        self.calculate_normalized_weights()
        
        self.find_similarities()
        
        self.sorted_similarities = self.sort_dictionary(self.similarities)
        self.similarities_to_show = dict(self.sorted_similarities[:max_number_of_docs])

        return dict(self.sorted_similarities)
        
    def fill_dictionary(self, tokens):
        for token in tokens:
            word_id = self.word_dictionary.add_word(token)
            if word_id not in self.dictionary:
                wordInfo = QueryWordInfo()
                wordInfo.frequency = 1
                self.dictionary[word_id] = wordInfo
            else:
                wordInfo = self.dictionary[word_id]
                wordInfo.frequency += 1
        
    def find_max_freq(self):
        max_frequency = 0
        for word_id, query_word_info in self.dictionary.items():
            if (query_word_info.frequency > max_frequency):
                max_frequency = query_word_info.frequency 
        
        return max_frequency
    
    def calculate_tfs(self):
        max_frequency = self.find_max_freq()
        for word_id, query_word_info in self.dictionary.items():
            query_word_info.tf = query_word_info.frequency / max_frequency
            
    def calculate_weights(self):
        for word_id, query_word_info in self.dictionary.items():
            idf = self.get_idf(word_id)
            query_word_info.w = query_word_info.tf * idf
            
    def get_idf(self, word_id):
        index_info = self.index.dictionary.get(word_id)
        if index_info is None:
            new_idf = math.log2(len(self.file_dictionary.dict) + 1)  + 1#
            return new_idf #
            #return sys.maxsize
        else:
            return index_info.idf
        
    def calculate_normalized_weights(self):
        self.find_norm_for_query()
        for word_id, query_word_info in self.dictionary.items():
            query_word_info.wn = query_word_info.w / self.norm_for_query
    
    def find_norm_for_query(self):
        self.norm_for_query = 0        
        for word_id, query_word_info in self.dictionary.items():
            self.norm_for_query += math.pow(query_word_info.w, 2)
        
        self.norm_for_query = math.sqrt(self.norm_for_query)
        
    def find_similarities(self):
        for file_id, norm_value in self.index.norm_per_file.items():
            sum_in_numerator = 0
            for word_id, query_word_info in self.dictionary.items():
                index_info = self.index.dictionary.get(word_id)
                if index_info is None:
                    continue
                
                word_file_pair = index_info.dictionary.get(file_id)
                if word_file_pair is None:
                    continue
                
                wn_ij = word_file_pair.wn
                wn_iq = self.dictionary[word_id].wn
                sum_in_numerator += wn_ij * wn_iq
            
            self.similarities[file_id] = sum_in_numerator
            ### TODO
#            denominator = norm_value * self.norm_for_query
#            if denominator != 0:
#                self.similarities[file_id] = sum_in_numerator / denominator
#            else:
#                #print("File ID: " + str(file_id) + ", npf: "+ str(self.index.norm_per_file[file_id]) + ", nfq: " + str(self.norm_for_query))
#                self.similarities[file_id] = 0
       
        # removing similarities where SIM value is 0
        self.similarities = {file_id:sim for file_id,sim in self.similarities.items() if sim!=0}
        self.number_of_results = len(self.similarities)
        
    def export(self, output_file):
        with open(output_file, 'w') as file:
            file.write("Time needed: " + str(self.time_needed) + "\n")
            for file_id, sim in self.similarities.items():
                file_path = self.file_dictionary.get_file_path(file_id)
                file_name = os.path.basename(file_path)
                file.write(file_name + "\t:\t" + str(sim))
                file.write("\n")
            
    def show_results(self, query):
        print('Q: \"' + query + '\"')
        print("Query time: {0:.5f} s".format(self.time_needed))
        print("Results: {0} / {1}".format(len(self.similarities_to_show), self.number_of_results))
        count = 1
        for file_id, sim in self.similarities_to_show.items():
            file_path = self.file_dictionary.get_file_path(file_id)
            file_name = os.path.basename(file_path)
            print("{0:2d}. {1:.5f}\t{2}".format(count, sim, file_name))
            #print(str(count) + ". " + str(sim) + "\t" + file_name)
            count += 1