import cv2

def key_x(rec):
    return rec[0][0]
def key_y(rec):
    return rec[0][1]          

small_cube_color_maps = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

def draw_small_cube(count, frame, mean_clr):
    global small_cube_color_maps
    if count < 0 or count > 5:
        return frame
    xy_left_top = mapping[count][0]

    p1 = (xy_left_top[0], xy_left_top[1])
    p2 = (xy_left_top[0] + 80, xy_left_top[1])
    p3 = (xy_left_top[0] + 160, xy_left_top[1])
    p4 = (xy_left_top[0] + 240, xy_left_top[1])


    p5 = (xy_left_top[0], xy_left_top[1] + 80)
    p6 = (xy_left_top[0] + 240, xy_left_top[1] + 80)

    p7 = (xy_left_top[0], xy_left_top[1] + 160)
    p8 = (xy_left_top[0] + 240, xy_left_top[1] + 160)


    p9  = (xy_left_top[0], xy_left_top[1] + 240)
    p10 = (xy_left_top[0] + 80, xy_left_top[1] + 240)
    p11 = (xy_left_top[0] + 160, xy_left_top[1] + 240)
    p12 = (xy_left_top[0] + 240, xy_left_top[1] + 240)
    
    if len(small_cube_color_maps[count]) == 0:
        small_cube_color_maps[count] = mean_clr

    # If atleast one side of the cube is captured
    if len(small_cube_color_maps[0]) != 0:

        for cube_index in range(0, (count+1)):
            if (len(small_cube_color_maps[cube_index]) != 9):
                i = 1
            else:
                i = 0
            try:
                cv2.rectangle(frame, (p1[0], p1[1]) , (p5[0] + 80, p2[1] + 80)  ,small_cube_color_maps[cube_index][0],-1) 
                cv2.rectangle(frame, (p2[0], p2[1]) , (p5[0] + 160, p3[1] + 80)  ,small_cube_color_maps[cube_index][1],-1)
                cv2.rectangle(frame, (p3[0], p3[1]) , (p6[0]      , p6[1])       ,small_cube_color_maps[cube_index][2],-1) 

                cv2.rectangle(frame, (p5[0], p5[1]) , (p7[0] + 80, p7[1])  ,small_cube_color_maps[cube_index][3],-1)
                # Cube[2][2] non detected due to chinese sticker
                if i == 1:
                    cv2.rectangle(frame, (p5[0] + 80, p5[1]) , (p7[0] + 160, p7[1])  ,(255,255,255),-1)
                else:
                    cv2.rectangle(frame, (p5[0] + 80, p5[1]) , (p7[0] + 160, p7[1])  ,small_cube_color_maps[cube_index][4],-1)
                cv2.rectangle(frame, (p5[0] + 160, p5[1]) , (p8[0], p8[1])  ,small_cube_color_maps[cube_index][5-i],-1) 

                cv2.rectangle(frame, (p7[0], p7[1]) , (p10[0], p10[1])  ,small_cube_color_maps[cube_index][6-i],-1)
                cv2.rectangle(frame, (p7[0] + 80, p7[1]) , (p11[0], p11[1])  ,small_cube_color_maps[cube_index][7-i],-1) 
                cv2.rectangle(frame, (p7[0] + 160, p7[1]) , (p12[0], p12[1])  ,small_cube_color_maps[cube_index][8-i],-1)
            except Exception as e:
                print("Cube index: ",cube_index)


    cv2.line(frame, p5 , p6, (0,0,0), 5)
    cv2.line(frame, p7 , p8, (0,0,0), 5)
    cv2.line(frame, p2 , p10, (0,0,0), 5)
    cv2.line(frame, p3 , p11, (0,0,0), 5)
    cv2.rectangle(frame,mapping[count][0], mapping[count][1],(0,0,0),5) 
    return frame

mapping = {0: ((30,30),(270,270)), 1: ((290,30),(530,270)), 2: ((550,30),(790,270)),
           3: ((810,30),(1050,270)), 4: ((1070,30),(1310,270)), 5: ((1330,30),(1570,270))}