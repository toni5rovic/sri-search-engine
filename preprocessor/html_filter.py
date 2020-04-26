# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 16:17:41 2020

@author: Toni
"""
import os.path
import bs4
from bs4 import BeautifulSoup

class HtmlFilter:
    def __init__(self, folderPath, fileName):
        self.folder_path = folderPath
        self.file_name = fileName
        self.content = ""
    
    def filter_html(self):
        'This method loads the .html file and returns only contents of it'
        full_path = os.path.join(self.folder_path, self.file_name)
        with open(full_path, 'r', encoding='utf8') as file:    
            soup = BeautifulSoup(file, features='lxml')
        
        title = soup.title.text
        self.content = title
       
        #main_tags = soup.select("#main")
        main_tags = soup.select("#home")
        main = main_tags[0]
        if main is None:
            raise Exception(message='Could not find tag with id `home`')
            
        content_list = []
        for each in main.descendants:
            if isinstance(each, bs4.element.Comment):
                continue
            if isinstance(each, bs4.element.NavigableString) and each.parent.name != 'script':
                text = each.strip()
                content_list.append(text)
        
        content_list = list(filter(lambda x: x!= '', content_list))
        self.content = self.content + ' ' + ' '.join(content_list)
        return self.content