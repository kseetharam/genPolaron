import numpy as np
import Grid
import pf_dynamic_sph
import os
import sys
from timeit import default_timer as timer
from copy import copy


if __name__ == "__main__":

    start = timer()

    # ---- INITIALIZE GRIDS ----

    (Lx, Ly, Lz) = (60, 60, 60)
    (dx, dy, dz) = (0.25, 0.25, 0.25)
    higherCutoff = False; cutoffRat = 1.0
    betterResolution = True; resRat = 0.5

    # (Lx, Ly, Lz) = (21, 21, 21)
    # (dx, dy, dz) = (0.375, 0.375, 0.375)
    # higherCutoff = False; cutoffRat = 1.0
    # betterResolution = False; resRat = 1.0

    xgrid = Grid.Grid('CARTESIAN_3D')
    xgrid.initArray('x', -Lx, Lx, dx); xgrid.initArray('y', -Ly, Ly, dy); xgrid.initArray('z', -Lz, Lz, dz)

    NGridPoints_cart = (1 + 2 * Lx / dx) * (1 + 2 * Ly / dy) * (1 + 2 * Lz / dz)
    NGridPoints_desired = (1 + 2 * Lx / dx) * (1 + 2 * Lz / dz)
    Ntheta = 50
    Nk = np.ceil(NGridPoints_desired / Ntheta)

    theta_max = np.pi
    thetaArray, dtheta = np.linspace(0, theta_max, Ntheta, retstep=True)

    # k_max = np.sqrt((np.pi / dx)**2 + (np.pi / dy)**2 + (np.pi / dz)**2)
    k_max = ((2 * np.pi / dx)**3 / (4 * np.pi / 3))**(1 / 3)

    k_min = 1e-5
    kArray, dk = np.linspace(k_min, k_max, Nk, retstep=True)
    if dk < k_min:
        print('k ARRAY GENERATION ERROR')

    kgrid = Grid.Grid("SPHERICAL_2D")

    if higherCutoff is True and betterResolution is False:
        kgrid.initArray('k', k_min, cutoffRat * k_max, dk)
        k_max = kgrid.getArray('k')[-1]
    elif higherCutoff is False and betterResolution is True:
        kgrid.initArray('k', k_min, k_max, resRat * dk)
        dk = kgrid.getArray('k')[1] - kgrid.getArray('k')[0]
    else:
        kgrid.initArray_premade('k', kArray)
    kgrid.initArray_premade('th', thetaArray)

    # for imdyn evolution

    # tMax = 1e5
    tMax = 30
    dt = 10
    CoarseGrainRate = int(1e4)

    tgrid = np.arange(0, tMax + dt, dt)

    gParams = [xgrid, kgrid, tgrid]
    NGridPoints = kgrid.size()

    print('Total time steps: {0}'.format(tgrid.size))
    print('UV cutoff: {0}'.format(k_max))
    print('dk: {0}'.format(dk))
    print('dtheta: {0}'.format(dtheta))
    print('NGridPoints: {0}'.format(NGridPoints))

    # Basic parameters

    mI = 1
    # mI = 10
    mB = 1
    n0 = 1
    gBB = (4 * np.pi / mB) * 0.05

    sParams = [mI, mB, n0, gBB]

    # Toggle parameters

    toggleDict = {'Location': 'work', 'Dynamics': 'imaginary', 'Coupling': 'twophonon', 'Grid': 'spherical', 'Longtime': 'false', 'CoarseGrainRate': CoarseGrainRate}

    # ---- SET PARAMS ----

    mB = 1
    n0 = 1
    gBB = (4 * np.pi / mB) * 0.05  # Dresher uses aBB ~ 0.2 instead of 0.5 here
    # gBB = (4 * np.pi / mB) * 0.02  # Dresher uses aBB ~ 0.2 instead of 0.5 here
    nu = np.sqrt(n0 * gBB / mB)

    aBB = (mB / (4 * np.pi)) * gBB
    xi = (8 * np.pi * n0 * aBB)**(-1 / 2)
    print(k_max * xi)
    print(5 * mB * xi**2)
    print(-3.0 / xi)
    print((n0 * aBB * 3)**(-1 / 2) * mB * xi**2)

    Params_List = []
    mI_Vals = np.array([0.5, 1.0, 2])
    aIBi_Vals = np.array([-15.0, -12.5, -10.0, -9.0, -8.0, -7.0, -5.0, -3.5, -2.0, -1.0, -0.75, -0.5, -0.1])
    P_Vals_norm = np.concatenate((np.linspace(0.1, 0.8, 10, endpoint=False), np.linspace(0.8, 5.0, 40)))
    print(P_Vals_norm)

    for mI in mI_Vals:
        P_Vals = mI * nu * P_Vals_norm
        for aIBi in aIBi_Vals:
            for P in P_Vals:
                sParams = [mI, mB, n0, gBB]
                cParams = [P, aIBi]
                if toggleDict['Location'] == 'home':
                    datapath = '/home/kis/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}'.format(NGridPoints_cart)
                elif toggleDict['Location'] == 'work':
                    datapath = '/media/kis/Storage/Dropbox/VariationalResearch/HarvardOdyssey/genPol_data/NGridPoints_{:.2E}'.format(NGridPoints_cart)
                elif toggleDict['Location'] == 'cluster':
                    datapath = '/n/scratchlfs02/demler_lab/kis/genPol_data/NGridPoints_{:.2E}'.format(NGridPoints_cart)
                if higherCutoff is True:
                    datapath = datapath + '_cutoffRat_{:.2f}'.format(cutoffRat)
                if betterResolution is True:
                    datapath = datapath + '_resRat_{:.2f}'.format(resRat)
                gridpath = copy(datapath)
                datapath = datapath + '/massRatio={:.1f}'.format(mI / mB)
                if toggleDict['Dynamics'] == 'real':
                    innerdatapath = datapath + '/redyn'
                elif toggleDict['Dynamics'] == 'imaginary':
                    innerdatapath = datapath + '/imdyn'
                if toggleDict['Grid'] == 'cartesian':
                    innerdatapath = innerdatapath + '_cart'
                elif toggleDict['Grid'] == 'spherical':
                    innerdatapath = innerdatapath + '_spherical'
                if toggleDict['Coupling'] == 'frohlich':
                    innerdatapath = innerdatapath + '_froh'
                elif toggleDict['Coupling'] == 'twophonon':
                    innerdatapath = innerdatapath
                Params_List.append([sParams, cParams, innerdatapath])

                # if os.path.isdir(gridpath) is False:
                #     os.mkdir(gridpath)
                # if os.path.isdir(datapath) is False:
                #     os.mkdir(datapath)
                # if os.path.isdir(innerdatapath) is False:
                #     os.mkdir(innerdatapath)

    # missedVals = np.concatenate((np.arange(0, 171), np.arange(212, 228), np.array([502, 503, 506, 507, 508])))
    # Params_List = [Params_List[i] for i in missedVals]

    print(len(Params_List))

    # # ---- COMPUTE DATA ON COMPUTER ----

    # runstart = timer()

    # for ind, Params in enumerate(Params_List):
    #     loopstart = timer()
    #     [sParams, cParams, innerdatapath] = Params_List[ind]
    #     [mI, mB, n0, gBB] = sParams
    #     [P, aIBi] = cParams
    #     dyncart_ds = pf_dynamic_cart.quenchDynamics_DataGeneration(cParams, gParams, sParams, toggleDict)
    #     dyncart_ds.to_netcdf(innerdatapath + '/P_{:.3f}_aIBi_{:.2f}.nc'.format(P, aIBi))
    #     loopend = timer()
    #     print('Index: {:d}, P: {:.2f}, aIBi: {:.2f} Time: {:.2f}'.format(ind, P, aIBi, loopend - loopstart))

    # end = timer()
    # print('Total Time: {:.2f}'.format(end - runstart))

    # ---- COMPUTE DATA ON CLUSTER ----

    runstart = timer()

    # taskCount = int(os.getenv('SLURM_ARRAY_TASK_COUNT'))
    # taskID = int(os.getenv('SLURM_ARRAY_TASK_ID'))

    taskCount = len(Params_List)
    taskID = 72

    if(taskCount > len(Params_List)):
        print('ERROR: TASK COUNT MISMATCH')
        P = float('nan')
        aIBi = float('nan')
        sys.exit()
    else:
        [sParams, cParams, innerdatapath] = Params_List[taskID]
        [mI, mB, n0, gBB] = sParams
        [P, aIBi] = cParams

    dynsph_ds = pf_dynamic_sph.quenchDynamics_DataGeneration(cParams, gParams, sParams, toggleDict)
    dynsph_ds.to_netcdf(innerdatapath + '/P_{:.3f}_aIBi_{:.2f}.nc'.format(P, aIBi))

    end = timer()
    print('Task ID: {:d}, mI: {:.1f}, P: {:.2f}, aIBi: {:.2f} Time: {:.2f}'.format(taskID, mI, P, aIBi, end - runstart))
