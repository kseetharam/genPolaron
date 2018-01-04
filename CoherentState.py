import numpy as np
from pf_spherical import kcos_func, ksin_func, kpow2_func
from scipy.integrate import ode
from copy import copy


class CoherentState:
    # """ This is a class that stores information about coherent state """

    def __init__(self, kgrid, xgrid):

        # last element of self.amplitude_phase is the phase, the rest is the amplitude
        self.amplitude_phase = np.zeros(kgrid.size() + 1, dtype=complex)
        self.time = 0

        self.kgrid = kgrid
        self.xgrid = xgrid
        # self.kFgrid = Grid.Grid('CARTESIAN_3D')  # useful for Fourier transforms when calculating distribution functions
        # self.kFgrid.initArray_premade('kx', np.fft.ifftshift(kgrid.getArray('kx'))); self.kFgrid.initArray_premade('ky', np.fft.ifftshift(kgrid.getArray('ky'))); self.kFgrid.initArray_premade('kz', np.fft.ifftshift(kgrid.getArray('kz')))

        self.coordinate_system = kgrid.coordinate_system
        if(kgrid.coordinate_system != xgrid.coordinate_system):
            print('ERROR: GRID COORDINATE SYSTEM MISTMATCH')

        # precompute quantities to make observable calculations computationally cheaper
        self.dVk = self.kgrid.dV()

        if(self.coordinate_system == "SPHERICAL_2D"):
            self.kzg_flat = kcos_func(kgrid)
            self.ksin = ksin_func(kgrid)
            self.kpow2 = kpow2_func(kgrid)
            self.dVk_prefac = 1
        if(self.coordinate_system == "CARTESIAN_3D"):
            self.xg, self.yg, self.zg = np.meshgrid(self.xgrid.getArray('x'), self.xgrid.getArray('y'), self.xgrid.getArray('z'), indexing='ij')
            self.kxg, self.kyg, self.kzg = np.meshgrid(self.kgrid.getArray('kx'), self.kgrid.getArray('ky'), self.kgrid.getArray('kz'), indexing='ij')
            # self.kxFg, self.kyFg, self.kzFg = np.meshgrid(self.kFgrid.getArray('kx'), self.kFgrid.getArray('ky'), self.kFgrid.getArray('kz'), indexing='ij', sparse=True)
            self.Nx, self.Ny, self.Nz = len(self.xgrid.getArray('x')), len(self.xgrid.getArray('y')), len(self.xgrid.getArray('z'))
            self.kzg_flat = self.kzg.reshape(self.kzg.size)
            self.dVk_const = self.dVk[0]
            self.dVk_prefac = (2 * np.pi)**(-3)

        # error for ODE solver
        self.abs_error = 1.0e-8
        self.rel_error = 1.0e-6

