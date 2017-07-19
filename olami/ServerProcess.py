'''
Created on Jun 28, 2017

@author: make ma
'''

from threading import Thread

class ServerProcess(Thread):
    '''
    classdocs
    '''


    def __init__(self):
        Thread.__init__(self, name = "ServerProcess")
        
        
    def init(self, handler):
        self.handler = handler
        return True
        
        
    def run(self):
        Thread.run(self)