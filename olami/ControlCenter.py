'''
Created on Jun 28, 2017

@author: make ma
'''
from threading import Thread
from MsgHandler import MsgHandler, Message, MsgConst
from TtsPlayer import TtsPlayer
from ServerProcess import ServerProcess
from SpeechProcess import SpeechProcess
from SemanticObject import SemanticObject

class ControlCenter(Thread):
    '''
    classdocs
    '''
    
    def onServerTtsEndListener(self, param):
        if param != None:
            msg = self.handler.obtainMessage1(MsgConst.MSG_SERVER_TTS_END)
            msg.arg1 = param
            self.handler.sendMessage(msg);

    
    def onTtsEndListener(self, param):
        msg = self.handler.obtainMessage1(MsgConst.MSG_NORMAL_TTS_END)
        msg.arg1 = param
        self.handler.sendMessage(msg);
    
    def onServerTtsPlay(self, msg):
        self.ttsPlayer.stop()
        self.ttsPlayer.speak(msg.obj, self.onServerTtsEndListener, msg.arg1 != 0)
    
    def onServerTtsEnd(self, msg):
        if msg.arg1:
            self.speechProcess.wakeupNow()


    def onTtsPlay(self, msg):
        self.ttsPlayer.stop()
        self.ttsPlayer.speak(msg.obj, self.onTtsEndListener)
    
    def onTtsEnd(self, msg):
        pass
    
    def onMusicStart(self, msg):
        pass
    
    def onMusicEnd(self, msg):
        pass


    def onAdjustVol(self, msg):
        pass
    
    def onServerSessionBroken(self, msg):
        pass
    
    
    def onDataFromServer(self, msg):
        obj = SemanticObject(msg.obj)
        obj.parse()
        if len(obj.getTts()) > 0:
            msg = self.handler.obtainMessage1(MsgConst.MSG_SERVER_TTS_PLAY)
            msg.obj = obj.getTts()
            msg.arg1 = obj.needAnswer()
            self.handler.sendMessage(msg)  
        pass
    
    def onUserDataRefresh(self, msg):
        pass


    def OnProcessServerQuerySuccessed(self, msg):
        pass
    
    def onMusicPlay(self, msg):
        pass
    
    def onMusicControl(self, msg):
        pass
    
    def onMusicStop(self, msg):
        pass


    def onMusicStopAudioBook(self, msg):
        pass
    
    def onForceStopTts(self, msg):
        self.ttsPlayer.stop()
    
    
    def __init__(self):        
        self.mExit = False
        self.msgMap = {\
            MsgConst.MSG_SERVER_TTS_PLAY : self.onServerTtsPlay, \
            MsgConst.MSG_SERVER_TTS_END : self.onServerTtsEnd, \
            MsgConst.MSG_NORMAL_TTS_PLAY : self.onTtsPlay, \
            MsgConst.MSG_NORMAL_TTS_END : self.onTtsEnd, \
            MsgConst.MSG_MUSIC_START : self.onMusicStart, \
            MsgConst.MSG_MUSIC_END : self.onMusicEnd, \
            MsgConst.MSG_ADJUST_VOL : self.onAdjustVol, \
            MsgConst.MSG_SERVER_SESSION_BROKEN : self.onServerSessionBroken, \
            MsgConst.MSG_DATA_FROM_SERVER : self.onDataFromServer, \
            MsgConst.MSG_USER_DATA_REFRESH : self.onUserDataRefresh, \
            MsgConst.MSG_PROCESS_SERVER_QUERY_SUCCESSED : self.OnProcessServerQuerySuccessed, \
            MsgConst.MSG_MUSIC_PLAY : self.onMusicPlay, \
            MsgConst.MSG_MUSIC_CONTROL : self.onMusicControl, \
            MsgConst.MSG_MUSIC_STOP : self.onMusicStop, \
            MsgConst.MSG_STOP_AUDIOBOOK : self.onMusicStopAudioBook, \
            MsgConst.MSG_FORCE_STOP_TTS : self.onForceStopTts, \
        }
        Thread.__init__(self, name = "ControlCenter")
        
    def handleMessage(self, msg):        
        if msg.what in self.msgMap.keys():
            self.msgMap[msg.what](msg)
        
    
    
    def init(self):        
        self.handler = MsgHandler()
        self.ttsPlayer = TtsPlayer()
        self.speechProcess = SpeechProcess()
        self.serverProcess = ServerProcess()
        ret = self.ttsPlayer.init()
        if ret:
            self.ttsPlayer.speak("你好，我是宇宙無敵最強AI智能機器人歐拉蜜", None)
            ret = self.speechProcess.init(self.handler)
        if ret:
            ret = self.serverProcess.init(self.handler)
            
        return ret
        
    def run(self):
        while not self.mExit:
            msg = self.handler.msgQueue.getNext()
            print("process message %d" % (msg.what))
            if msg != None:
                self.handleMessage(msg)                 

    def uninit(self):
        if self.ttsPlayer:
            self.ttsPlayer.destroy()
        
        if self.ttsPlayer:
            self.ttsPlayer.destroy()
