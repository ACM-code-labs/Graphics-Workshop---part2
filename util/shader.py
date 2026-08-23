

from OpenGL.GL import *

""" YOU DO NOT NEED TO LOOK HERE - IGNORE THIS FILE"""

class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path) as f:
            vertex_code = f.read()
        with open(fragment_path) as f:
            fragment_code = f.read()

        vertex = self._compile(vertex_code, GL_VERTEX_SHADER, "VERTEX")
        fragment = self._compile(fragment_code, GL_FRAGMENT_SHADER, "FRAGMENT")

        self.ID = glCreateProgram()
        glAttachShader(self.ID, vertex)
        glAttachShader(self.ID, fragment)
        glLinkProgram(self.ID)

        if not glGetProgramiv(self.ID, GL_LINK_STATUS):
            print("ERROR::SHADER::PROGRAM::LINKING_FAILED")
            print(glGetProgramInfoLog(self.ID).decode())

        glDeleteShader(vertex)
        glDeleteShader(fragment)

    @staticmethod
    def _compile(source, shader_type, label):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            print(f"ERROR::SHADER::{label}::COMPILATION_FAILED")
            print(glGetShaderInfoLog(shader).decode())
        return shader

    def use(self):
        glUseProgram(self.ID)

    def setBool(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def setFloat(self, name, value):
        glUniform1f(glGetUniformLocation(self.ID, name), value)
