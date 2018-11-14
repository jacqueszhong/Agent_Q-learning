
"""This module contains the Agent class"""


class Agent:

    """Robot class with:
    - position
    - energy level
    TODO: sensors

    """

    def __init__(self): #constructor

        self.coord = [8,12]
        self.energy = 40

    def move(self,x,y):
        self.energy-=1
        self.coord=[x,y]

    def eat(self):
        self.energy+=15    #is there a max level ?

          
    def __repr__(self):
        return "Position:{0}  Energy:{1}".format(self.coord,self.energy)
