#!/usr/bin/env python

# import the python renderman library
import prman

ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"  # "mug.rib"

ri.Begin("__render")
ri.Display("mug.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
ri.Projection(ri.PERSPECTIVE)

# now we start our world
ri.WorldBegin()
ri.Translate(0, -6, 15)
ri.Rotate(-90, 1, 0, 0)
ri.Cylinder(4, 4.5, 12, 360)
ri.Cylinder(4, 0.5, 4.5, 360)
ri.WorldEnd()
# and finally end the rib file
ri.End()