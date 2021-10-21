from array import *
import numpy as np
import math
import cv2

def path_init():
    #Creates a empty array to use as representation of field
    area = np.zeros((1000, 1000), int)

    return area


def path_outside(area, outside_points):
    #defines the outer edge in the representation of the field
    #Creates the field in pixels

    i = 0
    #Works by traveling between points along the gradent to the next point.

    while i < len(outside_points): #linearly interpolates between points
        starting_point = outside_points[i]
        area[starting_point[0]][starting_point[1]] = 1
        if (i+1) < len(outside_points):
            x_diff = outside_points[i+1][0] - outside_points[i][0]
            y_diff = outside_points[i+1][1] - outside_points[i][1]
            diff_total = abs(x_diff) + abs(y_diff)
            x_avg_diff = x_diff/diff_total
            y_avg_diff = y_diff/diff_total
        else:
            x_diff = outside_points[0][0] - outside_points[len(outside_points)-1][0]
            y_diff = outside_points[0][1] - outside_points[len(outside_points)-1][1]
            diff_total = abs(x_diff) + abs(y_diff)
            x_avg_diff = x_diff/diff_total
            y_avg_diff = y_diff/diff_total

        ii = 1
        while ii < diff_total: #placing interpolated points
            x_point = math.ceil(starting_point[0]+ x_avg_diff*ii)
            y_point = math.ceil(starting_point[1]+ y_avg_diff*ii)
            area[x_point][y_point] = 2
            ii += 1
        i += 1

    return area
  
