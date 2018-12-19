"""Run to play the simulation of an agent in a maze full of obstacles, ennemies and food"""
"""Virtual environnement :
virtualenv --system-site-packages -p python3 ./venv
source ./venv/bin/activate  # sh, bash, ksh, or zsh   
"""

import time
from simulator import *
import cProfile


sim = Simulator()





i=0
while(i<1):
	#sim.load_quicksave()

	#sim.env.agent.brain._lr = 0.01 + i*0.01

	sim.experiment_run(replay=False, delay = 0.0, nomap=True,nb_test=50)
	i += 1	
