# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 02:46:45 2020

@author: Toni
"""

class WordFilePair:
    def __init__(self):
        self.frequency = 0
        self.tf = -1
        self.w = -1
        self.wn = -1
    
    def export(self, file_hook):
        file_hook.write("\t\tFrequency: {0}".format(self.frequency))
        file_hook.write("\t\tTF: {:.4f}".format(self.tf))
        file_hook.write("\t\tW: {:.4f}".format(self.w))
        file_hook.write("\t\tWn: {:.4f}".format(self.wn))        