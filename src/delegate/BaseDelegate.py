'''
Created on Aug 10, 2011

@author: Alexander
'''

from google.appengine.ext import db
import time

class BaseDelegate(object):
    
    __shared_state = {}
    def __init__(self,entityName):
        self.__dict__ = self.__shared_state
        self.__EntityName = entityName

    def get(self, key):
        value = db.get(key)
        if(value == None):
            raise Exception("Key not found")
        
        return value
    
     

    def deleteAll(self):
        while True:
            q = db.GqlQuery("SELECT __key__ FROM "+self.__EntityName)
            assert q.count()
            db.delete(q.fetch(200))
            time.sleep(0.5)
            
    def delete(self,key):
        entity = self.get(key)
        entity.delete()
        return