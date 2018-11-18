
"""This module contains the Agent class"""

from constant import *
from sensor import *

class Agent:

    """Robot class with:
    - position
    - energy level
    TODO: sensors

    """

    def __init__(self): #constructor

        self.pos = [18,12] # list[int,int] : coordinates [x,y]
        self.energy = 40 # int: initial energy level
        self.food_sensor = []
        self.enemies_sensor = []
        self.obstacles_sensor = [] #40
        self.init_sensors()

    def init_sensors(self):
        for coord in SENSOR_X:
            self.food_sensor.append(Sensor('$','X',coord))
            self.enemies_sensor.append(Sensor('E','X',coord))                                                                              
        for coord in SENSOR_O:            
            self.food_sensor.append(Sensor('$','O',coord))          
            self.enemies_sensor.append(Sensor('E','O',coord))
        for coord in SENSOR_Y:           
            self.food_sensor.append(Sensor('$','Y',coord))
        for coord in SENSOR_o:           
            self.obstacles_sensor.append(Sensor('O','o',coord))
        

    def move(self,x,y):
        """
        int*int->null
        Change the position of the agent
        """
        self.energy-=1
        self.pos=[x,y]

    def eat(self):
        """
        Increase energy level by 15
        """
        self.energy+=15    #is there a max level ?


    def detect(self,e_map,size):
        """
        List[int][int]->null
        """
        print("Food")
        for f in self.food_sensor:
            f.detect(self.pos,e_map,size)
        print("Enemies")
        for e in self.enemies_sensor:
            e.detect(self.pos,e_map,size)
            
        print("Obstacles")
        for o in self.obstacles_sensor:
            o.detect(self.pos,e_map,size)

    def show_sensors(self,type):
        map=[[] for i in range(21)]
        for x in range(21):
            for y in range(21):
                map[x].append(' ')
        a=10
        map[a][a]='I'
        if type=='$':
            for i in self.food_sensor:
                map[a+i.pos[0]][a+i.pos[1]]=i.field
        if type=='E':
            for i in self.enemies_sensor:
                map[a+i.pos[0]][a+i.pos[1]]=i.field                
        if type=='O':
            for i in self.obstacles_sensor:
                map[a+i.pos[0]][a+i.pos[1]]=i.field

        for x in range(21):
            str=''
            for c in map[x]:
                str=str+c
            print(str)

    def __repr__(self):
        return "Position:{0}  Energy:{1}".format(self.pos,self.energy)
                        
