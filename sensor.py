
"""This module contains the Sensor class"""


class Sensor:

    """
    Robot class with:
    - type
    - field
    - position regarding the agent owner
    - response
    
    """

    def __init__(self,type_s,field,coord): #constructor
        self.type_s=type_s #char type of sensor 'O' obstacles, 'E' ennemies, '$' food
        self.field=field # char fix the range of the sensor 'o' 1 'X' 5 'O' 9 or 'Y' 13
        self.pos=coord # [int,int] position regarding the agent owner
        self.response=False # bool detect or not

    def __repr__(self):
        #return "(T:{0}  F:{1} Pos:{2}  ON? {3})".format(self.type_s,self.field,self.pos,self.response)
        return "{2}".format(self.type_s,self.field,self.pos,self.response)

    def detect(self,a_pos,e_map,size): #TODO: vérifier qu'on regarde dans la map size
        area=[]
        self.response=False
        x=a_pos[0]+self.pos[0]
        y=a_pos[1]+self.pos[1]
        self.response=self.detect_xy(e_map,[x,y],size)
        if self.response:
            print('o')
            return
        if self.field!='o':
            area=[[-1,0],[0,-1],[1,0],[0,1]]
            
            if self.field!='X':
                area=area+[[-1,-1],[1,-1],[1,1],[-1,1]]
            
                if self.field!='O':
                    area=area+[[-2,0],[0,-2],[2,0],[0,2]]
                    print('Y')
                else:
                    print('O')
            else:
                print('X')
        else:
            print('o')
            return
        

        i=0
        while not self.response and i<len(area):
            x=self.pos[0]+area[i][0]
            y=self.pos[1]+area[i][1]
            self.response=self.detect_xy(e_map,[x,y],size)
            i+=1

    def detect_xy(self,e_map,coord,size):
        x=coord[0]
        y=coord[1]
        if x>=0 and x<size and y>=0 and y<size:
            if e_map[x][y]==self.type_s:
                return True
            else:
                return False
