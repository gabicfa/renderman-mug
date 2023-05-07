from shaders.shaders import table

def Cube(ri,width=1.0,height=1.0,depth=1.0) :
    table(ri)
    points=[-0.5,-0.5,-0.5,
        0.5,-0.5,-0.5,
        -0.5, 0.5,-0.5,
        0.5, 0.5,-0.5,
        -0.5,-0.5, 0.5,
        0.5,-0.5, 0.5,
        -0.5, 0.5, 0.5,
        0.5, 0.5, 0.5]
    npolys=[4,4,4,4,4,4]
    nvertices=[0,2,3,1,0,1,5,4,0,4,6,2,1,3,7,5,2,6,7,3,4,5,7,6]
    ri.PointsPolygons(npolys,nvertices,{ri.P:points})
                    
def Table(ri):
    ri.TransformBegin()
    ri.Scale(8,2,0.2)
    ri.Translate(0, 0.1, -0.7)
    Cube(ri)
    ri.TransformEnd()