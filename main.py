"""Run to play the simulation of an agent in a maze full of obstacles, ennemies and food"""

from environment import *

#Creation of the environment of the game
env=Environment()
#Variable to save the input of the player
c_input=''
#Variable to follow the state of the game
game_state=0

#Loop of the game
while c_input!='x' and game_state==0:
    #Show the map on the terminal
    env.show()
    #Ask the player
    print("Press z, q, s or d to move or x to exit:")
    c_input=input()
    #Update the simulation
    if c_input in ['z','q','s','d']:
        game_state=env.update(c_input)
        
#End of the game
if game_state==-1:        
    print("Loser")
if game_state==1:        
    print("Winner")

