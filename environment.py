
"""This module contains the Environment class"""

from agent import *

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
        self.init_map()
        self.food = self.init_food()
        #self.enemies = self.init_enemies()

    def init_map(self):
        """ Initialize a clean map of size 25x25 with just obstacles"""
        f=open("clean_map.txt",'r')
        lignes =f.readlines()
        for i in range(len(lignes)):
            self.map.append(list(lignes[i])[:self.size])
        f.close()

    """def init_food():
        for i in range(15):
            list.append

    def is_free():
        if map"""

    def show(self):
        for i in range(len(self.map)):
            str=""
            for c in self.map[i]:
                str=str+c
            print(str)
                

