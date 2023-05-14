from shaders.shaders import table

# Function to create a cube with specified width, height, and depth, using the table shader
def Cube(ri, width=1.0, height=1.0, depth=1.0):
    # Apply the table shader to the cube
    table(ri)
    
    # Define the points for the vertices of the cube
    points = [-0.5, -0.5, -0.5,
              0.5, -0.5, -0.5,
              -0.5,  0.5, -0.5,
              0.5,  0.5, -0.5,
              -0.5, -0.5,  0.5,
              0.5, -0.5,  0.5,
              -0.5,  0.5,  0.5,
              0.5,  0.5,  0.5]
    
    # Define the number of polygons for each face of the cube
    npolys = [4, 4, 4, 4, 4, 4]
    
    # Define the indices for the vertices of each polygon
    nvertices = [0, 2, 3, 1, 0, 1, 5, 4, 0, 4, 6, 2, 1, 3, 7, 5, 2, 6, 7, 3, 4, 5, 7, 6]
    
    # Create the cube using the points, number of polygons, and vertex indices
    ri.PointsPolygons(npolys, nvertices, {ri.P: points})

# Function to create a table using the Cube function
def Table(ri):
    ri.TransformBegin()
    
    # Scale and position the table top
    ri.Scale(8, 2, 0.2)
    ri.Translate(0, 0.1, -0.7)
    
    # Create the table top using the Cube function
    Cube(ri)
    
    ri.TransformEnd()
