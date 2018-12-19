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
	sim.load_quicksave()

	sim.experiment_run(replay=True, delay = 0.0, nomap=True)
	#cProfile.run(sim.experiment_run(replay=False, delay = 0.0, nomap=True))
	
	i += 1
