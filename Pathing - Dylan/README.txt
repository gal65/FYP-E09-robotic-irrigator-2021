--------------------------Ardiuno C---------------------------
GPS_Location
Needs a ESP32 and a GPS/Mangnometer Module

Takes in an array of gps points and associated arrays with direction and irrigating
Outputs desired behaviour serially -> Bearing, Distance to next point, Irrigating and Fowards/Reverse


-------------------------Python- Three Seperate Programs
Pixel Testing
Pathing Points
Pathing Graphics - Can function as Pathing Points with some commenting out of functions which is shown in code

----------------------------Dependencies:-------------------------------- 
-Python 3.8.8
-array
-numpy
-math
-cv2
-------------------------Pixel Testing----------------------------------
Used to get the colours of points you set for pathing graphics

Input the location of the file and location of the pixel of the colour you want to check

-------------------------Pathing Points--------------------------------------
Outputs a path in latt/long 

Inputs:
Array of latt/long describing a field
Two points of latt/long describing direction you want irrigator to travel down
Single point of latt/long describing the location of the hydrat


-------------------------Pathing Graphics--------------------------------------
Outputs a path in latt/long 

Inputs:
Annotated image with a yellow line for direction you want irrigator to travel down
Annotated image with a blue and yellow to give us known points
Two points of latt/long describing the two known points
Array of latt/long describing a field
Single point of latt/long describing the location of the hydrant
