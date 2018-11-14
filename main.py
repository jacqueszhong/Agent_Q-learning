from environment import *

env=Environment()
env.show()
c=""
g=True
while c!='x' and g==True:
    print("Press z, q, s or d to move or x to exit:")
    c=input()
    if c in ['z','q','s','d']:
        g=env.update(c)
        env.show()

