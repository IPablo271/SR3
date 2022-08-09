
from Utilities import * 
from Obj import *
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
GREEN = color(0, 255 , 0)

class Render(object):
   
    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.current_color = BLACK
        self.clear_color = WHITE
        self.viewportx = 0
        self.viewporty = 0
        self.viewportwidth = 0
        self.viewortheight = 0
        self.viewportcolor = GREEN
        self.clear() #Limpiar la pantalla.
    def viewport(self,x, y,width,height):
        self.viewportx = x
        self.viewporty = y
        self.viewportwidth = width
        self.viewortheight = height
   
    def clear(self):
        #Generador del color.
        self.framebuffer = [
            #Los colores tienen que ir de 0 a 255.
            [WHITE for x in range(self.width)] 
            for y in range(self.height)
        ]
    
    def write(self, filename):
        #Esta no necesita recibir ningún nombre de archivo.
        #Abrir en bw: binary write.
        f = open(filename, "bw")
        
        #Pixel header.
        f.write(char('B'))
        f.write(char('M'))
        #Tamaño del archivo en bytes. 
        # El 3 es para los 3 bytes que seguirán. El 14 es el tamaño del infoheader y el 40 es el tamaño del otro header.
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0)) #Algo que no se usará. Este es de 2 bytes, por eso se utiliza el word.
        f.write(word(0)) #Algo que no se usará. Este es de 2 bytes, por eso se utiliza el word.
        f.write(dword(14 + 40)) #Offset a la información de la imagen. 14 bytes para el header, 40 para la información de la imagen. Aquí empieza la data.
        #Lo anterior suma 14 bytes.
        
        #Info header.
        f.write(dword(40)) #Este es el tamaño del header. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.width)) #Ancho de la imagen. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.height)) #Alto de la imagen. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(word(1)) #Número de planos. Esto es de 2 bytes, por eso se utiliza el word.
        f.write(word(24)) #24 bits por pixel. Esto es porque usa el true color y el RGB.
        f.write(dword(0)) #Esto es la compresión. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.width * self.height * 3)) #Tamaño de la imagen sin el header.
        #Pixels que no se usarán mucho.
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        #Lo anterior suma 40 bytes.

        
        
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()


    #Función que dibuja un punto en la pantalla. Esta es una función de bajo nivel. 
    def point(self, x, y): 
        if (0 < x < self.width and 0 < y < self.height):
            self.framebuffer[x][y] = self.current_color #El color del punto es el color actual.      
    def convertp(self,x,y):
        x_ini = x + 1
        y_ini = y + 1

        # calculada = (Sumada * width) / numero sumado

        calcux = (x_ini * self.viewportwidth) / 2
        calcuy = (y_ini * self.viewortheight) / 2

        #  xfinal = (coordenada inicial del viewport + calculada )
        xfinal = round(self.viewportx + calcux)
        yfinal = round(self.viewporty + calcuy)

        return [xfinal , yfinal]
    
    def line2(self, x0, y0, x1, y1):
        listap = []
        x0 = round(x0)
        y0 = round(y0)
        x1 = round(x1)
        y1 = round(y1)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Si es empinado, poco movimiento en x y mucho en y.
        steep = dy > dx

        # Se invierte si es empinado
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si la linea tiene direccion contraria, invertir
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
                listatemp = []
                listatemp.append(y)
                listatemp.append(x)
                listap.append(listatemp)

            else:
                self.point(x, y)
                listatemp = []
                listatemp.append(x)
                listatemp.append(y)
                listap.append(listatemp)


            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1

                threshold += dx * 2     
        return listap
    
    def transform_vertex(self,vertex,scale,translate):
        return [
            (vertex[0] * scale[0]) + translate[0], 
            (vertex[1] * scale[1]) + translate[1]
        ]
    def load_model(self, model, scale_factor, translate_factor):

        cube = Obj(model)

        for face in cube.faces:
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex (cube.vertices[f1], scale_factor , translate_factor)
                v2 = self.transform_vertex (cube.vertices[f2], scale_factor , translate_factor)
                v3 = self.transform_vertex (cube.vertices[f3], scale_factor , translate_factor)
                v4 = self.transform_vertex (cube.vertices[f4], scale_factor , translate_factor)



                self.line2(v1[0], v1[1], v2[0], v2[1])
                self.line2(v2[0], v2[1], v3[0], v3[1])
                self.line2(v3[0], v3[1], v4[0], v4[1])
                self.line2(v4[0], v4[1], v1[0], v1[1])

            if len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex (cube.vertices[f1], scale_factor , translate_factor)
                v2 = self.transform_vertex (cube.vertices[f2], scale_factor , translate_factor)
                v3 = self.transform_vertex (cube.vertices[f3], scale_factor , translate_factor)

                

                self.line2(v1[0], v1[1], v2[0], v2[1])
                self.line2(v2[0], v2[1], v3[0], v3[1])
                self.line2(v3[0], v3[1], v1[0], v1[1])
    


    