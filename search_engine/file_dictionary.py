# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:47:57 2020

@author: Toni
"""

class FileDictionary:
    def __init__(self):
        self.dict = {}
                 
    def add_file(self, file_path):
        'This method adds the file to the file dictionary'
        file_id = hash(file_path)
        if file_id not in self.dict:
            self.dict[file_id] = file_path
            return file_id
        else:
            return file_id
        
    def get_file_path(self, file_id):
        return self.dict.get(file_id)
    
    def get_num_of_files(self):
        return len(self.dict)