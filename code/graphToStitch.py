from stitch import *
import networkx as nx
import numpy as np


def annotateEdges(circuit,jumpfirst=True): #either JJJJJS or SJJJJJ
    opcircuit = []
    for edge in circuit:
        st = False #Stitch
        for i in range(0,len(opcircuit)):
            if opcircuit[i]==(edge,False): #True = Jump, False = Stitch
                if (jumpfirst==True):
                    opcircuit[i]=(edge,True)
                else:
                    st = True
            if opcircuit[i]==(edge[::-1],False):
                if (jumpfirst==True):
                    opcircuit[i]=(edge[::-1],True)
                else:
                    st = True
            
        opcircuit.append(((edge),st))
    return opcircuit


def straightStitches(circuit,stitchsize=0.5): #straight stitches, dist in mm
    circuit = annotateEdges(circuit,jumpfirst = False)
    
    stitchlist = []

    stitchlist.append(Stitch(StitchType.jump,circuit[0][0][0]))
    
    for edge in circuit:
        line = edge[0]
        if edge[1]==True: #we're jumping
            #jump it
            stitchlist.append(Stitch(StitchType.jump,line[1]))
            stitchlist.append(Stitch(StitchType.stitch,line[1]+np.array([0.1,0.1])))
        else:
            #stitch it
            beginning = np.asarray(line[0])
            end = np.asarray(line[1])
            vector = end-beginning
            len = np.linalg.norm(vector)
            numstitches = max(1,int(len*(1/float(stitchsize)))) #len is in mm, so this is 2 stitches per mm
            for i in range(0,numstitches+1):
               st = Stitch(StitchType.stitch,i*(vector/numstitches)+beginning)
               stitchlist.append(st)
    return stitchlist



def satinStitch(circuit,satinwidth = 3):
    
    stitchlist = []

    stitchlist.append(Stitch(StitchType.jump,circuit[0][0]))
