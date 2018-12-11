
"""This module contains the Environment class"""

from agent import *
import copy
import random
import math
import vect
import time

DEBUG = 0

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
        if self.food_counter<15:
            self.charge_food()

    def generate_map(self,nbMap,folder):
        print("Generating maps")

    def save_map(self,name):
        """
        String -> null
        Save the current map (obstacles and food position) in a file named name
        """
        f=open(name,'w')
        for line in self.map:
            str=''
            for c in line:
                str=str+c
            f.write(str+'\n')
        f.close

    def load_map(self, name):
        """
        String->null
        Load the map named name into the environment
        If there is already a map into the game, clear and load a new one
        """
        f=open(name,'r')
        lignes =f.readlines()
        self.map=[]
        for i in range(len(lignes)):
            self.map.append(list(lignes[i])[:self.size])
        f.close()
        self.food_counter=0
        for l in self.map:
            for c in l:
                if c=='$':
                    self.food_counter+=1

    def save_step(self,n):
        self.agent.save_step(n)

    def load_step(self,filename):
        self.agent.load_step(filename)

        
        
    def charge_food(self):
        """
        Add food into the map
        verif no food into the map at the beginning"""
        while self.food_counter<15:
            x=int(random.uniform(0,self.size))
            y=int(random.uniform(0,self.size))
            #print("x:{0}  y:{1}".format(x,y))
            if self.map[x][y]==' ':
                self.map[x][y]='$'
                self.food_counter+=1
                
    def show(self):
        """
        Show all the components of the environment
        """
        c_map=copy.deepcopy(self.map[:])
        c_map[self.agent.pos[0]][self.agent.pos[1]]="I"
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


    """ Meta meta functions """
    def run_manual(self):
        #Variable to save the input of the player
        c_input=''
        #Variable to follow the state of the game
        game_state=0

        #Loop of the game
        while c_input!='x' and game_state==0:
            #Show the map on the terminal
            self.show()
            #Ask the player
            print("Press z, q, s or d to move or x to exit:")
            c_input=input()
            #Update the simulation
            if c_input in ['z','q','s','d']:
                #game_state=env.update_manual(c_input)
                game_state = self.update_manual()

        #End of the game
        if game_state==-1:
            print("Loser")
        if game_state==1:
            print("Winner")   

    def run_simulation(self, nomap = False, delay = 0):
        game_state = 0
        step = 0
        #Loop of the game
        while game_state == 0:
            if nomap == False :
                self.show()
                time.sleep(delay)
            game_state = self.update_q()


        self.save_step(step)
        step += 1

    def run_simulations(self,maxstep,offsetstep = 0):
        step=0 + offsetstep

        while (step<maxstep):


            self.run_simulation()

            self.save_step(step)
            self.reset()


            step += 1


    def reset(self):
        self.map = []
        self.food_counter=0
        self.init_map()
        self.enemies = [[1,12],[6,12],[6,6],[6,18]]
        self.agent.reset()


    """ Meta functions """
    def update_manual(self,direction):
        """
        Char->Int
        Update all the elements of the environment
        Return 0 if the game can continue, 1 if the agent won or -1 if he lost
        """
        x=self.agent.pos[0]
        y=self.agent.pos[1]
        state=True
        #print("x: {0} y: {1}".format(x,y))
        if direction == "q": #move west
            self.agent.action = 3
            y -= 1
        elif direction == "d": #move east
            self.agent.action = 1
            y += 1
        elif direction == "z": #move north
            self.agent.action = 0
            x -= 1
        elif direction == "s": #move south
            self.agent.action = 2
            x += 1
        #print("x: {0} y: {1}".format(x,y))   

        status, reward, new_input_vec = self.step(x,y)

        return status


    def update_q(self):
        status = 0 # 0=nothing special, -1=dead, 1=got all food
        
        # Agent selects an action
        input_vec = self.agent.compute_input_vec(self.map, self.size,self.enemies)
        action = self.agent.select_action(input_vec)

        # Environnement performs the action
        x=self.agent.pos[0]
        y=self.agent.pos[1]
        if action == 0 : #north
            x -= 1
        elif action == 1 : #east
            y += 1
        elif action == 2 : #south
            x += 1
        elif action == 3 : #west
            y -= 1
        else :
            print("(update_q) ERROR, unknown action " + str(action))

        #self.move_agent(x,y)
        
        #Performs one environnement step
        status, reward, new_input_vec = self.step(x,y)

        #Agent adjusts its network
        self.agent.adjust_network(new_input_vec,reward)

        return status

    """ Environnement simulation """
    def step(self,x,y):

        reward = 0
        status = 0

        #Move the agent
        if x>=0 and x<self.size and y>=0 and y<self.size and self.map[x][y]!='O':
            self.agent.has_collided = False
            self.agent.move(x,y)
            if self.map[x][y]=='$':
                self.agent.eat()
                self.map[x][y]=" "
                self.food_counter-=1  
                reward = 0.4
        else : 
            self.agent.has_collided = True

        #Check game status, reward
        if ([x,y] in self.enemies) or self.agent.energy==0: 
            status = -1
            reward = -1
        elif self.food_counter==0:
            status = 1
        else:
            status = self.move_all_ennemies()
            if status == -1:
                reward = -1

        #Compute agent new state
        new_input_vec = self.agent.compute_input_vec(self.map, self.size, self.enemies)

        if DEBUG :
            print("LEAVING environment.step : \n\t status={0}\n\t reward={1}\n\tnew_input_vec={2}".format(status,reward,new_input_vec))

        return (status,reward, new_input_vec)
       
        
    def move_all_ennemies(self):
        """
        Move all the enemies of the environment toward the agent
        """
        a=self.agent.pos
        action=[[1,0],[0,1],[-1,0],[0,-1]]
        for e in self.enemies:
            prob=random.random()
            if prob<0.8:
                dist=vect.dist(a,e)
                P=[]
                for ac in action:
                    tmp=[e[0]+ac[0],e[1]+ac[1]]
                    if tmp==self.agent.pos:
                        return -1
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
        return 0

    def move_ennemy(self,n):
        """
        Int -> null
        Generate the motion of enemy number n
        """
        a=self.agent.pos
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
             
    
            
                

