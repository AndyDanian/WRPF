from lib import *
from h1i import *
from wave_function import *

nucleu: dict = {"overlap": 0, "nucpot": 1, "kinetic": 0, "angmom": 0, "sd": 0}
esp_sym: dict = {"overlap": 0, "nucpot": 0, "kinetic": 0, "angmom": 0, "sd": 1}
magnetic_r: dict = {"overlap": 0, "nucpot": 0, "kinetic": 0, "angmom": 1, "sd": 1}
integral_symmetry: dict = {"overlap": "sym", "nucpot": "sym", "kinetic": "sym", "angmom": "antisym", "sd": "sym"}

magnetic_components: dict = {0:"x", 1:"y", 2:"z"}

class eint:
    def __init__(self, wf: dict = None):
        """
        Manages the electronic integrals calculations

        Args:
            wf (dict): dictionary with information about wave function
        """

        if not wf:
            raise ValueError(
                "*** Error \n\n There isn't information in the  wave function object."
            )

        self._array_wf = wf
        # linealize arrays to calculate the integrals
        (
            self._charge,
            self._coord,
            self._exp,
            self._center,
            self._lx,
            self._ly,
            self._lz,
        ) = linealize_array_wf(wf)

    ##################################################################
    # METHODS
    ##################################################################

    def integration(
        self, names: list = None, properties: list = None, output: int = None
    ):

        if not names:
            raise ValueError("***Error \n\n what integral do you want?")
        else:
            for name in names:
                if name.lower() not in integral_symmetry.keys():
                    raise ValueError(f"*** Error \n\n\
                    Integral name is not implement or the name is mistake\n\n\
                    Integrals implemented: \n\
                        {integral_symmetry.keys()}")

        integrals = {}
        symmetry = {}

        for name in names:
            if nucleu[name.lower()] == 0 and esp_sym[name.lower()] == 0:
                symmetry[str(name)] = integral_symmetry[name.lower()]

                integrals[str(name)] = h1i(
                    charge = self._charge,
                    coord = self._coord,
                    exp = self._exp,
                    center = self._center,
                    lx = self._lx,
                    ly = self._ly,
                    lz = self._lz,
                    name = name,
                    output = output
                )

            if nucleu[name.lower()] == 1 and esp_sym[name.lower()] == 0:
                for atom in properties[name]["atoms"]:
                    symmetry[
                        name.lower() + " " + str(atom + 1)
                    ] = integral_symmetry[name.lower()]

                    integrals[name.lower() + " " + str(atom + 1)] = h1i(
                        charge = self._charge,
                        coord = self._coord,
                        exp = self._exp,
                        center = self._center,
                        lx = self._lx,
                        ly = self._ly,
                        lz = self._lz,
                        name = name,
                        output = output,
                        atom = atom,
                    )

            if magnetic_r[name.lower()] == 0 and esp_sym[name.lower()] == 1:
                for m_component in properties[name]["magnetic"]:
                    if type(m_component) == int:
                        integral_name: str = (name.lower() + " " 
                        + magnetic_components[m_component])
                        magnetic_xyz: int = m_component
                    else:
                        integral_name: str = (name.lower() + " " 
                        + m_component)
                        magnetic_xyz: int = (list(magnetic_components.keys())
                                            [list(magnetic_components.values()).index(m_component)])

                    symmetry[
                        integral_name
                    ] = integral_symmetry[name.lower()]

                    integrals[integral_name] = h1i(
                        charge = self._charge,
                        coord = self._coord,
                        exp = self._exp,
                        center = self._center,
                        lx = self._lx,
                        ly = self._ly,
                        lz = self._lz,
                        name = name,
                        output = output,
                        magnetic_xyz = magnetic_xyz,
                        gauge = properties[name]["gauge"]
                    )

            if magnetic_r[name.lower()] == 1 and esp_sym[name.lower()] == 1:
                number_atoms: int =  len(self._coord[0][:])

                for spatial in properties[name]["spatial"]:

                    # Selection of coordinate x, y, z for spatial symmetry
                    coordinate: int = spatial - 3 * int(spatial/3)
                    atom: int = int(spatial/3)
                    
                    if atom >= number_atoms:
                        raise ValueError(f"***Error \n\n\
                            atom {atom} doesn't exist") 
    
                    if coordinate == 0:
                        spatial_sym: int = 0
                    elif coordinate == 1:
                        spatial_sym: int = 1
                    elif coordinate == 2:
                        spatial_sym: int = 2
                    else:
                        raise ValueError("*** Error\n\n \
                            spatial sym doesn't exist")

                    for m_component in properties[name]["magnetic"]:

                        if type(spatial) == int:
                            integral_name: str = (name.lower() + " " +
                            str(spatial + 1) + " " + magnetic_components[m_component])
                            magnetic_xyz: int = m_component
                        else:
                            integral_name: str = (name.lower() + " " +
                            str(spatial + 1) + " "  + m_component)
                            magnetic_xyz: int = (list(magnetic_components.keys())
                            [list(magnetic_components.values()).index(m_component)])

                        symmetry[
                            integral_name
                        ] = integral_symmetry[name.lower()]

                        integrals[integral_name] = h1i(
                            charge = self._charge,
                            coord = self._coord,
                            exp = self._exp,
                            center = self._center,
                            lx = self._lx,
                            ly = self._ly,
                            lz = self._lz,
                            name = name,
                            output = output,
                            magnetic_xyz = magnetic_xyz,
                            spatial_sym = spatial_sym,
                            atom = atom
                        )

        # Print integral
        if output > 10:
            for atomic_integrals_name in integrals.keys():
                print_triangle_matrix(
                    vector_to_matrix(
                        len(self._exp),
                        integrals[
                            atomic_integrals_name
                        ],
                        symmetry[
                            atomic_integrals_name
                        ],
                    ),
                    atomic_integrals_name,
                )
        return integrals


if __name__ == "__main__":
    from wave_function import *

    wfn = wave_function("io/H2.molden")

    s = eint(wfn.build_wfn_array())

    s.integration(["sd"],
                  #["overlap", "pot", "angmom"], 
                  {"pot":{"atoms":[0, 1]}, 
                  "angmom":{"magnetic":[0, 1, 2], "gauge":[0.0, 0.0, 1.404552358700]},
                  "sd":{"spatial":[0,1,2,3,4,5], "magnetic":[0,1,2]}
                  }
                  , 12)
