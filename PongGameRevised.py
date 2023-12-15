# Revised to only have right paddle

import gym
from gym import spaces
import turtle
import numpy as np

class PongEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, render_mode=None):
        self.width = 1000
        self.height = 600
        self.hitPaddle = False

        self.observation_space = spaces.Dict({
            'paddle': spaces.Box(-self.height/2, self.height/2, shape=(2,)),
            'ball': spaces.Box(-self.width/2, self.width/2, shape=(2,))
        })

        self.action_space = spaces.Discrete(2)

        self._action_to_direction = {
            0: np.array([0, 20]),
            1: np.array([0, -20]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        return {"paddle": self._paddle_location, "ball": self._ball_location}

    def _get_info(self):
        return {"hitPaddle": self.hitPaddle}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        observation = self._get_obs()
        info = self._get_info()

        # Initialize paddle and ball locations in render frame
        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        direction = self._action_to_direction[action]
        self._paddle_location = np.clip(
            self._paddle_location + direction, 0, 1)

        terminated = self._ball_location[0] > 500
        reward = 1 if (360 < self._ball_location[0] < 370) and \
                     (self._paddle_location[1] + 40 > self._ball_location[1] > self._paddle_location[1] - 40) else 0
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        return self._render_frame()

    def _render_frame(self):
        # Create screen
        sc = turtle.Screen()
        sc.title("Pong game")
        sc.bgcolor("white")
        sc.setup(width=self.width, height=self.height)

        # Right paddle
        right_pad = turtle.Turtle()
        right_pad.speed(0)
        right_pad.shape("square")
        right_pad.color("black")
        right_pad.shapesize(stretch_wid=6, stretch_len=2)
        right_pad.penup()
        self._paddle_location = (400, 0)
        right_pad.goto(self._paddle_location[0], self._paddle_location[1])

        # Ball of circle shape
        hit_ball = turtle.Turtle()
        hit_ball.speed(40)
        hit_ball.shape("circle")
        hit_ball.color("blue")
        hit_ball.penup()
        self._ball_location = (0, 0)
        hit_ball.goto(self._ball_location[0], self._ball_location[1])
        hit_ball.dx = 5
        hit_ball.dy = -5

        # Initialize the score
        misses = 0

        # Displays the score
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("blue")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 260)
        sketch.write("Misses: 0",
                     align="center", font=("Courier", 24, "normal"))


        # Functions to move paddle vertically
        def paddlebup():
            y = right_pad.ycor()
            y += 20
            right_pad.sety(y)


        def paddlebdown():
            y = right_pad.ycor()
            y -= 20
            right_pad.sety(y)


        # Keyboard bindings
        sc.listen()
        sc.onkeypress(paddlebup, "Up")
        sc.onkeypress(paddlebdown, "Down")

        while True:
            sc.update()

            hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
            hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

            # Checking borders
            if hit_ball.ycor() > 280:
                hit_ball.sety(280)
                hit_ball.dy *= -1

            if hit_ball.ycor() < -280:
                hit_ball.sety(-280)
                hit_ball.dy *= -1

            if hit_ball.xcor() < -500:
                hit_ball.setx(-500)
                hit_ball.dx *= -1

            if hit_ball.xcor() > 500:
                hit_ball.goto(0, 0)
                hit_ball.dy *= -1
                misses += 1
                sketch.clear()
                sketch.write("Misses: {}".format(
                    misses), align="center",
                    font=("Courier", 24, "normal"))

            # Paddle ball collision
            if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and (hit_ball.ycor() < right_pad.ycor() + 40 and
                 hit_ball.ycor() > right_pad.ycor() - 40):
                self.hitPaddle = True
                hit_ball.setx(360)
                hit_ball.dx *= -1

