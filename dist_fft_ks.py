import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from timeit import default_timer as timer
from polaron_functions_cart import *
import Grid
import polrabi.staticfm as fm


matplotlib.rcParams.update({'font.size': 12, 'text.usetex': True})


def staticDistCalc(gridargs, params, datapath):
    [xgrid, kgrid, kFgrid] = gridargs
    [P, aIBi, aSi, DP, mI, mB, n0, gBB] = params
    bparams = [aIBi, aSi, DP, mI, mB, n0, gBB]

    # unpack grid args
    x = xgrid.getArray('x'); y = xgrid.getArray('y'); z = xgrid.getArray('z')
    (Nx, Ny, Nz) = (len(x), len(y), len(z))
    dx = xgrid.arrays_diff['x']; dy = xgrid.arrays_diff['y']; dz = xgrid.arrays_diff['z']

    kxF = kFgrid.getArray('kx'); kyF = kFgrid.getArray('ky'); kzF = kFgrid.getArray('kz')

    kx = kgrid.getArray('kx'); ky = kgrid.getArray('ky'); kz = kgrid.getArray('kz')
    dkx = kgrid.arrays_diff['kx']; dky = kgrid.arrays_diff['ky']; dkz = kgrid.arrays_diff['kz']

    # generation
    xg, yg, zg = np.meshgrid(x, y, z, indexing='ij', sparse=True)
    kxFg, kyFg, kzFg = np.meshgrid(kxF, kyF, kzF, indexing='ij', sparse=True)

    beta2_kxkykz = np.abs(BetaK(kxFg, kyFg, kzFg, *bparams))**2
    mask = np.isnan(beta2_kxkykz); beta2_kxkykz[mask] = 0

    decay_length = 5
    decay_xyz = np.exp(-1 * (xg**2 + yg**2 + zg**2) / (2 * decay_length**2))

    # Fourier transform and slice
    amp_beta_xyz_0 = np.fft.fftn(np.sqrt(beta2_kxkykz))
    amp_beta_xyz = np.fft.fftshift(amp_beta_xyz_0) * dkx * dky * dkz

    # Calculate Nph
    Nph = np.real(np.sum(beta2_kxkykz) * dkx * dky * dkz)
    Nph_x = np.real(np.sum(np.abs(amp_beta_xyz)**2) * dx * dy * dz * (2 * np.pi)**(-3))

    # Fourier transform and slice
    beta2_xyz_preshift = np.fft.fftn(beta2_kxkykz)
    beta2_xyz = np.fft.fftshift(beta2_xyz_preshift) * dkx * dky * dkz
    beta2_z = beta2_xyz[Nx // 2 + 1, Ny // 2 + 1, :]

    # Exponentiate, slice
    fexp = (np.exp(beta2_xyz - Nph) - np.exp(-Nph)) * decay_xyz
    # fexp = np.exp(beta2_xyz - Nph) - np.exp(-Nph)
    fexp_z = fexp[Nx // 2 + 1, Ny // 2 + 1, :]

    # Inverse Fourier transform
    nPB_preshift = np.fft.ifftn(fexp) * 1 / (dkx * dky * dkz)
    nPB = np.fft.fftshift(nPB_preshift)
    nPB_deltaK0 = np.exp(-Nph)

    # Integrating out y and z

    beta2_kz = np.sum(np.abs(beta2_kxkykz), axis=(0, 1)) * dkx * dky
    nPB_kx = np.sum(np.abs(nPB), axis=(1, 2)) * dky * dkz
    nPB_ky = np.sum(np.abs(nPB), axis=(0, 2)) * dkx * dkz
    nPB_kz = np.sum(np.abs(nPB), axis=(0, 1)) * dkx * dky
    nx_x = np.sum(np.abs(amp_beta_xyz)**2, axis=(1, 2)) * dy * dz
    nx_y = np.sum(np.abs(amp_beta_xyz)**2, axis=(0, 2)) * dx * dz
    nx_z = np.sum(np.abs(amp_beta_xyz)**2, axis=(0, 1)) * dx * dy
    nx_x_norm = np.real(nx_x / Nph_x); nx_y_norm = np.real(nx_y / Nph_x); nx_z_norm = np.real(nx_z / Nph_x)

    nPB_Tot = np.sum(np.abs(nPB) * dkx * dky * dkz) + nPB_deltaK0
    nPB_Mom1 = np.dot(np.abs(nPB_kz), kz * dkz)
    beta2_kz_Mom1 = np.dot(np.abs(beta2_kz), kzF * dkz)

    # beta2_kz_Mom1_2 = np.sum(np.abs(beta2_kxkykz) * kzFg) * dkx * dky * dkz
    # print(beta2_kz_Mom1_2)

    print("Nph = \sum b^2 = %f" % (Nph))
    print("Nph_x = %f " % (Nph_x))
    print("\int np dp = %f" % (nPB_Tot))
    print("\int p np dp = %f" % (nPB_Mom1))
    print("\int k beta^2 dk = %f" % (beta2_kz_Mom1))

    print("Exp[-Nph] = %f" % (nPB_deltaK0))

    # Save data
    Dist_data = np.concatenate((DP * np.ones(Nz)[:, np.newaxis], Nph * np.ones(Nz)[:, np.newaxis], Nph_x * np.ones(Nz)[:, np.newaxis], nPB_Tot * np.ones(Nz)[:, np.newaxis], nPB_Mom1 * np.ones(Nz)[:, np.newaxis], beta2_kz_Mom1 * np.ones(Nz)[:, np.newaxis], x[:, np.newaxis], y[:, np.newaxis], z[:, np.newaxis], nx_x_norm[:, np.newaxis], nx_y_norm[:, np.newaxis], nx_z_norm[:, np.newaxis], kx[:, np.newaxis], ky[:, np.newaxis], kz[:, np.newaxis], np.real(nPB_kx)[:, np.newaxis], np.real(nPB_ky)[:, np.newaxis], np.real(nPB_kz)[:, np.newaxis]), axis=1)
    np.savetxt(datapath + '/3Ddist_aIBi_{:.2f}_P_{:.2f}.dat'.format(aIBi, P), Dist_data)

    # Plot
    # fig, ax = plt.subplots(nrows=1, ncols=5)

    # ax[0].plot(kzF, np.abs(beta2_kz))
    # ax[0].set_title(r'$|\beta_{\vec{k}}|^2$')
    # ax[0].set_xlabel(r'$k_{z}$')

    # ax[1].plot(x, np.real(beta2_z))
    # ax[2].plot(x, np.abs(fexp_z))

    # ax[3].plot(kx, np.real(nPB_kz))
    # ax[3].plot(np.zeros(Nz), np.linspace(0, nPB_deltaK0, Nz))
    # ax[3].set_title(r'$n_{\vec{P_B}}$')
    # ax[3].set_xlabel(r'$P_{B,z}$')

    # ax[4].plot(x, np.real(nx_z_norm))
    # ax[4].set_title(r'$\frac{n(\vec{x})}{N_{ph}}$')
    # ax[4].set_xlabel(r'$z$')

    # fig.tight_layout()
    # plt.show()


# Create grids

start = timer()

(Lx, Ly, Lz) = (15, 15, 15)
(dx, dy, dz) = (1e-01, 1e-01, 1e-01)

xgrid = Grid.Grid('CARTESIAN_3D')
xgrid.initArray('x', -Lx, Lx, dx); xgrid.initArray('y', -Ly, Ly, dy); xgrid.initArray('z', -Lz, Lz, dz)

(Nx, Ny, Nz) = (len(xgrid.getArray('x')), len(xgrid.getArray('y')), len(xgrid.getArray('z')))

kxfft = np.fft.fftfreq(Nx) * 2 * np.pi / dx; kyfft = np.fft.fftfreq(Nx) * 2 * np.pi / dy; kzfft = np.fft.fftfreq(Nx) * 2 * np.pi / dz
kFgrid = Grid.Grid('CARTESIAN_3D')
kFgrid.initArray_premade('kx', kxfft); kFgrid.initArray_premade('ky', kyfft); kFgrid.initArray_premade('kz', kzfft)

kgrid = Grid.Grid('CARTESIAN_3D')
kgrid.initArray_premade('kx', np.fft.fftshift(kxfft)); kgrid.initArray_premade('ky', np.fft.fftshift(kyfft)); kgrid.initArray_premade('kz', np.fft.fftshift(kzfft))

gridargs = [xgrid, kgrid, kFgrid]

# precalculate for stuff below

kxFg, kyFg, kzFg = np.meshgrid(kFgrid.getArray('kx'), kFgrid.getArray('ky'), kFgrid.getArray('kz'), indexing='ij', sparse=True)
dVk = kgrid.arrays_diff['kx'] * kgrid.arrays_diff['ky'] * kgrid.arrays_diff['kz']


# Basic parameters
mI = 1
mB = 1
n0 = 1
gBB = (4 * np.pi / mB) * 0.05
nuV = nu(gBB)

datapath = os.path.dirname(os.path.realpath(__file__)) + '/fftdata'

# # INTERPOLATION

# Nsteps = 1e2
# createSpline_grid(Nsteps, kxFg, kyFg, kzFg, dVk, mI, mB, n0, gBB)

aSi_tck = np.load('aSi_spline.npy')
PBint_tck = np.load('PBint_spline.npy')

# Single function run

# P = 0.9 * nuV
# aIBi = -2

# Pc = PCrit_grid(kxFg, kyFg, kzFg, dVk, aIBi, mI, mB, n0, gBB)
# DP = DP_interp(0, P, aIBi, aSi_tck, PBint_tck)
# aSi = aSi_interp(DP, aSi_tck)

# params = [P, aIBi, aSi, DP, mI, mB, n0, gBB]
# print('DP: {0}'.format(DP))
# print('aSi: {0}, aSi_fm: {1}'.format(aSi, fm.aSi(DP, gBB, mI, mB, n0)))
# print('Pc: {0}, Pc_fm: {1}'.format(Pc, fm.PCrit(aIBi, gBB, mI, mB, n0)))

# staticDistCalc(gridargs, params, datapath)

# Multiple function run

paramsList = []
aIBi_Vals = [-5, -2, -1, 1, 2, 5]
Pc = PCrit_grid(kxFg, kyFg, kzFg, dVk, np.amin(aIBi_Vals), mI, mB, n0, gBB)
print('PCrit: {0}'.format(Pc))
PVals = np.linspace(0, 0.95 * Pc, 6)
for aIBi in aIBi_Vals:
    for P in PVals:
        DP = DP_interp(0, P, aIBi, aSi_tck, PBint_tck)
        aSi = aSi_interp(DP, aSi_tck)
        paramsList.append([P, aIBi, aSi, DP, mI, mB, n0, gBB])


for p in paramsList:
    staticDistCalc(gridargs, p, datapath)


end = timer()
print(end - start)
