import os, sys

modules_list = [
        os.path.abspath('.'),
        os.path.abspath('..'),
        os.path.abspath('../preprocessor'),
        os.path.abspath('../search_engine')]

for module in modules_list:
    if module not in sys.path:
        sys.path.append(module)

from preprocessor import Preprocessor
from search_engine.word_dictionary import WordDictionary
from search_engine.file_dictionary import FileDictionary
from search_engine.index import Index
from search_engine.exporter import Exporter
from search_engine.query_handler import QueryHandler

root_path = r"E:\Jaen\UJAEN\Sistemas de recuperacion de informacion\Project 2.0"

def get_file(file_name):
    config_file = os.path.join(root_path, "config_file.txt")
    with open(os.path.join(config_file), 'r') as file:
        strings = file.readlines()
    strings = list(map(lambda x: x.replace('\n', ''), strings))
    equal_sign_index = strings[1].find('=')
    # folder where original files are located
    original_files = strings[1][(equal_sign_index+1):]

    with open(os.path.join(original_files, file_name), 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def handle_query(query, prf=False, num_of_docs = 10):
    config_file = os.path.join(root_path, "config_file.txt")
    max_number_of_docs = num_of_docs  

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
        return error("Root path: " + root_path + " does not exist.")

    if os.path.exists(original_files) == False:
        return error("Folder with original files: " + original_files + " does not exist")

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
        preprocessor = Preprocessor(rootPath=root_path)
        preprocessor.preprocess(generate_metadata=True)
        print("Preprocessing finished.")

        word_dict = WordDictionary()
        file_dict = FileDictionary()
        
        print("Creating index...")
        #index = Index(preprocessor.p3_path, word_dict, file_dict)
        stemmer_path = os.path.join(output_path, "stemmer")
        if os.path.exists(stemmer_path) == False:
            return error("Stemmer output not found.")

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

    # Processing the query
    query_handler = QueryHandler(root_path, index, word_dict, file_dict)
    results = query_handler.process_query(query, max_number_of_docs, prf)
    results = results_with_file_names(file_dict, results)
    return results

def results_with_file_names(file_dict, results):
    final_results = []
    for file_id, sim in results.items():
        file_path = file_dict.get_file_path(file_id)
        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".txt", ".html")

        fileRes = FileResult()
        fileRes.fileID = file_id
        fileRes.fileName = file_name
        fileRes.similarity = sim
        fileRes.filePath = fileRes.fileName
        final_results.append(fileRes)

    return final_results

def error(message):
	error_dict = {}
	error_dict["error"] = message
	return error_dict

class FileResult:
    def __init__(self):
        self.fileID = ""
        self.fileName = ""
        self.similarity = 0.0
        self.filePath = ""