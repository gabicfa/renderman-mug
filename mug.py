#!/usr/bin/env python

# import the python renderman library
import prman

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

def mugsHandle(ri):
    ri.ArchiveRecord(ri.COMMENT, 'handle')
    ri.TransformBegin()
    ri.Rotate(-90,1,0,0)
    ri.Translate(4.9,-6.4,0)
    ri.Scale(0.2, 1.2, 1.2)
    ri.Scale(2, 1, 1)
    ri.Rotate(90,0,0,1)
    ri.Scale(0.8, 1.8, 1)

    #  --- DARK CERAMIC SHADER
    ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 1], "string expression": [expr]})
    ri.Bxdf(
        "PxrDiffuse",
        "diffuse",
        {
            #  'color diffuseColor'  : [1,0,0]
            "reference color diffuseColor": ["seTexture:resultRGB"]
        },
    )
    ri.Torus(4.3, 0.8, 0, 360, -90)

    ri.Scale(-1, -1, 1)
    # --- SPOT CERAMIC SHADER
    ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [1, 0, 0], "string expression": [expr]})
    ri.Bxdf(
        "PxrDiffuse",
        "diffuse",
        {
            #  'color diffuseColor'  : [1,0,0]
            "reference color diffuseColor": ["seTexture:resultRGB"]
        },
    )
    ri.Torus(4.3, 0.8, 0, 360, 90)
    ri.TransformEnd()

def mugsBottomSupport(ri):
    # ----- OUTSIDE ------
    ri.TransformBegin()
    ri.Translate(0, 0, -4.31)
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_oustide')

    # --- DARK CERAMIC SHADER
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

    # ----- INSIDE ------
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_inside')

    # --- CLEAN CERAMIC SHADER
    ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 1, 0], "string expression": [expr]})
    ri.Bxdf(
        "PxrDiffuse",
        "diffuse",
        {
            #  'color diffuseColor'  : [1,0,0]
            "reference color diffuseColor": ["seTexture:resultRGB"]
        },
    )
    ri.Paraboloid(4.8, 4.9, 4.1, 360)
    ri.Disk(4.3, 4.8, 360)
    ri.TransformEnd()

    # ----- BOTTOM ------
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_bottom')

    ri.TransformBegin()
    ri.Scale(1,1,0.1)
    ri.Translate(0,0,-2.8)
    # --- CERAMIC SHADER
    ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 1, 1]})
    ri.Torus(4.33, 0.3, 0, -180, 360)
    ri.TransformEnd()

    ri.TransformBegin()
    # --- DARK CERAMIC SHADER
    ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 1], "string expression": [expr]})
    ri.Bxdf(
        "PxrDiffuse",
        "diffuse",
        {
            #  'color diffuseColor'  : [1,0,0]
            "reference color diffuseColor": ["seTexture:resultRGB"]
        },
    )
    ri.Translate(0,0,-0.34)
    ri.Sphere(3.9,0,0.4,360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(0,0,-0.2)
    ri.Disk(0, 4, 360)
    ri.TransformEnd()

def mugsMainCylinder(ri) :
    # ----- OUTSIDE - TOP ------
    ri.TransformBegin()
    ri.Attribute("identifier", {"name": "top"})
 
    # --- SPOT CERAMIC SHADER
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

    # ----- INSIDE ------
    ri.Attribute("identifier", {"name": "inside"})

    # --- CLEAN CERAMIC SHADER
    ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 1, 0], "string expression": [expr]})
    ri.Bxdf(
        "PxrDiffuse",
        "diffuse",
        {
            #  'color diffuseColor'  : [1,0,0]
            "reference color diffuseColor": ["seTexture:resultRGB"]
        },
    )
    ri.Cylinder(4.8, 0.5, 11.95, 360)

    # ----- OUTSIDE - BOTTOM ------
    ri.Attribute("identifier", {"name": "bottom"})

    # --- DARK CERAMIC SHADER
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

    # ----- TOP EDGE ------
    ri.TransformBegin()
    ri.Translate(0, 0, 11.95)
    # --- CLEAN CERAMIC SHADER
    ri.Attribute("identifier", {"name": "inside_top_edge"})
    ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 1, 0]})
    ri.Torus(4.9, 0.1, 0, 180, 360)
    ri.TransformEnd()

    # ----- MIDDLE TEXTURE ------
    ri.TransformBegin()
    ri.Translate(0, 0, 4.424)
    ri.Attribute("identifier", {"name": "middle_texture"})
    # --- SPOT CERAMIC SHADER
    ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [1, 0, 0]})
    ri.Torus(4.95, 0.13, 0, 180, 360)
    ri.TransformEnd()

def scene(ri) :
    
    # MUG POSITION

    ri.TransformBegin()
    ri.Translate(0, -1, 4)
    ri.Rotate(-110, 1, 0, 0)
    # ri.Rotate(90, 0, 0, 1)
    # ri.Rotate(45, 0, 1, 0)
    ri.Scale(0.1,0.1,0.1)

    mugsMainCylinder(ri)
    mugsBottomSupport(ri)
    mugsHandle(ri)
    
    ri.TransformEnd()

if __name__ == '__main__':

    ri = prman.Ri()  # create an instance of the RenderMan interface
    ri.Option("rib", {"string asciistyle": "indented"})

    filename = "mug.rib"

    ri.Begin("__render")
    ri.Display("mug.exr", "it", "rgba")
    ri.Format(1920, 1080, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 48})
    ri.DepthOfField(2.2,0.055,5)
    
	##Update render type to apply shadows.

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.Integrator('PxrPathTracer', 'integrator')
    ri.ShadingRate(10)
    ri.PixelVariance(0.1)
    ri.Option("searchpath", {"string texture": "./textures/:@"})
    
    # now we start our world
    ri.WorldBegin()
    ri.TransformBegin()
    
    #######################################################################
    # Lighting We need geo to emit light
    #######################################################################
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("domeLight", "string")
    ri.Rotate(80, 1, 0, 0)
    ri.Rotate(180, 0, 1, 0)
    ri.Rotate(90, 0, 0, 1)
    ri.Light("PxrDomeLight", "hdrLight", {"string lightColorMap": "Luxo-Jr_4000x2000.tex"})
    ri.AttributeEnd()
    ri.TransformEnd()
    #######################################################################
    # end lighting
    #######################################################################

    scene(ri)

    ri.TransformEnd()
    ri.WorldEnd()

    # and finally end the rib file
    ri.End()