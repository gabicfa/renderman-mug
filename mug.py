#!/usr/bin/env python
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

def darkCeramicShader() :
    ri.Bxdf(
        "PxrSurface", 
        "ceramic",
        {
            "color diffuseColor": [110/255, 93/255, 77/255], 
            "float diffuseGain": 1.0, 
            "float diffuseRoughness": 0.1,
            "float diffuseExponent" : 50
        }
    )

def clearCeramicShader() :
    ri.Bxdf(
        "PxrSurface",
        "clearCeramic",
        {
            "color diffuseColor": [223/255, 232/255, 227/255],
            "float diffuseGain": 1.0, 
            "float diffuseRoughness": 0.1,
            "float diffuseExponent" : 50,
            "color clearcoatEdgeColor": [0.4, 0.4, 0.4]
        },
    )

def mugsHandle(ri):
    ri.ArchiveRecord(ri.COMMENT, 'handle')
    ri.TransformBegin()
    ri.Rotate(-90,1,0,0)
    ri.Translate(4.9,-6.4,0)
    ri.Scale(0.2, 1.2, 1.2)
    ri.Scale(2, 1, 1)
    ri.Rotate(90,0,0,1)
    ri.Scale(0.8, 1.8, 1)

    darkCeramicShader
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

    darkCeramicShader()
    ri.Paraboloid(5.06, 4.8, 4.0, -360)

    # ----- INSIDE ------
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_inside')

    # --- CLEAN CERAMIC SHADER
    clearCeramicShader()
    ri.Paraboloid(5.03, 4.9, 4.1, 360)
    ri.Disk(4.4, 4.8, 360)
    ri.TransformEnd()

    # ----- BOTTOM ------
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_bottom')

    ri.TransformBegin()
    ri.Scale(1,1,0.1)
    ri.Translate(0,0,-2.8)

    # --- CERAMIC SHADER
    ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0.95, 0.95, 0.95]})
    ri.Torus(4.33, 0.3, 0, -180, 360)
    ri.TransformEnd()

    ri.TransformBegin()
    darkCeramicShader()
    ri.Translate(0,0,-0.28)
    ri.Sphere(4,0,0.4,-360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(0,0,-0.2)
    ri.Disk(0, 4, -360)
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

    ri.Cylinder(5, 4.5, 14, 360)

    # ----- INSIDE ------
    ri.Attribute("identifier", {"name": "inside"})

    # --- CLEAN CERAMIC SHADER
    clearCeramicShader()
    ri.Cylinder(4.8, 0.5, 13.95, -360)

    # ----- OUTSIDE - BOTTOM ------
    ri.Attribute("identifier", {"name": "bottom"})

    darkCeramicShader()
    ri.Cylinder(5.05, 0.47, 4.5, 360)
    ri.TransformEnd()

    # ----- TOP EDGE ------
    ri.TransformBegin()
    ri.Translate(0, 0, 13.95)
    # --- CLEAN CERAMIC SHADER
    clearCeramicShader()
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
    ri.Translate(0, -0.6, 4)
    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(90, 0, 0, 1)
    ri.Rotate(15, 0, 1, 0)
    ri.Scale(0.1,0.1,0.1)

    mugsMainCylinder(ri)
    mugsBottomSupport(ri)
    # mugsHandle(ri)
    
    ri.TransformEnd()

if __name__ == '__main__':

    ri = prman.Ri()  # create an instance of the RenderMan interface
    ri.Option("rib", {"string asciistyle": "indented"})

    filename = "mug.rib"

    ri.Begin("__render")
    ri.Display("mug.exr", "it", "rgba")
    ri.Format(1920, 1080, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 38})
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