#  # THIS WAS FOR DISTRIBUTION FUNCTION ATTEMPT IN SPHERICAL COORDINATES -- DEPRACATED
        # self.th = kgrid.function_prod(list(kgrid.arrays.keys()), [lambda k: 0 * k + 1, lambda th: th])
        # self.xgrid = xgrid
        # self.xmagVals = xgrid.function_prod(list(xgrid.arrays.keys()), [lambda x: x, lambda th: 0 * th + 1])
        # self.xthetaVals = xgrid.function_prod(list(xgrid.arrays.keys()), [lambda x: 0 * x + 1, lambda th: th])
        # self.dV_x = (2 * np.pi)**3 * self.xgrid.dV()

        # self.PBgrid = PBgrid
        # self.PBmagVals = PBgrid.function_prod(list(PBgrid.arrays.keys()), [lambda PB: PB, lambda th: 0 * th + 1])
        # self.PBthetaVals = PBgrid.function_prod(list(PBgrid.arrays.keys()), [lambda PB: 0 * PB + 1, lambda th: th])
        # self.dV_PB = (2 * np.pi)**3 * self.PBgrid.dV()

        # self.FTkernel_kx = FTkernel_func(kgrid, xgrid, True)
        # # self.FTkernel_xPB = FTkernel_func(xgrid, PBgrid, True)

    # EVOLUTION

    def evolve(self, dt, hamiltonian):

        amp_phase0 = copy(self.amplitude_phase)
        print('Beta_k contains NaNs: {0}'.format(np.any(np.isnan(amp_phase0))))
        t0 = copy(self.time)
        amp_solver = ode(hamiltonian.update).set_integrator('zvode', method='bdf', atol=self.abs_error, rtol=self.rel_error, nsteps=100000)
        amp_solver.set_initial_value(amp_phase0, t0).set_f_params(self)
        self.amplitude_phase = amp_solver.integrate(amp_solver.t + dt)
        self.time = self.time + dt

    # CHARACTERISTICS

    def get_Amplitude(self):
        return self.amplitude_phase[0:-1]

    def get_Phase(self):
        return self.amplitude_phase[-1].real.astype(float)

    # PURELY MOMENTUM SPACE DEPENDENT OBSERVABLES

    def get_PhononNumber(self):
        amplitude = self.amplitude_phase[0:-1]
        return np.dot(amplitude * np.conjugate(amplitude), self.dVk_prefac * self.dVk).real.astype(float)

    def get_PhononMomentum(self):
        amplitude = self.amplitude_phase[0:-1]
        return np.dot(self.kzg_flat * amplitude * np.conjugate(amplitude), self.dVk_prefac * self.dVk).real.astype(float)

    def get_DynOverlap(self):
        # dynamical overlap/Ramsey interferometry signal
        NB = self.get_PhononNumber()
        phase = self.amplitude_phase[-1]
        exparg = -1j * phase - (1 / 2) * NB
        return np.exp(exparg)

    # def get_MomentumDispersion(self):
    #     amplitude = self.amplitude_phase[0:-1]
    #     return np.dot(self.kpow2 * amplitude * np.conjugate(amplitude), self.dVk).real.astype(float)

    # POSITION SPACE DEPENDENT OBSERVABLES

    def get_PhononDistributions(self):
        amplitude = self.amplitude_phase[0:-1]  # this is flattened and stored w.r.t. kgrid

        if self.coordinate_system != "CARTESIAN_3D":
            print('INVALID COORDINATE SYSTEM')
            return -1

        # generation

        prefactor = (2 * np.pi)**(-3 / 2)
        beta_kxkykz = prefactor * np.fft.ifftshift(amplitude.reshape((self.Nx, self.Ny, self.Nz)))  # unflatten Beta_k, reorder w.r.t. kF grid, and multiply be prefactor such that Beta_k -> Beta_~_k
        beta2_kxkykz = np.abs(beta_kxkykz)**2
        decay_length = 5
        decay_xyz = np.exp(-1 * (self.xg**2 + self.yg**2 + self.zg**2) / (2 * decay_length**2))

        # Calculate Nph
        Nph = self.get_PhononNumber()
        # Nph = np.real(np.sum(beta2_kxkykz) * dkx * dky * dkz)

        # Fourier transform
        amp_beta_xyz_preshift = np.fft.fftn(np.sqrt(beta2_kxkykz))
        amp_beta_xyz = np.fft.fftshift(amp_beta_xyz_preshift) * self.dVk_const
        nxyz = np.abs(amp_beta_xyz * (2 * np.pi)**(-3 / 2))**2  # this is the phonon position density distribution -> integrates to Nph
        nxyz_norm = nxyz / Nph  # this is the phonon position density distribution -> integrates to Nph

        # Fourier transform
        beta2_xyz_preshift = np.fft.fftn(beta2_kxkykz)
        beta2_xyz = np.fft.fftshift(beta2_xyz_preshift) * self.dVk_const

        # Exponentiate
        fexp = (np.exp(beta2_xyz - Nph) - np.exp(-Nph)) * decay_xyz

        # Inverse Fourier transform
        nPB_preshift = np.fft.ifftn(fexp) * 1 / (self.dVk_const)
        nPB = np.fft.fftshift(nPB_preshift)
        nPB_deltaK0 = np.exp(-Nph)

        phonon_pos_dist = nxyz_norm  # this is a 3D matrix in terms of x,y,z
        phonon_mom_dist = nPB  # this is a 3D matrix in terms of kx, ky, kz -> more accurately PB_x, PB_y, PB_z
        phonon_mom_k0deltapeak = nPB_deltaK0  # this is the weight of the delta peak in nPB at kx=ky=kz=0

        return phonon_pos_dist, phonon_mom_dist, phonon_mom_k0deltapeak


#  # THIS WAS FOR DISTRIBUTION FUNCTION ATTEMPT IN SPHERICAL COORDINATES -- DEPRACATED
    # def get_PositionDistribution(self):
    #     # outputs a vector of values corresponding to x, thetap pairs
    #     amplitude = self.amplitude_phase[0:-1]
    #     return (np.abs(np.dot(self.dV * amplitude, self.FTkernel_kx))**2).real.astype(float)

    # def get_MomentumDistribution(self, PBgrid):
    #     amplitude = self.amplitude_phase[0:-1]
    #     Nph = self.get_PhononNumber()
    #     FTkernel_xPB = FTkernel_func(self.xgrid, PBgrid, False)
    #     # G = np.exp(np.dot(self.dV * amplitude * np.conjugate(amplitude), self.FTkernel_kx) - Nph)
    #     # Ntheta = self.xgrid.arrays['th'].size
    #     # G0 = G[0:Ntheta - 1]
    #     MD = np.dot(self.dV_x * np.exp(np.dot(self.dV * amplitude * np.conjugate(amplitude), self.FTkernel_kx) - Nph), FTkernel_xPB)
    #     return MD.real.astype(float)
