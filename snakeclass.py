
import turtle
import time
import random
# setup the screen

score = 0
open_file = open('high_score.txt', 'r')
high_score = int(open_file.readline().strip())

delay = 0.2

class WnScreen:
        def __init__(self):
            self.wn = turtle.Screen()
            self.wn.title("Snake Game")
            self.wn.bgcolor('grey')
            self.wn.setup(width=600, height=600)
            self.wn.tracer(0)
            self.snake = Snake()

        def wn_update(self):
            self.wn.update()

        def key_binding(self):
            self.wn.listen()
            self.wn.onkeypress(self.snake.go_up, "Up")
            self.wn.onkeypress(self.snake.go_down, "Down")
            self.wn.onkeypress(self.snake.go_left, "Left")
            self.wn.onkeypress(self.snake.go_right, "Right")



# Snake of the game


class Snake:
    def __init__(self):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.color("green")
        self.head.shape("square")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.food = Food()
        self.segments = []
        self.pen = Pen()

    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 20)

        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 20)

        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 20)

        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 20)

    # Check for head collision with the body segments and board
    def check_collision(self):
        if self.head.xcor() > 290 or self.head.xcor() < -290 or self.head.ycor() > 290 or self.head.ycor() < -290:
            time.sleep(1)
            self.head.goto(0, 0)
            self.head.direction = "stop"
            self.segment_reset()
            self.pen.score_reset()
        for segment in self.segments:
            if segment.distance(self.head) < 20:
                time.sleep(1)
                self.head.goto(0, 0)
                self.head.direction = "stop"
                self.segment_reset()
                self.pen.score_reset()

    def food_check(self):
        if self.head.distance(self.food.cor_check()) < 20:
            # Move the food to a random spot
            self.food.move_food()
            # Eat food and increase length
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("circle")
            new_segment.color("green")
            new_segment.penup()
            self.segments.append(new_segment)
            self.pen.score_update()

            # Shorten the delay
            global delay
            global score
            global high_score

            delay -= 0.001
            # Increase the score
            score += 10

            if score > high_score:
                high_score = score

    def move_segments(self):
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x, y)

    def segment_reset(self):
        for segment in self.segments:
            segment.goto(1000, 1000)

            # Clear the segments list
        self.segments.clear()



# Food for the snake


class Food:
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)

    def cor_check(self):
        return self.food.xcor(),self.food.ycor()

    def move_food(self):
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        self.food.goto(x, y)

# Pen for writing the Score


class Pen:

    def __init__(self):
        global score
        global delay
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("yellow")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 280)
        self.pen.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                       font=("Courier", 10, "bold"))

    def score_reset(self):
        global score
        global delay

        score = 0
        delay = 0.2

        self.pen.clear()
        self.pen.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                  font=("Courier", 10, "bold"))

    def score_update(self):
        self.pen.clear()
        self.pen.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                       font=("Courier", 10, "bold"))


wn = WnScreen()
wn.key_binding()

while True:
    wn.wn_update()
    wn.snake.move()
    wn.snake.check_collision()
    wn.snake.food_check()
    wn.snake.move_segments()
    time.sleep(delay)
    open_file = open('high_score.txt', 'w')
    open_file.write(str(high_score))




