#version 450

#include <shader_corlib/meta.inc>

io struct pipeline {
    vec3 pos;
    vec3 normal;
};

generate(vertex,fragment)

shader(vertex) {
    in vec3 pos : 0;
    in vec3 normal : SV_NORMAL;

    void main()
    {
        gl_Position = pos;
        pipeline.pos = pos;
        pipeline.normal = normal;
    }
}

shader(fragment) {

    out vec4 color;
    void main()
    {
         vec4(pipeline.pos + pipeline.normal,1);
    }
}