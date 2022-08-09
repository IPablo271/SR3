from gl import *
from Obj import *
from Render import *


glCreateWindow(700, 700)

glColor(0.18, 0.18, 0.18)




scale_factor = (300, 300)
translate_factor = (350,120)

lmodel('tesla.obj', scale_factor, translate_factor)


    
   


"""
center = (150,150)

square_large = [
    (
        ((x- center[0]) * 1.5) + center[0], 
        ((y - center[1]) * 3.5) + center[1]
    ) for x, y in square
]

tsaqure = square_large

last_point = tsaqure[-1]
for point in tsaqure:
    createline(*last_point,*point)
    last_point = point
"""


glFinish()



