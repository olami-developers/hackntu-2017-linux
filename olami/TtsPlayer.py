'''
Created on Jun 27, 2017

@author: make ma
'''
from ctypes import *
from threading import Thread
import os

class PlayThread(Thread):
        def __init__(self, player, speech):
            self.player = player
            self.speech = speech
            Thread.__init__(self, name = "PlayThread")
        
        def run(self):
            c_speech = c_char_p(self.speech.encode('utf-8'))
            self.player.ttsLib.ttsSpeak(self.player.tts, c_speech)
            if not self.player.needStop:
                if self.player.onPlayEnd != None:
                    self.player.onPlayEnd(self.player.onPlayEndParam)            
            

class TtsPlayer(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.ttsLib = CDLL('./libs/libTts.so')
        
    def init(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        res = dir_path + '/res/tts_res.mp3'
        c_res = c_char_p(res.encode('utf-8'))
        self.tts = self.ttsLib.ttsCreate(c_res)    
        self.needStop = False  
        self.onPlayEnd = None
        self.playThread = None
        if self.tts != None:
            return True
        else:
            return False
            
        
        
    def destroy(self):
        self.stop()
        self.ttsLib.ttsDestory(self.tts)

    
    def speak(self, speech, onPlayEnd = None, onPlayEndParam = None):
        self.needStop = False
        self.onPlayEnd = onPlayEnd
        self.onPlayEndParam = onPlayEndParam
        self.playThread = PlayThread(self, speech)
        self.playThread.setDaemon(True)
        self.playThread.start()
        
    def stop(self):
        self.needStop = True
        self.ttsLib.ttsStop(self.tts)
        
        if self.playThread != None:
            self.playThread.join(2000)
            self.playThread = None
        
        
        
    