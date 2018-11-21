
"""This module contains the Sensor class"""


class Sensor:

    """
    Robot class with:
    - type: Char
    - field: Char
    - position regarding the agent owner: [Int,Int]
    - response: Bool 
    
    """

    def __init__(self,type_s,field,coord): #constructor
        self.type_s=type_s #char type of sensor 'O' obstacles, 'E' ennemies, '$' food
        self.field=field # char fix the range of the sensor 'o' 1 'X' 5 'O' 9 or 'Y' 13
        self.pos=coord # [int,int] position regarding the agent owner
        self.response=False # bool detect or not

    def __repr__(self):
        #return "(T:{0}  F:{1} Pos:{2}  ON? {3})".format(self.type_s,self.field,self.pos,self.response)
        return "{2}".format(self.type_s,self.field,self.pos,self.response)

    def detect(self,a_pos,e_map,size,enemies):
        """
        [Int,Int]*List[List[Char]*Int
        Look if the sensor detect something of type self.type in the map e_map
        """
        area=[]
        self.response=False
        x=a_pos[0]+self.pos[0]
        y=a_pos[1]+self.pos[1]

        self.response=self.detect_xy(e_map,[x,y],size,enemies) #Test sensor position
        
        if self.response:
            return
        if self.field!='o':
            area=[[-1,0],[0,-1],[1,0],[0,1]] # X
            
            if self.field!='X':
                area=area+[[-1,-1],[1,-1],[1,1],[-1,1]] # O
            
                if self.field!='O':
                    area=area+[[-2,0],[0,-2],[2,0],[0,2]] # Y
        else: # o           
            return

        i=0 
        while not self.response and i<len(area):
            x=a_pos[0]+self.pos[0]+area[i][0]
            y=a_pos[1]+self.pos[1]+area[i][1]
            self.response=self.detect_xy(e_map,[x,y],size,enemies)
            i+=1

        #print("{0}, {1}, {2}".format(x,y))

    def detect_xy(self,e_map,coord,size,enemies):
        """
        Look if the sensor detect something of type self.type in e_map at coord
        """
        x=coord[0]
        y=coord[1]
        if x>=0 and x<size and y>=0 and y<size:

            if self.type_s == 'E' and coord in enemies : #Enemy sensor
                return True

            elif e_map[x][y]==self.type_s: #Food / obstacle sensor
                return True

        return False
