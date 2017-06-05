import stitch
import networkx as nx

def straightStitches(circuit): #stitch the first time with stitch distance d, then jump the futures
    completedEdges = []
    stitchlist = []

    stitchlist.append(Stitch(StitchType.jump,circuit[0][0]))

    for line in circuit:
        if line in completedEdges or (line[1],line[0]) in completedEdges:
            #jump it
            stitchlist.append(Stitch(StitchType.jump,line[1]))
            stitchlist.append(Stitch(StitchType.stitch,line[1]+np.array([0.1,0.1])))
        else:
            #stitch it
            beginning = np.asarray(line[0])
            end = np.asarray(line[1])
            vector = end-beginning
            len = np.linalg.norm(vector)
            numstitches = int(len*2) #len is in mm, so this is 2 stitches per mm
            for i in range(0,numstitches+1):
               st = Stitch(StitchType.stitch,i*(vector/numstitches)+beginning)
               stitchlist.append(st)
            completedEdges.append(line)
    return stitchlist