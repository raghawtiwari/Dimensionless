# Dimensionless
# Steps and Algorithm involved in image pre-proccessing.
1. imported cv2 for image manipulations, numpy for working with arrays, imutils to rotate image 45 degree.
2. Read Images 
3. To get the boundries of the threate_objects i used cv2 ```setMouseCallback``` method to invoke ```clickevent ``` callback function which returned the co-ordinates of boundries of threat objects.
4. Then Cropped the rectangular region which inscribed threat object .
5. Since the rectangular region had white background, i masked with a dummy array of zeros with same deimension that of my cropped image. This gave me a masked array/image only conatining the threat object and background black.
6. Resized the image 
7. Because i had to overlay masked image to the bag image there were certain addition involved. And we know sum of two matrix will only happen if two matrices are of same value. So, I padded masked image with zeros to match with the dim. of original bag image. I used padding constant as 0 because while addition of masked image with bag image only pixel values corresponding to intersection region of masked image and bag image gets changed ie; where there is a threat object. 
8. There was problem while going with the above step. Ideally, there has to be n image with a bag in background and thread object pasted above it. But when i tried above step, the region's pixel values where threat object existed when gets added with bag image pixel values, the resultant image were the sum of the pixel value of the threat object and the corresponding bag's pixel value. Hence the resultant image got changed.
9. So i applied, if there exicted a non-zero pixel value in padded image at any position put corresponding  pixel value of the bag image as 0. Now when i added both padded and bag image the resulatant was the same as expected and named as ```merged```.
10. At the end i used ```cv2.addWeighted``` which was ```final_image = alpha*merged + beta*bag``` to add alpha saturation where ```alpha``` and ```beta``` were certain contant and ```beta = 1 - alpha ``` .
11. Finally saved the image. 
