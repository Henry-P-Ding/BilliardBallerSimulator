"""
Henry Ding,
Monday, May 23, 2022,

This entry-point file runs simulations based on simulation settings and the class functionality in simulation classes.
"""
from simulation_settings import *
from simulation_classes import *
import numpy as np
import os

# make output of data generation directory
if not os.path.exists(f'output'):
    os.makedirs(f'output')
x = 0
while x < N_TRIALS:
    if x % 1000 == 0:
         print(f"Performing Trial {x}")
    steps = np.random.randint(MIN_STEPS, MAX_STEPS)  # random number of steps within step range
    r = Run(steps, TIME_DELTA, SPACE_SIZE)
    r.populate_random(N_BALLS)
    for i in range(N_BALLS):
        r.push_random_ball(np.random.rand() * MAX_IMPULSE, i)
    # only advance trial number if simulation was not faulty and ball did not clip out of bounds
    if r.run_simulation():
        x += 1
        # create CSV file
        r.run_data.to_csv(f"output/trial_{x}_mtime_{int(steps/2)}_time_{steps}.csv", index=False)
