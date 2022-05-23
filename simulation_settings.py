"""
Henry Ding,
Monday, May 23, 2022,

This file contains settings for each simulation trial for data generation
"""
N_TRIALS = 10000  # total number of trials to generate for data
MIN_STEPS = 1  # minimum number of steps a simulation can proceed for
MAX_STEPS = 500  # maximum number of steps a simulation can proceed for
TIME_DELTA = 0.01  # time change between each step
N_BALLS = 1  # ball count
MAX_IMPULSE = 100  # maximum impulse on each ball in terms of pymunk impulse units
SPACE_SIZE = (100, 100)  # pixel size of the space
