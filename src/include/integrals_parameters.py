spatial_symmetry: dict = {"overlap": 0, "nucpot": 0, "kinetic": 0, "angmom": 0, "sd": 1, "fc": 0, "darwin": 0,
"massvelo": 0, "nelfld": 1, "diplen": 0, "dipvel": 0, "pso": 1, "nstcgo": 1, "dnske": 1, "psoke": 1,
"psooz": 1, "ozke": 0}
magnetic: dict = {"overlap": 0, "nucpot": 0, "kinetic": 0, "angmom": 1, "sd": 1, "fc": 0, "darwin": 0,
"massvelo": 0, "nelfld": 0, "diplen": 1, "dipvel": 1, "pso": 0, "nstcgo": 1, "dnske": 1, "psoke": 0,
"psooz": 1, "ozke": 1}
integral_symmetry: dict = {"overlap": "sym", "nucpot": "sym", "kinetic": "sym", "angmom": "antisym",
"sd": "sym", "fc": "sym", "darwin": "sym", "massvelo": "sym", "nelfld": "sym", "diplen": "sym",
"dipvel": "antisym", "pso": "antisym", "nstcgo": "sym", "dnske": "sym", "psoke": "square",
"psooz": "square", "ozke": "antisym"}

magnetic_axes: dict = {0:"x", 1:"y", 2:"z"}