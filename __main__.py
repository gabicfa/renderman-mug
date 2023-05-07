#!/usr/bin/env python
import prman

# import the python functions
import sys, os.path, subprocess
import ProcessCommandLine as cl

from mug import mugsHandle, mugsMainCylinder, mugsBottomSupport

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
 
def scene(ri) :

    # MUG POSITION
    ri.TransformBegin()
    ri.Translate(0, -0.7, 3.5)
    ri.Rotate(-110, 1, 0, 0)
    ri.Rotate(-100, 0, 0, 1)
    # ri.Rotate(-90, 0, 1, 0)
    ri.Scale(0.1,0.1,0.1)

    mugsMainCylinder(ri) 
    mugsBottomSupport(ri)
    mugsHandle(ri)
    
    ri.TransformEnd()
    
def lighting(ri):
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("domeLight", "string")
    ri.Rotate(-90,1,0,0)
    ri.Rotate(180,0,0,1)
    ri.Light("PxrDomeLight", "hdrLight", {"string lightColorMap": "Luxo-Jr_4000x2000.tex"})
    ri.AttributeEnd()
    ri.TransformEnd()

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
        "mug.exr",
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
    checkAndCompileShader("spots")
    print("shading rate {} pivel variance {} using {} {}".format(shadingrate, pixelvar, integrator, integratorParams))
    
    ri = prman.Ri()
    ri.Begin(filename)
    ri.Option("searchpath", {"string texture": "./textures/:@"})
    ri.Format(width, height, 1)
    displaySetUpForDenoise(ri, openProgram)

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1], "string pixelfiltermode": "importance"})
    ri.Integrator(integrator, "integrator", integratorParams)
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: fov})
    ri.DepthOfField(2.2,0.055,5)
    
    ri.WorldBegin()
    ri.TransformBegin()
    lighting(ri)
    scene(ri)
    ri.TransformEnd()
    ri.WorldEnd()

    ri.End()

if __name__ == '__main__':
    cl.ProcessCommandLine("mug.rib")
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