import ctypes # openGl is based on C++ so we need this to intract with it
import sys, os # we need to do file stuff

import glfw #the windows library to display 
from pyglm import glm #the vector math library

import numpy as np
from OpenGL.GL import *

from dataclasses import dataclass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.shader import Shader

HERE = os.path.dirname(os.path.abspath(__file__))

window = None

vertex = np.array([
    0.5, 0.5, 0.5,      
    0.5, 0.5, -0.5,     

    0.5, -0.5, 0.5,     
    0.5, -0.5, -0.5,    

    -0.5, 0.5, 0.5,     
    -0.5, 0.5, -0.5,    

    -0.5, -0.5, 0.5,    
    -0.5, -0.5, -0.5,   
], np.float32)

index = np.array([
   0, 1, 2,  2, 1, 3,
   
    4, 5, 6,  6, 5, 7,
  
    4, 0, 6,  6, 0, 2,
  
    1, 5, 3,  3, 5, 7,
  
    4, 1, 0,  4, 5, 1,
  
    2, 3, 6,  6, 3, 7
    ], np.uint32)

lastx : float = 0
lasty : float = 0
yaw : float
pitch : float

@dataclass
class Camera:
    up: glm.vec3
    pos: glm.vec3
    front: glm.vec3
    speed: float = 0.0
    sens : float = 0.0
    yaw : float = -90.0
    pitch : float = 0.0

    
    def __init__(self, pos : glm.vec3, front : glm.vec3, up : glm.vec3 ):
        self.up = up
        self.front = front
        self.pos = pos

@dataclass
class Light:
    pos: glm.vec3
    color: glm.vec3

    def __init__(self, pos : glm.vec3, color : glm.vec3):
        self.pos = pos
        self.color = color

@dataclass
class Object:
    color :  glm.vec3

    def __init__(self, color : glm.vec3):
        self.color = color  
       
shader_object : Shader = None
shader_light : Shader = None

camera : Camera = Camera(glm.vec3(0, 0, 3), glm.vec3(0, 0, -1), glm.vec3(0, 1, 0))

light : Light = Light(glm.vec3(1.2, 1.0, 2.0), glm.vec3(1, 1, 1))

cube : Object = Object(glm.vec3(1.0, 0.5, 0.31))

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
    
    window = glfw.create_window(width, height, "Basic light", None, None)
    if not window:
        print("couldnt make window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    glfw.set_framebuffer_size_callback(window, frame_Buffer_Size_CallBack)
    glfw.set_cursor_pos_callback(window, mouse_CallBack) 
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)    

def frame_Buffer_Size_CallBack(window, width: int, height: int):
    glViewport(0, 0, width, height)  

def mouse_CallBack(window , xpos, ypos):
    global lastx, lasty, camera
    camera.sens = 0.09

    xOffSet = (xpos - lastx) * camera.sens
    yOffSet = (lasty - ypos) * camera.sens
    lastx = xpos
    lasty = ypos

    camera.yaw += xOffSet
    camera.pitch += yOffSet

    if(camera.pitch > 89.9):
        camera.pitch = 89.9
    elif(camera.pitch < -89.9):
        camera.pitch = -89.9

    direction = glm.vec3(
            glm.cos(glm.radians(camera.yaw)) * glm.cos(glm.radians(camera.pitch)),
            glm.sin(glm.radians(camera.pitch)),
            glm.sin(glm.radians(camera.yaw)) * glm.cos(glm.radians(camera.pitch))
    )

    camera.front = glm.normalize(direction)

def process_Input(window) -> None:
    global camera, deltaTime
    camera.speed = 5 * deltaTime

    if(glfw.get_key(window, glfw.KEY_W)):
        camera.pos += camera.front * camera.speed
    if(glfw.get_key(window, glfw.KEY_S)):
        camera.pos -= camera.front * camera.speed
    if(glfw.get_key(window, glfw.KEY_A)):
        camera.pos -= glm.normalize(glm.cross(camera.front, camera.up)) * camera.speed
    if(glfw.get_key(window, glfw.KEY_D)):
        camera.pos += glm.normalize(glm.cross(camera.front, camera.up))* camera.speed

def main():
    global lastFrame, currentFrame, deltaTime, shader_object, direction, camera, window, shader_light,light

    startGlfwAndMakeWindow(800, 600)
    
    shader_object = Shader(os.path.join(HERE, "Shaders", "vertexShader.vs"), os.path.join(HERE, "Shaders", "fragmentShader.fs"))
    shader_light = Shader(os.path.join(HERE, "Shaders", "vertexShader.vs"), os.path.join(HERE, "Shaders", "lightFragmentShader.fs"))

    VAO = glGenVertexArrays(1)
    lightVAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    #object VAO
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertex.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    #light VAO
    glBindVertexArray(lightVAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertex.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)


    lightColorLoc = glGetUniformLocation(shader_object.ID, "lightColor")
    objectColorLoc = glGetUniformLocation(shader_object.ID, "objectColor")
    lightColorLoc_2 = glGetUniformLocation(shader_light.ID, "lightColor")

    shader_object.use()
    glUniform3fv(lightColorLoc, 1, glm.value_ptr(light.color))
    glUniform3fv(objectColorLoc, 1, glm.value_ptr(cube.color))

    shader_light.use()
    glUniform3fv(lightColorLoc_2, 1, glm.value_ptr(light.color))

    projection = glm.perspective(glm.radians(45), 800/600, 0.1, 100)
    glEnable(GL_DEPTH_TEST)
    
    while((not glfw.window_should_close(window)) and (not glfw.get_key(window, glfw.KEY_ESCAPE))):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        process_Input(window)

        shader_object.use()
        glBindVertexArray(VAO)

        viewLoc = glGetUniformLocation(shader_object.ID, "view")
        modelLoc = glGetUniformLocation(shader_object.ID, "model")
        peojectionLoc = glGetUniformLocation(shader_object.ID, "projection")

        model = glm.mat4(1)
        view = glm.lookAt(camera.pos, camera.pos + camera.front, camera.up)

        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(peojectionLoc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        shader_light.use()
        glBindVertexArray(lightVAO)

        viewLoc = glGetUniformLocation(shader_light.ID, "view")
        modelLoc = glGetUniformLocation(shader_light.ID, "model")
        peojectionLoc = glGetUniformLocation(shader_light.ID, "projection")

        model = glm.translate(model, light.pos)
        model = glm.scale(model, glm.vec3(0.2))

        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(peojectionLoc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))

        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
        

    glfw.terminate()

if __name__ == "__main__":
    main()
