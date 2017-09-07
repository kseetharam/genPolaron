import numpy as np
from polaron_functions import kcos_func, ksin_func, kpow2_func, FTkernel_func
from scipy.integrate import ode
from copy import copy


class CoherentState:
    # """ This is a class that stores information about coherent state """

    def __init__(self, kgrid, xgrid):

        # last element of self.amplitude_phase is the phase, the rest is the amplitude
        self.amplitude_phase = np.zeros(kgrid.size() + 1, dtype=complex)

        self.time = 0

        self.kgrid = kgrid
        self.dV = self.kgrid.dV()
        self.kcos = kcos_func(kgrid)
        self.ksin = ksin_func(kgrid)
        self.kpow2 = kpow2_func(kgrid)

        self.th = kgrid.function_prod(list(kgrid.arrays.keys()), [lambda k: 0 * k + 1, lambda th: th])

        self.xgrid = xgrid
        self.xmagVals = xgrid.function_prod(list(xgrid.arrays.keys()), [lambda x: x, lambda th: 0 * th + 1])
        self.xthetaVals = xgrid.function_prod(list(xgrid.arrays.keys()), [lambda x: 0 * x + 1, lambda th: th])
        self.dV_x = (2 * np.pi)**3 * self.xgrid.dV()

        # self.PBgrid = PBgrid
        # self.PBmagVals = PBgrid.function_prod(list(PBgrid.arrays.keys()), [lambda PB: PB, lambda th: 0 * th + 1])
        # self.PBthetaVals = PBgrid.function_prod(list(PBgrid.arrays.keys()), [lambda PB: 0 * PB + 1, lambda th: th])
        # self.dV_PB = (2 * np.pi)**3 * self.PBgrid.dV()

        # self.FTkernel_kx = FTkernel_func(kgrid, xgrid, True)
        # # self.FTkernel_xPB = FTkernel_func(xgrid, PBgrid, True)

        self.abs_error = 1.0e-8
        self.rel_error = 1.0e-6

    # EVOLUTION

    def evolve(self, dt, hamiltonian):

        amp_phase0 = copy(self.amplitude_phase)
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
        return np.dot(amplitude * np.conjugate(amplitude), self.dV).real.astype(float)

    def get_PhononMomentum(self):
        amplitude = self.amplitude_phase[0:-1]
        return np.dot(self.kcos, amplitude * np.conjugate(amplitude) * self.dV).real.astype(float)

    def get_DynOverlap(self):
        # dynamical overlap/Ramsey interferometry signal
        NB = self.get_PhononNumber()
        phase = self.amplitude_phase[-1]
        exparg = -1j * phase - (1 / 2) * NB
        return np.exp(exparg)

    def get_MomentumDispersion(self):
        amplitude = self.amplitude_phase[0:-1]
        return np.dot(self.kpow2 * amplitude * np.conjugate(amplitude), self.dV).real.astype(float)

    # POSITION SPACE DEPENDENT OBSERVABLES

    def get_PositionDistribution(self):
        # outputs a vector of values corresponding to x, thetap pairs
        amplitude = self.amplitude_phase[0:-1]
        return (np.abs(np.dot(self.dV * amplitude, self.FTkernel_kx))**2).real.astype(float)

    def get_MomentumDistribution(self, PBgrid):
        amplitude = self.amplitude_phase[0:-1]
        Nph = self.get_PhononNumber()
        FTkernel_xPB = FTkernel_func(self.xgrid, PBgrid, False)
        # G = np.exp(np.dot(self.dV * amplitude * np.conjugate(amplitude), self.FTkernel_kx) - Nph)
        # Ntheta = self.xgrid.arrays['th'].size
        # G0 = G[0:Ntheta - 1]
        MD = np.dot(self.dV_x * np.exp(np.dot(self.dV * amplitude * np.conjugate(amplitude), self.FTkernel_kx) - Nph), FTkernel_xPB)
        return MD.real.astype(float)
