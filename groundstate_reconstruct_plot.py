import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pf_dynamic_cart as pfc
import Grid
from scipy import interpolate
from timeit import default_timer as timer


if __name__ == "__main__":

    # ---- INITIALIZE GRIDS ----

    # (Lx, Ly, Lz) = (105, 105, 105)
    # (dx, dy, dz) = (0.375, 0.375, 0.375)

    (Lx, Ly, Lz) = (21, 21, 21)
    (dx, dy, dz) = (0.375, 0.375, 0.375)

    NGridPoints_cart = (1 + 2 * Lx / dx) * (1 + 2 * Ly / dy) * (1 + 2 * Lz / dz)

    # Toggle parameters

    toggleDict = {'Location': 'work', 'Dynamics': 'imaginary', 'Interaction': 'on', 'Grid': 'spherical', 'Coupling': 'twophonon'}

    # ---- SET OUTPUT DATA FOLDER ----

    if toggleDict['Location'] == 'home':
        datapath = '/home/kis/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}/massRatio={:.1f}'.format(NGridPoints_cart, 1)
        animpath = '/home/kis/Dropbox/VariationalResearch/DataAnalysis/figs'
    elif toggleDict['Location'] == 'work':
        datapath = '/media/kis/Storage/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}/massRatio={:.1f}'.format(NGridPoints_cart, 1)
        animpath = '/media/kis/Storage/Dropbox/VariationalResearch/DataAnalysis/figs'
    elif toggleDict['Location'] == 'cluster':
        datapath = '/n/regal/demler_lab/kis/genPol_data/NGridPoints_{:.2E}/massRatio={:.1f}'.format(NGridPoints_cart, 1)
        animpath = ''

    if toggleDict['Dynamics'] == 'real':
        innerdatapath = datapath + '/redyn'
        animpath = animpath + '/rdyn'
    elif toggleDict['Dynamics'] == 'imaginary':
        innerdatapath = datapath + '/imdyn'
        animpath = animpath + '/idyn'

    if toggleDict['Grid'] == 'cartesian':
        innerdatapath = innerdatapath + '_cart'
    elif toggleDict['Grid'] == 'spherical':
        innerdatapath = innerdatapath + '_spherical'

    if toggleDict['Coupling'] == 'frohlich':
        innerdatapath = innerdatapath + '_froh'
        animpath = animpath + '_frohlich'
    elif toggleDict['Coupling'] == 'twophonon':
        innerdatapath = innerdatapath
        animpath = animpath + '_twophonon'

    # # Analysis of Total Dataset
    interpdatapath = innerdatapath + '/interp'
    aIBi = -10
    Pnorm_des = 2.0
    # Pnorm_des = 1.0
    # Pnorm_des = 0.1

    linDimList = [(2, 2)]
    linDimMajor, linDimMinor = linDimList[0]

    qds_orig = xr.open_dataset(innerdatapath + '/quench_Dataset_aIBi_{:.2f}.nc'.format(aIBi))
    n0 = qds_orig.attrs['n0']; gBB = qds_orig.attrs['gBB']; mI = qds_orig.attrs['mI']; mB = qds_orig.attrs['mB']
    nu = np.sqrt(n0 * gBB / mB)
    mc = mI * nu
    PVals = qds_orig['P'].values
    Pnorm = PVals / mc
    Pind = np.abs(Pnorm - Pnorm_des).argmin().astype(int)
    P = PVals[Pind]

    # Plot

    interp_ds = xr.open_dataset(interpdatapath + '/InterpDat_P_{:.2f}_aIBi_{:.2f}_lDM_{:.2f}_lDm_{:.2f}.nc'.format(P, aIBi, linDimMajor, linDimMinor))
    kxL = interp_ds['kx'].values
    kzL = interp_ds['kz'].values
    xL = interp_ds['x'].values
    zL = interp_ds['z'].values
    PI_mag = interp_ds['PI_mag'].values
    kxLg_xz_slice, kzLg_xz_slice = np.meshgrid(kxL, kzL, indexing='ij')
    xLg_xz_slice, zLg_xz_slice = np.meshgrid(xL, zL, indexing='ij')
    PhDenLg_xz_slice = interp_ds['PhDen_xz'].values
    np_xz_slice = interp_ds['np_xz'].values
    na_xz_slice = interp_ds['na_xz'].values
    nPI_mag = interp_ds['nPI_mag'].values
    mom_deltapeak = interp_ds.attrs['mom_deltapeak']

    n0 = interp_ds.attrs['n0']
    gBB = interp_ds.attrs['gBB']
    mI = interp_ds.attrs['mI']
    mB = interp_ds.attrs['mB']
    nu = np.sqrt(n0 * gBB / mB)
    mc = mI * nu

    # Interpolate 2D slice of position distribution
    # posmult = 5
    # kzL_xz_slice_interp = np.linspace(np.min(kzL), np.max(kzL), posmult * kzL.size); kxL_xz_slice_interp = np.linspace(np.min(kxL), np.max(kxL), posmult * kxL.size)
    # kxLg_xz_slice_interp, kzLg_xz_slice_interp = np.meshgrid(kxL_xz_slice_interp, kzL_xz_slice_interp, indexing='ij')
    # PhDenLg_xz_slice_interp = interpolate.griddata((kxLg_xz_slice.flatten(), kzLg_xz_slice.flatten()), PhDenLg_xz_slice.flatten(), (kxLg_xz_slice_interp, kzLg_xz_slice_interp), method='cubic')

    # zL_xz_slice_interp = np.linspace(np.min(zL), np.max(zL), posmult * zL.size); xL_xz_slice_interp = np.linspace(np.min(xL), np.max(xL), posmult * xL.size)
    # xLg_xz_slice_interp, zLg_xz_slice_interp = np.meshgrid(xL_xz_slice_interp, zL_xz_slice_interp, indexing='ij')
    # np_xz_slice_interp = interpolate.griddata((xLg_xz_slice.flatten(), zLg_xz_slice.flatten()), np_xz_slice.flatten(), (xLg_xz_slice_interp, zLg_xz_slice_interp), method='cubic')
    # na_xz_slice_interp = interpolate.griddata((xLg_xz_slice.flatten(), zLg_xz_slice.flatten()), na_xz_slice.flatten(), (xLg_xz_slice_interp, zLg_xz_slice_interp), method='cubic')

    # xLg_xz_slice = xLg_xz_slice_interp
    # zLg_xz_slice = zLg_xz_slice_interp
    # np_xz_slice = np_xz_slice_interp
    # na_xz_slice = na_xz_slice_interp

    # print(np.any(np.isnan(PhDenLg_xz_slice_interp)))

    # All Plotting:

    # Individual Phonon Momentum Distribution (Original Spherical data)
    Bk_2D_orig = (qds_orig['Real_CSAmp'] + 1j * qds_orig['Imag_CSAmp']).sel(P=P).isel(t=-1).values
    Nph_orig = qds_orig['Nph'].sel(P=P).isel(t=-1).values
    PhDen_orig_Vals = ((1 / Nph_orig) * np.abs(Bk_2D_orig)**2).real.astype(float)

    kgrid = Grid.Grid("SPHERICAL_2D"); kgrid.initArray_premade('k', qds_orig.coords['k'].values); kgrid.initArray_premade('th', qds_orig.coords['th'].values)
    kVec = kgrid.getArray('k')
    thVec = kgrid.getArray('th')
    kg, thg = np.meshgrid(kVec, thVec, indexing='ij')
    PhDen_orig_da = xr.DataArray(PhDen_orig_Vals, coords=[kVec, thVec], dims=['k', 'th'])

    interpmul = 5
    PhDen_orig_smooth, kg_orig_smooth, thg_orig_smooth = pfc.xinterp2D(PhDen_orig_da, 'k', 'th', interpmul)
    kxg_smooth = kg_orig_smooth * np.sin(thg_orig_smooth)
    kzg_smooth = kg_orig_smooth * np.cos(thg_orig_smooth)

    fig1, ax1 = plt.subplots()
    quad1 = ax1.pcolormesh(kzg_smooth, kxg_smooth, PhDen_orig_smooth, norm=colors.LogNorm(vmin=1e-3, vmax=np.max(PhDenLg_xz_slice)), cmap='inferno')
    quad1m = ax1.pcolormesh(kzg_smooth, -1 * kxg_smooth, PhDen_orig_smooth, norm=colors.LogNorm(vmin=1e-3, vmax=np.max(PhDenLg_xz_slice)), cmap='inferno')
    ax1.set_xlim([-1 * linDimMajor, linDimMajor])
    ax1.set_ylim([-1 * linDimMinor, linDimMinor])
    ax1.set_xlabel('kz (Impurity Propagation Direction)')
    ax1.set_ylabel('kx')
    ax1.set_title('Individual Phonon Momentum Distribution (Orig)')
    fig1.colorbar(quad1, ax=ax1, extend='both')

    # Individual Phonon Momentum Distribution (Interp)
    fig2, ax2 = plt.subplots()
    quad2 = ax2.pcolormesh(kzLg_xz_slice, kxLg_xz_slice, PhDenLg_xz_slice, norm=colors.LogNorm(vmin=1e-3, vmax=np.max(PhDenLg_xz_slice)), cmap='inferno')
    # quad2 = ax2.pcolormesh(kzLg_xz_slice_interp, kxLg_xz_slice_interp, PhDenLg_xz_slice_interp, norm=colors.LogNorm(vmin=1e-3, vmax=np.max(PhDenLg_xz_slice_interp)), cmap='inferno')
    # ax2.set_xlim([-1 * 0.1, 0.1])
    # ax2.set_ylim([-1 * 0.02, 0.02])
    ax2.set_xlabel('kz (Impurity Propagation Direction)')
    ax2.set_ylabel('kx')
    ax2.set_title('Individual Phonon Momentum Distribution (Interp)')
    fig2.colorbar(quad2, ax=ax2, extend='both')

    # Individual Phonon Position Distribution (Interp)
    # fig3, ax3 = plt.subplots()
    # quad3 = ax3.pcolormesh(zLg_xz_slice, xLg_xz_slice, np_xz_slice, norm=colors.LogNorm(vmin=np.abs(np.min(np_xz_slice)), vmax=np.max(np_xz_slice)), cmap='inferno')
    # poslinDim3 = 2300
    # ax3.set_xlim([-1 * poslinDim3, poslinDim3])
    # ax3.set_ylim([-1 * poslinDim3, poslinDim3])
    # # ax3.set_xlim([-800, 800])
    # # ax3.set_ylim([-50, 50])
    # ax3.set_xlabel('z (Impurity Propagation Direction)')
    # ax3.set_ylabel('x')
    # ax3.set_title('Individual Phonon Position Distribution (Interp)')
    # fig3.colorbar(quad3, ax=ax3, extend='both')

    # Bare Atom Position Distribution (Interp)
    # fig4, ax4 = plt.subplots()
    # quad4 = ax4.pcolormesh(zLg_xz_slice, xLg_xz_slice, na_xz_slice, norm=colors.LogNorm(vmin=np.abs(np.min(na_xz_slice)), vmax=np.max(na_xz_slice)), cmap='inferno')
    # poslinDim4 = 1300
    # ax4.set_xlim([-1 * poslinDim4, poslinDim4])
    # ax4.set_ylim([-1 * poslinDim4, poslinDim4])
    # ax4.set_xlabel('z (Impurity Propagation Direction)')
    # ax4.set_ylabel('x')
    # ax4.set_title('Individual Atom Position Distribution (Interp)')
    # fig4.colorbar(quad4, ax=ax4, extend='both')

    # Impurity Momentum Magnitude Distribution (Interp)
    fig5, ax5 = plt.subplots()
    ax5.plot(mc * np.ones(PI_mag.size), np.linspace(0, 1, PI_mag.size), 'y--', label=r'$m_{I}c_{BEC}$')
    curve = ax5.plot(PI_mag, nPI_mag, color='k', lw=3, label='')
    D = nPI_mag - np.max(nPI_mag) / 2
    indices = np.where(D > 0)[0]
    ind_s, ind_f = indices[0], indices[-1]
    FWHMcurve = ax5.plot(np.linspace(PI_mag[ind_s], PI_mag[ind_f], 100), nPI_mag[ind_s] * np.ones(100), 'b-', linewidth=3.0, label='Incoherent Part FWHM')
    FWHMmarkers = ax5.plot(np.linspace(PI_mag[ind_s], PI_mag[ind_f], 2), nPI_mag[ind_s] * np.ones(2), 'bD', mew=0.75, ms=7.5, label='')
    Zline = ax5.plot(P * np.ones(PI_mag.size), np.linspace(0, mom_deltapeak, PI_mag.size), 'r-', linewidth=3.0, label='Delta Peak (Z-factor)')
    Zmarker = ax5.plot(P, mom_deltapeak, 'rx', mew=0.75, ms=7.5, label='')
    dPIm = PI_mag[1] - PI_mag[0]
    nPIm_Tot = np.sum(nPI_mag * dPIm) + mom_deltapeak
    norm_text = ax5.text(0.7, 0.65, r'$\int n_{|\vec{P_{I}}|} d|\vec{P_{I}}| = $' + '{:.2f}'.format(nPIm_Tot), transform=ax5.transAxes, color='k')

    ax5.legend()
    ax5.set_xlim([-0.01, np.max(PI_mag)])
    ax5.set_ylim([0, 1.05])
    ax5.set_title('Impurity Momentum Magnitude Distribution (Interp) (' + r'$aIB^{-1}=$' + '{0}, '.format(aIBi) + r'$\frac{P}{m_{I}c_{BEC}}=$' + '{:.2f})'.format(P / mc))
    ax5.set_ylabel(r'$n_{|\vec{P_{I}}|}$')
    ax5.set_xlabel(r'$|\vec{P_{I}}|$')

    # Impurity Momentum Magnitude Distribution (Original Cartesian data)

    cartdatapath = '/media/kis/Storage/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}/massRatio={:.1f}/imdyn_cart'.format(NGridPoints_cart, 1)
    qds_orig_cart = xr.open_dataset(cartdatapath + '/quench_Dataset_aIBi_{:.2f}.nc'.format(aIBi)).isel(t=-1)

    qds_nPIm_inf = qds_orig_cart['nPI_mag'].sel(P=P, method='nearest').dropna('PI_mag')
    P_cart = qds_nPIm_inf.coords['P'].values
    PI_mag_cart = qds_nPIm_inf.coords['PI_mag'].values
    nPI_mag_cart = qds_nPIm_inf.values
    mom_deltapeak_cart = qds_orig_cart.sel(P=P_cart)['mom_deltapeak'].values

    fig6, ax6 = plt.subplots()
    ax6.plot(mc * np.ones(PI_mag_cart.size), np.linspace(0, 1, PI_mag_cart.size), 'y--', label=r'$m_{I}c_{BEC}$')
    curve = ax6.plot(PI_mag_cart, nPI_mag_cart, color='k', lw=3, label='')
    D = nPI_mag_cart - np.max(nPI_mag_cart) / 2
    indices = np.where(D > 0)[0]
    ind_s, ind_f = indices[0], indices[-1]
    FWHMcurve = ax6.plot(np.linspace(PI_mag_cart[ind_s], PI_mag_cart[ind_f], 100), nPI_mag_cart[ind_s] * np.ones(100), 'b-', linewidth=3.0, label='Incoherent Part FWHM')
    FWHMmarkers = ax6.plot(np.linspace(PI_mag_cart[ind_s], PI_mag_cart[ind_f], 2), nPI_mag_cart[ind_s] * np.ones(2), 'bD', mew=0.75, ms=7.5, label='')
    Zline = ax6.plot(P_cart * np.ones(PI_mag_cart.size), np.linspace(0, mom_deltapeak_cart, PI_mag_cart.size), 'r-', linewidth=3.0, label='Delta Peak (Z-factor)')
    Zmarker = ax6.plot(P_cart, mom_deltapeak_cart, 'rx', mew=0.75, ms=7.5, label='')
    dPIm_cart = PI_mag_cart[1] - PI_mag_cart[0]
    nPIm_Tot = np.sum(nPI_mag_cart * dPIm_cart) + mom_deltapeak_cart
    norm_text = ax6.text(0.7, 0.65, r'$\int n_{|\vec{P_{I}}|} d|\vec{P_{I}}| = $' + '{:.2f}'.format(nPIm_Tot), transform=ax6.transAxes, color='k')

    ax6.legend()
    ax6.set_xlim([-0.01, np.max(PI_mag)])
    ax6.set_ylim([0, 1.05])
    ax6.set_title('Impurity Momentum Magnitude Distribution (Cart) (' + r'$aIB^{-1}=$' + '{0}, '.format(aIBi) + r'$\frac{P}{m_{I}c_{BEC}}=$' + '{:.2f})'.format(P_cart / mc))
    ax6.set_ylabel(r'$n_{|\vec{P_{I}}|}$')
    ax6.set_xlabel(r'$|\vec{P_{I}}|$')

    plt.show()
