# Revised to only have right paddle

class Game():
    def createGame(self):
        # Import required library
        import turtle

        # Create screen
        sc = turtle.Screen()
        sc.title("Pong game")
        sc.bgcolor("white")
        sc.setup(width=1000, height=600)

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
                hit_ball.setx(360)
                hit_ball.dx *= -1

    def createEnv(self):
        self.createGame()
