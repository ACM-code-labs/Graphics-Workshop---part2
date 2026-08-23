import ctypes # openGl is based on C++ so we need this to intract with it using a wrapper
import sys, os # we need to do file stuff

import glfw #the windows display library 
from pyglm import glm #the vector math library

import numpy as np # the array lib we need for vertex and index storage
from OpenGL.GL import * # the graphics api (OpenGl)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # dw about this line
from util.shader import Shader # you need a shader to run 3D stuff

HERE = os.path.dirname(os.path.abspath(__file__)) # used for file paths

window = None 

vertex = np.array([
    0.5, 0.5, 0.5,      1,0,0,
    0.5, 0.5, -0.5,     1,0,0,

    0.5, -0.5, 0.5,     0,1,0,
    0.5, -0.5, -0.5,    0,1,0,

    -0.5, 0.5, 0.5,     0,0,1,
    -0.5, 0.5, -0.5,    0,0,1,

    -0.5, -0.5, 0.5,    1,1,1,
    -0.5, -0.5, -0.5,   1,1,1,
], np.float32)

index = np.array([
   0, 1, 2,  2, 1, 3,
   
    4, 5, 6,  6, 5, 7,
  
    4, 0, 6,  6, 0, 2,
  
    1, 5, 3,  3, 5, 7,
  
    4, 1, 0,  4, 5, 1,
  
    2, 3, 6,  6, 3, 7
    ], np.uint32)

shader : Shader = None 

lastFrame : float = 0.0
currentFrame : float = 0.0
deltaTime : float = 0.0

def startGlfwAndMakeWindow(width: int, height: int):
    global window
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    
    window = glfw.create_window(width, height, "EX2: Vertext Shader and transform", None, None)
    if not window:
        print("couldnt make window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    glfw.set_framebuffer_size_callback(window, frame_Buffer_Size_CallBack)

def frame_Buffer_Size_CallBack(window, width: int, height: int):
    glViewport(0, 0, width, height)  

# you do not need to touch anything above this line 
# (I left comments above only for explination incase you wanna know)

def main():
    global lastFrame, currentFrame, deltaTime, shader

    startGlfwAndMakeWindow(800, 600)  
    
    shader = Shader(os.path.join(HERE, "Shaders", "vertexShader.vs"), os.path.join(HERE, "Shaders", "fragmentShader.fs"))
    shader.use()

    
    EBO = glGenBuffers(1)
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertex.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * index.itemsize, ctypes.c_void_p(3 * index.itemsize))
    glEnableVertexAttribArray(1)

    
    glEnable(GL_DEPTH_TEST)

    viewLoc = glGetUniformLocation(shader.ID, "view")
    modelLoc = glGetUniformLocation(shader.ID, "model")
    peojectionLoc = glGetUniformLocation(shader.ID, "prjection")

      
    view = glm.mat4(1)
    view = glm.translate(view, glm.vec3(0, 0, -3))

    
    projection = glm.perspective(glm.radians(45), 800/600, 0.1, 100)


    model = glm.mat4(1)


    while(not glfw.window_should_close(window)):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        model = glm.rotate(model, (glm.radians(45) * deltaTime), glm.vec3(0.5, 0.5, 0)) 

        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(peojectionLoc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))

        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        glfw.poll_events()
        glfw.swap_buffers(window)


    glfw.terminate()    


if __name__ == "__main__":
    main()