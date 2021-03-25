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
#Play panned left audio
pole = []
def threadone(m,bottombool,output):
    global song,pole,z
    
    #song[0:5000] = song.pan(0.5)[0:5000]
    #song[5000:10000] = song.pan(-0.5)[5000:1000]
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
        print("Opakování" + str(x))
        print("Z=" + str(z))
        print("Y=" + str(y))
        print("Bottom="+str(bottom))
        print("Bottomval="+str(bottomval))
        print("Bottombool="+str(bottombool))
        if (bottombool==True):
            if(bottom!=True): # and song[ z : y].dBFS*-1>16
                pole.append(song[ z : y].pan(pan)+(bottomval/2))
            else:
                if (song[z:y].dBFS*-1>13):
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
        print("Čas="+str(minuta)+":"+str(timestamp))
        
        
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
                bottomval+=0.125
                   
            
            if (bottomdown ==True):
                bottomval-=0.125
        
                
                
            if (bottomval<0):
                bottomup=True
                bottomdown=False
           
            elif(bottomval>=3):
                bottomdown = True
                bottomup = False
        
        
    
    #pole.append(song[2000:15000].pan(0.5))
    
    song = sum(pole) #.normalize()
    
    
    
    
    print("Částí: " + str(len(pole)))
    
    
    outputstr = output 
    try:
        song.export(outputstr, format="mp3")
        print("Export byl úspěšný")
    except:
        print("Export selhal")
    

def threadtwo():
    pass
  
def main(argv):
    print(argv)
    inputfile = ""
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["i=","o=","s=","pan=","htrf="])

    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        #sys.exit(2)
        pass
        inputfile = ""
    inputfile = ""
    outputfile = ""
    #for opt, arg in opts:
        
     #   if opt in ("-i", "--ifile"):
            #inputfile = arg
      #  elif opt in ("-o", "--ofile"):
         #   outputfile = arg
        #elif opt in ("-s", "--silent"):
        #    silent = arg
        #elif opt in ("-p", "--pan"):
        #    pan = arg
        #elif opt in ("-h", "--htrf-bottom"):
        #    temp = arg
            
        
    try:
        argv[1]
    except:
        pass
    else:
        inputfile = argv[1]
    try:
        argv[3]
    except:
        pass
    else:
        outputfile = argv[3]
    try:
        argv[5]
    except:
        pass
    else:
        pan = int(argv[5])/100
    try:
        argv[6]
    except:
        pass
    else:
        temp = True
    try:
        argv[7]
    except:
        pass
    else:
        silent = True
        
    loadfile(inputfile)
    print("Inputfile =" + inputfile)
    print("Outputfile=" + outputfile)
    try:
        silent
    except:
        print("Opravdu chcete převést soubor na 8D? [y/n]")
        stop = False  
        i=str(input())
    else:
        i = "y"
    if(i == "y"):
        try:
            pan
        except:
            print("|ABS| max / min rozsahu PAN (0..100)")
            i=(float(input()) / 100)
        else:
            i = pan 
        try:
            temp
        except:
            print("|BOOL| HTRF (bottom effect)? [y]/[n]")
            i2=(input())
        else:
            i2 = temp 
        
        
        if (i2=="y"or i2=="Y"):
            temp=True
        else:
            temp=False
        t = threading.Thread(target=threadone, args=(i,temp,outputfile,))
        
        
        t.start()
    else:
        quit()
    
if __name__ == "__main__":
   main(sys.argv[1:])




#t2 = threading.Thread(target=threadtwo(), args=(1,))
#t2.start()

