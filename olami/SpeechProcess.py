'''
Created on Jun 28, 2017

@author: make ma
'''
from AudioSrc import AudioSrc
from threading import Thread
from MsgHandler import MsgHandler, Message, MsgConst
from VoiceCmd import VoiceCmd
from OlamiNlp import OlamiNlp
import time

class SpeechProcess(Thread):
    '''
    classdocs
    '''


    def __init__(self):
        Thread.__init__(self, name = "SpeechProcess")
        
        
    def init(self, handler):
        self.handler = handler  
        self.audioSrc = AudioSrc()        
        self.audioSrc.startRecord()  
        self.voiceCmd = VoiceCmd()
        self.voiceCmd.init(self.audioSrc)
        self.setDaemon(True)
        self.nlp = OlamiNlp()
        self.nlp.setLocalization("https://tw.olami.ai/cloudservice/api")
        self.nlp.setAuthorization("bbebed6dd2084d3b8e92bec2aec129d1", "b56c88b13e174288903a1a29b97a1eb6")     
        self.start()      
        return True
    
    def destroy(self):
        self.needStop = True
        self.join(2000)        
        self.audioSrc.stopRecord()        
        self.voiceCmd.destroy()
        
    def wakeupNow(self):
        self.voiceCmd.cancelDetect()
             
        
    def run(self):
        self.needStop = False        
        
        while not self.needStop:
            wakeup = self.voiceCmd.startDetect()   
            self.handler.sendEmptyMessage(MsgConst.MSG_FORCE_STOP_TTS)
            if wakeup != VoiceCmd.STATE_STOPPED:  
                    
                if wakeup == VoiceCmd.STATE_DETECTED_KEY:
                    msg = self.handler.obtainMessage1(MsgConst.MSG_NORMAL_TTS_PLAY)
                    msg.obj = "在"                
                    self.handler.sendMessage(msg)
                    time.sleep(0.5)
                    self.audioSrc.clearData() 
                nlpResult = self.nlp.getNlpResult(self.audioSrc)
                if nlpResult != None:
                    msg = self.handler.obtainMessage1(MsgConst.MSG_DATA_FROM_SERVER)
                    msg.obj = nlpResult            
                    self.handler.sendMessage(msg)
                
                self.audioSrc.clearData()
                
                
        
        
        
        
