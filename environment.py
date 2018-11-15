
"""This module contains the Environment class"""

from agent import *
import copy
import random
import math
import vect

class Environment:

    """

    Environment class with:
        - self.size: size of the square map
        - self.agent: agent
        - self.map: 2D-array representing the map with the obstacles
        - self.food: list of 2-uplets representing the food elements
        - self.ennemies: list of 2-uplets representing the enemies

    """

    def __init__(self): #constructor

        self.size = 25
        self.agent = Agent()
        self.map = []
        self.food_counter=0
        self.init_map()
        self.enemies = [[1,12],[6,12],[6,6],[6,18]]

    def init_map(self):
        """Initialize a clean map of size 25x25 with just obstacles"""
        f=open("clean_map.txt",'r')
        lignes =f.readlines()
        for i in range(len(lignes)):
            self.map.append(list(lignes[i])[:self.size])
        f.close()
        self.charge_food()    

    def load_map(self, name):
        """
        String->null
        Load the map named name into the environment
        If there is already a map into the game, clear and load a new one
        """
        f=open(name,'r')
        lignes =f.readlines()
        for i in range(len(lignes)):
            self.map.append(list(lignes[i])[:self.size])
        f.close()
        
    def charge_food(self):
        """ add food into the map
        TODO: verif no food into the map at the beginning"""
        while self.food_counter<15:
            x=int(random.uniform(0,25))
            y=int(random.uniform(0,25))
            #print("x:{0}  y:{1}".format(x,y))
            if self.map[x][y]==' ':
                self.map[x][y]='$'
                self.food_counter+=1
                
    def show(self):
        """
        Show alle the components of the environment
        """
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
        """
        Char->Bool
        Update all the elements of the environment
        """
        x=self.agent.coord[0]
        y=self.agent.coord[1]
        state=True
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
        if [x,y] in self.enemies:
            return False
        else:         
            return self.move_all_ennemies() 
        
    def move_all_ennemies(self):
        """
        Move all the enemies of the environment toward the agent
        """
        a=self.agent.coord
        action=[[1,0],[0,1],[-1,0],[0,-1]]
        for e in self.enemies:
            prob=random.random()
            if prob<0.8:
                dist=vect.dist(a,e)
                P=[]
                for ac in action:
                    tmp=[e[0]+ac[0],e[1]+ac[1]]
                    if tmp==self.agent.coord:
                        return False
                    elif self.map[tmp[0]][tmp[1]]!='O':
                        angle=vect.angle(ac,[a[0]-e[0],a[1]-e[1]])
                        w=(180-abs(angle))/180
                        P.append(math.exp(0.33*w*t(dist)))
                    else:
                        P.append(0)
                sum=0
                #print(P)
                for p in P:
                    sum=sum+p
                for i in range(len(P)):
                    P[i]=P[i]/sum
                #print(P)
                move=P.index(max(P))
                e[0]+=action[move][0]
                e[1]+=action[move][1]
        return True

    def move_ennemy(self,n):
        a=self.agent.coord
        action=[[1,0],[0,1],[-1,0],[0,-1]] # south east north west 
        e=self.enemies[n]
        dist=vect.dist(a,e)
        P=[]
        for ac in action:
            tmp=[e[0]+ac[0],e[1]+ac[1]]
            if self.map[tmp[0]][tmp[1]]!='O':
                angle=vect.angle(ac,[a[0]-e[0],a[1]-e[1]])
                print(angle)
                w=(180-abs(angle))/180
                P.append(math.exp(0.33*w*t(dist)))
            else:
                P.append(0)
        sum=0
        print(P)
        for p in P:
            sum=sum+p
        for i in range(len(P)):
            P[i]=P[i]/sum
        #print(P)
        move=P.index(max(P))
        self.enemies[n][0]=e[0]+action[move][0]
        self.enemies[n][1]=e[1]+action[move][1]

    
def t(dist):
    """
    For the calculation of the probabilities to do a certain action for ennemies
    """
    if dist<=4:
        return 15-dist
    if dist <=15:
        return 9-dist/2
    else:
        return 1
             
    
            
                

