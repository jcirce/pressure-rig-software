'''
Curvature, circumradius, and circumcenter functions
written by Hunter Ratliff on 2019-02-03
'''
'''
Curvate function modified with the addition of r, and pixel size
'''

def curvature(x_data,y_data, pxlx, pxly):
    '''
    Calculates curvature for all interior points
    on a curve whose coordinates are provided
    Input:
        - x_data: list of n x-coordinates
        - y_data: list of n y-coordinates
    Output:
        - curvature: list of n-2 curvature values
    '''
    curvature = []
    r = 0
    for i in range(1,len(x_data)-1):
        R = circumradius(x_data[i-1:i+2],y_data[i-1:i+2], pxlx, pxly)
        if ( R == 0 ):
            print('Failed: points are either collinear or not distinct')
            i = i+1
            r = 1
            #return 0
        if r == 0:  # added r so that it keeps printing results even if one point failed
            curvature.append(1/R)
        r = 0
    return curvature

def circumradius(xvals,yvals, pxlx, pxly):
    '''
    Calculates the circumradius for three 2D points
    '''
    x1, x2, x3, y1, y2, y3 = xvals[0]/pxlx, xvals[1]/pxlx, xvals[2]/pxlx, yvals[0]/pxly, yvals[1]/pxly, yvals[2]/pxly
    den = 2*((x2-x1)*(y3-y2)-(y2-y1)*(x3-x2))
    num = ( (((x2-x1)**2) + ((y2-y1)**2)) * (((x3-x2)**2)+((y3-y2)**2)) * (((x1-x3)**2)+((y1-y3)**2)) )**(0.5)
    if ( den == 0 ):
        print('Failed: points are either collinear or not distinct')
        return 0
    R = abs(num/den)
    return R

def circumcenter(xvals,yvals, pxlx, pxly):
    '''
    Calculates the circumcenter for three 2D points
    '''
    x1, x2, x3, y1, y2, y3 = xvals[0]/pxlx, xvals[1]/pxlx, xvals[2]/pxlx, yvals[0]/pxly, yvals[1]/pxly, yvals[2]/pxly
    A = 0.5*((x2-x1)*(y3-y2)-(y2-y1)*(x3-x2))
    if ( A == 0 ):
        print('Failed: points are either collinear or not distinct')
        return 0
    xnum = ((y3 - y1)*(y2 - y1)*(y3 - y2)) - ((x2**2 - x1**2)*(y3 - y2)) + ((x3**2 - x2**2)*(y2 - y1))
    x = xnum/(-4*A)
    y =  (-1*(x2 - x1)/(y2 - y1))*(x-0.5*(x1 + x2)) + 0.5*(y1 + y2)
    return x, y

# test values
x = [2590, 1792, 1989]
y = [1940, 1185, 1127]

x1 = [1858, 2341, 2624, 2407, 1972]
y1 = [2331, 2271, 1777, 1250, 1141]

x2 = [2341, 2624, 2407]
y2 = [2271, 1777, 1250]

# x3 = [2553, 2392, 1703, 2509, 2331, 1634, 2541]
# y3 = [1419, 2239, 2266, 2065, 1215, 1303, 2041]

# x3 = [26, 48, 127, 180, 334, 340]
# y3 = [280, 405, 465, 476, 377, 298]
x3 = [26, 127, 340]
y3 = [280, 465, 298]

# 1634 1703 2331 2392 2509 2541 2553
# 1303 2266 1215 2239 2065 2041 1419

# 1215 1303 1419 2041 2065 2239 2266
# 2331 1634 2553 2541 2509 2392 1703

# print('Curvature:')
# print(curvature(x3,y3))
# # print(curvature(x1,y1))
# # print(curvature(x2,y2))

# print('Other Data:')
# print(circumradius(x[0:3],y[0:3]))
# print(circumcenter(x[0:3],y[0:3]))
# print(circumradius(x1[0:3],y1[0:3]))
# print(circumcenter(x1[0:3],y1[0:3]))
# print(circumradius(x2[0:3],y2[0:3]))
# print(circumcenter(x2[0:3],y2[0:3]))
