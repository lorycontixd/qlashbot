#games
import random
import threading
from instances import *


#*****************************************************************************************************************
#*********************************************       BOMB     ****************************************************
#*****************************************************************************************************************

math_expressions = {
    "150x12":1800,
    "220/5":44,
    "330x9":2970,
    "70x71":4970
}

bombIsSet = False

async def BombExplode():
    print("BOOOM")

async def BombSet():

    global bombIsSet
    assert bombIsSet == False
    t = threading.Timer(10.0, BombExplode)
    bombIsSet = True
    t.start()

    return t

async def BombDefuse(timer):
    global math_expressions
    choice = random.choice(list(math_expressions.keys()))
    print("To defuse please solve "+str(choice))
    x = input()
    if int(x)==int(math_expressions[choice]):
        print("bomb defused")
        timer.cancel()
    else:
        print("wrong")
        BombExplode()

timer = BombSet()
BombDefuse(timer)
