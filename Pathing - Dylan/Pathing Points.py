from array import *
import numpy as np
import math
import cv2

hydrant_point = [0, 0]

def path_init():
    #Creates a empty array to use as representation of field
    area = np.zeros((1000, 1000), int)

    return area


def path_outside(area, outside_points):
    #defines the outer edge in the representation of the field
    i = 0

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

    #area[hydrant_point[0]][hydrant_point[1]] = 3
    return area
  
def irrigator_path(area, hydrant_point):
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

    x_diff = -limit_point_array[0][0] + limit_point_array[1][0] #limit_point_array[1][0]
    y_diff = -limit_point_array[0][1] + limit_point_array[1][1] #limit_point_array[1][1]
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

        # while iii < 3:
        #     ii += 1
        #     next_x_point = math.ceil(limit_point_array[1][0]+ -x_avg_diff*ii)
        #     next_y_point = math.ceil(limit_point_array[1][1]+ -y_avg_diff*ii)
            
        #     if next_x_point < 0 or next_x_point >= len(area) or next_y_point < 0 or next_y_point >= len(area):
        #         complete = False
        #         break

        #     if area[next_x_point][next_y_point] == 2:
        #         break
            #area[next_x_point][next_y_point] = 5
            # if area[next_x_point][next_y_point] == 4:
            #     x_diff = hydrant_found_x - limit_point_array[0][0] #limit_point_array[1][0]
            #     y_diff = hydrant_found_y - limit_point_array[0][1] #limit_point_array[1][1]
            #     diff_total = abs(x_diff) + abs(y_diff)
            #     path_x_avg_diff = -y_diff/diff_total
            #     path_y_avg_diff = x_diff/diff_total
            #     x_avg_diff = x_diff/diff_total
            #     y_avg_diff = y_diff/diff_total
            #     next_x_point = hydrant_found_x
            #     next_y_point = hydrant_found_y
            #     ii = 1
            #     print("Hit this mass")

            #area[next_x_point][next_y_point] = 7
            iii += 1
            

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
    #Creates the relative position
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
    #Generates the path perpendicular to the input path - Not really but becuase of inputs it does
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

    y_avg_diff = -y_avg_diff
    x_avg_diff = -x_avg_diff
    x_point = math.ceil(starting_x_point + x_avg_diff*ii)
    y_point = math.ceil(starting_y_point + y_avg_diff*ii)

    while area[x_point][y_point] != 2 and area[x_point][y_point] != 3 and cross_search(area, x_point, y_point, 1):
        index_back += 1
        x_point = math.ceil(starting_x_point + x_avg_diff*index_back)
        y_point = math.ceil(starting_y_point + y_avg_diff*index_back)

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


#gps_points = [[-43.51034630641096, 172.27928584945678], [-43.50869752859104, 172.2810818047255], [-43.509868165480015, 172.28356545172684], [-43.50977748315201, 172.28138586677255]]

# gps_points = [[-43.51033643662982, 172.27927233023183], [-43.50869955111582, 172.28103238255895], [-43.50980548535269, 172.28348280023854], [-43.50974221105482, 172.2825762215614], [-43.50972570470534, 172.28193137480366], [-43.50976421951377, 172.28149515493809], [-43.50986325747977, 172.28087686069384], [-43.50995954423536, 172.2803951222336], [-43.51014386416757, 172.27980338050298]]
# hydrant_point = [-43.50940856954941, 172.28031738705576]
# hydrant_line = [[-43.51014111312795, 172.27957199431341], [-43.50884260842684, 172.28105893507254]]

gps_points = [[-43.5255092168901, 172.2503196415151], [-43.52512067358927, 172.2497454951688], [-43.523945777431, 172.2497710127842], [-43.521841083383244, 172.25208673638505], [-43.52399203359736, 172.25622696948187], [-43.52396890550832, 172.25414090442385], [-43.52429732354182, 172.25245036240437], [-43.52478300890572, 172.25114258461568], [-43.52538432822429, 172.25013463880782]]
hydrant_point = [-43.52293275802217, 172.25071516455793]
#hydrant_line = [[-43.52379313174176, 172.25027498569247], [-43.522303659794574, 172.2519782865197]]
hydrant_line = [[-43.52219675985696, 172.2522043015012], [-43.52463171327306, 172.25044477245413]]

# gps_points = [[-43.525717842428676, 172.2590376724629], [-43.5275217544466, 172.26211254511725], [-43.53007489155093, 172.2593056074245], [-43.52790103164819, 172.25813179711662], [-43.52650416968434, 172.2572131629626]]
# hydrant_point = [-43.52744774886091, 172.2606325234247]
# hydrant_line = [[-43.52794728480232, 172.2611045993094], [-43.52864107785793, 172.2605559705785]]

# gps_points = [[-43.525717842428676, 172.2590376724629], [-43.5275217544466, 172.26211254511725], [-43.53007489155093, 172.2593056074245], [-43.52790103164819, 172.25813179711662], [-43.52650416968434, 172.2572131629626]]
# hydrant_point = [-43.52744774886091, 172.2606325234247]
# hydrant_line = [[-43.52794728480232, 172.2611045993094], [-43.52864107785793, 172.2605559705785]]

# gps_points = [[-43.52076812868694, 172.5839050917364], [-43.52167616923269, 172.58348117373978], [-43.52294810966299, 172.58526942551862], [-43.52147124298847, 172.58547407558595]]
# hydrant_point = [-43.52135570335104, 172.58484242686166]
# hydrant_line = [[-43.5213712626877, 172.58489607103877], [-43.52133625417457, 172.58477268943145]]

irrigation_radius = 10 #Irrigation radius in meters

# outside_points = [[7, 7], [1, 20], [20, 20], [20, 1]]
# outside_points[0] = [0, 25]
# hydrant_point = (147, 222)


np.set_printoptions(threshold=np.inf)
path_empty = path_init()
outside_points, clean_hydrant_point, clean_hydrant_line, max_x_point, max_y_point = gps_clean(gps_points, hydrant_point, hydrant_line)
path_limit = path_outside(path_empty, outside_points)    
the_pathx, the_pathy = hydrant_line_maker(path_limit, clean_hydrant_line, irrigation_radius)
convert_path(the_pathx, the_pathy, max_x_point, max_y_point)
cv2.waitKey(0)

# irrigator_path(path_limit, hydrant_point)


# http://www.edwilliams.org/avform147.htm#LL