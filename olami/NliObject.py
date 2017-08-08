'''
Created on Jul 11, 2017

@author: make ma
'''

from DialogueObject import DialogueObject
from StockSemantic import StockSemantic
from RestaurantSemantic import RestaurantSemantic

class NliObject(object):
    '''
    classdocs
    '''
    
    semanticMap = { \
        "stock":StockSemantic, \
        "restaurant": RestaurantSemantic, \
        }

    def __init__(self, params):
        '''
        Constructor
        '''       
        if params != None:
            self.obj = params[0]
        else:
            self.boj = None
     
    def parse(self):
        ret = None
        if self.obj != None:
            self.desc_obj = self.obj.get("desc_obj")
            if self.desc_obj != None:
                status = self.desc_obj.get("status", 1)
                if status == 0:
                    ret = True
            self.type = self.obj.get("type")
            self.dataObjs = self.obj.get("data_obj")
            self.semanticObjs = self.obj.get("semantic")
            
            if self.semanticObjs != None:
                classType = NliObject.semanticMap.get(self.type, None)
                if classType != None:
                    ret = classType(self.type, self.desc_obj, self.semanticObjs)
            else:
                ret = DialogueObject(self.type, self.desc_obj, self.dataObjs)           
        return ret
