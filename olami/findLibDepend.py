'''
Created on Jun 27, 2017

@author: make ma
'''

import os,sys

lib_patterns=[]
def loadLibPattens():
        f = open("libpattern");
        global lib_patterns
        lib_patterns = f.readlines();
        f.close()

def getlibs(lib,dir):
        libs = os.popen("ldd "+lib).readlines()
        for line in libs:
                line = line.strip('\n')
                line = line.strip('\t')
                index = line.find(" => ")
                if(index < 0):
                        continue
                libName = line[0:index]
                libPath = line[index+4:]
                libPath = libPath[0:libPath.find(" (")]

                #for l in lib_patterns:
                #        l = l.strip('\n')
                 #       if(libName.find(l) >= 0):
                                #print libName, l
                os.popen("cp "+libPath+" "+dir)
                getlibs(libName,dir)






if __name__=='__main__':
        if(len(sys.argv)<3):
                print("Usage: get_files_in_vcxproj.py  file")
        else:
                #loadLibPattens()
                getlibs(sys.argv[1],sys.argv[2])