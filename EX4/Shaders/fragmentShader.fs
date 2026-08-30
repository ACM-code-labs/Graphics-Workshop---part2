#version 330 core

struct Material {
     sampler2D diffuse; //the diffuse and ambient are usally the same color on the object
     sampler2D specular;
     float shininess;
};

struct Light {
     vec3 lightPos;
     vec3 ambient;
     vec3 diffuse;
     vec3 specular;

};

out vec4 FragColor;

in vec3 Normal;
in vec3 FragPos;
in vec2 textcords;

uniform Material material;
uniform Light light;
uniform vec3 viewPos;


void main(){

     //ambient
     vec3 ambient = light.ambient * texture(material.diffuse, textcords).rgb;

     //diffuse
     vec3 norm = normalize(Normal);
     vec3 lightDir = normalize(vec3(light.lightPos - FragPos));
     float diff = max(dot(norm, lightDir), 0);
     vec3 diffuse = light.diffuse * diff * texture(material.diffuse, textcords).rgb;
     
     //specular
     vec3 viewDir = normalize(viewPos - FragPos);
     vec3 reflectDir = reflect(-lightDir, norm);
     float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
     vec3 specular = (vec3(texture(material.specular, textcords)) * spec) * light.specular;

     vec3 result = (specular + diffuse + ambient);
     FragColor = vec4(result, 1);
}
