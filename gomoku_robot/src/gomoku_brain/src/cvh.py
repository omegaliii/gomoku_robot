
# coding: utf-8

# In[ ]:

def pic2matrix(image):
    # %%time
    # %matplotlib inline
    import pylab as pl
    import numpy as np
    import operator

    #import Opencv library
    import cv2

    #import imread from local file
    #path_string = '../p2.jpg'
    image_sudoku_original = image

    #convert back the color into original
    image_sudoku_original = cv2.cvtColor(image_sudoku_original, cv2.COLOR_BGR2RGB)

    #Show Images
    # _=pl.imshow(image_sudoku_original) 
    # _=pl.axis("off")

    # cv2.imshow('ImageWindow', image_sudoku_original)
    # cv2.waitKey(0)

    #function to compute the distance of two points
    def diss(op, pt):
        return ((op[0] - pt[0]) ** 2 + (op[1] - pt[1]) ** 2) ** 0.5
        for pt in pt2s:
            if ((pt1[0] - pt[0]) ** 2 + (pt1[1] - pt[1]) ** 2) ** 0.5 < minidistance:
                minidistance = ((pt1[0] - pt[0]) ** 2 + (pt1[1] - pt[1]) ** 2) ** 0.5
        return dis < minidistance

    #function to determine if the distance of two points is less than a given distance
    def minidis(pt1, pt2s, dis):
        minidistance = 9999999
        for pt in pt2s:
            if ((pt1[0] - pt[0]) ** 2 + (pt1[1] - pt[1]) ** 2) ** 0.5 < minidistance:
                minidistance = ((pt1[0] - pt[0]) ** 2 + (pt1[1] - pt[1]) ** 2) ** 0.5
        return dis < minidistance

    #function to determine if there is a green/red mark
    def det_if_color(conpt, lower, upper):
    #     points1 = np.array([
    #         np.array([0.0,0.0] ,np.float32) + np.array([144,0], np.float32),
    #         np.array([0.0,0.0] ,np.float32),
    #         np.array([0.0,0.0] ,np.float32) + np.array([0.0,144], np.float32),
    #         np.array([0.0,0.0] ,np.float32) + np.array([144,144], np.float32),
    #     ],np.float32)

    #     outerPoints = conpt

    #     points2 = np.array(outerPoints,np.float32)

    #     #Transformation matrix
    #     pers = cv2.getPerspectiveTransform(points2,  points1 );

    #     #remap the image
    #     warp = cv2.warpPerspective(ggray, pers, (SUDOKU_SIZE*IMAGE_HEIGHT, SUDOKU_SIZE*IMAGE_WIDHT));
    #     warp = ggray[conpt[0][0]:conpt[0][1], conpt[2][0]:conpt[2][1]]
    #     hsv = cv2.cvtColor(warp, cv2.COLOR_RGB2HSV)
        hsv = ggray[conpt[0][1]:conpt[2][1], conpt[0][0]:conpt[1][0]]
        # hsv = cv2.cvtColor(warp, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        # cv2.imshow("sb",mask)
        # print(sum([sum(i) for i in mask]) /255.0/ len(mask))
        # print('check:', sum([sum(i) for i in mask]) /255.0 /len(mask))
        return sum([sum(i) for i in mask]) /255.0 /len(mask) > 1


    def det_if_green(conpt):
        return det_if_color(conpt, np.array([0,60,50]), np.array([25,80,70]))

    def det_if_red(conpt):
        return det_if_color(conpt, np.array([100,40,20]), np.array([150,70,70]))

    #gray image
    image_sudoku_gray = cv2.cvtColor(image_sudoku_original,cv2.COLOR_BGR2GRAY)
    #adaptive threshold
    thresh = cv2.adaptiveThreshold(image_sudoku_gray,255,1,1,11,15)


    #show image
    # _=pl.imshow(thresh, cmap=pl.gray())
    # _=pl.axis("off")

    #set width and height
    height, width = image_sudoku_original.shape[:2]

    #set corner points
    bun0 = []
    bun0.append([0, height])
    bun0.append([0, 0])
    bun0.append([width, 0])
    bun0.append([width, height])

    bun = []
    bun.append([[width/2, height/2]])
    bun.append([[width/2, height/2]])
    bun.append([[width/2, height/2]])
    bun.append([[width/2, height/2]])

    #find the countours 
    test, contours0, hierarchy = cv2.findContours( thresh,
                                            cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
    #size of the image (height, width)
    h, w = image_sudoku_original.shape[:2]

    #copy the original image to show the posible candidate
    image_sudoku_candidates = image_sudoku_original.copy()

    size_rectangle_max = 0; 
    for i in range(len(contours0)):
        #aproximate countours to polygons
        approximation = cv2.approxPolyDP(contours0[i], 4, True)


        #has the polygon 4 sides?
        if(not (len (approximation)==4)):
            continue;
        #is the polygon convex ?
        if(not cv2.isContourConvex(approximation) ):
            continue; 
        #area of the polygon
        size_rectangle = cv2.contourArea(approximation)
        #store the biggest
        for i in approximation:
            for j in i:
                for k in range(4):
                    if diss(bun0[k], j) < diss(bun0[k], bun[k][0]):
                        bun[k] = [j]

    #show the best candidate
    bun[0] = [[bun[0][0][0]-10, bun[0][0][1]+10]]
    bun[1] = [[bun[1][0][0]-10, bun[1][0][1]-10]]
    bun[2] = [[bun[2][0][0]+10, bun[2][0][1]-10]]
    bun[3] = [[bun[3][0][0]+10, bun[3][0][1]+10]]
    # print(bun)

    approximation = bun
    for i in range(len(approximation)):
        cv2.line(image_sudoku_candidates,
                 (bun[(i%4)][0][0], bun[(i%4)][0][1]), 
                 (bun[((i+1)%4)][0][0], bun[((i+1)%4)][0][1]),
                 (255, 0, 0), 2)
    big_rectangle = bun
    #show image
    # _=pl.imshow(image_sudoku_candidates, cmap=pl.gray()) 
    # _=pl.axis("off")

    #set value for transformation
    IMAGE_WIDHT = 16
    IMAGE_HEIGHT = 16
    SUDOKU_SIZE= 9
    N_MIN_ACTVE_PIXELS = 10

    #point to remap
    points1 = np.array([
                        np.array([0.0,0.0] ,np.float32) + np.array([0,500], np.float32),
                        np.array([0.0,0.0] ,np.float32),
                        np.array([0.0,0.0] ,np.float32) + np.array([500,0], np.float32),
                        np.array([0.0,0.0] ,np.float32) + np.array([500,500], np.float32),
                        ],np.float32)    
    outerPoints = approximation
    points2 = np.array(outerPoints,np.float32)

    #Transformation matrix
    pers = cv2.getPerspectiveTransform(points2,  points1 );

    #remap the image
    warp = cv2.warpPerspective(image_sudoku_original, pers, (500, 500));

    #show image
    # _=pl.imshow(ggray)
    # _=pl.axis("off")
    tst = warp

    image_sudoku_original = warp
    ggray = image_sudoku_original

    #gray image
    image_sudoku_gray = cv2.cvtColor(image_sudoku_original,cv2.COLOR_BGR2GRAY)
    #adaptive threshold
    thresh = cv2.adaptiveThreshold(image_sudoku_gray,255,1,1,11,15)


    #show image
    # _=pl.imshow(thresh, cmap=pl.gray())
    # _=pl.axis("off")

    #set width and height
    height, width = image_sudoku_original.shape[:2]

    #set corner points
    bun0 = []
    bun0.append([0, height])
    bun0.append([0, 0])
    bun0.append([width, 0])
    bun0.append([width, height])

    bun = []
    bun.append([[width/2, height/2]])
    bun.append([[width/2, height/2]])
    bun.append([[width/2, height/2]])
    bun.append([[width/2, height/2]])

    #find the countours 
    test, contours0, hierarchy = cv2.findContours( thresh,
                                            cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
    #size of the image (height, width)
    h, w = image_sudoku_original.shape[:2]

    #copy the original image to show the posible candidate
    image_sudoku_candidates = image_sudoku_original.copy()

    size_rectangle_max = 0; 
    for i in range(len(contours0)):
        #aproximate countours to polygons
        approximation = cv2.approxPolyDP(contours0[i], 4, True)


        #has the polygon 4 sides?
        if(not (len (approximation)==4)):
            continue;
        #is the polygon convex ?
        if(not cv2.isContourConvex(approximation) ):
            continue; 
        #area of the polygon
        size_rectangle = cv2.contourArea(approximation)
        #store the biggest
        for i in approximation:
            for j in i:
                for k in range(4):
                    if diss(bun0[k], j) < diss(bun0[k], bun[k][0]):
                        bun[k] = [j]
    # print(bun)

    ggray = image_sudoku_original

    # corner pts
    coll = []


    #find the countours 
    test, contours0,hierarchy = cv2.findContours( thresh,
                                            cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
    #size of the image (height, width)
    h, w = ggray.shape[:2]

    #copy the original image to show the posible candidate
    image_sudoku_candidates = ggray.copy()

    #biggest rectangle
    size_rectangle_max = 0; 
    for i in range(len(contours0)):
        #aproximate countours to polygons
        approximation = cv2.approxPolyDP(contours0[i], 4, True)




        #has the polygon 4 sides?
        if(not (len (approximation)==4)):
            continue;
        #is the polygon convex ?
        if(not cv2.isContourConvex(approximation) ):
            continue; 


        #area of the polygon
        size_rectangle = cv2.contourArea(approximation)



        for i in range(len(approximation)):
            if len(coll) == 0:
                coll.append((approximation[(i%4)][0][0], approximation[(i%4)][0][1]))
                cv2.circle(image_sudoku_candidates,
                           (approximation[(i%4)][0][0], approximation[(i%4)][0][1]),
                           1, (255, 0, 0), 1)
            else:
                if minidis((approximation[(i%4)][0][0], approximation[(i%4)][0][1]), coll, 20):
                    coll.append((approximation[(i%4)][0][0], approximation[(i%4)][0][1]))
                    cv2.circle(image_sudoku_candidates,
                               (approximation[(i%4)][0][0], approximation[(i%4)][0][1]),
                               5, (255, 0, 0), 5)

    #     _=pl.imshow(image_sudoku_candidates, cmap=pl.gray()) 
    #     _=pl.axis("off")

    collx = [(0, 0), (width, 0), (0, height), (width, height)]


    first_pt = min(coll, key = lambda t: (t[0] ** 2 + t[1] ** 2) ** 0.5)
    last_pt = max(coll, key = lambda t: (t[0] ** 2 + t[1] ** 2) ** 0.5)
    grid_size = (abs((first_pt[0] - last_pt[0]) / 10), abs((first_pt[1] - last_pt[1]) / 10))

    ar0 = min(coll, key = lambda t: (t[0] ** 2 + t[1] ** 2) ** 0.5)

    result = []
    for i in range(11):
        for j in range(11):
            result.append((int(round(ar0[0]+(j)*grid_size[0])),int(round(ar0[1]+(i)*grid_size[1]))))

    chess_board = []
    # avg_colors = []
    for i in range(len(result)):
        if i < len(result) - 11 and i % 11 != 10:

            corner_pts = [result[i], result[i+1], result[i+12], result[i+11]]
            # print(corner_pts)
            if det_if_green(corner_pts):
                # if det_if_red(corner_pts):
                #     print(corner_pts)
                chess_board.append(1)
            elif det_if_red(corner_pts):
                chess_board.append(2)
            else:
                chess_board.append(0)

    data = np.array(chess_board)
    shape = ( 10, 10 )
    data = data.reshape( shape )
    return data


# In[ ]:

# pic2matrix('../oop.jpg')


# In[ ]:



