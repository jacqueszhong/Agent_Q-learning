"""Run to play the simulation of an agent in a maze full of obstacles, ennemies and food"""
"""Virtual environnement :
virtualenv --system-site-packages -p python3 ./venv
source ./venv/bin/activate  # sh, bash, ksh, or zsh   
"""

import time
from environment import *

maxstep = 200

env = Environment()

step = 0
while (step<maxstep):


    env.run_simulation()

    env.save_step(step)
    env.reset()


    step += 1