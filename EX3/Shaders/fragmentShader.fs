#version 330 core

out vec4 FragColor;

in vec2 textcords;

uniform sampler2D utexture;

void main(){

     FragColor = texture(utexture, textcords);
 
}
