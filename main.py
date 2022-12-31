import cv2
import numpy as np

from hsv_color_range import color_range, check_color_range
from utilities import key_x, key_y, small_cube_color_maps, draw_small_cube, mapping

count = 0

cap = cv2.VideoCapture(0)

mean_clr = [] # initialised here for usage in line 91
while 1:
    color = None
    ret, frame = cap.read()
    annotless_frame = frame.copy()
    for i in range(count):
        if i > 5:
            break
        frame = draw_small_cube(i, frame, mean_clr)
    if count < 6:
        cv2.rectangle(frame,mapping[count][0], mapping[count][1],(0,0,255),10) # When a cube is filled, next empty cube is drawn

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray_blur = cv2.GaussianBlur(gray, (5,5), 4)
    edges = cv2.Canny(gray_blur, 30,55)

    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

    dilation = cv2.dilate(edges,kernel1,iterations = 3)
    erosion = cv2.erode(dilation,kernel2,iterations = 5)

    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(frame.shape[:2], dtype='uint8')

    RR = []
    for i in contours:
        
        approx = cv2.approxPolyDP(i, 0.1*cv2.arcLength(i, True), True)
        if (len(approx) != 4):
            continue
        rec = cv2.minAreaRect(i) # center, (width, height), angle of rotation
            
        # Small squares
        if (rec[1][0] * rec[1][1] > 8000) and (rec[1][0] * rec[1][1] < 18000):
            ratio = float(rec[1][0])/rec[1][1] # width / height

            if ratio >= 1.15 or ratio <= 0.88: 
                continue
            print(rec[1][0] * rec[1][1])
            RR.append(rec)
    
    # TO draw box around cube
    if len(RR) >= 9:
        #print(RR)
        y_sorted = sorted(RR, key=key_y)
        subarray = [y_sorted[:3], y_sorted[3:6], y_sorted[6:9]]
        for i in range(len(subarray)):
            subarray[i] = sorted(subarray[i], key=key_x)  

        Top_left = subarray[0][0]
        Top_right = subarray[0][2]
        Bottom_left = subarray[2][0]
        Bottom_Right = subarray[2][2]
        
        box1 = cv2.boxPoints(Top_left)
        box1 = np.int0(box1)
        if box1[2][0] < box1[3][0]:
            Top_left = (box1[2]) 
        else:
            Top_left = (box1[3]) 
        
        box1 = cv2.boxPoints(Top_right)
        box1 = np.int0(box1)
        if box1[2][0] > box1[3][0]:
            Top_right = (box1[2]) 
        else:
            Top_right = (box1[3])

        box1 = cv2.boxPoints(Bottom_left)
        box1 = np.int0(box1)
        if box1[0][0] < box1[1][0]:
            Bottom_left = (box1[0]) 
        else:
            Bottom_left = (box1[1])
        
        box1 = cv2.boxPoints(Bottom_Right)
        box1 = np.int0(box1)
        if box1[0][0] > box1[1][0]:
            Bottom_Right = (box1[0]) 
        else:
            Bottom_Right = (box1[1])
        
        #print(Top_left)
        #print(Top_right)
        #cv2.line(frame,(int(Top_left[0]), int(Top_left[1])),(int(Top_right[0]), int(Top_right[1])),(255,0,0),15)
        #cv2.line(frame,(int(Top_right[0]), int(Top_right[1])),(int(Bottom_Right[0]),int(Bottom_Right[1])),(255,0,0),15)
        #cv2.line(frame,(int(Bottom_Right[0]),int(Bottom_Right[1])),(int(Bottom_left[0]), int(Bottom_left[1])),(255,0,0),15)
        #cv2.line(frame,(int(Bottom_left[0]), int(Bottom_left[1])), (int(Top_left[0]), int(Top_left[1])),(255,0,0),15)
            
        #cv2.waitKey()
    mean_clr = []
    if len(RR) < 9:
        subarray = [RR]
    for REC in subarray:
        for rec in REC:
            box = cv2.boxPoints(rec)
            box = np.int0(box)

            cv2.circle(frame,(int(rec[0][0]), int(rec[0][1])), int(rec[1][0]/2), (0,255,255), 10) # img, center, radius, color, thickness

            cv2.circle(mask,(int(rec[0][0]), int(rec[0][1])), int(rec[1][0]/2), (255,255,255), -1) 

            mask2 = np.zeros(frame.shape[:2], dtype='uint8')
            cv2.circle(mask2,(int(rec[0][0]), int(rec[0][1])), int(rec[1][0]/2), (255,255,255), -1) 

            mean_val_hsv = np.array(cv2.mean(cv2.cvtColor(annotless_frame.copy(), cv2.COLOR_BGR2HSV), mask=mask2)[:-1])
    
            color = check_color_range(mean_val_hsv)
            if len(RR) >= 9:
                mean_clr.append(color)
            
            if color == None:
                color = (0,0,0)
                print("----------None----------")
            else:
                ...
            shift = np.ceil(3.5 * int(rec[1][0]) + 0.5 * int(rec[1][0]))
            org = (int(shift + rec[0][0]), int(rec[0][1]))
            cv2.putText(frame, "C", org ,cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, thickness=10)


    frame3 = cv2.bitwise_and(annotless_frame, annotless_frame, mask=mask)

    concat1 = np.concatenate((edges, dilation))

    cv2.imshow("final image", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(60) & 0xFF == ord('e'):
        count += 1
        if count > 6:
            small_cube_color_maps = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
            count = 0
        
    
