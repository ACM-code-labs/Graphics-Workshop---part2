#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out  vec3 aFrag;

uniform mat4 model;
uniform mat4 view;
uniform mat4 prjection; 

void main(){

    gl_Position = prjection * view *  model *  vec4(aPos.x, aPos.y, aPos.z, 1.0);
    aFrag = aColor;
    
}