# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:49:19 2020

@author: Toni
"""

import sys, os
from timeit import default_timer as timer

modules_list = [
        os.path.abspath('.'),
        os.path.abspath('./preprocessor'),
        os.path.abspath('./search_engine')]

for module in modules_list:
    if module not in sys.path:
        sys.path.append(module)

from preprocessor import Preprocessor
from search_engine.word_dictionary import WordDictionary
from search_engine.file_dictionary import FileDictionary
from search_engine.index import Index
from search_engine.exporter import Exporter
from search_engine.query_handler import QueryHandler    

# argv[1] - config file with information where the index and original files are stored
# argv[2] - file with queries
# argv[3] - max number of relevant documents to be returned

if (len(sys.argv) < 4):
    print("Wrong number of arguments.")
    sys.exit()
    
config_file = sys.argv[1]
queries_file = sys.argv[2]
max_number_of_docs = int(sys.argv[3])
if (max_number_of_docs < 1):
    print("Error: Number of docs can't be negative.")
    sys.exit()

root_path = os.path.dirname(queries_file)
output_path = os.path.join(root_path, "output")

# load config file 
with open(os.path.join(config_file), 'r') as file:
    strings = file.readlines()
strings = list(map(lambda x: x.replace('\n', ''), strings))
equal_sign_index = strings[0].find('=')
# folder where the index is located
index_folder = strings[0][(equal_sign_index+1):]
equal_sign_index = strings[1].find('=')
# folder where original files are located
original_files = strings[1][(equal_sign_index+1):]

if os.path.exists(root_path) == False:
    print("Root path: " + root_path + " does not exist.")
    sys.exit()

if os.path.exists(original_files) == False:
    print("Folder with original files: " + original_files + " does not exist")
    sys.exit()
    
if os.path.exists(queries_file) == False:
    print("Queries file: " + queries_file +  " does not exist.")
    sys.exit()

if os.path.exists(output_path) == False:
    os.makedirs(output_path)
    print("Output folder created in: " + root_path)

index_path = os.path.join(index_folder, 'index.bin')

index = None
word_dict = None
file_dict = None

exporter = Exporter()
if os.path.exists(index_path) == False:
    if os.path.exists(index_folder) == False:
        os.makedirs(index_folder)

    # index file does not exist, so we 
    # need to preprocess original files and 
    # we need to generate index
    print("Index not found...")
    print("Preprocessing started...")
    preprocessor = Preprocessor(root_path, original_files)
    preprocessor.preprocess(generate_metadata=True)
    print("Preprocessing finished.")

    word_dict = WordDictionary()
    file_dict = FileDictionary()
    
    print("Creating index...")
    #index = Index(preprocessor.p3_path, word_dict, file_dict)
    stemmer_path = os.path.join(output_path, "stemmer")
    if os.path.exists(stemmer_path) == False:
        print("Stemmer output not found.")
        sys.exit()

    index = Index(stemmer_path, word_dict, file_dict, index_folder, True)
    index.create_index()
    print("Index has been created.")
    
    print("Exporting index...")
    exporter.export_objects(index_folder, word_dict, file_dict, index)
    print("Index exported.")
else:
    print("Index already exists.")
    print("Loading index...")
    word_dict, file_dict, index = exporter.import_objects(index_folder)
    print("Index loaded.")

# load queries
with open(os.path.join(queries_file), 'r', encoding='utf-8') as file:
    queries = file.readlines()

queries = list(map(lambda x: x.replace('\n', ''), queries))

# create the query output folder if it doesn't exist
query_output_folder = os.path.join(output_path, "query_results")
if os.path.exists(query_output_folder) == False:
    os.makedirs(query_output_folder)

# process queries, one by one
query_id = 1
for query in queries:
    if (query.isspace() or query == None or query == ''):
        continue
    
    start_time = timer()
    # Processing the query
    query_handler = QueryHandler(root_path, index, word_dict, file_dict)
    query_handler.process_query(query, max_number_of_docs)
    
    end_time = timer()
    query_handler.time_needed = end_time - start_time
    
    output_file = os.path.join(query_output_folder, str(query_id) + '.txt')
    query_handler.export(output_file)
    
    query_handler.show_results(query)
    
    query_id += 1
    print("-----------------------------")

print("Bye!")