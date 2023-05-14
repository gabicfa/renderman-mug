#!/usr/bin/env python
import prman

# Import required modules
import sys, os.path, subprocess
import ProcessCommandLine as cl

# Import Mug and Table assets
from assets.mug import Mug 
from assets.table import Table

# Check and compile shader if needed
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

# Define the scene with geometry and transformations
def scene(ri) :
    ri.TransformBegin()
    ri.Translate(0, -0.6, 3.3)
    ri.Rotate(-95, 1, 0, 0)

    ri.TransformBegin()
    Mug(ri)
    ri.TransformEnd()

    ri.TransformBegin()
    Table(ri)
    ri.TransformEnd()

    ri.TransformEnd()

# Set up the lighting environment
def lighting(ri):
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("domeLight", "string")
    ri.Rotate(265,1,0,0)
    ri.Rotate(-80,0,0,1)
    ri.Scale(1,-1,1)
    ri.Light("PxrDomeLight", 
        "hdrLight", {
            "string lightColorMap": "kitchen.tex",
            "float intensity": 0.85,
            "float exposure": -0.2
        })
    ri.AttributeEnd()
    ri.TransformEnd()

# Set up the display channels for denoising
def displaySetUpForDenoise(ri, openProgram = "it"):
    # Beauty...
    ri.DisplayChannel("color Ci")
    ri.DisplayChannel("float a")
    ri.DisplayChannel("color mse", {"string source": "color Ci", "string statistics": "mse"})

    # Shading...
    ri.DisplayChannel(
        "color albedo",
        {"string source": "color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)"},
    )

    ri.DisplayChannel(
        "color albedo_var",
        {
            "string source": "color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)",
            "string statistics": "variance",
        },
    )

    ri.DisplayChannel("color diffuse", {"string source": "color lpe:C(D[DS]*[LO])|O"})
    ri.DisplayChannel("color diffuse_mse", {"string source": "color lpe:C(D[DS]*[LO])|O", "string statistics": "mse"})
    ri.DisplayChannel("color specular", {"string source": "color lpe:CS[DS]*[LO]"})
    ri.DisplayChannel("color specular_mse", {"string source": "color lpe:CS[DS]*[LO]", "string statistics": "mse"})

    # Geometry...
    ri.DisplayChannel("float zfiltered", {"string source": "float z", "string filter": "gaussian"})
    ri.DisplayChannel(
        "float zfiltered_var", {"string source": "float z", "string filter": "gaussian", "string statistics": "variance"}
    )
    ri.DisplayChannel("normal normal", {"string source": "normal Nn"})
    ri.DisplayChannel("normal normal_var", {"string source": "normal Nn", "string statistics": "variance"})
    ri.DisplayChannel("vector forward", {"string source": "vector motionFore"})
    ri.DisplayChannel("vector backward", {"string source": "vector motionBack"})
    ri.Display(
        "output.exr",
        openProgram,
        "Ci,a,mse,albedo,albedo_var,diffuse,diffuse_mse,specular,specular_mse,zfiltered,zfiltered_var,normal,normal_var,forward,backward",
        {"int asrgba": [1]},
    )

# Main rendering routine
def main(
    filename,
    shadingrate=10,
    pixelvar=0.1,
    fov=48.0,
    width=1920,
    height=1080,
    integrator="PxrPathTracer",
    integratorParams={},
    openProgram = "it"
):
    # Check and compile shaders if necessary
    checkAndCompileShader("shaders/spotsCeramicShader")
    checkAndCompileShader("shaders/woodShader")

    print("shading rate {} pivel variance {} using {} {}".format(shadingrate, pixelvar, integrator, integratorParams))
    
    ri = prman.Ri()
    ri.Begin(filename)
    ri.Option("searchpath", {"string texture": "./textures/:@"})
    ri.Format(width, height, 1)

    # Set up display for denoising
    displaySetUpForDenoise(ri, openProgram)

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1], "string pixelfiltermode": "importance"})
    ri.Integrator(integrator, "integrator", integratorParams)
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: fov})
    ri.DepthOfField(2.2,0.055,3)
    
    ri.WorldBegin()
    # Set up scene transformations and lighting
    ri.TransformBegin()
    ri.Translate(0,-1,0)
    ri.Rotate(-15,1,0,0)
    lighting(ri)
    scene(ri)
    ri.TransformEnd()

    ri.WorldEnd()

    ri.End()

# Process command line arguments and call main function
if __name__ == '__main__':
    cl.ProcessCommandLine("main.rib")
    main(
        cl.filename,
        cl.args.shadingrate,
        cl.args.pixelvar,
        cl.args.fov,
        cl.args.width,
        cl.args.height,
        cl.integrator,
        cl.integratorParams,
        cl.openProgram
    )