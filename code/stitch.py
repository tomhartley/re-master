from enum import Enum
import csv

StitchType = Enum('StitchType', 'jump stitch end')

class Stitch(object):
    def __init__(self,stype,pos=None):
        self.type = stype
        if (self.type==StitchType.end):
            pos = [0,0]
        if (pos is None):
            print "Error: Please provide a position for this stitch"
        self.x = float(pos[0])
        self.y = float(pos[1])
    
    def getArr(self):
        if (self.type == StitchType.jump):            
            return ['*','JUMP',str(self.x),str(self.y)]
        elif (self.type == StitchType.stitch):
            return ['*','STITCH',str(self.x),str(self.y)]
        elif (self.type == StitchType.end):
            return ['*','END','0','0']
        else:
            print "Error: Undefined StitchType" + self.type
            return None

def minimiseDesign(ls):
    minX = 10000000
    minY = 10000000
    for s in ls:
        if s.type != StitchType.end:
            if s.x < minX:
                minX = s.x
            if s.y < minY:
                minY = s.y
    for s in ls:
        if s.type != StitchType.end:
            s.x -= minX
            s.y -= minY

def checkDesign(ls):
    maxX = 0
    maxY = 0
    for s in ls:
        if s.x > maxX:
            maxX = s.x
        if s.y > maxY:
            maxY = s.y
            
    if (maxX > 100):
        print "MaxX value is: " + str(maxX)
        return False
    if (maxY > 100):
        print "MaxY value is: " + str(maxY)
        return False
    return True

def writeStitches(ls,fname):
    if len(ls)==0:
        print "No stitches"
        return
    if ls[-1]!=StitchType.end:
        ls.append(Stitch(StitchType.end))
    with open(fname, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for st in ls:
            csvwriter.writerow(st.getArr())
    

if __name__=='__main__':
    testStitch = Stitch(StitchType.jump)
    print testStitch.getArr()