
"""This module contains the Sensor class"""


class Sensor:

    """
    Robot class with:
    - type
    - position regarding the agent owner
    - response
    
    """

    def __init__(self,type_s,field,x,y): #constructor
        self.type_s=type_s #type of sensor 'O' obstacles, 'E' ennemies, '$' food
        self.field=field # fix the range of the sensor 'X' 5 'O' 9 or 'Y' 13
        self.pos=[x,y]
        self.response=False

    def __repr__(self):
        return "Type:{0}  Field:{1} Position:{2}  Activated ? {3}".format(self.type_s,self.field,self.pos,self.response)

    def detect_area(self,a_pos,e_map):
        self.response=False
        i=0
        self.response=self.detect_xy(e_map,self.pos[0],self.pos[1])
        if self.response:
            return
        
        area=[[-1,0],[0,-1],[1,0],[0,1]]            
        if self.field!='X':
            area=area+[[-1,-1],[1,-1],[1,1],[-1,1]]
        if self.field=='Y':
            area=area+[[-2,0],[0,-2],[2,0],[0,2]]
        
        while not self.response and i<len(area):
            self.response=self.detect_xy(e_map,self.pos[0]+area[i][0],self.pos[1]+area[i][1])
            i+=1

    def detect_xy(self,e_map,x,y):
        if e_map[x][y]==self.type_s:
            return True
        else:
            return False
