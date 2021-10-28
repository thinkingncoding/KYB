import math
import turtle
t = turtle.Turtle()
t.shape("circle")
t.pensize(1)
a_list = []
x = 0
y = 0

for i in range(0, 370,10):
    a_list.append(i)
print(a_list)

for j in a_list :
    x = x + math.cos(math.radians(j))
    y = y + math.sin(math.radians(j))

    x1 = x * 40
    y1 = y * 40
    print(f'x:{x1}, y:{y1}')

    t.pendown()
    t.goto(x1,y1)
    t.stamp()


turtle.mainloop()



