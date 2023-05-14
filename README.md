# Realistic Mug and Table Scene

This repository contains a Python script to generate a realistic 3D scene featuring a mug and a table using Pixar's RenderMan Interface. The code is organized into several Python scripts and shader files that define the geometry, shaders, and rendering attributes for the mug, table, and the scene's environment.

![img1](/img/img1.jpg)

## Files

The repository is organized as follows:

1. `main.py`: The main Python script that sets up the scene, including the camera, light sources, and objects (mug and table), and renders the scene using RenderMan.
2. `shaders/shaders.py`: A collection of custom shaders for the mug and table.
3. `shaders/spotsCeramicShader.osl`: An Open Shading Language (OSL) shader for creating a spotted ceramic material.
4. `shaders/woodShader.osl`: An OSL shader for creating a wood material.
5. `/assets/mug.py`: A Python script that defines the geometry and shading for the mug using the custom shaders.
6. `/assets/table.py`: A Python script that defines the geometry and shading for the table using the custom shaders.

## Usage

To render the scene, you will need to have Pixar's RenderMan installed on your machine. You can download RenderMan for free for non-commercial use from the [official website](https://renderman.pixar.com/).

Once RenderMan is installed, you can run the main script to render the scene:

```
python main.py
```

This will generate a rendered image of the scene in the current working directory as `output.exr`.

## Customization

You can customize the scene by modifying the main.py script. Some of the customizable attributes include:

1. Camera position and orientation
2. Light sources and their attributes (color, intensity, etc.)
3. Mug and table shaders (colors, textures, etc.)

Additionally, you can create new objects using the provided shaders or create new shaders by adding new OSL shader files and importing them into the `shaders/shaders.py` file.
