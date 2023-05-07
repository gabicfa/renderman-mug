#!/usr/bin/env python
import prman

def spotCeramicShader(ri, repeatCount = 150, pointProbability = 0.6) :
    baseColor = [colorConverter(207), colorConverter(203), colorConverter(194)]
    spotsColor = [colorConverter(26), colorConverter(26), colorConverter(23)]
    ri.Pattern("spots", "spots", {
        'color baseColor' : baseColor,
        'color spotsColor' : spotsColor,
        'float repeatCount': repeatCount,
        'float pointProbability': pointProbability
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
            "color diffuseColor": [colorConverter(110), colorConverter(93), colorConverter(77)], 
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

def colorConverter(colourValue) :
	return colourValue / 255