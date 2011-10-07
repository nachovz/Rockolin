'''
Created on 08/09/2010

@author: Administrador
'''

class InvalidArgumentException(Exception):
    def __init__(self):
        self.__code = -1
        
    def setCode(self,value):
        self.__code = value