def irrigator_path(area, hydrant_point):
    #Generates the irrigator path in pixels
    print(area)
    print(len(area))
    #find line closest to hydrant
    #follow line closest to hydrant
    not_found = True
    search_radius = 1
    while not_found:
        hydrant_x = hydrant_point[0]
        hydrant_y = hydrant_point[1]
        print(search_radius)

        if hydrant_x-search_radius >= 0 and hydrant_x-search_radius < len(area[0]):
            if area[hydrant_x-search_radius][hydrant_y] == 2 or area[hydrant_x-search_radius][hydrant_y] == 1:
                not_found = False
                found_x = hydrant_x-search_radius
                found_y = hydrant_y
                break

        if hydrant_x+search_radius >= 0 and hydrant_x+search_radius < len(area[0]):
            if area[hydrant_x+search_radius][hydrant_y] == 2 or area[hydrant_x+search_radius][hydrant_y] == 1:
                not_found = False
                found_x = hydrant_x+search_radius
                found_y = hydrant_y
                break
        
        if hydrant_y-search_radius >= 0 and hydrant_y-search_radius < len(area[0]):
            if area[hydrant_x][hydrant_y-search_radius] == 2 or area[hydrant_x][hydrant_y-search_radius] == 1:
                not_found = False
                found_x = hydrant_x
                found_y = hydrant_y-search_radius
                break
        
        if hydrant_y+search_radius >= 0 and hydrant_y+search_radius < len(area[0]):
            if area[hydrant_x][hydrant_y+search_radius] == 2 or area[hydrant_x][hydrant_y+search_radius] == 1:
                not_found = False
                found_x = hydrant_x
                found_y = hydrant_y+search_radius
                break
        search_radius += 1
    
    hydrant_found_x = found_x 
    hydrant_found_y = found_y
    area[hydrant_found_x][hydrant_found_y] = 4
    print(area)
    print()

    limits_found = 0
    search_array = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    limit_point_array = [[0, 0], [0, 0]]
    found_array = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    reset_flag = 0
    found_amount = 0
    found_flag = 1
    total_points = 0
    total_points = []
    while limits_found < 2: #find path for irrgator closest hydrant
        i = 0
        if found_flag == 0:
            found_x = found_array[1][0]
            found_y = found_array[1][1]
        
        if limits_found == 1 and reset_flag == 0:
            reset_flag = 1
            found_x = hydrant_found_x
            found_y = hydrant_found_y

        found_amount = 0
        found_flag = 0
        while i < len(search_array):
            search_x = search_array[i][0]
            search_y = search_array[i][1]

            if area[found_x-search_x][found_y-search_y] == 1:
                area[found_x][found_y] = 5
                found_x = found_x-search_x
                found_y = found_y-search_y
                area[found_x][found_y] = 6
                limit_point_array[limits_found] = [found_x, found_y]
                limits_found += 1
                found_flag = 1
                break

            if area[found_x-search_x][found_y-search_y] == 2:
                new_found_x = found_x-search_x
                new_found_y = found_y-search_y
                area[found_x][found_y] = 5
                found_array[found_amount] = [new_found_x, new_found_y]
                found_amount += 1
                found_flag = 1
                total_points.append([new_found_x, new_found_y])
            i += 1
        found_x = found_array[0][0]
        found_y = found_array[0][1]
        #limit_point_array
    area[hydrant_found_x][hydrant_found_y] = 4
    #FIND WHICH WAY TO GET FROM HYDRANT POINT
    print("found array:")
    print(total_points)

    print(limit_point_array)

    x_diff = -limit_point_array[0][0] + limit_point_array[1][0] 
    y_diff = -limit_point_array[0][1] + limit_point_array[1][1] 
    diff_total = abs(x_diff) + abs(y_diff)
    path_x_avg_diff = -y_diff/diff_total
    path_y_avg_diff = x_diff/diff_total
    x_avg_diff = x_diff/diff_total
    y_avg_diff = y_diff/diff_total
    
    

    
    ii = 0
    point_counter = 0
    print()
    next_x_point = math.ceil(total_points[point_counter][0]+ x_avg_diff*ii)
    next_y_point = math.ceil(total_points[point_counter][1]+ y_avg_diff*ii)
    complete = True
    while area[next_x_point, next_y_point] == 5 or area[next_x_point, next_y_point] == 4 or complete:
        path_not_found = True
        i = 0
        while path_not_found: #placing interpolated points from the gradient of the length path
            x_point = math.ceil(next_x_point+ path_x_avg_diff*i)
            y_point = math.ceil(next_y_point+ path_y_avg_diff*i)
            
            if x_point < 0 or x_point >= len(area) or y_point < 0 or y_point >= len(area):
                path_not_found = False
                break

            if area[x_point][y_point] == 2 or area[x_point][y_point] == 1:
                path_not_found = False
                area[x_point][y_point] = 8
                
                i = 0
                path_creating = True
                while path_creating: #placing interpolated points from the gradient of the length path
                    x_point = math.ceil(next_x_point+ path_x_avg_diff*i)
                    y_point = math.ceil(next_y_point+ path_y_avg_diff*i)
                    i += 1
                    if area[x_point][y_point] == 8:
                        path_creating = False
                    else:
                        area[x_point][y_point] = 7
                
            i += 1
        iii = 0
        point_counter += 5
        if point_counter < len(total_points):
            next_x_point = math.ceil(total_points[point_counter][0]+ x_avg_diff*ii)
            next_y_point = math.ceil(total_points[point_counter][1]+ y_avg_diff*ii)
        
        else:
            break
            

        if next_x_point < 0 or next_x_point >= len(area) or next_y_point < 0 or next_y_point >= len(area):
            break

    i = 0
    ii = 0

    new_gps_points = np.zeros((1000, 1000), int)
    while i < 999:
        ii = 0
        while ii < 999:
            new_gps_points[i][ii] = area[999-i][999-ii]
            ii += 1
        i += 1

    print(area)
    new_gps_points = new_gps_points*30
    new_gps_points = new_gps_points.astype(np.uint8)
    print(new_gps_points)
    cv2.imshow('Area', new_gps_points)
    cv2.waitKey(0)

    

