'''
Created on Aug 1, 2017

@author: Jeff Huang
'''

from uartapi import UartAPISample
import time

class LedControl(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def LightAll(self,color):
        uartApi = UartAPISample()
        time.sleep(0.001)
        uartApi.openUart()

        if uartApi.uartIsOpen():

            try:
                '''flush input buffer, discarding all its contents'''
                uartApi.ser.flushInput()
                '''flush output buffer, aborting current output 
                   and discard all that is in buffer'''
                uartApi.ser.flushOutput()

                if color == "red":
                    uartApi.RunRED()
                elif color == "blue":
                    uartApi.RunBLUE()
                elif color == "green":
                    uartApi.RunGREEN()
                elif color == "white":
                    uartApi.RunWHITE()
                else: 
                    uartApi.RunDARK()
                time.sleep(0.001)
                uartApi.closeUart()
            except Exception as e1:
                print ("error communicating...: " + str(e1))

        else:
            print ("cannot open serial port ")
     

     
