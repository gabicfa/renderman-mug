#!/usr/bin/env python
import prman

# Ceramic shader with spots
def spotCeramicShader(ri, repeatCount = 150, pointProbability = 0.6) :
    baseColor = [colorConverter(207), colorConverter(203), colorConverter(194)]
    spotsColor = [colorConverter(26), colorConverter(26), colorConverter(23)]
    ri.Pattern("spotsCeramic", "spotsCeramic", {
        'color baseColor' : baseColor,
        'color spotsColor' : spotsColor,
        'float repeatCount': repeatCount,
        'float pointProbability': pointProbability
    })
    ri.Bxdf(
        "PxrSurface", "with_spots", {
            "reference color diffuseColor": ["spotsCeramic:Cout"], 
            "int diffuseDoubleSided": [1],
            "float diffuseGain": 1.0, 
            "float diffuseRoughness": 0.1,
            "float diffuseExponent" : 50,
            "color clearcoatEdgeColor": [0.7, 0.7, 0.7]
    })

# Dark ceramic shader
def darkCeramicShader(ri) :
    ri.Bxdf(
        "PxrSurface", 
        "ceramic",
        {
            "color diffuseColor": [colorConverter(110), colorConverter(93), colorConverter(77)], 
            "float diffuseGain": 1.0, 
            "float diffuseRoughness": 0.1,
            "float diffuseExponent" : 50,
            "color clearcoatEdgeColor": [0.7, 0.7, 0.7]
        }
    )

# Clear ceramic shader
def clearCeramicShader(ri) :
    baseColor = [colorConverter(223), colorConverter(232), colorConverter(227)]

    ri.Bxdf('PxrDisney','glowinside',
    {
        'color baseColor' : baseColor, 
        'float specular' : [1], 
        'float specularTint' : [0], 
        'float anisotropic' : [1], 
        'float sheenTint' : [.5], 
        'float clearcoat' : [1]
    })

# Table shader with wood pattern
def table(ri) :
    ri.Pattern('wood','wood', {})
    ri.Bxdf('PxrSurface', 'woodtable',
    {
        'reference color diffuseColor' : ['wood:Cout'],
        "float diffuseGain": 1.0, 
        "float diffuseRoughness": 0.3,
        "float diffuseExponent" : 30
    })

# Convert color values from 0-255 to 0-1 range
def colorConverter(colourValue) :
    return colourValue / 255
