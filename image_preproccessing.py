import cv2
import numpy as np
import imutils


# 1). Read image from the dir.
bag = cv2.imread('bag5.jpg')
knife = cv2.imread('threat5.jpg')

# 2). Rotated knife 45 degree
angle = 45
knife = imutils.rotate_bound(knife, angle)

# Gets the co-ordinates of threat images

def click_event(event, x, y, flags, params):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append([x, y])
        if len(pts) >= 2:
            cv2.line(knife, tuple(pts[-1]), tuple(pts[-2]), (0,225,0), 2)
        cv2.imshow('knife',knife)
        print(pts)
    k = cv2.waitKey(0)
    if k == 27:
        pts = np.array(pts)


# 3). Got the co-ordinates of the knife's boundry
pts = []
# pts = np.array([[262, 626], [271, 611], [270, 606], [265, 598], [262, 593], [257, 584], [252, 572], [245, 555], [236, 535], [232, 525], [228, 515], [227, 508], [226, 499], [225, 497], [220, 495], [216, 492], [214, 491], [212, 492], [205, 478], [198, 462], [194, 450], [184, 425], [176, 402], [170, 377], [167, 369], [163, 359], [157, 357], [154, 358], [158, 373], [160, 389], [163, 407], [170, 431], [178, 453], [186, 481], [189, 492], [192, 497], [188, 504], [187, 506], [191, 513], [197, 528], [204, 546], [208, 558], [215, 575], [223, 589], [234, 606], [248, 620], [256, 626], [261, 623]])
cv2.imshow('knife',knife)
cv2.setMouseCallback('knife', click_event)

# 4). Masked it with the cropped knife's image
rect = cv2.boundingRect(pts)  # Gets the coordinate of the rectangular bounded boundry
x,y,w,h = rect
croped = knife[y:y+h, x:x+w].copy() # Croped image
pts = pts - pts.min(axis=0)
print("croped",croped.shape)
mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255,255,255), -1, cv2.LINE_AA) # Draws Countour
masked = cv2.bitwise_and(croped,croped,mask= mask)

# 5). Resized it appropritely
scale_percent = 60
width = int(masked.shape[1] * scale_percent / 100)
height = int(masked.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(masked, dim, interpolation=cv2.INTER_AREA)

bag1 = bag.copy() # Copying the original image

# 5). Padded to match with the original bag image with the appropriate values such that it mactches with the dim. of th original immage.

y = (0,66)
x = (0,71)
padded_resized = np.pad(resized, (y, x,(0,0)),'constant')

# Padding size varies image to image
print('padded_resized:', padded_resized.shape)

count_i=0
count_j=0
count_k=0

# 6). if there is a non-zero pixel value in padded image at any position put corresponding  pixel value of the bag image as 0.
for i in padded_resized:
    count_j=0
    for j in i:
        count_k=0
        for k in j :
            if(k>5):
                bag1[count_i,count_j,count_k] = 0
            count_k+=1
        count_j+=1
    count_i+=1

# 7). Overlayed paaded image with the original bag image with some saturation.
alpha =.74
beta = .26
cv2.imshow('bag:1',bag1)
merged = bag1 + padded_resized # Overlays Knife to the copied image
cv2.addWeighted(merged ,alpha,bag,beta,0,padded_resized) # Overlays overlayed Knife image with some saturation such that background is visible

# 8). Saved the Image
cv2.imshow("merged1", padded_resized)
#cv2.imwrite('merged_5.png',padded_resized)

cv2.waitKey(0)
cv2.destroyAllWindows()