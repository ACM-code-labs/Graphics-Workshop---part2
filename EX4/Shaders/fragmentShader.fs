#version 330 core

in vec3 aFrag;
out vec4 FragColor;

void main(){

     FragColor = vec4(aFrag.x, aFrag.y, aFrag.z, 1);

}
