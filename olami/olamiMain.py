#-*- coding：utf-8 -*-
'''
Created on Jun 27, 2017

@author: make ma
'''

from Config import Config
from ControlCenter import ControlCenter

def checkConfig():
    ret = False
    if len(Config.NLI_SERVER) > 0 and len(Config.APP_KEY) > 0 and len(Config.APP_SECRET) > 0:
        ret = True
    else:
        print("Please set NLI_SERVER, APP_KEY, APP_SECRET in Config.py\n")
    return ret

if __name__ == '__main__':
    print("Olami python demo: 1.00\n")
    if checkConfig():
        controlCenter = ControlCenter()
        if controlCenter.init() == True:
            controlCenter.setDaemon(True);
            controlCenter.start()

        print("ctrl+c to exit")
        controlCenter.join()
        controlCenter.uninit()


