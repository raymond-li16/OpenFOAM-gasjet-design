import os

x_blocks = 10
y_blocks = 10
z_blocks = 10

xmin = 0
xmax = 30
ymin = -10
ymax = 10
zmin = -10
zmax = 10

path = "../OpenFOAM-Nozzle/3DJet_template_rhosimple/system/blockMeshDict"
with open(path, 'w') as f:
    # write header
    f.write(
    "FoamFile"
    "{\n"
    "    version     2.0;\n"
    "    format      ascii;\n"
    "    class       dictionary;\n"
    "    object      blockMeshDict;\n"
    "}\n\n"
    "convertToMeters 0.001;\n\n"
    )

    # Write vertices
    f.write('vertices\n(\n')
    for i in range(2):
        x = xmin + (xmax - xmin) * i
        for j in range(2):
            y = ymin + (ymax - ymin) * j
            for k in range(2):
                z = zmin + (zmax - zmin) * k
                f.write(f'    ({x} {y} {z})\n')
    f.write(');\n')

    # Write blocks
    # Start at lowest coordinates in all axes
    f.write('blocks\n(\n')
    vertices = [
        0,
        4,
        6,
        2,
        1,
        5,
        7,
        3,
    ]
    f.write('    hex (')
    f.write(' '.join([str(x) for x in vertices]))
    f.write(')\n')
    f.write(f'    ({x_blocks} {y_blocks} {z_blocks})\n')
    f.write('    SimpleGrading (1 1 1)\n);\n')

    # Write edges
    f.write("edges\n")
    f.write("(\n")
    f.write(");\n\n")

    f.write(
        """
boundary
(
    inlet              // patch name
    {
        type patch;    // patch type for patch 0
        faces
        (
            (0 1 3 2)  // block face in this patch
        );
    }                  // end of 0th patch definition

    outlet             // patch name
    {
        type patch;    // patch type for patch 1
        faces
        (
            (4 6 7 5)
        );
    }
    walls
    {
        type wall;
        faces
        (
            (0 4 5 1)
            (3 7 6 2)
            (0 2 6 4)
            (1 5 7 3)
        );
    }
);
"""
    )


    # Write