def gps_clean(gps_points, hydrant_point, hydrant_line):
    #Creates the relative position in pixels
    max_x_point = 0
    max_y_point = 0
    convert_factor = 0.000111111
    clean_hydrant_point = np.zeros((2, 1), int)
    clean_hydrant_line = np.zeros((2, 2), int)


    ii = 0
    max_x_index = 0
    max_y_index = 0

    for point in gps_points:
        if point[0] > max_x_point:
            max_x_point = abs(point[0])
            max_x_index = ii

        if point[1] > max_y_point:
            max_y_point = abs(point[1])
            max_y_index = ii
        ii += 1

    max_x_point = gps_points[max_x_index][0]
    max_y_point = gps_points[max_y_index][1]

    i = 0

    for point in gps_points:
        gps_points[i][0] = int(abs(5*(gps_points[i][0] - max_x_point)/convert_factor))
        gps_points[i][1] = int(abs(5*(gps_points[i][1] - max_y_point)/convert_factor))
        i += 1
    
    clean_hydrant_point[0] = int(abs(5*(hydrant_point[0] - max_x_point)/convert_factor))
    clean_hydrant_point[1] = int(abs(5*(hydrant_point[1] - max_y_point)/convert_factor))
    
    clean_hydrant_line[0][0] = int(abs(5*(hydrant_line[0][0] - max_x_point)/convert_factor))
    clean_hydrant_line[0][1] = int(abs(5*(hydrant_line[0][1] - max_y_point)/convert_factor))
    clean_hydrant_line[1][0] = int(abs(5*(hydrant_line[1][0] - max_x_point)/convert_factor))
    clean_hydrant_line[1][1] =  int(abs(5*(hydrant_line[1][1] - max_y_point)/convert_factor))


    print(gps_points)
    print(clean_hydrant_point)
    print(clean_hydrant_line)
    
    return gps_points, clean_hydrant_point, clean_hydrant_line, max_x_point, max_y_point

def cross_search(area, x_point, y_point, radius):
    not_found = True
    search_radius = radius

    hydrant_x = x_point
    hydrant_y = y_point

    if hydrant_x-search_radius >= 0 and hydrant_x-search_radius < len(area[0]):
        if area[hydrant_x-search_radius][hydrant_y] == 2 or area[hydrant_x-search_radius][hydrant_y] == 1:
            not_found = False


    if hydrant_x+search_radius >= 0 and hydrant_x+search_radius < len(area[0]):
        if area[hydrant_x+search_radius][hydrant_y] == 2 or area[hydrant_x+search_radius][hydrant_y] == 1:
            not_found = False
        
    if hydrant_y-search_radius >= 0 and hydrant_y-search_radius < len(area[0]):
        if area[hydrant_x][hydrant_y-search_radius] == 2 or area[hydrant_x][hydrant_y-search_radius] == 1:
            not_found = False

        
    if hydrant_y+search_radius >= 0 and hydrant_y+search_radius < len(area[0]):
        if area[hydrant_x][hydrant_y+search_radius] == 2 or area[hydrant_x][hydrant_y+search_radius] == 1:
            not_found = False
    
    return not_found


def sideruns(area, starting_x_point, starting_y_point, x_avg_diff, y_avg_diff, pointsx, pointsy, points_direction, points_irrigating):
    #Generates the path perpendicular to the input path
    ii = 0
    index_foward = 0
    index_back = 0
    x_point = math.ceil(starting_x_point + x_avg_diff*ii)
    y_point = math.ceil(starting_y_point + y_avg_diff*ii)

    storingreversepointsx = []
    storingreversepointsy = []

    x_avg_diff = - x_avg_diff

    while area[x_point][y_point] != 2 and area[x_point][y_point] != 3 and cross_search(area, x_point, y_point, 1):
        index_foward += 1
        x_point = math.ceil(starting_x_point + x_avg_diff*index_foward)
        y_point = math.ceil(starting_y_point + y_avg_diff*index_foward)
        if x_point >= 1000 or x_point < 0 or y_point >= 1000 or y_point < 0:
            break

    y_avg_diff = -y_avg_diff
    x_avg_diff = -x_avg_diff
    x_point = math.ceil(starting_x_point + x_avg_diff*ii)
    y_point = math.ceil(starting_y_point + y_avg_diff*ii)

    while area[x_point][y_point] != 2 and area[x_point][y_point] != 3 and cross_search(area, x_point, y_point, 1):
        index_back += 1
        x_point = math.ceil(starting_x_point + x_avg_diff*index_back)
        y_point = math.ceil(starting_y_point + y_avg_diff*index_back)
        if x_point >= 1000 or x_point < 0 or y_point >= 1000 or y_point < 0:
            break

    if index_foward > index_back:
        y_avg_diff = -y_avg_diff
        x_avg_diff = -x_avg_diff

    x_point = math.ceil(starting_x_point + x_avg_diff*ii)
    y_point = math.ceil(starting_y_point + y_avg_diff*ii)

    while area[x_point][y_point] != 2 and area[x_point][y_point] != 3 and cross_search(area, x_point, y_point, 1): #placing interpolated points
        if (x_point < 999 and y_point < 999 and x_point > 1 and y_point > 1):
            pointsx.append(x_point)
            pointsy.append(y_point)
            storingreversepointsx.append(x_point)
            storingreversepointsy.append(y_point)
            points_direction.append(0)
            points_irrigating.append(0)
            area[x_point][y_point] = 5
            ii += 1
            x_point = math.ceil(starting_x_point + x_avg_diff*ii)
            y_point = math.ceil(starting_y_point + y_avg_diff*ii)
        
        else:
            break
    
    reverselenpoints = len(storingreversepointsx)-1

    while reverselenpoints >= 0:
        pointsx.append(storingreversepointsx[reverselenpoints])
        pointsy.append(storingreversepointsy[reverselenpoints])
        points_direction.append(1)
        points_irrigating.append(0)
        reverselenpoints -= 1
    
    return area, pointsx, pointsy, points_direction, points_irrigating


