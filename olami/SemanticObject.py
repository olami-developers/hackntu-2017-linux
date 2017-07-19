'''
Created on Jul 5, 2017

@author: make ma
'''

class SemanticObject(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        if params != None:
            self.obj = params[0]
        else:
            self.boj = None
            
    def parseDataObjs(self):
        tts = None
        for dataObj in self.dataObjs:
            if self.type == "baike":
                tts = dataObj.get("description")
            elif self.type == "news":
                tts = dataObj.get("detail")
            elif self.type == "tvprogram":
                tts = dataObj.get("time")
                if tts != None:
                    tts += " "
                    tts += dataObj.get("name")
            elif self.type == "joke":
                tts = dataObj.get("content")
            elif self.type == "stock":
                tts = dataObj.get("cur_price")
            elif self.type == "cooking":
                tts = dataObj.get("content")          
            
            if tts != None:
                self.tts += tts + "。"
            
    def parse(self):
        tts = None
        self.tts = ""
        if self.obj != None:
            self.desc_obj = self.obj.get("desc_obj")
            self.type = self.obj.get("type")
            if self.desc_obj != None:
                tts = self.desc_obj.get("result")
                if tts != None:
                    self.tts += tts
            self.dataObjs = self.obj.get("data_obj")
            
            if self.dataObjs != None:
                self.parseDataObjs()
                
            
    def getTts(self):
        return self.tts     
    
    def needAnswer(self):
        if self.type == "question" or self.type == "confirmation" or self.type == "selection":
            return True
        else:
            return False   
        