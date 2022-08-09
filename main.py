from gl import *
from Obj import *
from Render import *


glCreateWindow(300, 300)

glColor(0, 1, 1)




scale_factor = (10, 10)
translate_factor = (150,30)

lmodel('face.obj', scale_factor, translate_factor)


    
   


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



