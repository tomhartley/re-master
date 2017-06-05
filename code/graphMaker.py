"""
An example using Graph as a weighted network.
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import postman
from linefinder import closestDistanceBetweenLines

def toNode(i):
    return (i[0],i[1])

def showGraph(G):
    pos = {}
    for i in G.nodes():
        pos[i]=np.asarray(i)
    
    nx.draw_networkx_nodes(G,pos,node_size=10)
 
    nx.draw_networkx_edges(G,pos,width=3,alpha=0.5)

    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

def generateIntersectionNodes(G):
    edgesToHandle = list(G.edges())
    while len(edgesToHandle)!=0:
        i = edgesToHandle[0]
        edgesToHandle.remove(i)
        for j in edgesToHandle:
            if i[0]==j[0] or i[1]==j[0] or i[0]==j[1] or i[1]==j[1]:
                continue
            a,b,d = closestDistanceBetweenLines([i[0][0],i[0][1],i[1][0],i[1][1]],[j[0][0],j[0][1],j[1][0],j[1][1]])
            if d<3.0: #tweak me
                newpt = (a+b)/2
                newnode = toNode(newpt)
                
                G.add_node(newnode)
                
                G.add_edge(i[0],newnode)
                G.add_edge(i[1],newnode)
                G.add_edge(j[0],newnode)
                G.add_edge(j[1],newnode)
                
                G.remove_edge(*i)
                G.remove_edge(*j)
                edgesToHandle.remove(j)

                #edgesToHandle.append((i[0],newnode))
                #edgesToHandle.append((i[1],newnode))
                #edgesToHandle.append((j[0],newnode))
                #edgesToHandle.append((j[1],newnode))
                break
    return G

def connectNearbyNodes(G):
    print len(G)
    cntr = 0
    nodesToHandle = list(G.nodes())
    while len(nodesToHandle)!=0:
        i = nodesToHandle[0]
        nodesToHandle.remove(i)
        bundled = [i]
        for j in nodesToHandle:
            if np.linalg.norm(np.asarray(i)-np.asarray(j))<5: #tweak me
                bundled.append(j)
        for toDel in bundled[1:]:
            nodesToHandle.remove(toDel)
        av_pt = sum(np.asarray(bundled))/len(bundled)
        av_pt_node = toNode(av_pt)
        G.add_node(av_pt_node)
        for n in bundled:
            G = nx.contracted_nodes(G,av_pt_node,n,self_loops=False)
        cntr +=1
    print cntr
    return G


def graphFromLines(ls):
    G=nx.Graph()
    for i in ls:
        G.add_edge(toNode(i[0]),toNode(i[1]))
    #showGraph(G)
    G = connectNearbyNodes(G)
    while True:
        prev = len(G)
        #showGraph(G)
        G = generateIntersectionNodes(G)
        mid = len(G)
        #showGraph(G)
        G = connectNearbyNodes(G)
        now = len(G)
        if (prev==now==mid):
            break
    
    #showGraph(G)
    
    for u,v,d in G.edges(data=True):
        d["weight"] = np.linalg.norm(np.asarray(v)-np.asarray(u))
    
    oddnodes = []
    for n in G.nodes_iter():
        if G.degree(n)%2 == 1:
            oddnodes.append(n)
    
    print nx.is_eulerian(G)     
    MG = nx.MultiGraph(G)
    

    for a in range(len(oddnodes)/2):
        a1 = oddnodes[2*a]
        a2 = oddnodes[2*a+1]
        p = nx.shortest_path(G,a1,a2) #before doing this, make sure all nodes are weighted.
        #also do all the nodes.
        MG.add_path(p,jump=True) #extra credit, make these added nodes jump only, not stitch
    
    #print nx.is_eulerian(MG)
    #x =  list(nx.eulerian_circuit(MG)) 
    #print(x)
    #print len(x)
        
    MG2,path = postman.single_chinese_postman_path(G)
    print "MG1 edges: ",len(MG.edges())
    print "MG2 edges: ",len(MG2.edges())
    showGraph(MG2)
    return MG2
