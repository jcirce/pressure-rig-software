'''
Curvature, circumradius, and circumcenter functions
written by Hunter Ratliff on 2019-02-03
'''

def curvature(x_data,y_data):
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
    for i in range(1,len(x_data)-1):
        R = circumradius(x_data[i-1:i+2],y_data[i-1:i+2])
        if ( R == 0 ):
            print('Failed: points are either collinear or not distinct')
            return 0
        curvature.append(1/R)
    return curvature

def circumradius(xvals,yvals):
    '''
    Calculates the circumradius for three 2D points
    '''
    x1, x2, x3, y1, y2, y3 = xvals[0], xvals[1], xvals[2], yvals[0], yvals[1], yvals[2]
    den = 2*((x2-x1)*(y3-y2)-(y2-y1)*(x3-x2))
    num = ( (((x2-x1)**2) + ((y2-y1)**2)) * (((x3-x2)**2)+((y3-y2)**2)) * (((x1-x3)**2)+((y1-y3)**2)) )**(0.5)
    if ( den == 0 ):
        print('Failed: points are either collinear or not distinct')
        return 0
    R = abs(num/den)
    return R

def circumcenter(xvals,yvals):
    '''
    Calculates the circumcenter for three 2D points
    '''
    x1, x2, x3, y1, y2, y3 = xvals[0], xvals[1], xvals[2], yvals[0], yvals[1], yvals[2]
    A = 0.5*((x2-x1)*(y3-y2)-(y2-y1)*(x3-x2))
    if ( A == 0 ):
        print('Failed: points are either collinear or not distinct')
        return 0
    xnum = ((y3 - y1)*(y2 - y1)*(y3 - y2)) - ((x2**2 - x1**2)*(y3 - y2)) + ((x3**2 - x2**2)*(y2 - y1))
    x = xnum/(-4*A)
    y =  (-1*(x2 - x1)/(y2 - y1))*(x-0.5*(x1 + x2)) + 0.5*(y1 + y2)
    return x, y

# test values
x = [0,0.8,2.8]
y = [0,1.6,-0.4]

print(curvature(x,y))
#print(circumradius(x[0:3],y[0:3]))
#print(circumcenter(x[0:3],y[0:3]))