from stitch import *
import linefinder
import cv2
import numpy as np
import os
import graphMaker
import networkx as nx
import graphToStitch

#cap = cv2.VideoCapture(0)

#ret, img = cap.read()
img = cv2.imread("IMG_7440.JPG")
#img = cv2.imread("IMG_2030.JPG")
img = cv2.resize(img,(img.shape[1]/4,img.shape[0]/4))

lines, img = linefinder.getLines(img)
#div by 7 to get something that fits.
lines = map(lambda (start,end): (start/7,end/7), lines)

#invert the design so it maps to the output coordinate axis
lines = map(lambda (start,end): (np.asarray([start[0],start[1]*-1]),np.asarray([end[0],end[1]*-1])),lines)

MG = graphMaker.graphFromLines(lines)

circuit = list(nx.eulerian_circuit(MG))

stitchlist = graphToStitch.straightStitches(circuit)

minimiseDesign(stitchlist) #brings it to bottom left

if (not checkDesign(stitchlist)):
    print "Design may be too large for machine"
else:
    print "Design is correct size"

writeStitches(stitchlist,'csv_out/output.csv')

os.system("./libembroidery-convert csv_out/output.csv pes_out/output.pes")

#cv2.imshow("Output",img)

#cv2.waitKey(0)
