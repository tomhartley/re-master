import cv2
import numpy as np
import math
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
    
    lenD = closestDistanceBetweenLines(l1,l2)[2] #returns 3 things
    
    return (diffmain<angdiff and lenD<distdiff)

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged
#/Users/tom/Documents/Embroidery/shaded/IMG_1966.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1967.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1968.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1969.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1972.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1973.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1980.jpg
#/Users/tom/Documents/Embroidery/shaded/IMG_1981.jpg

#/Users/tom/Documents/Embroidery/complex/IMG_2029.JPG
#/Users/tom/Documents/Embroidery/complex/IMG_2030.JPG
#/Users/tom/Documents/Embroidery/complex/IMG_2033.JPG
#/Users/tom/Documents/Embroidery/complex/IMG_2034.JPG

#/Users/tom/Documents/Embroidery/testsample/nonworking.tiff

img = cv2.imread("complex/IMG_2030.JPG") #1991,1992,1993,1996,1999,2001,2004,2005

small = cv2.resize(img,(img.shape[0]/3,img.shape[1]/3))

img_grey = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(img_grey,(9,9),0)

ret,thresh1 = cv2.threshold(blur,65,255,cv2.THRESH_BINARY_INV) #60

#thresh1 = auto_canny(thresh1)

cv2.imshow("Output",thresh1)
cv2.waitKey(0)


lines = cv2.HoughLinesP(thresh1, 1, 1*math.pi/180.0, 75, None, 45,1) #100,30,0
#lines = cv2.HoughLinesP(thresh1, 10, 5*math.pi/180.0, 5, None, 10,2) #100,30,0

print len(lines)
lines = map(lambda x: x[0],lines)
sL = sorted(lines,key=lambda x: (x[2]-x[0])**2+(x[3]-x[1])**2, reverse=True)

bins = [] #list of line segments?
toHandle = list(sL)
bins.append([toHandle[0]])
del toHandle[0]

runcount = 0

while len(toHandle)!=0:
    delids = []
    for li in range(len(toHandle)):
        for bi in bins: #todo: check all items in each bin
            changed = False
            for b_item in bi:             
                runcount+=1   
                if check_sim(b_item, toHandle[li]):
                    bi.append(toHandle[li])
                    delids.append(li)
                    changed = True
                    break
            if changed: break
    for i in sorted(delids,reverse=True):
        del toHandle[i]
    if len(delids)==0:
        bins.append([toHandle[0]])
        del toHandle[0]
            
print("runcount: " + str(runcount))
print map(len,bins)

for l in sL:
    cv2.line(small, (l[0], l[1]), (l[2], l[3]), (0,255,255), 1, 8 )

toDel = []

for i in range(len(bins)):
    if len(bins[i]) <= 1:
        toDel.append(i)
for i in sorted(toDel,reverse=True):
    del bins[i]


for b in bins:
    pnts = []
    for bi in b:
        pnts.append((bi[0],bi[1]))
        pnts.append((bi[2],bi[3]))
    rect = cv2.minAreaRect(np.asarray(pnts))
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(small,[box],0,(150,150,0),2)

    #l = b[0]
    #cv2.line(small, (l[0], l[1]), (l[2], l[3]), (0,255,0), 1, 8)



cv2.imshow("Output",small)
cv2.waitKey(0)

