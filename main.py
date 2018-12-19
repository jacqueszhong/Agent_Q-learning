"""Run to play the simulation of an agent in a maze full of obstacles, ennemies and food"""
"""Virtual environnement :
virtualenv --system-site-packages -p python3 ./venv
source ./venv/bin/activate  # sh, bash, ksh, or zsh   
"""

import time
from simulator import *


sim = Simulator()





i=0
while(i<1):
	sim.load_quicksave()
	sim.experiment_run(replay=False, delay = 0.0, nomap=True)	

"""


#sim.test_run(10)
i=1
while(i<20):
	#Parameter to change
	sim.env.agent.brain._lr = 0.01 + i*0.01	

	#sim.load_quicksave()
	sim.experiment_run(replay=False, delay = 0.0, nomap=True)
	sim = Simulator()
	

	i+=1
#sim.generate_maps(301,50)

i=1
while(i<10):
	#Parameter to change
	sim.env.agent.brain._lr = 0.01 - i*0.001	

	#sim.load_quicksave()
	sim.experiment_run(replay=False, delay = 0.0, nomap=True)
	sim = Simulator()
	

	i+=1

"""