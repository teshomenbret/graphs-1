import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os


program = None


def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders1", filename)
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

    vertexes = [         
        -0.5, -0.5,  0.0,    1.0, 0.0, 0.0,
         0.5, -0.5,  0.0,    0.0, 1.0, 0.0,
         0.5,  0.5,  0.0,    1.0, 0.2, 0.8,
        -0.5,  0.5,  0.0,    1.0, 1.0, 1.0,
    ], 
    vertexes = np.array(vertexes, dtype=np.float32)

    triangleVbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, triangleVbo)
    glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)

    indices = [0, 1, 2, 2, 3, 0,]
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


def draw():
    global program
    glUseProgram(program)
    glClearColor(.30, 0.20, 0.20, 1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glDrawElements(GL_TRIANGLES,6, GL_UNSIGNED_INT, None)


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()
