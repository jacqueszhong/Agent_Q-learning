
"""This module contains the Agent class"""


class Agent:

    """Robot class with:
    - position
    - energy level
    TODO: sensors

    """

    def __init__(self): #constructor

        self.coord = [18,12]
        self.energy = 40

    def move(self, direction):

        x=self.coord[0]
        y=self.coord[1]
        if direction == "w": #move west
            x = x - 1
            self.energy-=1
        elif direction == "e": #move east
            x = x + 1
            self.energy-=1
        elif direction == "n": #move north
            y = y - 1
            self.energy-=1
        elif direction == "s": #move south
            y = y + 1
            self.energy-=1
        else:
            pass
        self.coord=[x,y]

    def eat(self):
        energy=+15    #is there a max level ?

          
    def __repr__(self):
        return "Position:{0}  Energy:{1}".format(self.coord,self.energy)
