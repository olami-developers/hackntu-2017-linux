#-*- coding：utf-8 -*-
'''
Created on Jun 27, 2017

@author: make ma
'''

from ControlCenter import ControlCenter

def readKey():
    s = input('Enter ctrl+c to exit:')
    return s
    

if __name__ == '__main__':
    controlCenter = ControlCenter()
    if controlCenter.init() == True:
        controlCenter.setDaemon(True);
        controlCenter.start()
    
    #key = readKey()
    print("ctrl+c to exit")
    controlCenter.join()
    controlCenter.uninit()



