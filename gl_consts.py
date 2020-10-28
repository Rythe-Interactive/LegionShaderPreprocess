# ifndef LGSL_PREPROCESSOR_DEFINED
# define LGSL_PREPROCESSOR_DEFINED 
# if 0
GL_VERTEX_SHADER = 0x8B31
GL_FRAGMENT_SHADER = 0x8B30
GL_GEOMETRY_SHADER = 0x8DD9
GL_TESS_EVALUATION_SHADER = 0x8E87
GL_TESS_CONTROL_SHADER = 0x8E88
# endif
# if 1 /*
""" */
constexpr unsigned long long
/*"""
# */
gl_mask = 0xFFFFFFFF;
# endif

# if 1 /*
""" */
constexpr unsigned long long
/*"""
# */
# endif
lgn_mask = ~gl_mask;

# if 0

LGN_VERTEX_SHADER = 1
LGN_FRAGMENT_SHADER = 2
LGN_GEOMETRY_SHADER = 3
LGN_TESS_EVALUATION_SHADER = 4
LGN_TESS_CONTROL_SHADER = 5

GL_LGN_VERTEX_SHADER = GL_VERTEX_SHADER + (LGN_VERTEX_SHADER << 32)
GL_LGN_FRAGMENT_SHADER = GL_FRAGMENT_SHADER + (LGN_FRAGMENT_SHADER << 32)
GL_LGN_GEOMETRY_SHADER = GL_GEOMETRY_SHADER + (LGN_GEOMETRY_SHADER << 32)
GL_LGN_TESS_EVALUATION_SHADER = GL_TESS_EVALUATION_SHADER + (LGN_TESS_EVALUATION_SHADER << 32)
GL_LGN_TESS_CONTROL_SHADER = GL_TESS_CONTROL_SHADER + (LGN_TESS_CONTROL_SHADER << 32)

# endif
# if 0
"""
#endif

inline unsigned long get_gl_type(unsigned long long v)
{
	return static_cast<int>( v & gl_mask );
}

inline unsigned long get_lgn_type(unsigned long long v)
{
	return static_cast<int>( (v & lgn_mask) >> 32);
}

# if 0
"""
# endif
# endif