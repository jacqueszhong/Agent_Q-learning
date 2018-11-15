"""Run to play the simulation of an agent in a maze full of obstacles, ennemies and food"""

from environment import *

#Creation of the environment of the game
env=Environment()

c=""
g=True

#Loop of the game
while c!='x' and g==True:
    #Show the map on the terminal
    env.show()
    #Ask the player
    print("Press z, q, s or d to move or x to exit:")
    c=input()
    #Update the game
    if c in ['z','q','s','d']:
        g=env.update(c)
    if not g:        
        print("Loser")

