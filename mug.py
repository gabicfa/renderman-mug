#!/usr/bin/env python

# import the python renderman library
import prman

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "mug.rib"

ri.Begin("__render")
ri.Display("mug.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

# setup the raytrace / integrators
ri.Hider("raytrace", {"int incremental": [1]})
ri.ShadingRate(10)
ri.PixelVariance(0.1)
ri.Integrator("PxrPathTracer", "integrator", {})
ri.Option("statistics", {"filename": ["stats.txt"]})
ri.Option("statistics", {"endofframe": [1]})
ri.Option("searchpath", {"string texture": "./textures/:@"})


# now we start our world
ri.WorldBegin()

# create a simple checker pattern
expr = """
$colour = c1;
$c = floor( 10 * $u ) +floor( 10 * $v );
if( fmod( $c, 2.0 ) < 1.0 )
{
	$colour=c2;
}
$colour
"""

 #######################################################################
# Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("domeLight", "string")
ri.Rotate(45, 0, 1, 0)
ri.Rotate(90, 1, 0, 0)
ri.Rotate(100, 0, 0, 1)
ri.Attribute("visibility", {"int camera": [0]})
ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "Luxo-Jr_4000x2000.tex"})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################

ri.Translate(0, -1.5, 30)
ri.Rotate(-90, 1, 0, 0)
# ri.Rotate(90, 0, 0, 1)
# ri.Rotate(90, 0, 1, 0)


ri.TransformBegin()
ri.Attribute("identifier", {"name": "top"})
# use the pattern
ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [1, 0, 0], "string expression": [expr]})
ri.Bxdf(
    "PxrDiffuse",
    "diffuse",
    {
        #  'color diffuseColor'  : [1,0,0]
        "reference color diffuseColor": ["seTexture:resultRGB"]
    },
)

ri.Cylinder(5, 4.5, 12, 360)
ri.Attribute("identifier", {"name": "inside"})
# ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 1, 0]})
ri.Cylinder(4.85, 0.5, 11.95, 360)

ri.Attribute("identifier", {"name": "bottom"})
# use the pattern
ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 1], "string expression": [expr]})
ri.Bxdf(
    "PxrDiffuse",
    "diffuse",
    {
        #  'color diffuseColor'  : [1,0,0]
        "reference color diffuseColor": ["seTexture:resultRGB"]
    },
)
ri.Cylinder(5.05, 0.5, 4.5, 360)
ri.TransformEnd()

ri.TransformBegin()
ri.Translate(0, 0, 11.95)
ri.Attribute("identifier", {"name": "inside_top_edge"})
ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [1, 0, 0]})
ri.Torus(4.9, 0.1, 0, 180, 360)
ri.TransformEnd()

ri.TransformBegin()
ri.Translate(0, 0, 4.424)
ri.Attribute("identifier", {"name": "middle_texture"})
ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 0, 1]})
ri.Torus(5, 0.13, 0, 180, 360)
ri.TransformEnd()

ri.TransformBegin()
ri.Translate(0, 0, -4.31)
ri.Attribute("identifier", {"name": "bottom_suport"})
ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 1], "string expression": [expr]})
ri.Bxdf(
    "PxrDiffuse",
    "diffuse",
    {
        #  'color diffuseColor'  : [1,0,0]
        "reference color diffuseColor": ["seTexture:resultRGB"]
    },
)
ri.Paraboloid(5.06, 4.8, 4.0, 360)
# ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 1, 1]})
ri.Disk(4, 4.6, 360)
ri.TransformEnd()

ri.TransformBegin()
ri.Rotate(-90,1,0,0)
ri.Translate(5,-5.4,0)
ri.Scale(0.3, 1.2, 1.2)
ri.Scale(2, 1, 1)

ri.Rotate(90,0,0,1)
# ri.Rotate(7,0,0,1)
ri.Scale(0.8, 1, 1)


# ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 1], "string expression": [expr]})
# ri.Bxdf(
#     "PxrDiffuse",
#     "diffuse",
#     {
#         #  'color diffuseColor'  : [1,0,0]
#         "reference color diffuseColor": ["seTexture:resultRGB"]
#     },
# )
ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 1, 1]})
ri.Torus(4.3, 0.8, 0, 360, -90)
ri.TransformEnd()

ri.WorldEnd()

# and finally end the rib file
ri.End()