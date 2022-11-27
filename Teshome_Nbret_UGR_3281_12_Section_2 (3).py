import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
import transform4d

program = None

def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders2", filename)
    return open(p, 'r').read()


def init():
    global  program
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glViewport(0, 0, 500, 500)

    vertexShader = compileShader(getFileContents("triangle.vertex.shader"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents("triangle.fragment.shader"), GL_FRAGMENT_SHADER)

    # program creation attaching and linking
    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)


    vertexes = [ -0.5, -0.5, 0.5,    1.0, 0.0, 0.0,
                  0.5, -0.5, 0.5,    0.0, 1.0, 0.0,
                  0.5,  0.5, 0.5,    0.0, 0.0, 1.0,
                 -0.5,  0.5, 0.5,    1.0, 1.0, 1.0,

                 -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
                  0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
                  0.5,  0.5, -0.5,  0.0, 0.0, 1.0,
                 -0.5,  0.5, -0.5,  1.0, 1.0, 1.0
             ] 
    vertexes = np.array(vertexes, dtype=np.float32)

    triangleVbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, triangleVbo)
    glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)

    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7
               ]
    indices = np.array(indices, dtype = np.uint32)

    elementBufferObject = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementBufferObject)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(positionLocation)

    colorLocation = glGetAttribLocation(program, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(colorLocation)


    glUseProgram(program)
    glClearColor(0.30, 0.20, 0.20, 1.0)
    

def draw(angle, axis):
    global program
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    rotateMatLocation = glGetUniformLocation(program, "transform")
    rotateMat = transform4d.makeRotation(angle, axis)
    glUniformMatrix4fv(rotateMatLocation, 1, GL_FALSE,rotateMat)
    glDrawElements(GL_TRIANGLES,36, GL_UNSIGNED_INT, None)


def main():
    init()
    axis=(0,0.6,0.4)
    angle = 0
    jump =1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw(angle, axis)
        pygame.display.flip()
        pygame.time.wait(10)
        angle =angle+jump
        if angle >360:
            angle =0


main()
