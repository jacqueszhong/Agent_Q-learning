# Agent_Q-learning
Self-learning agent based on Q-learning

This project is based on the article "Self-Improving Reactive Agent Based on Reinforcement Learning" by Long-Ji Lin (1992).
Coded in Python.

We developped this project as part of our master's degree in AI in 2018.

## Getting Started

You are playing an agent in a closed environment with obstacles 'O', 4 enemies 'E' and food '$'.
Your goal is to live as long as you can, avoiding enemies and eating food in order to get energy.

Your initial energy level is 40 and you earn 15 every time you eat.

Once the game is running no more food can appear on the map.
If one ennemy is on the same place than you or if you run out of energy you die.

To run the simulation as a game just run the main.py file
```
python main.py
```

To move the agent use:
'z' to move north
's' to move south
'q' to move west
'd' to move east

To exit use:
'x'

## Minor bugs
* Fix the nparray / list conflict 

## Authors

* **Maëva A.** - [BarbeBleue](https://github.com/barbebleue)

* **Jacques Z.** - [Jaquapi](https://github.com/jacqueszhong)
