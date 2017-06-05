from stitch import *
import linefinder
import cv2
import numpy as np
import os
import graphMaker
import networkx as nx
import graphToStitch

def justcopy():
    #cap = cv2.VideoCapture(0)
    #ret, img = cap.read()
    #cv2.imshow("Output",img)
    #cv2.waitKey(0)

    #img = cv2.imread("IMG_7440.JPG")
    img = cv2.imread("tree.jpg")
    #img = cv2.imread("IMG_2030.JPG")
    img = cv2.resize(img,(img.shape[1]/4,img.shape[0]/4))
    #cv2.imshow("Output",img)
    #cv2.waitKey(0)

    lines, img = linefinder.getLines(img)
    #div by 7 to get something that fits.
    lines = map(lambda (start,end): (start/7,end/7), lines)

    #invert the design so it maps to the output coordinate axis
    lines = map(lambda (start,end): (np.asarray([start[0],start[1]*-1]),np.asarray([end[0],end[1]*-1])),lines)

    MG = graphMaker.graphFromLines(lines)

    circuit = list(nx.eulerian_circuit(MG))

    stitchlist = graphToStitch.tree(circuit,MG,bottomwidth = 10,topwidth=0)

    minimiseDesign(stitchlist) #brings it to bottom left

    if (not checkDesign(stitchlist)):
        print "Design may be too large for machine"
    else:
        print "Design is correct size"
    writeStitches(stitchlist,'csv_out/output.csv')
    os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes")
    print("written")
    
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
    os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes")

justcopy()

#testsatin()