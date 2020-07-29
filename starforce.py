import time, random
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.path as path

# data taken from https://strategywiki.org/wiki/MapleStory/Spell_Trace_and_Star_Force
# https://en.wikipedia.org/wiki/Moving_average#Cumulative_moving_average
# https://stackoverflow.com/questions/513882/python-list-vs-dict-for-look-up-table
# changing list lookup -> dict lookup wil reduce runtime for large input n
# runtime may be slightly longer with if-statement logic which bypasses fail maintain/decrease logic
# instead, two numbers are generated per iteration: 
#   first to see if the success passes
#   if not, then roll again for destroy chance

# global variables
__INITSTAR__ = 20
__GOAL__ = 22
__EQUIPMENTLEVEL__ = 150
__SIMULATIONS__ = 1 * 10 ** 4

star = __INITSTAR__
goal = __GOAL__
destroyed = False
failstack = 0
safeguard = False
starcatch = True
_5_10_15 = False
_30off = False
boom = 0
meso = 0
meso_avg = 0
count = 0

min_meso = 10 ** 22
max_meso = 0
# normal starring array: 
success_arr = [0.95, 0.90, 0.85, 0.85, 0.8, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.03, 0.02, 0.01]
# star_catch success_arr:
# success_arr = [0.99275, 0.9405, 0.88825, 0.88825, 0.836, 0.78375, 0.7315, 0.67925, 0.627, 0.57475, 0.5225, 0.47025, 0.418, 0.36575, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.03135, 0.0209, 0.01045]
# 5_10_15 success_arr: 
# success_arr = [0.95, 0.90, 0.85, 0.85, 0.8, 1, 0.70, 0.65, 0.60, 0.55, 1, 0.45, 0.40, 0.35, 0.30, 1, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.03, 0.02, 0.01]
# star_catch success_arr during 5/10/15, given by [1.045 * i for i in success_arr] and float errors removed:
# success_arr = [0.99275, 0.9405, 0.88825, 0.88825, 0.836, 1.045, 0.7315, 0.67925, 0.627, 0.57475, 1.045, 0.47025, 0.418, 0.36575, 0.3135, 1.045, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.03135, 0.0209, 0.01045]
destroy_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.01, 0.02, 0.03, 0.03, 0.03, 0.03, 0.04, 0.04, 0.10, 0.10, 0.20, 0.30, 0.40]
meso_array = [1000 + __EQUIPMENTLEVEL__ ** 3 * (0 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (1 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (2 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (3 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (4 + 1) / 25,
    1000 + __EQUIPMENTLEVEL__ ** 3 * (5 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (6 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (7 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (8 + 1) / 25, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (9 + 1) / 25,
    1000 + __EQUIPMENTLEVEL__ ** 3 * (10 + 1) ** 2.7 / 400, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (11 + 1) ** 2.7 / 400, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (12 + 1) ** 2.7 / 400, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (13 + 1) ** 2.7 / 400, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (14 + 1) ** 2.7 / 400, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (15 + 1) ** 2.7 / 120, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (16 + 1) ** 2.7 / 120, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (17 + 1) ** 2.7 / 120, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (18 + 1) ** 2.7 / 110, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (19 + 1) ** 2.7 / 110, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (20 + 1) ** 2.7 / 100, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (21 + 1) ** 2.7 / 100, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (22 + 1) ** 2.7 / 100, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (23 + 1) ** 2.7 / 100, 
    1000 + __EQUIPMENTLEVEL__ ** 3 * (24 + 1) ** 2.7 / 100]
meso_array = [int(i) for i in meso_array]
# print(meso_array)

# initialize results dict
if __name__ == "__main__":
    results = dict()
    for i in range(26): 
        results.setdefault(i, 0)

    start_time = time.time()
    for i in range(__SIMULATIONS__): 
    # while count < __SIMULATIONS__:
        # print()
        while not destroyed and star != goal:
            # print(meso, star, failstack)
            # chance time
            if failstack == 2: 
                meso += meso_array[star]
                star += 1
                failstack = 0
                # print(meso, star, failstack)
            # normal starring
            meso += meso_array[star]
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
                        failstack += 1 
                    else: 
                        destroyed = True
                        boom += 1 
                else: 
                    # checkpoints
                    if star <= 10 or star == 15 or star == 20: 
                        pass
                    else: 
                        star -= 1
                        failstack += 1

        results[star] += 1

        if not destroyed: 
            min_meso = min(meso, min_meso)
            max_meso = max(meso, max_meso)
            meso_avg = (meso + count * meso_avg) / (count + 1)
        
        count = count + 1 if not destroyed else count
        star = __INITSTAR__ if not destroyed else 12
        meso = 0 if not destroyed else meso
        
        destroyed = False
    for i in range(12,26):
        print(i, results[i])
    print("average meso from stars %i to %i:" % (__INITSTAR__, __GOAL__), int(meso_avg))
    print("booms:", boom)
    print("simulations:", __SIMULATIONS__)
    end_time = time.time()
    print("time elapsed:", end_time - start_time)
    print("min:", min_meso)
    print("max:", max_meso)


# print(results.keys())
# print(results.values())
# data = np.array(list(results.items()))
# n, bins = np.histogram(data, 100)
# plt.bar(results.keys(), results.values())
# plt.show()
    # print(star, destroyed)