def hydrant_line_maker(area, clean_hydrant_line, irrigation_radius):
    #This function generates the path to follow, direction, irrigating, foward/reverse
    #Outputs the path in pixels in x and y
    i = 0

    pointsx = []
    pointsy = []
    points_direction = []
    points_irrigating = []

    starting_point = clean_hydrant_line[i]
    area[starting_point[0]][starting_point[1]] = 7
    if (i+1) < len(clean_hydrant_line[0]):
        x_diff = clean_hydrant_line[i+1][0] - clean_hydrant_line[i][0]
        y_diff = clean_hydrant_line[i+1][1] - clean_hydrant_line[i][1]
        diff_total = abs(x_diff) + abs(y_diff)
        x_avg_diff = x_diff/diff_total
        y_avg_diff = y_diff/diff_total
    else:
        x_diff = clean_hydrant_line[0][0] - clean_hydrant_line[len(clean_hydrant_line)-1][0]
        y_diff = clean_hydrant_line[0][1] - clean_hydrant_line[len(clean_hydrant_line)-1][1]
        diff_total = abs(x_diff) + abs(y_diff)
        x_avg_diff = y_diff/diff_total
        y_avg_diff = x_diff/diff_total

    iii = 0
    x_point = math.ceil(clean_hydrant_line[0][0]+ x_avg_diff*iii)
    y_point = math.ceil(clean_hydrant_line[0][1]+ y_avg_diff*iii)

    while area[x_point][y_point] != 2 and area[x_point][y_point] != 3 and cross_search(area, x_point, y_point, 1): #placing interpolated points
    #while iii < 50: #placing interpolated points
        if (x_point <= 999 and y_point <= 999 and x_point > 1 and y_point > 1): #placing interpolated points
            iii += 1
            x_point = math.ceil(clean_hydrant_line[0][0]+ x_avg_diff*iii)
            y_point = math.ceil(clean_hydrant_line[0][1]+ y_avg_diff*iii)
            #area[x_point][y_point] = 4
        
        else:
            break

    startingedgex = x_point
    startingedgey = y_point



    ii = 5
    x_point = math.ceil(startingedgex + x_avg_diff*-ii)
    y_point = math.ceil(startingedgey + y_avg_diff*-ii)
    while area[x_point][y_point] != 2 and area[x_point][y_point] != 3 and cross_search(area, x_point, y_point, 1): #placing interpolated points
        if (x_point < 999 and y_point < 999 and x_point > 1 and y_point > 1): #placing interpolated points
            x_point = math.ceil(startingedgex + x_avg_diff*-ii)
            y_point = math.ceil(startingedgey + y_avg_diff*-ii)

            cross_search(area, x_point, y_point, 1)
            if ii % irrigation_radius == 0:
                word = 1
                area, pointsx, pointsy, points_direction, points_irrigating = sideruns(area, x_point, y_point, y_avg_diff, x_avg_diff, pointsx, pointsy, points_direction, points_irrigating)
            area[x_point][y_point] = 7
            pointsx.append(x_point)
            pointsy.append(y_point)
            points_direction.append(0)
            points_irrigating.append(1)
            ii += 1
        
        else:
            break
 
    print(pointsx)
    print(pointsy)
    print("Foward/Reverse Array:")
    print(points_direction)
    print("Direction Irrigating:")
    print(points_irrigating)
    area_display = (area * 30).astype(np.uint8)
    cv2.imshow('Area', area_display)
    
    return pointsx, pointsy

