'''
Created on Jul 5, 2017

@author: make ma
'''

class SemanticObject(object):
    '''
    classdocs
    '''
    def __init__(self, obj_type, desc_obj, symantic_objs):
        '''
        Constructor
        '''        
        self.type = obj_type
        self.desc_obj = desc_obj
        self.semanticObjs = symantic_objs
        self.tts = ""
            
    def getTts(self):
        return ""
    
    def process(self, handler):
        pass
    
    def needAnswer(self):
        return False

        
 
        