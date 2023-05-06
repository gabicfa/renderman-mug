#!/usr/bin/env python
import prman

def colorConverter(colourValue) :
	return colourValue / 255

def spotCeramicShader(ri, repeatCount = 100) :
    baseColor = [colorConverter(207), colorConverter(203), colorConverter(194)]
    spotsColor = (0,0,0)
    ri.Pattern("spots", "spots", {
        'color baseColor' : baseColor,
        'color spotsColor' : spotsColor,
        'float repeatCount': repeatCount
    })
    ri.Bxdf(
        "PxrSurface", "with_spots", {
            "reference color diffuseColor": ["spots:Cout"], 
            "int diffuseDoubleSided": [1],
            "float diffuseGain": 1.0, 
            "float diffuseRoughness": 0.1,
            "float diffuseExponent" : 50
    })

def darkCeramicShader(ri) :
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

def clearCeramicShader(ri) :
    # ri.Bxdf(
    #     "PxrSurface",
    #     "clearCeramic",
    #     {
    #         # "color diffuseColor" : [.2,.5,.8], 
    #         "color diffuseColor": [223/255, 232/255, 227/255],
    #         "float diffuseGain": 1.0, 
    #         # "float diffuseRoughness": 0.1,
    #         # "float diffuseExponent" : 50,
    #         "color clearcoatEdgeColor": [1, 1, 1],
    #     },
    # )
    ri.Bxdf('PxrDisney','glow inside',
    {
        'color baseColor' : [223/255, 232/255, 227/255], 
        'float specular' : [1], 
        'float specularTint' : [0], 
        'float anisotropic' : [1], 
        'float sheenTint' : [.5], 
        'float clearcoat' : [1]
    })