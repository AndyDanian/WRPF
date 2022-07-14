spatial_symmetry: dict = {"overlap": 0, "nucpot": 0, "kinetic": 0, "angmom": 0, "sd": 1, "fc": 0, "darwin": 0,
"massvelo": 0, "nelfld": 1, "diplen": 0, "dipvel": 0, "pso": 1, "nstcgo": 1, "dnske": 1, "psoke": 1,
"psooz": 1, "ozke": 0, "spinorbit": 1, "laplacian": 0, "sofiel": 1}
magnetic: dict = {"overlap": 0, "nucpot": 0, "kinetic": 0, "angmom": 1, "sd": 1, "fc": 0, "darwin": 0,
"massvelo": 0, "nelfld": 0, "diplen": 1, "dipvel": 1, "pso": 0, "nstcgo": 1, "dnske": 1, "psoke": 0,
"psooz": 1, "ozke": 1, "spinorbit": 0, "laplacian": 1, "sofield": 1}
integral_symmetry: dict = {"overlap": "sym", "nucpot": "sym", "kinetic": "sym", "angmom": "antisym",
"sd": "sym", "fc": "sym", "darwin": "sym", "massvelo": "sym", "nelfld": "sym", "diplen": "sym",
"dipvel": "antisym", "pso": "antisym", "nstcgo": "sym", "dnske": "sym", "psoke": "square",
"psooz": "square", "ozke": "antisym", "spinorbit": "antisym", "laplacian": "sym", "sofiel": "sym"}

# Separated magnetic axes of cartessian component (laplacian), i. e., to make a cartessian component by
# separated in e_integral.py

magnetic_axes: dict = {0:"x", 1:"y", 2:"z"}
spatial_components: dict = {0:"xx", 1:"yy", 2:"zz", 3:"xy", 4:"xz", 5:"yz"}