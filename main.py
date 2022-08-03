from gl import *
from Obj import *
from Render import *


glCreateWindow(300, 300)

glColor(0, 1, 0)

square = [(100,100),(200,100),(200,200),(100,200)]

cube = Obj('face.obj')

def transform_vertex(vertex,scale,translate):
    return [
            (vertex[0] * scale[0]) + translate[0], 
            (vertex[1] * scale[1]) + translate[1]
    ]

scale_factor = (10, 10)
translate_factor = (150,30)


for face in cube.faces:

    if len(face) == 4:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        f4 = face[3][0] - 1

        v1 = transform_vertex (cube.vertices[f1], scale_factor , translate_factor)
        v2 = transform_vertex (cube.vertices[f2], scale_factor , translate_factor)
        v3 = transform_vertex (cube.vertices[f3], scale_factor , translate_factor)
        v4 = transform_vertex (cube.vertices[f4], scale_factor , translate_factor)



        createline(v1[0], v1[1], v2[0], v2[1])
        createline(v2[0], v2[1], v3[0], v3[1])
        createline(v3[0], v3[1], v4[0], v4[1])
        createline(v4[0], v4[1], v1[0], v1[1])

    if len(face) == 3:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1

        v1 = transform_vertex (cube.vertices[f1], scale_factor , translate_factor)
        v2 = transform_vertex (cube.vertices[f2], scale_factor , translate_factor)
        v3 = transform_vertex (cube.vertices[f3], scale_factor , translate_factor)

        

        createline(v1[0], v1[1], v2[0], v2[1])
        createline(v2[0], v2[1], v3[0], v3[1])
        createline(v3[0], v3[1], v1[0], v1[1])


    
   


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



