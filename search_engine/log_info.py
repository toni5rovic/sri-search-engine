# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:42:01 2020

@author: Toni
"""

import platform
import psutil
import sys
from types import ModuleType, FunctionType
from gc import get_referents

BLACKLIST = type, ModuleType, FunctionType

class LogInformation:
    def __init__(self, file_path):
        self.time_needed = ""
        self.memory_usage = 0
        self.logfile_path = file_path
    def export_log(self):
        with open(self.logfile_path, 'w') as file:
            file.write("-------------------------------\n")
            file.write("           LOG INFO            \n")
            file.write("-------------------------------\n")
            
            file.write("Time needed for generating the data structure:\n")
            file.write("\t" + self.time_needed)
            file.write("\n")
            
            file.write("Memory used:\n")
            file.write("\t" + str(self.memory_usage) + " B\n")
            file.write("\t" + str(self.memory_usage / 1024 / 1024) + " MB\n")
            file.write("\n")
            
            file.write("Platform information:\n")
            file.write("\tPlatform: " + platform.platform() + "\n")
            file.write("\tProcessor: " + platform.processor() + "\n")
            file.write("\tRAM: " + str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB")
            file.write("\n")
            
    def getsize(self, obj):
        """sum size of object & members."""
        if isinstance(obj, BLACKLIST):
            raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
        seen_ids = set()
        size = 0
        objects = [obj]
        while objects:
            need_referents = []
            for obj in objects:
                if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                    seen_ids.add(id(obj))
                    size += sys.getsizeof(obj)
                    need_referents.append(obj)
            objects = get_referents(*need_referents)
        return size