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


def running(circuit,stitchsize=0.5): #straight stitches, dist in mm
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

def singlesatin(line1, line2, gap=0.4):
    line1 = np.asarray(line1)
    line2 = np.asarray(line2)
    len1 = np.linalg.norm(line1[1]-line1[0])
    len2 = np.linalg.norm(line2[1]-line2[0])
    lenm = (len1+len2)/2
    numstitches = max(int(lenm/gap),1)

    beg1 = line1[0]
    beg2 = line2[0]
    
    vec1 = (line1[1]-line1[0])/float(numstitches)
    vec2 = (line2[1]-line2[0])/float(numstitches)
    
    print vec1

    
    sts = []
    
    for i in range(numstitches):
        st1 = Stitch(StitchType.stitch,i*vec1+beg1)
        st2 = Stitch(StitchType.stitch,i*vec2+beg2)
        sts.append(st1)
        sts.append(st2)
    return sts
        

def satin(circuit,satinwidth = 3): #satin width is over each side
    
    stitchlist = []

    stitchlist.append(Stitch(StitchType.jump,circuit[0][0]))
    
    circuit = annotateEdges(circuit,jumpfirst=True)
    
    for edge in circuit:
        line = np.asarray(edge[0])
        if edge[1]==True: #we're jumping
            #jump it
            stitchlist.append(Stitch(StitchType.jump,line[1]))
            stitchlist.append(Stitch(StitchType.stitch,line[1]+np.array([0.1,0.1])))
        else:
            #SATIN STITCH it
            
            vec = line[1]-line[0]
            clock90 = [vec[1],-vec[0]]
            aclock90 = [-vec[1],vec[0]]
            
            veclen = np.linalg.norm(vec)
            d = satinwidth/2.0
            
            v1 = (clock90/veclen)*d
            v2 = (aclock90/veclen)*d
            
            line1 = [line[0]+v1,line[1]+v1]
            line2 = [line[0]+v2,line[1]+v2]
            
            st = singlesatin(line1,line2,0.4)
            stitchlist+=st
    return stitchlist

def tree(circuit,MG,bottomwidth = 10,topwidth=1):
    lowestnode = MG.nodes().pop()
    for node in MG.nodes():
        if (node[1]<lowestnode[1]): #smallest y value
            lowestnode = node
    
    furthestnodedist = 0
    furthestnode = lowestnode
    
    for node in MG.nodes():
        d = nx.shortest_path_length(MG,node,lowestnode,'weight')
        print d
        if (d>furthestnodedist):
            furthestnodedist = d
            furthestnode = node
    
    stitchlist = []

    stitchlist.append(Stitch(StitchType.jump,circuit[0][0]))
    
    circuit = annotateEdges(circuit,jumpfirst=True)
    
    for edge in circuit:
        oline = edge[0]
        line = np.asarray(edge[0])
        if edge[1]==True: #we're jumping
            #jump it
            stitchlist.append(Stitch(StitchType.jump,line[1]))
            stitchlist.append(Stitch(StitchType.stitch,line[1]+np.array([0.1,0.1])))
        else:
            #SATIN STITCH it getting wider (or thinner)
            
            vec = line[1]-line[0]
            clock90 = [vec[1],-vec[0]]
            aclock90 = [-vec[1],vec[0]]
            
            veclen = np.linalg.norm(vec)
            lowd = nx.shortest_path_length(MG,oline[0],lowestnode,'weight')
            highd = nx.shortest_path_length(MG,oline[1],lowestnode,'weight')
            
            lowwidth = ((lowd/furthestnodedist)*(topwidth-bottomwidth)+bottomwidth)/2.0
            highwidth = ((highd/furthestnodedist)*(topwidth-bottomwidth)+bottomwidth)/2.0
            
            print "low,high", (lowwidth,highwidth)
            
            v1 = (clock90/veclen)
            v2 = (aclock90/veclen)
            
            line1 = [line[0]+v1*lowwidth,line[1]+v1*highwidth]
            line2 = [line[0]+v2*lowwidth,line[1]+v2*highwidth]
            
            st = singlesatin(line1,line2,0.4)
            stitchlist+=st
    return stitchlist
