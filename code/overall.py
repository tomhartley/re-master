from stitch import *
import linefinder
import cv2
import numpy as np
import os
import graphMaker
import networkx as nx
import graphToStitch
import time
import datetime
import imfade

stitchtype = 3 # 1 is jump, 2 is running, 3 is satin, 4 is tree
cap = cv2.VideoCapture(0) #change to 1 if you need the later
ret, img = cap.read()
time.sleep(0.5)
quit = False

def getnewfname(base):
    curnum = 0
    while True:
        if (not os.path.isfile(base+str(curnum)+".pes")):
            break
        else:
            curnum+=1
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d::%H:%M:%S')
    fin = base+st+".pes"

    return base+str(curnum) + ".pes"

    #return fin

def justcopy():
    while True:
        ret, img = cap.read()
        if (img is None):
            print "WTF"
            break
        imgbig = cv2.resize(img,(img.shape[1]*2,img.shape[0]*2))
        cv2.imshow("RE~MASTER",img)
        x = cv2.waitKey(30) #25 fps
        global stitchtype
        if (x==ord(' ')):
            break
        elif (x==ord('j')):
            stitchtype=1
            print "Switching to jump stitch"
        elif (x==ord('r')):
            stitchtype=2
            print "Switching to running stitch"
        elif (x==ord('s')):
            stitchtype=3
            print "Switching to satin stitch"
        elif (x==ord('t')):
            stitchtype=4
            print "Switching to new quality stitch"
        elif (x==ord('q')):
            global quit
            quit=True
            return None
     
    imstack = []
    #img = cv2.imread("IMG_2030.JPG")
    #img = cv2.resize(img,(img.shape[1]/4,img.shape[0]/4))
    imstack.append((img.copy(),0)) 
    #cv2.imshow("RE~MASTER",img)
    #cv2.waitKey(3000)


    #cv2.imshow("Output",img)
    
    lines, stack = linefinder.getLines(img)
    imstack = imstack + stack
    #div by 7 to get something that fits.
    lines = map(lambda (start,end): (start/7,end/7), lines)

    #invert the design so it maps to the output coordinate axis
    lines = map(lambda (start,end): (np.asarray([start[0],start[1]*-1]),np.asarray([end[0],end[1]*-1])),lines)

    MG = graphMaker.graphFromLines(lines)

    circuit = list(nx.eulerian_circuit(MG))
    
    #######CHANGE ME!! put a # in front of the ones you aren't using
    
    if (stitchtype == 1):
        stitchlist = graphToStitch.jumponly(circuit)
    elif (stitchtype == 2):
        stitchlist = graphToStitch.running(circuit,stitchsize=0.5)
    elif (stitchtype == 3):
        stitchlist = graphToStitch.satin(circuit,satinwidth = 4)
    elif (stitchtype == 4):
        stitchlist = graphToStitch.tree(circuit,MG,bottomwidth = 8,topwidth=0) #change the numbers << all in mm
    


    minimiseDesign(stitchlist) #brings it to bottom left

    if (not checkDesign(stitchlist)):
        print "Design may be too large for machine"
    else:
        print "Design is correct size"
    writeStitches(stitchlist,'csv_out/output.csv')
    os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes")
    f = getnewfname("all_pes/out")
    os.system("cp pes_out/output.pes " + f)
    os.system("cp pes_out/output.pes /Volumes/NO\ NAME/embroider.pes")
    
    print("Written file")
    
    #cv2.waitKey(30)
    #
    #graphMaker.showGraph(MG)
    
    for i in range(0,len(imstack)-1):
        imfade.showfade(imstack[i][0],imstack[i+1][0],imstack[i+1][1])
    
    imfade.addlines(imstack[-1][0],circuit,5)
    
    #cv2.imshow("RE~MASTER",imstack[-1][0])
    cv2.waitKey(0)

def testsatin():
    stitchlist = graphToStitch.singlesatin([[40,40],[80,60]],[[40,40],[60,80]])
    minimiseDesign(stitchlist) #brings it to bottom left
    if (not checkDesign(stitchlist)):
        print "Design may be too large for machine"
    else:
        print "Design is correct size"
    writeStitches(stitchlist,'csv_out/output.csv')
    os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes") #change the pes to dst to output dst

while not quit:
    justcopy()

#testsatin()

#todo: save files to a folder, incrementing number. Make it do that before showing things.

