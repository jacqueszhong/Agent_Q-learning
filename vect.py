import math

def len(u):
    """
    [int,int] -> int
    Return the length of vector u"""
    return math.sqrt(u[0]*u[0]+u[1]*u[1])
    

def dist(u,v):
    """
    [int,int]*[int,int] -> int
    Return the distance bewteen points u and v"""
    return math.sqrt((u[0]-v[0])*(u[0]-v[0])+(u[1]-v[1])*(u[1]-v[1]))

def angle(u,v):
    """
    [int,int]*[int,int] -> int
    Return the angle in degree formed by two vectors u and v"""
    scal = u[0]*v[0]+u[1]*v[1]
    return math.degrees(math.acos(scal/(len(u)*len(v))))
