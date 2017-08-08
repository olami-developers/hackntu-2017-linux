'''
Created on Jul 18, 2017

@author: make ma
'''
from SemanticObject import SemanticObject

class RestaurantSemantic(SemanticObject):
    '''
    classdocs
    '''
    
    mapSlot = { \
        "restaurant_flavours":"菜品风味:", \
        "restaurant_type": "饭店类型：", \
        "restaurant_name": "饭店名称:", \
        "restaurant_place": "饭店位置:" \
        }

    def __init__(self, obj_type, desc_obj, symantic_objs):
        '''
        Constructor
        '''
        SemanticObject.__init__(self, obj_type, desc_obj, symantic_objs)
        
    def getTts(self):
        return self.tts
    
    def process(self, handler):
        self.tts = ""
        if self.semanticObjs != None:
            obj = self.semanticObjs[0]
            self.modifier = obj.get("modifier")
            self.slots = obj.get("slots")
            
            if self.modifier[0] == "query_name":
                self.tts += "服务器返回的语义是：查询饭店名称。具体如下："
                if self.slots != None and len(self.slots) > 0:
                    for slot in self.slots:
                        name = slot.get("name")
                        value = slot.get("value")
                        if name != None and value != None:
                            ttsName = RestaurantSemantic.mapSlot.get(name)
                            if ttsName != None:
                                self.tts += ttsName + "," + value + "。"
            elif self.modifier[0] == "query_address":                
                if self.slots != None and len(self.slots) > 0:
                    self.tts += "服务器返回的语义是：查询饭店地址.具体如下:"
                    for slot in self.slots:
                        name = slot.get("name")
                        value = slot.get("value")
                        if name != None and value != None:
                            ttsName = RestaurantSemantic.mapSlot.get(name)
                            if ttsName != None:
                                self.tts += ttsName + "," + value + "。"
                                

