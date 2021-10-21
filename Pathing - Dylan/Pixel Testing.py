import cv2
import numpy as np


gameimage = cv2.imread(r"C:\Users\dylan\Desktop\Uni\400 Year\Robotic Irrigator\Pathing Python\GraphicsTest2points.png")
pixel = gameimage[0, 462] #Grabs the colour of the pixel at that location, 0,0 is top left of the display and you can see the pixels number in paint in the bottem left
print(pixel)

image = np.full((100, 100, 3), pixel, np.uint8)
cv2.imshow('Area', image)
cv2.waitKey(0)

#Yellow location 0, 561, - (y, x) - Yellow Value = [0, 242, 255]
#Blue Location 0, 293 - (y, x) - Blue Value = [232, 162, 0]
#Purple value = [164  73 163]
