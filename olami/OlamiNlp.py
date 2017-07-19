# -*- coding: utf-8 -*-
'''
Created on Jun 30, 2017

@author: make ma
'''

import time
import hashlib
import urllib.request, urllib.error
import json
from speex import *   

class OlamiNlp(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        

    API_NAME_ASR = "asr";
    
    apiBaseUrl = ''
    appKey = ''
    appSecret = ''
    cookies = ''
    

    def setAuthorization(self, appKey, appSecret):
        self.appKey = appKey
        self.appSecret = appSecret


    def setLocalization(self, apiBaseURL):
        self.apiBaseUrl = apiBaseURL
        
    def stopProcess(self):
        self.stop = True
        
    def psize(self, size):
        buffer = b''
        mask = 0
        while (size > 0):
            buffer = bytes([(size % 2**7) | mask]) + buffer
            mask = 0x80
            size >>= 7
        return buffer    
        
    def encodeSpeex(self, audioData):
        #encoder = speex.Encoder()
        #encoder.initialize(speex.SPEEX_MODE_WB)
        encoder = WBEncoder()     
        encoder.quality = 10   
        vocoded = b''
        packet_size = encoder.frame_size * 2 * 1

        for i in range(0, len(audioData), packet_size):
            packet = audioData[i:i + packet_size]
            if len(packet) != packet_size:
                end = len(audioData) - len(audioData) % (encoder.frame_size * 2)
                packet = audioData[i:end]        
            raw = encoder.encode(packet)
            #vocoded += self.psize(len(raw)) + raw
            vocoded += raw
        return vocoded
        
        
    def getNlpResult(self, audioSrc):
        ret = None
        self.cookies = None
        self.stop = False
        
        startTime = time.time()
        foundVoice = False
        while True:
            audioData = audioSrc.getRecordData()    
            audioData = self.encodeSpeex(audioData)
            #audioData = bytearray(audioData)
            postData = str(self.getBasicQueryString(OlamiNlp.API_NAME_ASR, "seg,nli"))
            postData += "&compress=" + "1"
            postData += "&stop=" + "0"
        
            url = str(self.apiBaseUrl) + "?" + str(postData)
            
            if self.cookies == None:
                headers = { 'Connection'    : "Keep-Alive", \
                    'Content-Type'  : "application/octet-stream" }
            else:
                headers = { 'Connection'    : "Keep-Alive", \
                    'Content-Type'  : "application/octet-stream", \
                    'Cookie': self.cookies }
            req = urllib.request.Request(url,audioData, headers)
            f = urllib.request.urlopen(req)
            response = f.read().decode()
            #print(response + "\n")
            
            if self.cookies == None:
                self.cookies = f.getheader('Set-Cookie')
                
            res =  json.loads(response)
            resData = res.get("data")
            resAsr = None
            speechStatus = None
            if res != None:
                resAsr = resData.get("asr")
                
            if resAsr != None:  
                speechStatus = resAsr.get("speech_status")
            if speechStatus == 1:
                foundVoice = True;
                
            if (not foundVoice) and time.time() > startTime + 10:
                break;
            
            if foundVoice and speechStatus == 0:
                startTime = time.time()
                while True:
                    response = self.getRecognitionResult(OlamiNlp.API_NAME_ASR, "nli,seg")
                    #print(response + "\n")
                    res =  json.loads(response)
                    resData = res.get("data")
                    resAsr = None
                    isFinal = None
                    if resData != None:
                        resAsr = resData.get("asr")
                    
                        if resAsr != None:
                            isFinal = resAsr.get("final")
                            #retTemp = resAsr.get("result")     
                            #if retTemp != None:
                            #    ret = retTemp
                        
                        if isFinal:
                            ret = resData.get("nli")
                            print(response + "\n")
                            break                                   
                    
                    if isFinal or time.time() > startTime + 10:
                        break       

                break 
        return ret

 
    def sendAudioFile(self, apiName, seqValue, finished, filePath, compressed): 
        with open(filePath, "rb") as audioFile:
            af = audioFile.read()
            bAudioData = bytearray(af)
        if (bAudioData is None): 
            return "[ERROR] File not found!";
        
        ''' composite post data field''' 
        postData = str(self.getBasicQueryString(apiName, seqValue))
        postData += "&compress=" + ("1" if compressed else "0")
        postData += "&stop=" + ("1" if finished else "0")
        
        ''' Request speech recognition service by HTTP POST '''
        url = str(self.apiBaseUrl) + "?" + str(postData)
        headers = { 'Connection'    : "Keep-Alive",
                    'Content-Type'  : "application/octet-stream" }
        req = urllib.request.Request(url,bAudioData,headers)
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode()
        
        '''Now you can check the status here.'''
        #print("Sending 'POST' request to URL : " + self.apiBaseUrl)
        #print("Post parameters : " + str(postData))
        #print("Response Code : " + str(f.getcode()))
        
        '''Get cookie'''
        self.cookies = f.getheader('Set-Cookie')
        if (self.cookies is None): 
            return "Failed to get cookies.";
        #print("Cookies : " + str(self.cookies))
        
        '''Get the response'''
        return str(getResponse)

    def getRecognitionResult(self, apiName, seqValue):
        query = self.getBasicQueryString(apiName, seqValue) + "&stop=1"

        '''Request speech recognition service by HTTP GET'''
        url = str(self.apiBaseUrl) + "?" + str(query)
        req = urllib.request.Request(url,headers = {'Cookie': self.cookies})
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode()
        
        '''Now you can check the status here.'''
        #print("Sending 'GET' request to URL : " + self.apiBaseUrl)
        #print("get parameters : " + str(query))
        #print("Response Code : " + str(f.getcode()))
        
        '''Get the response'''
        return str(getResponse)
    

    def getBasicQueryString(self, apiName, seqValue):
        timestamp = int(round(time.time() * 1000))
        
        '''Prepare message to generate an MD5 digest.'''
        signMsg = str(self.appSecret)
        signMsg += 'api='+apiName
        signMsg += 'appkey='+str(self.appKey)
        signMsg += 'timestamp='+str(timestamp)
        signMsg += str(self.appSecret)
        
        '''Generate MD5 digest.'''
        md = hashlib.md5()
        md.update(signMsg.encode('utf-8'))
        sign = md.hexdigest()
        
        '''Assemble all the HTTP parameters you want to send'''
        postData = 'appkey='+str(self.appKey)
        postData +='&api='+apiName
        postData +='&timestamp='+str(timestamp)
        postData +='&sign='+str(sign)
        postData +='&seq=' +seqValue
        
        return str(postData)

        
