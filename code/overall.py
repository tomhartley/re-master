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
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    ret, img = cap.read()
    cv2.imshow("Input image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #img = cv2.imread("IMG_2030.JPG")
    #img = cv2.resize(img,(img.shape[1]/4,img.shape[0]/4))
    #cv2.imshow("Output",img)
    #cv2.waitKey(0)
    
    lines, img = linefinder.getLines(img)
    #div by 7 to get something that fits.
    lines = map(lambda (start,end): (start/7,end/7), lines)

    #invert the design so it maps to the output coordinate axis
    lines = map(lambda (start,end): (np.asarray([start[0],start[1]*-1]),np.asarray([end[0],end[1]*-1])),lines)

    MG = graphMaker.graphFromLines(lines)

    circuit = list(nx.eulerian_circuit(MG))
    
    #######CHANGE ME!! put a # in front of the ones you aren't using
    
    #stitchlist = graphToStitch.tree(circuit,MG,bottomwidth = 6,topwidth=0) #change the numbers << all in mm
    stitchlist = graphToStitch.satin(circuit,satinwidth = 2)
    #stitchlist = graphToStitch.running(circuit,stitchsize=0.5)
    #stitchlist = graphToStitch.jumponly(circuit)


    minimiseDesign(stitchlist) #brings it to bottom left

    if (not checkDesign(stitchlist)):
        print "Design may be too large for machine"
    else:
        print "Design is correct size"
    writeStitches(stitchlist,'csv_out/output.csv')
    os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes")
    f = getnewfname("all_pes/out")
    os.system("cp pes_out/output.pes " + f)
    print("Written file")
    
    #cv2.imshow("Output",img)
    #cv2.waitKey(0)



def testsatin():
    stitchlist = graphToStitch.singlesatin([[40,40],[80,60]],[[40,40],[60,80]])
    minimiseDesign(stitchlist) #brings it to bottom left
    if (not checkDesign(stitchlist)):
        print "Design may be too large for machine"
    else:
        print "Design is correct size"
    writeStitches(stitchlist,'csv_out/output.csv')
    os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes") #change the pes to dst to output dst

justcopy()

#testsatin()

#todo: save files to a folder, incrementing number. Make it do that before showing things.

