from libfock import *

class fock():
    def __init__(self, eom: list = None):
        """
        Fock object

        This object is to build or any action with fock matrix

        Args:
        ----

        eom (list): Molecular orbitals energies
        """

        if not eom or None in eom:
            print("***Warning \n\n\
                The fock object didn't recive any or nothing of the molecular orbitals energies.\n\n\
                    if you'll want calculate, you can use:\n\
                    * calculate_hf_moe: Use the wave funtion or kinetic, e->-<nucleu interactoin,\n\
                    and electron repulsion integrals")

        self._eom = eom

    ################################################################################################
    # METHODS
    ################################################################################################

    def run_hf_fock_calculate(self, intk: list = None, inten: dict = None, intee: list = None,
                            mocoef: list = None, nprim: int = None, natoms: int = None, ne: int = None,
                            charge: list = None, coord: list = None, verbose: int = 0):
        """
        Run calculation Hartree--Fock molecular orbital energies

        Args:
        ----

        intk (list): 2d array with atomic kinetic integrals
        inten (dict): dictionary of 2d arrays with atomic electron--nucleus interactions integrals
        intk (list): 2d array with atomic electron repulsion integrals
        mocoef (list): 2d array with molecular obital coefficients
        nprim (int): primitive number
        natoms (int): atoms number
        ne (int): electrons number
        charge (list): atomic charges
        coord (list): 2d array with atomic coordinates
        verbose (int): print level

        Return:
        ------

        eom (list): 1d array with molecular orbitals energies
        """
        print("\n*** Calculating: Fock matrix at Hartree--Fock level")
        time_start_eom = time()

        if verbose > 20:
            print_triangle_matrix(integral = mocoef, name = "Molecular Orbital Coefficients", matriz_sym = "square")

        time_start_dm = time()
        mocoef_T = [list(value) for value in zip(*mocoef)]
        density_matrix: list = [[0.0 for zero in range(nprim)]for zero in range(nprim)]
        if ne%2 ==0:
            ne2 = int(ne/2)
        else:
            ne2 = int(ne/2) + 1
        for i in range(nprim):
            for j in range(nprim):

                for k in range(ne2):
                    density_matrix[i][j] += 2.0*mocoef[i][k]*mocoef[j][k]
        if verbose > 10:
            print(f"Time to calculate density matrix: {time() - time_start_dm}")
        if verbose > 20:
            print_triangle_matrix(integral = density_matrix, name= "Density Matrix", matriz_sym = "sym")

        #Core Hamiltonian
        time_start_ch = time()
        hcore: list = [[0 for zero in range(nprim)]for zero in range(nprim)]
        for i in range(nprim):
            for j in range(nprim):
                ven = 0.0
                for atom_en in inten.values():
                    ven += atom_en[i][j]
                hcore[i][j] = intk[i][j] + ven
        if verbose > 10:
            print(f"Time to calculate Core Hamiltonian Matrix: {time() - time_start_ch}")
        if verbose > 20:
            print_triangle_matrix(integral = hcore, name = "Core Hamiltonian Matrix", matriz_sym = "sym")


        #Matriz G
        time_start_g = time()
        g: list = [[0 for zero in range(nprim)]for zero in range(nprim)]
        for i in range(nprim):
            for j in range(nprim):
                g[i][j] = 0.0
                for k in range(nprim):
                    for l in range(nprim):
                        g[i][j] += density_matrix[k][l]*(intee[i][j][k][l]-0.5*intee[i][l][k][j])
        if verbose > 10:
            print(f"Time to calculate G Matrix: {time() - time_start_g}")
        if verbose > 20:
            print_triangle_matrix(integral = g, name = "G Matrix", matriz_sym = "sym")

        #Matriz Fock
        time_start_fock_ao = time()
        fock: list = [[0 for zero in range(nprim)]for zero in range(nprim)]
        for i  in range(nprim):
            for j  in range(nprim):
                fock[i][j] = hcore[i][j] + g[i][j]
        if verbose > 10:
            print(f"Time to calculate Fock Matrix in AO: {time() - time_start_fock_ao}")
        if verbose > 20:
            print_triangle_matrix(integral = fock, name = "Fock Matrix in AO", matriz_sym = "square")

        #FOCK
        #AO TO MO
        fock_mo = np.matmul(np.array(mocoef_T),np.matmul(np.array(fock),np.array(mocoef)))
        eom: list = [value for irow, row in enumerate(fock_mo)
                    for icol, value in enumerate(row) if irow == icol]
        #Nuleu Repulsion
        time_start_te = time()
        vnn = 0.0
        distance_coordinate = [0 for i in range(3)]
        for i in range(natoms-1):
            for k in range(i + 1, natoms):
                for l in range(3):
                    distance_coordinate[l] = coord[k][l] - coord[i][l]
                    distance_coordinate[l] *= distance_coordinate[l]

                distance_magnitud = np.sqrt(sum(distance_coordinate))
                vnn += charge[i]*charge[k]/distance_magnitud

        #Electronic energy
        electronic_energy = 0.0
        for i in range(nprim):
            for j in range(nprim):
                electronic_energy += 0.5*density_matrix[i][j]*(hcore[i][j] + fock[i][j])
        if verbose > 10:
            print(f"Time to calculate Total energy: {time() - time_start_te}")

        if verbose <= 10 or not verbose:
            print(f"\n Print the first 20 Hartree--Fock molecular orbitals energies: \n")
            if float(nprim/5) >= 5:
                rows: int = 5
            else:
                rows: int = int(nprim/5)
        else:
            print(f"Print all Hartree--Fock molecular orbitals energies: \n")
            rows: int = int(nprim/5)

        if nprim % 5 != 0:
            rows += 1

        for row in range(rows):
            if (row+1)*5 < nprim:
                columns = (row + 1)*5
            else:
                columns = nprim

            print(
                *[str("{:.6f}".format(eom[i])).center(14)
                for i in range(row*5, columns)],
                #end="",
            )

        print("\n")
        print(40*"=")
        gap = eom[ne2]-eom[ne2-1]
        print(f"  E(LUMO):  {eom[ne2]} au")
        print(f"- E(HOMO):  {eom[ne2-1]}   au")
        print(f"----------------------------")
        print(f"    gap  :  {gap}        au")
        print(40*"=")
        print("\n")
        print(40*"=")
        print(f"\nElectronic energy: {electronic_energy}")
        print(f"Nuclear energy: {vnn}")
        print(f"Total energy (HF): {electronic_energy + vnn} \n")
        print(40*"=")
        if verbose > 10:
            print(f"Time to calculate molecular orbitals energies: {time()-time_start_eom} ")

        return eom

    def calculate_hf_moe(self, wf: dict = None, intk: list = None, inten: dict = None, intee: list = None,
                        mocoef: list = None, nprim: int = None, natoms: int = None, ne: int = None,
                        charge: list = None, coord: list = None, dalton_normalization: bool = False,
                        verbose: int = 0):
        """
        Driver to calculate Hartree--Fock molecular orbital energies

        Args:
        ----

        wf (dict): dictionary with information about wave function
        intk (list): 2d array with atomic kinetic integrals
        inten (dict): dictionary of 2d arrays with atomic electron--nucleus interactions integrals
        intk (list): 2d array with atomic electron repulsion integrals
        mocoef (list): 2d array with molecular obital coefficients
        nprim (int): primitive number
        natoms (int): atoms number
        ne (int): electrons number
        charge (list): atomic charges
        coord (list): 2d array with atomic coordinates
        dalton_normalization (bool): Use dalton normalization to d, f, ...
        verbose (int): print level

        Return:
        ------

        eom (list): 1d array with molecular orbitals energies

        NOTE: It's neccesary to pass list arrays to numpy arrays for time
        https://towardsdatascience.com/python-lists-are-sometimes-much-faster-than-numpy-heres-a-proof-4b3dad4653ad
        """

        if not wf and (not intk  or not inten or intee or not mocoef):
            raise ValueError("***Error\n\n\
                It's neccesary the wave function or kinetic, e->-<nucleu interactoin, electron \n\
                repulsion integrals, and molecular orbitals coefficient to calculate molecular\n\
                orbitals energies.")

        if wf and (not intk  or not inten or intee or not mocoef):
            calculate_integrals = eint(wf)
            print("\n\n*** Calculating: kinetic, nucpot and electron repulsion atomic integrals")
            integrals_onebody, symmetries = calculate_integrals.integration_onebody(
                integrals_names = ["kinetic", "nucpot"],
                integrals_properties = None, output = verbose,
                dalton_normalization = dalton_normalization)

            integrals_twobody: list = calculate_integrals.integration_twobody(
                integrals_names = ["e2pot"], output = verbose,
                dalton_normalization = False
            )
            intee = integrals_twobody["e2pot"]

            # Coefficient from fock are in vector form
            mocoef: list = [list(value) for value in zip(*wf.mo_coefficients)]

            if not nprim:
                nprim = wf.primitives_number

            intk: list = integrals_onebody["kinetic"]
            inten: dict = {}
            for name, values in integrals_onebody.items():
                if name != "kinetic":
                    inten[name] = values

            if not charge:
                charge = wf.atomic_numbers
            if not ne:
                ne = sum(charge)
            if not coord:
                coord = wf.coordinates
            if not natoms:
                natoms = len(coord)
            #Verification mocoef would be square

        if not nprim or not ne or not natoms or not charge or not coord:
            raise ValueError("***Error\n\n\
                Information insufficient. It is necesary: primitives or atoms or\n\
                    electrons number or charges or coordinates")

        eom: list = self.run_hf_fock_calculate(intk = intk, inten = inten, intee = intee, mocoef = mocoef,
                    nprim = nprim, natoms = natoms, ne = ne, charge = charge, coord = coord, verbose = verbose)

        return eom

if __name__ == "__main__":
    wfn = wave_function("../tests/molden_file/LiH.molden")

    print("\n Calculate MO energies used wave function \n")
    eom_values = fock()
    eom_values.calculate_hf_moe(wfn, verbose=21)

# H2 STO-1G
#@    Final HF energy:              -0.160779200015
#@    Nuclear repulsion:             0.742994646761
#@    Electronic energy:            -0.903773846776

# H2 HF/STO-2G
#@    Final HF energy:              -1.095728776299
#@    Nuclear repulsion:             0.742994646761
#@    Electronic energy:            -1.838723423060
