# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:21:43 2020

@author: Toni
"""

import os

from html_filter import HtmlFilter
from normalize_tokenize import NormalizationTokenization
from stopper import Stopper
from stemmer import Stemmer
from meta_info import Metadata
from timeit import default_timer as timer

# folder names and paths
outputFolder = 'output'
practice_1_output_folder = 'extraction_normalization'
practice_2_output_folder = 'stopper'
practice_3_output_folder = 'stemmer'

class Preprocessor:
    def __init__(self, rootPath="", inputFolder=""):
        self.metadata = Metadata()
        
        self.stopper = Stopper()
        stopwords_folder = os.path.join(rootPath, "stopwords")
        print("Preprocessor root path: ", rootPath)
        self.stopper.load_stopwords(stopwords_folder)
        
        self.normalizer_tokenizer = NormalizationTokenization()
        self.stemmer = Stemmer()
        
        self.p1_path = ""
        self.p2_path = ""
        self.p3_path = ""
        
        self.rootPath = rootPath
        self.inputFolder = inputFolder
        
    def prepare_output_folders(self):
        self.p1_path = os.path.join(self.rootPath, outputFolder, practice_1_output_folder)
        self.p2_path = os.path.join(self.rootPath, outputFolder, practice_2_output_folder)
        self.p3_path = os.path.join(self.rootPath, outputFolder, practice_3_output_folder)
        if not os.path.exists(self.p1_path):
            os.makedirs(self.p1_path)
        if not os.path.exists(self.p2_path):
            os.makedirs(self.p2_path)
        if not os.path.exists(self.p3_path):
            os.makedirs(self.p3_path)
    
    def preprocess_text(self, text):
        token_list = self.normalizer_tokenizer.process_text(text)
        tokens_without_stopwords = self.stopper.remove_stopwords(token_list)
        tokens_stems_only = self.stemmer.get_stems(tokens_without_stopwords)
        return tokens_stems_only
        
    def preprocess(self, generate_metadata=False, generate_output_files=False):
        self.prepare_output_folders()
    
        start_time = timer()
        inputPath = os.path.join(self.rootPath, self.inputFolder)
        for file in os.listdir(inputPath):
            fileName = os.fsdecode(file)
            
            ### <Practice 1>
            htmlFilter = HtmlFilter(inputPath, fileName)
            text = htmlFilter.filter_html()
            
            token_list = self.normalizer_tokenizer.process_text(text)
            
            txtFileName = fileName.replace('.html', '.txt')
            if generate_output_files:
                full_path = os.path.join(self.p1_path, txtFileName)
                self.write_string_list_to_file(full_path, token_list)
            ### </Practice 1>    
            
            ### <Practice 2>
            tokens_without_stopwords = self.stopper.remove_stopwords(token_list)
            if generate_output_files:
                full_path = os.path.join(self.p2_path, txtFileName)
                self.write_string_list_to_file(full_path, tokens_without_stopwords)
            ### </Practice 2>
            
            ### <Practice 3>
            tokens_stems_only = self.stemmer.get_stems(tokens_without_stopwords)
            full_path = os.path.join(self.p3_path, txtFileName)
            self.write_string_list_to_file(full_path, tokens_stems_only)
            ### </Practice 3>
            
            if (generate_metadata):
                self.metadata.practice1_metadata(token_list)
                self.metadata.num_of_files += 1
                self.metadata.practice2_metadata(tokens_without_stopwords)
                self.metadata.practice3_metadata(tokens_stems_only)
        
        if (generate_metadata):
            self.metadata.final_metadata()
            
            self.metadata.avg_tokens_per_file = self.metadata.num_of_tokens / self.metadata.num_of_files
            self.metadata.avg_num_of_words_per_file = self.metadata.num_of_words_after_removing_stopwords / self.metadata.num_of_files
            self.metadata.avg_words_stemming = self.metadata.num_of_words_after_stemming / self.metadata.num_of_files
            end_time = timer()
            self.metadata.time_needed = str(end_time - start_time)
            
            self.metadata.print_metadata()
    
    def write_string_list_to_file(self, path, string_list):
        with open(path, 'w+') as file:
            file.write('\n'.join(string_list))