def convert_path(the_pathx, the_pathy, max_x_point, max_y_point):
    #Converts the path from pixels to gps points
    convert_factor = 0.000111111
    

    path_length = len(the_pathx)
    new_x_point = []
    new_y_point = []
    i = 0
    while i < path_length:
        new_x_point.append((the_pathx[i]/5)*convert_factor + max_x_point)
        new_y_point.append((the_pathy[i]/5)*-convert_factor + max_y_point)
        i += 1
    #gps_points[i][1] = int(abs(5*(gps_points[i][1] - max_y_point)/convert_factor))

    print(new_x_point)
    print(new_y_point)

def load_image(image_filelocation, point_1, point_2):
    image = cv2.imread(r"C:\Users\dylan\Desktop\Uni\400 Year\Robotic Irrigator\Pathing Python\%s" %image_filelocation)
    image_x = image.shape[0] - 1
    image_y = image.shape[1] - 1
    pixel = 0
    edge_colour = [232, 162, 0]
    edge2_colour = [164, 73, 163]
    line_colour = [0, 242, 255]
    edge_colour_pixels_x = [0]
    edge_colour_pixels_y = [0]
    edge2_colour_pixels_x = [0]
    edge2_colour_pixels_y = [0]
    line_colour_pixels_x = [0]
    line_colour_pixels_y = [0]
    notfound_1 = 1
    notfound_2 = 1
    notfound_3 = 1
    notfound_4 = 1
    notfound_5 = 1
    notfound_6 = 1
    notfound_7 = 1
    notfound_8 = 1


    while (pixel <= image_y): 
        if (image[0, pixel][0] == edge_colour[0] and image[0][pixel, 1] == edge_colour[1] and image[0, pixel][2] == edge_colour[2] and notfound_1):
            edge_colour_pixels_x.append(0)
            edge_colour_pixels_y.append(pixel)
            notfound_1 = 0

        if (image[0, pixel][0] == edge2_colour[0] and image[0][pixel, 1] == edge2_colour[1] and image[0, pixel][2] == edge2_colour[2] and notfound_1):
            edge2_colour_pixels_x.append(0)
            edge2_colour_pixels_y.append(pixel)
            notfound_1 = 0

        if (image[0, pixel][0] == line_colour[0] and image[0, pixel][1] == line_colour[1] and image[0, pixel][2] == line_colour[2] and notfound_2):
            line_colour_pixels_x.append(0)
            line_colour_pixels_y.append(pixel)
            notfound_2 = 0

        if (image[image_x, pixel][0] == edge2_colour[0] and image[image_x, pixel][1] == edge2_colour[1] and image[image_x, pixel][2] == edge2_colour[2] and notfound_3):
            edge2_colour_pixels_x.append(image_x)
            edge2_colour_pixels_y.append(pixel)
            notfound_3 = 0

        if (image[image_x, pixel][0] == edge_colour[0] and image[image_x, pixel][1] == edge_colour[1] and image[image_x, pixel][2] == edge_colour[2] and notfound_3):
            edge_colour_pixels_x.append(image_x)
            edge_colour_pixels_y.append(pixel)
            notfound_3 = 0

        if (image[image_x, pixel][0] == line_colour[0] and image[image_x, pixel][1] == line_colour[1] and image[image_x, pixel][2] == line_colour[2] and notfound_4):
            line_colour_pixels_x.append(image_x)
            line_colour_pixels_y.append(pixel)
            notfound_4 = 0

        pixel += 1

    pixel = 0

    while (pixel <= image_x): 
        if (image[pixel, 0][0] == edge_colour[0] and image[pixel, 0][1] == edge_colour[1] and image[pixel, 0][2] == edge_colour[2] and notfound_5):
            edge_colour_pixels_x.append(pixel)
            edge_colour_pixels_y.append(0)
            notfound_5 = 0

        if (image[pixel, 0][0] == edge2_colour[0] and image[pixel, 0][1] == edge2_colour[1] and image[pixel, 0][2] == edge2_colour[2] and notfound_5):
            edge2_colour_pixels_x.append(pixel)
            edge2_colour_pixels_y.append(0)
            notfound_5 = 0

        if (image[pixel, 0][0] == line_colour[0] and image[pixel, 0][1] == line_colour[1] and image[pixel, 0][2] == line_colour[2] and notfound_6):
            line_colour_pixels_x.append(pixel)
            line_colour_pixels_y.append(0)
            notfound_6 = 0

        if (image[pixel, image_y][0] == edge_colour[0] and image[pixel, image_y][1] == edge_colour[1] and image[pixel, image_y][2] == edge_colour[2] and notfound_7):
            edge_colour_pixels_x.append(pixel)
            edge_colour_pixels_y.append(image_y)
            notfound_7 = 0

        if (image[pixel, image_y][0] == edge2_colour[0] and image[pixel, image_y][1] == edge2_colour[1] and image[pixel, image_y][2] == edge2_colour[2] and notfound_7):
            edge2_colour_pixels_x.append(pixel)
            edge2_colour_pixels_y.append(image_y)
            notfound_7 = 0

        if (image[pixel, image_y][0] == line_colour[0] and image[pixel, image_y][1] == line_colour[1] and image[pixel, image_y][2] == line_colour[2] and notfound_8):
            line_colour_pixels_x.append(pixel)
            line_colour_pixels_y.append(image_y)
            notfound_8 = 0

        pixel += 1

    x_pixel_dist = edge_colour_pixels_x[1] - edge2_colour_pixels_x[1]
    y_pixel_dist = edge_colour_pixels_y[1] - edge2_colour_pixels_y[1]
    long_per_pixel = (point_1[0] - point_2[0])/x_pixel_dist 
    latt_per_pixel = (point_1[1] - point_2[1])/y_pixel_dist 

    edge_long_1 = (line_colour_pixels_x[1] -  edge_colour_pixels_x[1])*long_per_pixel + point_1[0]
    edge_latt_1 = (line_colour_pixels_y[1] -  edge_colour_pixels_y[1])*latt_per_pixel + point_1[1]
    edge_long_2 = (line_colour_pixels_x[2] -  edge_colour_pixels_x[1])*long_per_pixel + point_1[0]
    edge_latt_2 = (line_colour_pixels_y[2] -  edge_colour_pixels_y[1])*latt_per_pixel + point_1[1]

    return [edge_long_1, edge_latt_1], [edge_long_2, edge_latt_2]



