import ctypes # openGl is based on C++ so we need this to intract with it
import sys, os # we need to do file stuff

import glfw #the windows library to display 
from pyglm import glm #the vector math library

import numpy as np
from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.shader import Shader

HERE = os.path.dirname(os.path.abspath(__file__))

window = None

#[x, y, z] cordinates
vertices = np.array([
    0, 0.5, 0,      1, 0, 0,
    -0.5, -0.5, 0,  0, 1, 0,
    0.5, -0.5, 0,   0, 0, 1,
    ], np.float32)

shader : Shader = None

# you do not need to check these methods
def startGlfwAndMakeWindow(width: int, height: int):
    global window
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfw.create_window(width, height, "EX1: VBO and VAO", None, None)
    if not window:
        print("couldnt make window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    glfw.set_framebuffer_size_callback(window, frame_Buffer_Size_CallBack)

def frame_Buffer_Size_CallBack(window, width: int, height: int):
    glViewport(0, 0, width, height)  

def main():
    startGlfwAndMakeWindow(800, 600)
    
    VBO = glGenBuffers(1)
    VAO = glGenVertexArrays(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)


    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)

    shader = Shader(os.path.join(HERE, "Shaders", "vertexShader.vs"),
                    os.path.join(HERE, "Shaders", "fragmentShader.fs"))
    shader.use()

    glEnable(GL_DEPTH_TEST)


    while (not glfw.window_should_close(window)):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()


#FINAL EX1