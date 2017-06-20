import cv2
import time
import numpy as np

def showfade(im1,im2,t): #t in seconds
    if len(im1.shape)==2:
        im1 = cv2.cvtColor(im1, cv2.COLOR_GRAY2BGR)
    if len(im2.shape)==2:
        im2 = cv2.cvtColor(im2, cv2.COLOR_GRAY2BGR)
    
    framelength = 40 # = 40ms
    framelengthS = framelength / 1000.0
    numframes = int(t/framelengthS)+1
    fadeamount = 1.0/(numframes-1)
    for i in range(0,numframes):
        fade_pc = i*fadeamount
        frameImage = cv2.addWeighted(im1,1.0-fade_pc,im2,fade_pc,0.0)
        cv2.imshow("RE~MASTER",frameImage)
        cv2.waitKey(framelength)

def fixpoint(pt):
    pt = np.asarray(pt)
    pt = np.asarray([pt[0],pt[1]*-1])
    pt = pt * 7
    return pt

def addlines(bg,path,t):
    fpath = []
    tlen = 0.0
    for line in path:
        st = fixpoint(line[0])
        fin = fixpoint(line[1])
        tlen+=np.linalg.norm(fin-st)
        fpath.append((st,fin))
    
    framelength = 18 # = 40ms
    framelengthS = framelength / 1000.0
    numframes = int(t/framelengthS)+1
    
    lenperframe = tlen/(numframes-1)
    
    frameImage = bg.copy()
    
    for i in range(0,len(fpath)):
        curline = fpath[i]
        curpoint = curline[0]
        curlinelen = np.linalg.norm(curline[0]-curline[1])
        count = int(curlinelen/lenperframe)
        step_pc = 1.0/count
        v = step_pc*(curline[1]-curline[0])
     
        smallI = 0
        
        while smallI<count: #if count == 5 then that means 5 jumps yes.
            st = curpoint
            end = curpoint + v
            cv2.line(frameImage,(int(st[0]), int(st[1])),(int(end[0]), int(end[1])),(0,69,255),2,8) #255 69 0 bgr
            cv2.imshow("RE~MASTER",frameImage)
            cv2.waitKey(framelength)
            smallI+=1
            curpoint = end

if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    time.sleep(1)
    ret, img1 = cap.read()
    time.sleep(1)
    ret, img2 = cap.read()
    showfade(img1,img2,5)