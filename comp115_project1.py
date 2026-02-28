import turtle
import random
import math
sc = turtle.Screen()
t = turtle.Turtle()
turtle.tracer(0, 0) 
sc.bgcolor("black")
t.hideturtle()

def random_star():
  t.color("white")
  t.penup()
  x=random.randint(-640,640)
  y=random.randint(-200,640)
  dot_size=random.random()*3
  t.goto(x,y)
  t.dot(dot_size)

def moon():
    t.penup()
    t.color("grey")
    t.goto(300,300)
    t.pendown()
    t.begin_fill()
    t.circle(80)
    t.end_fill()

def rectangle(w, h, c):
    t.fillcolor(c)
    t.begin_fill()
    for _ in range(2):
        t.forward(w); t.left(90)
        t.forward(h); t.left(90)
    t.end_fill()

def roof():
    t.goto(-300, -200)
    t.fillcolor("maroon")
    t.begin_fill()

    t.left(30)

    for _ in range(2):
        t.forward(80)
        t.left(105)
        t.forward(100 / math.sqrt(2))
        t.left(75)
    t.end_fill()

def side(x,y):
    t.fillcolor("maroon")
    t.begin_fill()

    for _ in range(2):
        t.forward(x)
        t.left(60)
        t.forward(y)
        t.left(120)

    t.left(90)
    t.end_fill()

def triangel():
    t.fillcolor("firebrick")
    t.begin_fill()

    t.forward(100)
    t.left(135)

    for _ in range(2):
        t.forward(71)
        t.left(90 if _ == 0 else 135)

    t.end_fill()



for _ in range(1000):
     random_star()
moon()
t.penup()
t.goto(700,-400)
rectangle(-1360,200,"darkgreen") # grass
t.penup()
t.goto(-400,-300)
rectangle(100,100,"firebrick")
t.penup()
t.goto(-400,-200)
triangel()
t.penup()
roof()


t.penup()
t.goto(-300,-300)
t.penup()
side(80,100)
t.penup() 
t.goto(-300,-280)
t.penup()
t.right(120)
t.penup()
t.goto(-365,-300)
t.penup()
rectangle(30,40,"orange") #door


sc.mainloop()
