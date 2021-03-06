import cv2
import numpy as np
import math
import csv

from matplotlib import pyplot as plt

def closestDistanceBetweenLines(l1, l2,clampAll=True,clampA0=False,clampA1=False,clampB0=False,clampB1=False):

    ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return the closest points on each segment and their distance
    '''

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0=True
        clampA1=True
        clampB0=True
        clampB1=True

    a0=np.array([l1[0],l1[1],0])
    a1=np.array([l1[2],l1[3],0])
    b0=np.array([l2[0],l2[1],0])
    b1=np.array([l2[2],l2[3],0])

    # Calculate denomitator
    A = a1 - a0
    B = b1 - b0
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    if (magA == 0):
        magA = 0.001
    if (magB == 0):
        magB = 0.001
    _A = A / magA
    _B = B / magB

    cross = np.cross(_A, _B);
    denom = np.linalg.norm(cross)**2


    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A,(b0-a0))

        # Overlap only possible with clamping
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A,(b1-a0))

            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.absolute(d0) < np.absolute(d1):
                        return a0,b0,np.linalg.norm(a0-b0)
                    return a0,b1,np.linalg.norm(a0-b1)


            # Is segment B after A?
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.absolute(d0) < np.absolute(d1):
                        return a1,b0,np.linalg.norm(a1-b0)
                    return a1,b1,np.linalg.norm(a1-b1)


        # Segments overlap, return distance between parallel segments
        return None,None,np.linalg.norm(((d0*_A)+a0)-b0)



    # Lines criss-cross: Calculate the projected closest points
    t = (b0 - a0);
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA/denom;
    t1 = detB/denom;

    pA = a0 + (_A * t0) # Projected closest point on segment A
    pB = b0 + (_B * t1) # Projected closest point on segment B


    # Clamp projections
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1

        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1

        # Clamp projection A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B,(pA-b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)

        # Clamp projection B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A,(pB-a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)

    #return np.linalg.norm(pA-pB)
    return pA,pB,np.linalg.norm(pA-pB)


def get_angle(x):
    angleInDegrees = math.atan2(x[3]-x[1], x[2]-x[0]) * 180 / math.pi
    if angleInDegrees<0:
        angleInDegrees+=180
    return angleInDegrees

def check_sim(l1,l2,angdiff=10,distdiff=15):
    ang1 = get_angle(l1)
    ang2 = get_angle(l2)
    diffmain = abs(get_angle(l1) - get_angle(l2))
    #angles are between 0 and 180. But 180 == 0
    diffalt = abs(get_angle(l1) - get_angle(l2) + 180)
    diffalt2 = abs(get_angle(l1) - get_angle(l2) - 180)
    
    if diffalt < diffmain: diffmain = diffalt
    if diffalt2 < diffmain: diffmain = diffalt2
    if (diffmain>angdiff):
        return 2 #very dissimilar
    lenD = closestDistanceBetweenLines(l1,l2)[2] #returns 3 things
    if (lenD<distdiff): return 0 #great!
    if (lenD<(distdiff*10)): return 1 #eh save it for later; could be
    return 2

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged
    
def bin_lines(lns):
    bins = [] #list of line segments?
    toHandle = list(lns)
    bins.append([toHandle[0]])
    del toHandle[0]

    runcount = 0

    while len(toHandle)!=0:
        delids = []
        for li in range(len(toHandle)):
            for bi in bins: 
                changed = False
                for b_item in bi:             
                    runcount+=1
                    z = check_sim(b_item, toHandle[li])
                    if z == 2: #angle wrong, dist wrong
                        break
                    elif z == 0: #both right
                        bi.append(toHandle[li])
                        delids.append(li)
                        changed = True
                        break
                    else: #just angle right
                        continue
                if changed: break
        for i in sorted(delids,reverse=True):
            del toHandle[i]
        if len(delids)==0:
            bins.append([toHandle[0]])
            del toHandle[0]
    print("runcount: " + str(runcount))
    print map(len,bins)
    return bins

cap = cv2.VideoCapture(0)


while True:

    #/Users/tom/Documents/Embroidery/testsample/nonworking.tiff
    ret, img = cap.read()

    #img = cv2.imread("complex/IMG_2030.JPG")

    #cv2.imshow("Output",img)
    #cv2.waitKey(0)
    #cv2.imwrite("0original.jpg",img)
    small = cv2.resize(img,(img.shape[1]/1,img.shape[0]/1))

    #cv2.imshow("Output",small)
    #cv2.waitKey(0)
    #cv2.imwrite("1smaller.jpg",small)

    img_grey = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    #cv2.imshow("Output",img_grey)
    #cv2.waitKey(0)
    #cv2.imwrite("2blackandwhite.jpg",img_grey)


    blur = cv2.GaussianBlur(img_grey,(9,9),0)

    #cv2.imshow("Output",blur)
    #cv2.waitKey(0)
    #cv2.imwrite("3blurred.jpg",blur)


    ret,thresh1 = cv2.threshold(blur,65,255,cv2.THRESH_BINARY_INV) #65 before

    #cv2.imshow("Output",thresh1)
    #cv2.waitKey(0)
    #cv2.imwrite("4thresholded+inverted.jpg",thresh1)


    #thresh1 = auto_canny(thresh1)



    lines = cv2.HoughLinesP(thresh1, 1, 1*math.pi/180.0, 50, None, 25,1) #100,30,0
    #lines = cv2.HoughLinesP(thresh1, 10, 5*math.pi/180.0, 5, None, 10,2) #100,30,0
    if lines==None:
        break
    print len(lines)
    
    lines = map(lambda x: x[0],lines)
    sL = sorted(lines,key=lambda x: (x[2]-x[0])**2+(x[3]-x[1])**2, reverse=True)
    if (len(sL)>350):
        bins = []
    else:
        bins = bin_lines(sL)

    for l in sL:
        #cv2.line(small, (l[0], l[1]), (l[2], l[3]), (255,255,255), 1, 8)
        pass
    
    toDel = []

    for i in range(len(bins)):
        if len(bins[i]) <= 1:
            toDel.append(i)
    for i in sorted(toDel,reverse=True):
        del bins[i]

    #cv2.imshow("Output",small)
    #cv2.waitKey(0)
    #cv2.imwrite("5lines.jpg",small)


    rectpts = []

    for b in bins:
        pnts = []
        for bi in b:
            pnts.append((bi[0],bi[1]))
            pnts.append((bi[2],bi[3]))
        rect = cv2.minAreaRect(np.asarray(pnts))
        box = cv2.boxPoints(rect)
        rectpts.append(box)
        box = np.int0(box)
        #cv2.drawContours(small,[box],0,(200,0,0),2) #blue rectangles

        #l = b[0]
        #cv2.line(small, (l[0], l[1]), (l[2], l[3]), (0,255,0), 1, 8)
    lns = []
    for i in rectpts:
        #if i[0] to i[1] is less than i[1] to i[2], then average points 0 and 1, and 2 and 3. Else 1 and 2, 0 and 3
        
        if (np.linalg.norm(i[0]-i[1])<np.linalg.norm(i[1]-i[2])):
            pt1 = (i[0]+i[1])/2
            pt2 = (i[2]+i[3])/2
        else:
            pt1 = (i[1]+i[2])/2
            pt2 = (i[0]+i[3])/2
        cv2.line(small, (pt1[0],pt1[1]), (pt2[0],pt2[1]), (0,0,255), 3, 8 )
        pt1 = pt1/15
        pt2 = pt2/15
        lns.append(((pt1[0],pt1[1]), (pt2[0],pt2[1])))

        
    with open('outputtest.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        csvwriter.writerow (['*','JUMP','0','0'])
        for i in lns:
            csvwriter.writerow (['*','JUMP',i[0][0],i[0][1]])
            csvwriter.writerow (['*','STITCH',i[1][0],i[1][1]])
        csvwriter.writerow (['*','JUMP','0','0'])
        csvwriter.writerow (['*','END','0','0'])

    cv2.imshow("Output",small)
    if cv2.waitKey(0): # & 0xFF == ord('q'):
        break
    
    #cv2.imwrite("6boxed_final.jpg",small)


