
"""This module contains the Agent class"""

import numpy as np
from math import floor
import time #sauvegarde de poids

from constant import *
from sensor import *
from agent_brain import AgentBrain

class Agent:

    """Robot class with:
    - position
    - energy level
    TODO: sensors

    """

    def __init__(self): #constructor

        self.has_collided = False
        self.action = -1

        self.pos = [18,12] # list[int,int] : coordinates [x,y]
        self.energy = 40 # int: initial energy level
        self.food_sensor = []
        self.enemies_sensor = []
        self.obstacles_sensor = [] #40
        self.init_sensors()

        self.brain = AgentBrain()

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
        

    def compute_input_vec(self, e_map, e_size, enemies):
        """
        Return the input representation given some information about the environement.

        :return: numpy.ndarray, shape (1x145)
        """

        #Observe environnement
        self.detect(e_map,e_size, enemies)

        #Constructs state vector
        #Sensors input units
        input_vec = np.zeros(145,np.int)
        i = 0
        for f in self.food_sensor:
            input_vec[i] = f.response
            i+=1

        for e in self.enemies_sensor:
            input_vec[i] = e.response
            i+=1

        for o in self.obstacles_sensor:
            input_vec[i] = o.response
            i+=1

        #Energy input units
        ind = floor((self.energy+3)/7)
        if ind > 15:
            ind = 15
        input_vec[124 + ind] = 1

        #History input units
        if self.action != -1 :
            input_vec[140 + self.action] = 1

        #Collision input unit
        input_vec[144] = self.has_collided

        return input_vec


    def select_action(self,input_vec):
        """
        Wrapper of AgentBrain.select_action
        """
        return self.brain.select_action(input_vec)

    def adjust_network(self,new_input_vec,reward):
        """
        Wrapper of AgentBrain.adjust_network
        """
        self.brain.adjust_network(new_input_vec, reward)

    def save_step(self,step):
        """ Wrapper of agent_brain.savew """
        name = "Hidden"+str(self.brain.get_nbHidden())+"_Step" + str(step) + "_"
        s = str(time.time())
        s = s.replace(".","")
        s = s[4:]
        name = "NN_save/" + name + s + ".h5"
        self.brain.savew(name)
        self.brain.savew("NN_save/quicksave.h5")

    def load_step(self,filename):
        """ Wrapper of agent_brain.loadw """
        self.brain.loadw(filename)

    def reset(self):
        self.has_collided = False
        self.action = -1
        self.pos = [18,12]
        self.energy = 40
        
        self.brain.reset()


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


    def detect(self,e_map,size,enemies):
        """
        List[int][int]->null
        """
        for f in self.food_sensor:
            f.detect(self.pos,e_map,size,enemies)
        for e in self.enemies_sensor:
            e.detect(self.pos,e_map,size,enemies)
        for o in self.obstacles_sensor:
            o.detect(self.pos,e_map,size,enemies)

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
                        
