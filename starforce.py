import time, random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# global variables
__INITSTAR__ = 17
__GOAL__ = 22
__EQUIPMENTLEVEL__ = 150
__SIMULATIONS__ = 100000

success_arr = [0.95, 0.90, 0.85, 0.85, 0.8, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.03, 0.02, 0.01]
destroy_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.01, 0.02, 0.03, 0.03, 0.03, 0.03, 0.04, 0.04, 0.10, 0.10, 0.20, 0.30, 0.40]

star = __INITSTAR__
goal = __GOAL__
destroyed = False
failstack = 0
safeguard = False
starcatch = True
_5_10_15 = False
boom = 0
meso = 0

# initialize results dict
results = dict()
for i in range(26): 
    results.setdefault(i, 0)

start_time = time.time()
for i in range(__SIMULATIONS__): 
    while not destroyed and star != goal:
        # chance time
        if failstack == 2: 
            star += 1
            failstack = 0    
        # normal starring
        else: 
            # if successful, star += 1
            if random.random() < success_arr[star]:
                star += 1
                failstack = 0
            # failed logic 
            else: 
                # fail maintain logic
                # check if boomed
                if random.random() < destroy_arr[star]:
                    # 18 and higher cannot safeguard
                    if safeguard and star < 17:
                        star -= 1
                        failstack +=1 
                    else: 
                        destroyed = True
                        boom += 1 
                else: 
                    # checkpoints
                    if star <= 10 or star == 15 or star == 20: 
                        failstack += 1
                        continue
                    else: 
                        star -= 1
                        failstack += 1
        # print(star)
    results[star] += 1
    star = 12
    destroyed = False
for i in range(12,26):
    print(i, results[i])
print("booms:", boom)
print("simulations:", __SIMULATIONS__)
end_time = time.time()
print("time elapsed:", end_time - start_time)

    # print(star, destroyed)