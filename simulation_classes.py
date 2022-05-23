"""
Henry Ding,
Monday, May 23, 2022,

This program implements class functionality for simulating numbers of trials for data generation.
"""


import pymunk
import pandas as pd
import numpy as np


class Ball:
    """Ball class associated with a billiard ball."""
    def __init__(self, space, pos, mass, radius):
        self.body = pymunk.Body()
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = mass / (radius * radius * np.pi)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)


class Run:
    """Run class representing one simulation trial"""
    BALL_RADIUS = 6.15  # in pixels
    BALL_MASS = 1  # in arbitrary mass units, set to 1 so impulse units in push_random_ball method corresponds to velocity

    def __init__(self, steps, time_delta, size):
        self.space = pymunk.Space()
        self.size = size
        self.step_limit = steps  # total number of steps in the run
        self.step = 0
        self.time_delta = time_delta  # time change between each step
        self.balls = []  # list of all Ball objects in run
        self.walls = []  # list of all boundary walls in run
        # four walls: top, right, bottom left
        self.add_wall((0, 0), (self.size[0], 0))
        self.add_wall((self.size[0], 0), (self.size[0], size[1]))
        self.add_wall((self.size[0], self.size[1]), (0, size[1]))
        self.add_wall((0, self.size[1]), (0, 0))

        # feature/label data saving
        self.run_data = None

    def run_simulation(self):
        """
        Runs simulation associated with run.

        Each Run object should only call this method once after setup
        """
        # store initial feature data
        features = []
        for j, ball in enumerate(self.balls):
            # calculates speed/angle of ball
            speed = np.sqrt(ball.body.velocity[0] * ball.body.velocity[0] + ball.body.velocity[1] * ball.body.velocity[1])
            angle = np.arctan(ball.body.velocity[1] / ball.body.velocity[0])
            # ball distances to walls
            wall_ds = [
                ball.body.position[0],
                self.size[0] - ball.body.position[0],
                ball.body.position[1],
                self.size[1] - ball.body.position[1]
            ]
            # maps arctan range to (0, 2pi) for angle
            if ball.body.velocity[0] < 0:
                angle += np.pi
            if angle < 0:
                angle += np.pi * 2
            features.append([j] + wall_ds + [speed, angle, ball.body.position[0], ball.body.position[1], ball.body.velocity[0], ball.body.velocity[1]])
        # adds features to dataframe
        features_df = pd.DataFrame(features, columns=['id', 'left_d0', 'right_d0', 'bot_d0', 'top_d0', 'speed0', 'angle0', 'px0', 'py0', 'vx0', 'vy0'])

        # run trials
        m_features = []  # features at half-time of simuation
        for i in range(self.step_limit):
            if i == int(self.step_limit / 2):
                for j, ball in enumerate(self.balls):
                    # calculates speed/angle of ball
                    speed = np.sqrt(
                        ball.body.velocity[0] * ball.body.velocity[0] + ball.body.velocity[1] * ball.body.velocity[1])
                    angle = np.arctan(ball.body.velocity[1] / ball.body.velocity[0])
                    # ball distances to walls
                    wall_ds = [
                        ball.body.position[0],
                        self.size[0] - ball.body.position[0],
                        ball.body.position[1],
                        self.size[1] - ball.body.position[1]
                    ]
                    # rejects faulty trials of ball clips out of bounds
                    if not(0 <= ball.body.position[0] <= self.size[0] and 0 <= ball.body.position[1] <= self.size[1]):
                        return False

                    # maps arctan range to (0, 2pi) for angle
                    if ball.body.velocity[0] < 0:
                        angle += np.pi
                    if angle < 0:
                        angle += np.pi * 2
                    m_features.append(wall_ds + [speed, angle, ball.body.position[0], ball.body.position[1], ball.body.velocity[0], ball.body.velocity[1]])
                # adds half-time features to dataframe
                m_features_df = pd.DataFrame(m_features, columns=['left_dm', 'right_dm', 'bot_dm', 'top_dm', 'speedm', 'anglem', 'pxm', 'pym', 'vxm', 'vym'])
            # advances one simulation step
            self.space.step(self.time_delta)

        # store final label data
        labels = []
        for j, ball in enumerate(self.balls):
            labels.append([ball.body.position[0], ball.body.position[1]])
            # checks for faulty out of bounds clips for the ball
            if not (0 <= ball.body.position[0] <= self.size[0] and 0 <= ball.body.position[1] <= self.size[1]):
                return False
        labels_df = pd.DataFrame(labels, columns=['pxf', 'pyf'])
        self.run_data = pd.concat([features_df, m_features_df, labels_df], axis=1)
        self.run_data.set_index('id')
        return True

    def populate_random(self, n_balls):
        """Populates the Run pymunk space with a number of balls."""
        for i in range(n_balls):
            self.add_ball((np.random.rand() * self.size[0], np.random.rand() * self.size[1]))

    def push_random_ball(self, mag, i):
        """Pushes a random ball at a random angle with a random impulse"""
        angle = np.random.rand() * 2 * np.pi
        self.balls[i].body.apply_impulse_at_local_point((mag * np.cos(angle), mag * np.sin(angle)))

    def add_ball(self, pos):
        """Adds Ball object to the simulation space"""
        self.balls.append(Ball(self.space, pos, Run.BALL_MASS, Run.BALL_RADIUS))

    def add_wall(self, pos1, pos2):
        """Adds wall shape to the pymunk space"""
        shape = pymunk.Segment(
            self.space.static_body, pos1, pos2, 0.0
        )
        shape.elasticity = 1.0
        self.space.add(shape)
        self.walls.append(shape)