def main():
    image_filelocation = "GraphicsTest3points.png" #Name of the image with the alterations, need to change the file path in load_image
    gps_points = [[-43.53223533938059, 172.20322871852102], [-43.527575889946746, 172.204242159892], [-43.5287860037952, 172.21015146472553], [-43.52892336653555, 172.20844633707128], [-43.529034564715296, 172.20782383014986], [-43.52941394519742, 172.20649761975216], [-43.52968866750516, 172.20565858868417], [-43.530159617121534, 172.20473836106126], [-43.530467040581826, 172.20420607253428]]
    point_2 = [-43.528346668133885, 172.20816748607697] #Point on image so you can determine position, colour =[232, 162, 0]
    point_1 = [-43.53006552472572, 172.20330078966384] #Point on image so you can determine position, colour = [164, 73, 163]
    #You can get colours using pixel testing
    hydrant_point = [0, 0]

    irrigation_boomlength = 10 #Irrigation radius in meters
    np.set_printoptions(threshold=np.inf)
    path_empty = path_init()



    hydrant_line = load_image(image_filelocation, point_1, point_2) #Generates the hydrant line from the image, can remove this and just grab it from google earth
    print(hydrant_line)
    outside_points, clean_hydrant_point, clean_hydrant_line, max_x_point, max_y_point = gps_clean(gps_points, hydrant_point, hydrant_line) #place in pixels
    path_limit = path_outside(path_empty, outside_points)    #Creates the field in pixels
    the_pathx, the_pathy = hydrant_line_maker(path_limit, clean_hydrant_line, irrigation_boomlength) #Outputs the path in pixels in x and y
    convert_path(the_pathx, the_pathy, max_x_point, max_y_point) #Converts the path from pixels to gps points
    cv2.waitKey(0)

main()