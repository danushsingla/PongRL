# Import required library
import turtle
import gym
from stable_baselines3 import PPO
import numpy as np
import gym_envs

# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=1000, height=600)

# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("black")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400, 0)

# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("black")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0)

# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(40)
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5

# Initialize the score
left_player = 0
right_player = 0

# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left_player : 0 Right_player: 0",
             align="center", font=("Courier", 24, "normal"))


# Functions to move paddle vertically
def paddleaup():
    y = left_pad.ycor()
    y += 20
    left_pad.sety(y)


def paddleadown():
    y = left_pad.ycor()
    y -= 20
    left_pad.sety(y)


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
sc.onkeypress(paddleaup, "Up")
sc.onkeypress(paddleadown, "Down")

env = gym.make('gym_envs/PongGame', render_mode='human')
model = PPO.load("PongGame_model", env=env, verbose=1)

while True:
    sc.update()

    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    obs = {"paddle": np.array([right_pad.xcor(), right_pad.ycor()]),
           "ball": np.array([hit_ball.xcor(), hit_ball.ycor()])}
    action, state = model.predict(obs)

    if action == 0:
        paddlebup()
    elif action == 1:
        paddlebdown()
    elif action == 2:
        pass

    # Checking borders
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    if right_pad.ycor() < -230:
        right_pad.sety(-230)

    if right_pad.ycor() > 230:
        right_pad.sety(230)

    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        left_player += 1
        sketch.clear()
        sketch.write("Left_player : {} Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        right_player += 1
        sketch.clear()
        sketch.write("Left_player : {} Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    # Paddle ball collision
    if (hit_ball.xcor() > 355 and hit_ball.xcor() < 375) and (hit_ball.ycor() < right_pad.ycor() + 60 and
         hit_ball.ycor() > right_pad.ycor() - 60):
        hit_ball.setx(355)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -355 and hit_ball.xcor() > -375) and (hit_ball.ycor() < left_pad.ycor() + 60 and
         hit_ball.ycor() > left_pad.ycor() - 60):
        hit_ball.setx(-355)
        hit_ball.dx *= -1
