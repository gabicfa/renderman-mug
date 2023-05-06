#!/usr/bin/env python
import prman

# import the python functions
import sys, os.path, subprocess

from shaders import darkCeramicShader, clearCeramicShader, spotCeramicShader
from handle import mugsHandle
"""
function to check if shader exists and compile it, we assume that the shader
is .osl and the compiled shader is .oso If the shader source is newer than the
compiled shader we will compile it. It also assumes that oslc is in the path.
"""
def checkAndCompileShader(shader):
    if (
        os.path.isfile(shader + ".oso") != True
        or os.stat(shader + ".osl").st_mtime - os.stat(shader + ".oso").st_mtime > 0
    ):
        print("compiling shader %s" % (shader))
        try:
            subprocess.check_call(["oslc", shader + ".osl"])
        except subprocess.CalledProcessError:
            sys.exit("shader compilation failed")

# def mugsHandle(ri):
#     ri.ArchiveRecord(ri.COMMENT, 'handle')
#     ri.TransformBegin()
#     ri.Rotate(-90,1,0,0)
#     ri.Translate(4.9,-6.4,0)
#     ri.Scale(0.2, 1.2, 1.2)
#     ri.Scale(2, 1, 1)
#     ri.Rotate(90,0,0,1)
#     ri.Scale(0.8, 1.8, 1)

#     darkCeramicShader(ri)
#     ri.Torus(4.3, 0.8, 0, 360, -90)

#     spotCeramicShader(ri)
#     ri.Torus(4.3, 0.8, 0, 360, 90)
#     ri.TransformEnd()

def mugsBottomSupport(ri):
    # ----- OUTSIDE ------
    ri.TransformBegin()
    ri.Translate(0, 0, -4.31)
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_oustide')

    darkCeramicShader(ri)
    ri.Paraboloid(5.06, 4.8, 4.0, -360)

    # ----- INSIDE ------
    ri.ArchiveRecord(ri.COMMENT, 'bottom_suport_inside')
    clearCeramicShader(ri)
    ri.Paraboloid(5.05, 5.3, 4.1, 360)
    ri.Disk(4.5, 4.9, 360)
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
    darkCeramicShader(ri)
    ri.Translate(0,0,-0.29)
    ri.Scale(1,1,0.2)
    ri.Sphere(4.1,0,2.2,-360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Disk(0.15, 4, -360)
    ri.TransformEnd()

def mugsMainCylinder(ri) :
    # ----- OUTSIDE - TOP ------
    ri.TransformBegin()
    ri.Attribute("identifier", {"name": "top"})
    ri.Scale(1,1,1.05)

    ri.TransformBegin()
    spotCeramicShader(ri, 100)

    ri.Cylinder(5, 4.5, 14, 360)

    # ----- INSIDE ------
    ri.Attribute("identifier", {"name": "inside"})

    clearCeramicShader(ri)
    ri.Cylinder(4.8, 0.5, 13.95, -360)

    # ----- OUTSIDE - BOTTOM ------
    ri.Attribute("identifier", {"name": "bottom"})

    darkCeramicShader(ri)
    ri.Cylinder(5.05, 0.45, 4.5, 360)
    ri.TransformEnd()

    # ----- TOP EDGE ------
    ri.TransformBegin()
    ri.Translate(0, 0, 13.95)
    clearCeramicShader(ri)
    ri.Torus(4.9, 0.1, 0, 180, 360)
    ri.TransformEnd()

    # ----- MIDDLE TEXTURE ------
    ri.TransformBegin()
    ri.Translate(0, 0, 4.424)
    ri.Attribute("identifier", {"name": "middle_texture"})
    spotCeramicShader(ri, 100)
    ri.Torus(4.95, 0.1, 0, 180, 360)
    ri.TransformEnd()
    ri.TransformEnd()
 
def scene(ri) :

    # MUG POSITION

    ri.TransformBegin()
    ri.Translate(0, -0.7, 4)
    ri.Rotate(-110, 1, 0, 0)
    ri.Rotate(-100, 0, 0, 1)
    # ri.Rotate(-90, 0, 1, 0)
    ri.Scale(0.1,0.1,0.1)

    
    mugsMainCylinder(ri) 
    mugsBottomSupport(ri)
    mugsHandle(ri)
    
    ri.TransformEnd()

if __name__ == '__main__':
    checkAndCompileShader("spots")

    ri = prman.Ri()  # create an instance of the RenderMan interface 
    ri.Option("rib", {"string asciistyle": "indented"})

    filename = "mug.rib"

    ri.Begin("__render")
    ri.Display("mug.exr", "it", "rgba")
    ri.Format(1920, 1080, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})
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
    ri.Rotate(-90,1,0,0)
    ri.Rotate(180,0,0,1)
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