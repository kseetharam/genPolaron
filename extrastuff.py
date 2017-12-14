    # SPLIT SPLINE INTERPOLATION

    # PB_mask = PB_unique < nuV
    # PI_mask = PI_unique < nuV

    # PB_unique_S = PB_unique[PB_mask]
    # PB_unique_L = PB_unique[np.logical_not(PB_mask)]
    # nPBm_cum_S = nPBm_cum[PB_mask]
    # nPBm_cum_L = nPBm_cum[np.logical_not(PB_mask)]

    # PI_unique_S = PI_unique[PI_mask]
    # PI_unique_L = PI_unique[np.logical_not(PI_mask)]
    # nPIm_cum_S = nPIm_cum[PI_mask]
    # nPIm_cum_L = nPIm_cum[np.logical_not(PI_mask)]

    # nPBm_tck_S = interpolate.splrep(PB_unique_S, nPBm_cum_S, k=3, s=1)
    # nPBm_tck_L = interpolate.splrep(PB_unique_L, nPBm_cum_L, k=3, s=1)

    # nPIm_tck_S = interpolate.splrep(PI_unique_S, nPIm_cum_S, k=3, s=1)
    # nPIm_tck_L = interpolate.splrep(PI_unique_L, nPIm_cum_L, k=3, s=1)

    # PBm_Vec_S = np.linspace(0, nuV, 50, endpoint=False)
    # PBm_Vec_L = np.linspace(nuV, np.max(PB_unique), 50)
    # PIm_Vec_S = np.linspace(0, nuV, 50, endpoint=False)
    # PIm_Vec_L = np.linspace(nuV, np.max(PI_unique), 50)

    # nPBm_cum_Vec_S = interpolate.splev(PBm_Vec_S, nPBm_tck_S, der=0)
    # nPBm_cum_Vec_L = interpolate.splev(PBm_Vec_L, nPBm_tck_L, der=0)
    # nPIm_cum_Vec_S = interpolate.splev(PIm_Vec_S, nPIm_tck_S, der=0)
    # nPIm_cum_Vec_L = interpolate.splev(PIm_Vec_L, nPIm_tck_L, der=0)

    # nPBm_Vec_S = interpolate.splev(PBm_Vec_S, nPBm_tck_S, der=1)
    # nPBm_Vec_L = interpolate.splev(PBm_Vec_L, nPBm_tck_L, der=1)
    # nPIm_Vec_S = interpolate.splev(PIm_Vec_S, nPIm_tck_S, der=1)
    # nPIm_Vec_L = interpolate.splev(PIm_Vec_L, nPIm_tck_L, der=1)

    # PBm_Vec = np.concatenate((PBm_Vec_S, PBm_Vec_L))
    # PIm_Vec = np.concatenate((PIm_Vec_S, PIm_Vec_L))
    # nPBm_cum_Vec = np.concatenate((nPBm_cum_Vec_S, nPBm_cum_Vec_L))
    # nPIm_cum_Vec = np.concatenate((nPIm_cum_Vec_S, nPIm_cum_Vec_L))
    # nPBm_Vec = np.concatenate((nPBm_Vec_S, nPBm_Vec_L))
    # nPIm_Vec = np.concatenate((nPIm_Vec_S, nPIm_Vec_L))

    # dPBm_L = PBm_Vec[-1] - PBm_Vec[-2]
    # dPIm_L = PIm_Vec[-1] - PIm_Vec[-2]
    # nPBm_Tot = np.dot(nPBm_Vec, np.ediff1d(nPBm_Vec, to_end=dPBm_L)) + nPB_deltaK0
    # nPIm_Tot = np.dot(nPIm_Vec, np.ediff1d(nPIm_Vec, to_end=dPIm_L)) + nPB_deltaK0

    # PBm_max = PBm_Vec[np.argmax(nPBm_Vec)]
    # PIm_max = PIm_Vec[np.argmax(nPIm_Vec)]

    ####

    # ax[2, 0].plot(PB_unique, nPBm_unique, 'k*')
    # # ax[2, 0].plot(np.zeros(PB_unique.size), np.linspace(0, nPB_deltaK0, PB_unique.size))
    # ax[2, 0].set_title(r'$n_{\vec{P_B}}$')
    # ax[2, 0].set_xlabel(r'$|P_{B}|$')

    # ax[2, 1].plot(PI_unique, nPIm_unique, 'k*')
    # # ax[2, 1].plot(P * np.ones(PI_unique.size), np.linspace(0, nPB_deltaK0, PI_unique.size))
    # ax[2, 1].set_title(r'$n_{\vec{P_I}}$')
    # ax[2, 1].set_xlabel(r'$|P_{I}|$')

    # ax[2, 2].plot(PBm_Vec, nPBm_Vec)
    # ax[2, 2].set_title(r'$n_{\vec{P_B}}$')
    # ax[2, 2].set_xlabel(r'$|P_{B}|$')
    # ax[2, 2].plot(np.zeros(PB_unique.size), np.linspace(0, nPB_deltaK0, PB_unique.size))

    # ax[3, 2].plot(PIm_Vec, nPIm_Vec)
    # ax[3, 2].set_title(r'$n_{\vec{P_I}}$')
    # ax[3, 2].set_xlabel(r'$|P_{I}|$')
    # ax[3, 2].plot(P * np.ones(PI_unique.size), np.linspace(0, nPB_deltaK0, PI_unique.size))

    # ax[3, 0].plot(PB_unique, nPBm_cum, 'k*')
    # ax[3, 0].set_title('Cumulative Distribution Function')
    # ax[3, 0].set_xlabel(r'$|P_{B}|$')
    # ax[3, 0].plot(PBm_Vec, nPBm_cum_Vec, 'r-')

    # ax[3, 1].plot(PI_unique, nPIm_cum, 'k*')
    # ax[3, 1].set_title('Cumulative Distribution Function')
    # ax[3, 1].set_xlabel(r'$|P_{I}|$')
    # ax[3, 1].plot(PIm_Vec, nPIm_cum_Vec, 'r-')