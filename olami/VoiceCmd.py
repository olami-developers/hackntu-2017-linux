#-*- coding：utf-8 -*-
'''
Created on Jun 29, 2017

@author: make ma
'''
from ctypes import *
from AudioSrc import AudioSrc
import os

class VoiceCmd(object):
    '''
    classdocs
    '''
    STATE_CANCELED = 1
    STATE_STOPPED = 2
    STATE_DETECTED_KEY = 3
    STATE_DETECTED_SENTENCE = 4
    
    def __init__(self):
        '''
        Constructor
        '''
    def init(self, audioSrc):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        self.openblasLib = CDLL(dir_path + '/libs/libopenblas.so')
        self.asrLib = CDLL(dir_path + '/libs/libAsrKaldi.so')
        self.audioSrc = audioSrc
        resFolder = dir_path + '/res/voicecmd'
        
        self.asrLib.voiceCmdSendAudioData.arg_types = (c_void_p, c_int, c_int)
        self.asrLib.voiceCmdSendAudioData.restype  = c_char_p
        c_resFolder = c_char_p(resFolder.encode('utf-8'))
        self.asrLib.voiceCmdInit(c_resFolder)
        
    def destroy(self):
        self.asrLib.voiceCmdUnInit()
        
    def cancelDetect(self):
        self.needCancel = True
    
    def stoplDetect(self):
        self.needStop = True
    
    def startDetect(self):
        ret = VoiceCmd.STATE_STOPPED
        self.asrLib.voiceCmdStartDetect()
        self.needStop = False
        self.needCancel = False
        
        while (not self.needStop) and (not self.needCancel):
            data = self.audioSrc.getRecordData()
            if data != None:
                pData = cast(data, c_void_p)
                hyp = self.asrLib.voiceCmdSendAudioData(pData, len(data) // 2, 0);
                if hyp:
                    hyp = hyp.decode("utf-8")
                    print(hyp)
                    if "欧拉密" == hyp:
                        if self.asrLib.voiceCmdIsSpeaking() != 0:
                            ret = VoiceCmd.STATE_DETECTED_SENTENCE
                            
                        else:
                            if self.asrLib.voiceCmdGetKeyWordStart() > self.asrLib.voiceCmdGetKeyWordLen() + 16000 * 8 / 10:
                                ret = VoiceCmd.STATE_DETECTED_SENTENCE
                            else:
                                ret = VoiceCmd.STATE_DETECTED_KEY
                        
                        if ret == VoiceCmd.STATE_DETECTED_SENTENCE:
                            self.audioSrc.restoreData(self.asrLib.voiceCmdGetKeyWordStart())
                            
                        self.asrLib.voiceCmdStopDetect();
                        self.asrLib.voiceCmdStartDetect();
                        break

        if self.needStop:
            ret = VoiceCmd.STATE_STOPPED
        elif self.needCancel:
            ret = VoiceCmd.STATE_CANCELED
            
        return ret
    
