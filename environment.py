
"""This module contains the Environment class"""

from agent import *
import copy
import random
import math

class Environment:

    """

    Environment class with:
        - self.size: size of the square map
        - self.agent: agent
        - self.map: 2D-array representing the map with the obstacles
        - self.food: list of 2-uplets representing the food elements
        - self.ennemies: list of 2-uplets representing the enemies



    """

    def __init__(self):

        self.size = 25
        self.agent = Agent()
        self.map = []
        self.food_counter=0
        self.init_map()
        self.enemies = [[1,12],[6,12],[6,6],[6,18]]

    def init_map(self):
        """ Initialize a clean map of size 25x25 with just obstacles"""
        f=open("clean_map.txt",'r')
        lignes =f.readlines()
        for i in range(len(lignes)):
            self.map.append(list(lignes[i])[:self.size])
        f.close()
        self.init_food()    

    def loaf_map(self, name):
        f=open(name,'r')
        lignes =f.readlines()
        for i in range(len(lignes)):
            self.map.append(list(lignes[i])[:self.size])
        f.close()
        
    def init_food(self):
        """ add food into the map
        TODO: verif no food into the map at the begnning"""
        while self.food_counter<15:
            x=int(random.uniform(0,25))
            y=int(random.uniform(0,25))
            #print("x:{0}  y:{1}".format(x,y))
            if self.map[x][y]==' ':
                self.map[x][y]='$'
                self.food_counter+=1
                
    def show(self):
        c_map=copy.deepcopy(self.map[:])
        c_map[self.agent.coord[0]][self.agent.coord[1]]="I"
        for e in self.enemies:
            c_map[e[0]][e[1]]="E"
        #print(c_map)
        print("---------------------------")
        for i in range(len(c_map)):
            str=""
            for c in c_map[i]:
                str=str+c
            print("|"+str+"|")
        
        print("---------------------------")
        str2=""
        for i in range(self.agent.energy):
            str2=str2+"H"
        print(str2)

    def update(self,direction):
        x=self.agent.coord[0]
        y=self.agent.coord[1]
        #print("x: {0} y: {1}".format(x,y))
        if direction == "q": #move west
            y -= 1
        elif direction == "d": #move east
            y += 1
        elif direction == "z": #move north
            x -= 1
        elif direction == "s": #move south
            x += 1
        #print("x: {0} y: {1}".format(x,y))   
            
        if x>0 and x<25 and y>0 and y<25 and self.map[x][y]!='O':
            self.agent.move(x,y)
            if self.map[x][y]=='$':
                self.agent.eat()
                self.map[x][y]=" "
                self.food_counter-=1
                print(self.food_counter)
        #self.move_ennemies() #TODO
        if [x,y] in self.enemies:
            print("You loose")
            return False
        else:
            return True
        

    """"
    TODO
    def move_ennemies(self):
        prob=random.random()
        #if prob<0.2
        a=self.agent.coord
        for e in self.enemies:
        w=(180-abs(a))/180
        dist=math.sqrt((a[0]-e[0])*(a[0]-e[0])+(a[1]-e[1])*(a[1]-e[1]))"""
            
                

