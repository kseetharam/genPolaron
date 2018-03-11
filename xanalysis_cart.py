import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import itertools

if __name__ == "__main__":

    # # Initialization

    # matplotlib.rcParams.update({'font.size': 12, 'text.usetex': True})

    # gParams

    (Lx, Ly, Lz) = (21, 21, 21)
    (dx, dy, dz) = (0.375, 0.375, 0.375)

    # (Lx, Ly, Lz) = (20, 20, 20)
    # (dx, dy, dz) = (0.5, 0.5, 0.5)

    NGridPoints = (1 + 2 * Lx / dx) * (1 + 2 * Ly / dy) * (1 + 2 * Lz / dz)

    datapath = '/home/kis/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}'.format(NGridPoints)
    # datapath = '/media/kis/Storage/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}'.format(NGridPoints)

    innerdatapath = datapath + '/cart'
    # innerdatapath = datapath + '/imdyn_cart'

    figdatapath = datapath + '/figures'

    # # # Concatenate Individual Datasets

    # ds_list = []; P_list = []; aIBi_list = []; mI_list = []
    # for ind, filename in enumerate(os.listdir(innerdatapath)):
    #     if filename == 'quench_Dataset_cart.nc':
    #         continue
    #     print(filename)
    #     ds = xr.open_dataset(innerdatapath + '/' + filename)
    #     ds_list.append(ds)
    #     P_list.append(ds.attrs['P'])
    #     aIBi_list.append(ds.attrs['aIBi'])
    #     mI_list.append(ds.attrs['mI'])

    # s = sorted(zip(aIBi_list, P_list, ds_list))
    # g = itertools.groupby(s, key=lambda x: x[0])

    # aIBi_keys = []; aIBi_groups = []; aIBi_ds_list = []
    # for key, group in g:
    #     aIBi_keys.append(key)
    #     aIBi_groups.append(list(group))

    # for ind, group in enumerate(aIBi_groups):
    #     aIBi = aIBi_keys[ind]
    #     _, P_list_temp, ds_list_temp = zip(*group)
    #     ds_temp = xr.concat(ds_list_temp, pd.Index(P_list_temp, name='P'))
    #     aIBi_ds_list.append(ds_temp)

    # ds_tot = xr.concat(aIBi_ds_list, pd.Index(aIBi_keys, name='aIBi'))
    # del(ds_tot.attrs['P']); del(ds_tot.attrs['aIBi']); del(ds_tot.attrs['nu']); del(ds_tot.attrs['gIB'])
    # ds_tot.to_netcdf(innerdatapath + '/quench_Dataset_cart.nc')

    # # Analysis of Total Dataset

    # qds = xr.open_dataset(innerdatapath + '/quench_Dataset_cart.nc')
    # qds['nPI_mag'].sel(aIBi=-2, P=3, t=99).dropna('PI_mag').plot()
    # qds['nPI_xz_slice'].sel(aIBi=-2, P=3, t=99).dropna('PI_z').plot()
    # plt.show()

    # # nPI xz slice

    # aIBi = -2
    # qds_am2 = qds['nPI_xz_slice'].sel(aIBi=aIBi, t=99)

    # fig1, ax1 = plt.subplots()

    # PVec = qds_am2.coords['P'].values
    # vmin = 1
    # vmax = 0
    # for ind, Pv in enumerate(PVec):
    #     vec = qds_am2.sel(P=Pv).dropna('PI_z').values
    #     if np.min(vec) < vmin:
    #         vmin = np.min(vec)
    #     if np.max(vec) > vmax:
    #         vmax = np.max(vec)

    # # tds0 = qds_am2.isel(P=0).dropna('PI_z')[:-1, :-1]
    # # PI_x_g, PI_z_g = np.meshgrid(tds0['PI_x'].values, tds0['PI_z'].values, indexing='ij')
    # # quad = ax1.pcolormesh(PI_z_g, PI_x_g, tds0.values[:-1, :-1], vmin=vmin, vmax=vmax)

    # quad = qds_am2.isel(P=0).dropna('PI_z')[:-1, :-1].plot.pcolormesh(ax=ax1, vmin=vmin, vmax=vmax, add_colorbar=False, add_labels=False)
    # P_text = ax1.text(0.85, 0.9, 'P: {:.2f}'.format(PVec[0]), transform=ax1.transAxes, color='r')

    # ax1.set_title('Impurity Longitudinal Momentum Distribution ' + r'($a_{IB}^{-1}=$' + '{:.2f})'.format(aIBi))
    # ax1.set_ylabel(r'$P_{I,x}$')
    # ax1.set_xlabel(r'$P_{I,z}$')
    # # ax1.grid(True, linewidth=0.5)
    # ax1.set_xlim([-4, 4])
    # ax1.set_ylim([-4, 4])
    # fig1.colorbar(quad, ax=ax1, extend='both')

    # def animate1(i):
    #     # tds = qds_am2.isel(P=i).dropna('PI_z')[:-1, :-1]
    #     # PI_x_g, PI_z_g = np.meshgrid(tds['PI_x'].values, tds['PI_z'].values, indexing='ij')
    #     # quad.set_array(tds.values.ravel())

    #     qds_am2.isel(P=i).dropna('PI_z')[:-1, :-1].plot.pcolormesh(ax=ax1, vmin=vmin, vmax=vmax, add_colorbar=False, add_labels=False)
    #     ax1.set_xlim([-4, 4])
    #     ax1.set_ylim([-4, 4])
    #     P_text.set_text('P: {:.2f}'.format(PVec[i]))

    # anim1 = FuncAnimation(fig1, animate1, interval=1000, frames=PVec.size, blit=False)
    # # anim1.save(figdatapath + '/nPI_xz_aIBi_{:.2f}.gif'.format(aIBi), writer='imagemagick')
    # plt.show()

    # # nPB xz slice

    # aIBi = -2
    # qds_am2 = qds['nPB_xz_slice'].sel(aIBi=aIBi, t=99)

    # fig1, ax1 = plt.subplots()

    # PVec = qds_am2.coords['P'].values
    # vmin = 1
    # vmax = 0
    # for ind, Pv in enumerate(PVec):
    #     vec = qds_am2.sel(P=Pv).values
    #     if np.min(vec) < vmin:
    #         vmin = np.min(vec)
    #     if np.max(vec) > vmax:
    #         vmax = np.max(vec)

    # quad = qds_am2.isel(P=0)[:-1, :-1].plot.pcolormesh(ax=ax1, vmin=vmin, vmax=vmax, add_colorbar=False, add_labels=False)
    # P_text = ax1.text(0.85, 0.9, 'P: {:.2f}'.format(PVec[0]), transform=ax1.transAxes, color='r')

    # ax1.set_title('Phonon Longitudinal Momentum Distribution ' + r'($a_{IB}^{-1}=$' + '{:.2f})'.format(aIBi))
    # ax1.set_ylabel(r'$P_{B,x}$')
    # ax1.set_xlabel(r'$P_{B,z}$')
    # # ax1.grid(True, linewidth=0.5)
    # ax1.set_xlim([-4, 4])
    # ax1.set_ylim([-4, 4])
    # fig1.colorbar(quad, ax=ax1, extend='both')

    # def animate1(i):
    #     qds_am2.isel(P=i)[:-1, :-1].plot.pcolormesh(ax=ax1, vmin=vmin, vmax=vmax, add_colorbar=False, add_labels=False)
    #     ax1.set_xlim([-4, 4])
    #     ax1.set_ylim([-4, 4])
    #     P_text.set_text('P: {:.2f}'.format(PVec[i]))

    # anim1 = FuncAnimation(fig1, animate1, interval=1000, frames=PVec.size, blit=False)
    # # anim1.save(figdatapath + '/nPI_xz_aIBi_{:.2f}.gif'.format(aIBi), writer='imagemagick')
    # plt.show()

    # # nxyz xz slice

    # aIBi = -2
    # qds_am2 = qds['nxyz_xz_slice'].sel(aIBi=aIBi, t=99)

    # fig1, ax1 = plt.subplots()
    # # np.log(qds['nxyz_xz_slice']).sel(aIBi=-2, P=3, t=99).plot(ax=ax1, vmin=-10, vmax=0)
    # # ax1.set_xlim([-10, 10])
    # # ax1.set_ylim([-10, 10])

    # qds['nxyz_x_slice'].sel(aIBi=-5, P=3, t=99).plot()

    # plt.show()

    # fig1, ax1 = plt.subplots()

    # PVec = qds_am2.coords['P'].values
    # vmin = 1
    # vmax = 0
    # for ind, Pv in enumerate(PVec):
    #     vec = qds_am2.sel(P=Pv).values
    #     if np.min(vec) < vmin:
    #         vmin = np.min(vec)
    #     if np.max(vec) > vmax:
    #         vmax = np.max(vec)

    # quad = qds_am2.isel(P=0)[:-1, :-1].plot.pcolormesh(ax=ax1, vmin=vmin, vmax=vmax, add_colorbar=False, add_labels=False)
    # P_text = ax1.text(0.85, 0.9, 'P: {:.2f}'.format(PVec[0]), transform=ax1.transAxes, color='r')

    # ax1.set_title('Impurity Longitudinal Position Distribution ' + r'($a_{IB}^{-1}=$' + '{:.2f})'.format(aIBi))
    # ax1.set_ylabel(r'$x$')
    # ax1.set_xlabel(r'$z$')
    # # ax1.grid(True, linewidth=0.5)
    # ax1.set_xlim([-2, 2])
    # ax1.set_ylim([-2, 2])
    # fig1.colorbar(quad, ax=ax1, extend='both')

    # def animate1(i):
    #     qds_am2.isel(P=i)[:-1, :-1].plot.pcolormesh(ax=ax1, vmin=vmin, vmax=vmax, add_colorbar=False, add_labels=False)
    #     ax1.set_xlim([-2, 2])
    #     ax1.set_ylim([-2, 2])
    #     P_text.set_text('P: {:.2f}'.format(PVec[i]))

    # anim1 = FuncAnimation(fig1, animate1, interval=1000, frames=PVec.size, blit=False)
    # # anim1.save(figdatapath + '/nxyz_xz_aIBi_{:.2f}.gif'.format(aIBi), writer='imagemagick')
    # plt.show()

    # # MISC

    # ds1 = xr.open_dataset(innerdatapath + '/P_1.000_aIBi_-2.00.nc')
    # ds2 = xr.open_dataset(innerdatapath + '/P_3.000_aIBi_-2.00.nc')
    # ds_tot = xr.concat(objs=[ds1, ds2], dim=pd.Index([2.000, 3.000], name='P'))
    # print(ds_tot['PI_mag'].values)
    # # print(ds_tot['PI_z'])
    # # print(ds1['PI_mag'])
    # # print(ds2['PI_mag'])
    # # print(ds1['PI_z'])
    # # print(ds2['PI_z'])

    # print(ds_tot['nPI_mag'].sel(P=3.000, t=99).values)

    # # ds_tot['nPI_mag'].sel(P=3.000, t=99).dropna('PI_mag').plot()
    # ds_tot['nPI_xz_slice'].isel(P=0, t=-1).dropna('PI_z').plot()
    # # ds_tot['nPI_xy_slice'].sel(P=3, t=99).plot()
    # plt.show()

    # # SUBSONIC TO SUPERSONIC

    qds = xr.open_dataset(innerdatapath + '/quench_Dataset_cart.nc')
    qds_im = xr.open_dataset(datapath + '/imdyn_cart' + '/quench_Dataset_cart.nc')

    nu = 0.792665459521

    # aIBi = -2
    # fig, axes = plt.subplots(nrows=2, ncols=3)
    # # PList = [0.8, 1.2, 1.5, 1.8, 2.1, 2.4]
    # PList = [0.1, 0.8, 1.2, 1.5, 1.8, 2.4]
    # qdsA = qds.sel(aIBi=aIBi)
    # PIm = qdsA.coords['PI_mag'].values

    # for ind, P in enumerate(PList):
    #     if ind == 0:
    #         ax = axes[0, 0]
    #     elif ind == 1:
    #         ax = axes[0, 1]
    #     elif ind == 2:
    #         ax = axes[0, 2]
    #     elif ind == 3:
    #         ax = axes[1, 0]
    #     elif ind == 4:
    #         ax = axes[1, 1]
    #     else:
    #         ax = axes[1, 2]

    #     qdsA['nPI_mag'].sel(P=P, t=99).dropna('PI_mag').plot(ax=ax, label='')
    #     ax.plot(P * np.ones(len(PIm)), np.linspace(0, qdsA['mom_deltapeak'].sel(P=P, t=99).values, len(PIm)), 'g--', label=r'$\delta$-peak')
    #     ax.plot(nu * np.ones(len(PIm)), np.linspace(0, 1, len(PIm)), 'k:', label=r'$m_{I}\nu$')
    #     ax.set_ylim([0, 1])
    #     ax.set_title('$P=${:.2f}'.format(P))
    #     ax.set_xlabel(r'$|P_{I}|$')
    #     ax.set_ylabel(r'$n_{|P_{I}|}$')
    #     ax.legend()

    # plt.show()

    # P = 2.4
    # aIBi = -5
    # fig, axes = plt.subplots()
    # qds['nPI_xz_slice'].sel(P=P, aIBi=aIBi).isel(t=-1).dropna('PI_z').plot(ax=axes)

    # axes.set_title('Impurity Longitudinal Momentum Distribution ' + r'($a_{IB}^{-1}=$' + '{:.2f}'.format(aIBi) + '$P=${:.2f})'.format(P))
    # axes.set_ylabel(r'$P_{I,x}$')
    # axes.set_xlabel(r'$P_{I,z}$')
    # axes.set_xlim([-3, 3])
    # axes.set_ylim([-3, 3])
    # axes.grid(True, linewidth=0.5)
    # plt.show()

    # P = 0.1
    # aIBi = -5
    # fig, axes = plt.subplots()
    # qds['nPB_xz_slice'].sel(P=P, aIBi=aIBi, t=99).dropna('PB_z').plot(ax=axes)

    # axes.set_title('Phonon Longitudinal Momentum Distribution ' + r'($a_{IB}^{-1}=$' + '{:.2f}'.format(aIBi) + '$P=${:.2f})'.format(P))
    # axes.set_ylabel(r'$P_{B,x}$')
    # axes.set_xlabel(r'$P_{B,z}$')
    # axes.set_xlim([-2, 2])
    # axes.set_ylim([-2, 2])
    # axes.grid(True, linewidth=0.5)
    # plt.show()

    aIBi = -5
    P = 2.4
    fig, ax = plt.subplots()
    PIm = qds_im.coords['PI_mag'].values

    print(qds_im['mom_deltapeak'].sel(P=P, aIBi=aIBi).isel(t=-1).values)

    qds_im['nPI_mag'].sel(P=P, aIBi=aIBi).isel(t=-1).dropna('PI_mag').plot(ax=ax, label='idyn')
    ax.plot(P * np.ones(len(PIm)), np.linspace(0, qds_im['mom_deltapeak'].sel(P=P, aIBi=aIBi).isel(t=-1).values, len(PIm)), 'g--', label=r'$\delta$-peak idyn')

    qds['nPI_mag'].sel(P=P, aIBi=aIBi).isel(t=-1).dropna('PI_mag').plot(ax=ax, label='rdyn')
    ax.plot(P * np.ones(len(PIm)), np.linspace(0, qds['mom_deltapeak'].sel(P=P, aIBi=aIBi).isel(t=-1).values, len(PIm)), 'm--', label=r'$\delta$-peak rdyn')

    ax.plot(nu * np.ones(len(PIm)), np.linspace(0, 1, len(PIm)), 'k:', label=r'$m_{I}\nu$')
    ax.set_ylim([0, 1])
    ax.set_title('$P=${:.2f}'.format(P))
    ax.set_xlabel(r'$|P_{I}|$')
    ax.set_ylabel(r'$n_{|P_{I}|}$')
    ax.legend()
    plt.show()
