'''
8D Sound converter in python using pydub
Developed by Adam Huml 2021 
Ideal values:

Normal HTRF, normal PAN - PAN = 50, HTRF = Y
No HTRF, normal PAN - PAN = 50, HTRF = N  
Normal HTRF + Strong PAN - PAN = 75, HTRF = Y
No HTRF + Strong PAN - PAN = 75, HTRF = N

'''
from pydub import AudioSegment
from pydub.playback import play
from pydub import effects
from pydub import utils
import pydub.scipy_effects

import sys, getopt, math
import threading
import time
import multiprocessing

#AudioSegment.converter = "C:\\Program Files (x86)\\ffmpeg\\bin"


def loadfile(inputfile):
    global song
    
    try: 
        song = AudioSegment.from_mp3(inputfile)
    except:
        song = AudioSegment.from_mp3("input\\ihope.mp3")#.low_pass_filter(bottomval)
    print(song)
 

z=0
pole = []
def threadone(m,bottombool):
    global song,pole,z
    ranges = int(song.duration_seconds)
    pan = 0
    up = False
    down = True
    bottom = False
    bottomdown = True
    bottomup = False
    bottomval=1
    minuta=0
    timestamp =0
    for x in range(1,10*ranges):
        y = x*100
        z = (x*100)-100
        print("****")
        print("Iteration" + str(x))
        print("Z=" + str(z))
        print("Y=" + str(y))
        print("Bottom="+str(bottom))
        print("Bottomval="+str(bottomval))
        print("Bottombool="+str(bottombool))
        if (bottombool==True):
            if(bottom!=True): # and song[ z : y].dBFS*-1>16
                pole.append(song[ z : y].pan(pan)+(bottomval/2))
            else:
                if (song[z:y].dBFS*-1>13): #Can be changed to improve 8D performance in some cases
                    pole.append(song[ z : y].pan(pan)-bottomval)
                else:
                    pole.append(song[ z : y].pan(pan)-bottomval)
        else: 
            pole.append(song[ z : y].pan(pan))
       
             
        print("Power="+str(pole[x-1].dBFS*-1))
        
        timestamp=float(len(pole)/10)
        
        if(timestamp>=60):
            minuta=int(timestamp/60)
            timestamp="{:.2f}".format(timestamp-minuta*60)
        print("Time="+str(minuta)+":"+str(timestamp))
        
        
        print("****")
        z+=1000
        #print(x/1000)
        
        if (pan<=0):
            if (down ==True):
                pan-=0.05
            else:
                pan+=0.05
                
        if (pan>=0):
            if (down ==True):
                pan-=0.05
            else:
                pan+=0.05
                
        if (pan<=-m):
            up=True
            down=False
            if (bottom==False):
                bottom = True
        elif(pan>=m):
            down = True
            up = False
            if (bottom==True):
                bottom = False
        
        
        if (bottombool==True):
            
            if (bottomup ==True):
                bottomval+=0.125 #0.125
                   
            
            if (bottomdown ==True):
                bottomval-=0.125 #0.125
        
                
            if (bottomval<0):
                bottomup=True
                bottomdown=False
           
            elif(bottomval>=4): #4
                bottomdown = True
                bottomup = False
        
        
    
    song = sum(pole) #.normalize() can normalize entire song (not recommended while using the HTRF bottom effect)
    
    
    
    
    print("Parts count: " + str(len(pole)))
    
    
    
    try:
        song.export("output\\export.mp3", format="mp3")
        print("Export completed successfully")
    except:
        print("Export failed!")
    

def threadtwo():
    pass
  
def main(argv):
    inputfile = ""
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

    except getopt.GetoptError:
        print ('8dizer.py -i <inputfile>')
        sys.exit(2)
        inputfile = ""
    for opt, arg in opts:
        
        if opt in ("-i", "--ifile"):
            inputfile = arg
        else:
            inputfile = ""
            
    loadfile(inputfile)
    
    print("Do you really want to convert the Audio file to 8D? [y/n]")
    stop = False  
    i=str(input())
    if(i == "y"):
        print("|ABS| max / min range PAN (0..100)")
        i=(float(input()) / 100)
        print("|BOOL| HTRF (bottom effect)? [y]/[n]")
        i2=(input())
        
        if (i2=="y"or i2=="Y"):
            temp=True
        else:
            temp=False
        t = threading.Thread(target=threadone, args=(i,temp,))
        
        
        t.start()
    else:
        quit()
    
if __name__ == "__main__":
   main(sys.argv[1:])

#t2 = threading.Thread(target=threadtwo(), args=(1,))  place for other threads (for GUI and others)
#t2.start()

