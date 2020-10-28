#version 450 
#define VERTEX_SHADER
#state CULL OFF
#pragma once
#define epsilon 0.00001
#define pi 3.141592653589793
float sum(vec2 v)
{
return v.x + v.y;
}
float sum(vec3 v)
{
return v.x + v.y + v.z;
}
float sum(vec4 v)
{
return v.x + v.y + v.z + v.w;
}
float length2(vec2 v)
{
return sum(v*v);
}
float length2(vec3 v)
{
return sum(v*v);
}
float length2(vec4 v)
{
return sum(v*v);
}
float dot01(vec2 a, vec2 b)
{
return max(dot(a, b), 0.0)
}
float dot01(vec3 a, vec3 b)
{
return max(dot(a, b), 0.0)
}
float dot01(vec4 a, vec4 b)
{
return max(dot(a, b), 0.0)
}
float clamp01(float v)
{
return clamp(v, 0, 1);
}
vec2 clamp01(vec2 v)
{
return clamp(v, 0, 1);
}
vec3 clamp01(vec3 v)
{
return clamp(v, 0, 1);
}
vec4 clamp01(vec4 v)
{
return clamp(v, 0, 1);
}
float safeDiv(float a, float b)
{
return a / max(b, epsilon);
}
vec2 safeDiv(vec2 a, float b)
{
return a / max(b, epsilon);
}
vec3 safeDiv(vec3 a, float b)
{
return a / max(b, epsilon);
}
vec4 safeDiv(vec4 a, float b)
{
return a / max(b, epsilon);
}
vec2 safeDiv(vec2 a, vec2 b)
{
return a / max(b, epsilon);
}
vec3 safeDiv(vec3 a, vec3 b)
{
return a / max(b, epsilon);
}
vec4 safeDiv(vec4 a, vec4 b)
{
return a / max(b, epsilon);
}
// sah
layout(location = SV_POSITION)    in vec3 vertex;
layout(location = SV_MODELMATRIX) in mat4 modelMatrix;
layout(location = SV_VIEW)    uniform mat4 viewMatrix;
layout(location = SV_PROJECT) uniform mat4 projectionMatrix;
void main(void)
{
gl_Position = (projectionMatrix * viewMatrix * modelMatrix) * vec4(vertex, 1.f);
}
