
"""This module contains the Agent class"""


class Agent:

    """Robot class with:
    - position
    - energy level
    TODO: sensors

    """

    def __init__(self): #constructor

        self.coord = [18,12] # list[int,int] : coordinates [x,y]
        self.energy = 40 # int: initial energy level
        self.obstacle_sensor = [] # list[int*]
        self.food_sensor = [] # list[int*]
        self.enemies_sensor = [] # list[int*]

    def move(self,x,y):
        """
        int*int->null
        Change the position of the agent
        """
        self.energy-=1
        self.coord=[x,y]

    def eat(self):
        """
        Increase energy level by 15
        """
        self.energy+=15    #is there a max level ?

          
    def __repr__(self):
        return "Position:{0}  Energy:{1}".format(self.coord,self.energy)
