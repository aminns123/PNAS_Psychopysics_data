"""Function definitions extracted from supplied code; source lines in provenance.
No top-level analysis scripts are executed. Numerical bodies are preserved.
"""
import numpy as np
from numpy import real
from math import factorial
from itertools import combinations

# LIB001 source lines 7151-7182
def convert_wavenumber_parameters_to_frequency(params):
    """
    Rescale spatial coefficients for k = 2*pi*f while preserving
    every total coupling W = w_local + 2*w_lateral.
    """
    params = np.asarray(params, dtype=float).copy()
    q = (2.0 * np.pi)**2

    # (local index, lateral index)
    pairs = [
        (0, 4),  # wEE, wEe
        (1, 5),  # wEI, wEi
        (2, 6),  # wIE, wIe
        (3, 7),  # wII, wIi
    ]

    for local_index, lateral_index in pairs:
        local_old = params[local_index]
        lateral_old = params[lateral_index]

        lateral_new = lateral_old / q
        local_new = (
            local_old
            + 2.0*lateral_old
            - 2.0*lateral_new
        )

        params[local_index] = local_new
        params[lateral_index] = lateral_new

    # alpha, rI0 and rE0 remain unchanged.
    return params

# LIB001 source lines 7184-7257
def model_EI_kn(x, x0, x1, x2, x3, x4,x5,x6,x7,x8,x9,x10):#,x11, x12):
    
    scale   = 1.0
    offset  = 100 
    
    X       = scale*np.log10(x+offset)


    #wEE,wEI,wIE,wII = 0.6, 5., 7.2, 6.
    #wEe,wEi,wIe,wIi = 3.4, 6.4, 1.4, 1.0,
    
    #params          = [x0, x1, x2, x3, x4,x5,x6,x7,x8,x9,x10]
    #converted_parms = convert_wavenumber_parameters_to_frequency(params)
    #x0, x1, x2, x3, x4,x5,x6,x7,x8,x9,x10 = converted_parms
    
    
    wEE       = x0
    wEI       = x1
    wIE       = x2
    wII       = x3
    
    wEe       = x4
    wEi       = x5
    wIe       = x6
    wIi       = x7
   
    alpha     = x8
    rI0       = x9
    rE0       = x10

    
    WEE, WEI, WII, WIE = wEE + 2*wEe,  wEI + 2*wEi, wII + 2*wIi, wIE + 2*wIe
    DEE, DEI, DII, DIE = wEe, wEi, wIi, wIe
    
    
    iE0 = alpha*X
    iI0 = (1-alpha)*X

    X0 = rE0*WEE-rI0*WEI+iE0
    Y0 = rE0*WIE-rI0*WII+iI0


    rE0  = np.tanh(X0)
    rI0  = np.tanh(Y0)
    
    RE0 = 1/(1-pow(rE0,2))
    RI0 = 1/(1-pow(rI0,2))
    
    A0=RE0-WEE
    D0=RI0+WII
    
    #print('a = (DIE*DEI-(DEE*DII))                  : ',(DIE*DEI-(DEE*DII)))
    #print('b = (DEE*D0-(DII*A0)-(DIE*WEI)-(DEI*WIE)): ',(DEE*D0-(DII*A0)-(DIE*WEI)-(DEI*WIE)))
    #print('c = (A0*D0+WIE*WEI)                      : ',(A0*D0+WIE*WEI))
    
    a = np.array([DIE*DEI-(DEE*DII)])
    b = np.array(DEE*D0-(DII*A0)-(DIE*WEI)-(DEI*WIE))
    c = np.array(A0*D0+WIE*WEI)
    ## == ##
    
    npa = a.astype(complex)
    npb = b.astype(complex)
    npc = c.astype(complex)

    mu2 = (-npb-np.sqrt(
                    np.power(npb,2)
                    -(4*npa*npc))
                    )/(2*npa)
    k2p = np.sqrt(mu2)
    
    #kn = real(k2p)
    #fn = kn / (2.0*np.pi)
    #return fn
    return real(k2p)

# LIB001 source lines 7270-7283
def model_EI_fn(x, x0, x1, x2, x3, x4, x5,
                x6, x7, x8, x9, x10):
    """
    Return the ordinary intrinsic spatial frequency f_n.
    """
    params = np.array(
        [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10],
        dtype=float,
    )

    converted = convert_wavenumber_parameters_to_frequency(params)
    kn = model_EI_kn(x, *converted)

    return kn / (2.0*np.pi)

# LIB001 source lines 9188-9207
def preferredk_r0_abc(kwargs):
    # same math you had
    wEE = kwargs['wEE']; wEI = kwargs['wEI']; wIE = kwargs['wIE']; wII = kwargs['wII']
    wEe = kwargs['wEe']; wEi = kwargs['wEi']; wIe = kwargs['wIe']; wIi = kwargs['wIi']
    rI0 = kwargs['rI0']; rE0 = kwargs['rE0']

    WEE, WEI, WII, WIE = wEE + 2*wEe, wEI + 2*wEi, wII + 2*wIi, wIE + 2*wIe
    DEE, DEI, DII, DIE = wEe, wEi, wIi, wIe

    RE0 = 1.0 / (1 - (rE0 ** 2))
    RI0 = 1.0 / (1 - (rI0 ** 2))

    A0 = RE0 - WEE
    D0 = RI0 + WII

    a = ((-DEE * DII) + DIE * DEI)
    b = DEE * D0 + (-DII * A0) + (-DIE * WEI) + (-DEI * WIE)
    c = A0 * D0 + WIE * WEI

    return a, b, c, DEE * D0, (-DII * A0)

# LIB001 source lines 9210-9228
def coupledODEs_rE0_rI0(var, kwargs):
    x0 = var[0]; x1 = var[1]
    wEE = kwargs['wEE']; wEI = kwargs['wEI']; wIE = kwargs['wIE']; wII = kwargs['wII']
    wEe = kwargs['wEe']; wEi = kwargs['wEi']; wIe = kwargs['wIe']; wIi = kwargs['wIi']
    Lb = kwargs['Lb']; alpha = kwargs['alpha']; tauE = kwargs['tauE']

    rE0 = x0; rI0 = x1
    iE0 = alpha * Lb
    iI0 = (1.0 - alpha) * Lb

    WEE, WEI, WII, WIE = wEE + 2 * wEe, wEI + 2 * wEi, wII + 2 * wIi, wIE + 2 * wIe
    DEE, DEI, DII, DIE = wEe, wEi, wIi, wIe

    X0 = rE0 * WEE - rI0 * WEI + iE0
    Y0 = rE0 * WIE - rI0 * WII + iI0

    rE0out = (-rE0 + np.tanh(X0)) / (tauE)
    rI0out = (-rI0 + np.tanh(Y0))
    return [rE0out, rI0out]

# LIB001 source lines 9270-9281
def jacobian_numeric(func, x, args=(), eps=1e-6):
    x = np.asarray(x, dtype=float)
    n = x.size
    J = np.zeros((n, n), dtype=float)
    f0 = np.asarray(func(x, *args), dtype=float)
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = eps
        f1 = np.asarray(func(x + dx, *args), dtype=float)
        f2 = np.asarray(func(x - dx, *args), dtype=float)
        J[:, i] = (f1 - f2) / (2.0 * eps)
    return J

# LIB001 source lines 9293-9383
def rErI_eq0_simulation(kwargs):
    from scipy import optimize
    import numpy.linalg as npl
    
    """
    Find a stable equilibrium for given kwargs.
    Uses previous-state guess provided in kwargs['rE0'], kwargs['rI0'] if possible.
    Returns (rE, rI) floats.
    """

    # --- previous state (guaranteed floats) ---
    rE_prev = float(kwargs.get('rE0', 0.0))
    rI_prev = float(kwargs.get('rI0', 0.0))
    prev = np.array([rE_prev, rI_prev], dtype=float)

    cand = []

    # ---------- 1. smart initial guess ----------
    try:
        sol = optimize.root(
            coupledODEs_rE0_rI0,
            prev,
            args=(kwargs,),
            tol=1e-10
        )
        if sol.success:
            cand.append(np.asarray(sol.x, dtype=float).ravel())
    except Exception:
        pass

    # ---------- 2. fallback grid ----------
    if not cand:
        guesses = np.linspace(-1.5, 1.5, 9)
        for rE_guess in guesses:
            for rI_guess in guesses:
                try:
                    sol = optimize.root(
                        coupledODEs_rE0_rI0,
                        [rE_guess, rI_guess],
                        args=(kwargs,),
                        tol=1e-10
                    )
                    if sol.success:
                        cand.append(np.asarray(sol.x, dtype=float).ravel())
                except Exception:
                    continue

    # ---------- 3. ultimate fallback ----------
    if not cand:
        return rE_prev, rI_prev

    # ---------- 4. deduplicate safely ----------
    uniq = []
    tol = 1e-6

    for r in cand:
        r = np.asarray(r, dtype=float).ravel()
        if r.shape != (2,):
            continue
        if len(uniq) == 0:
            uniq.append(r)
        else:
            if all(npl.norm(r - u) > tol for u in uniq):
                uniq.append(r)

    if len(uniq) == 0:
        return rE_prev, rI_prev

    uniq = np.array(uniq)

    # ---------- 5. stability check ----------
    stable = []
    for r in uniq:
        try:
            J = jacobian_numeric(coupledODEs_rE0_rI0, r, args=(kwargs,))
            eigvals = npl.eigvals(J)
            if np.all(np.real(eigvals) < 0):
                stable.append(r)
        except Exception:
            pass

    # ---------- 6. selection logic ----------
    if stable:
        stable = np.array(stable)
        dists = npl.norm(stable - prev, axis=1)
        chosen = stable[np.argmin(dists)]
    else:
        dists = npl.norm(uniq - prev, axis=1)
        chosen = uniq[np.argmin(dists)]

    return float(chosen[0]), float(chosen[1])

# LIB001 source lines 9449-9543
def simulate_PSF(kwargs):
    wEE = kwargs["wEE"]
    wEI = kwargs["wEI"]
    wIE = kwargs["wIE"]
    wII = kwargs["wII"]

    wEe = kwargs["wEe"]
    wEi = kwargs["wEi"]
    wIe = kwargs["wIe"]
    wIi = kwargs["wIi"]

    WEE = wEE + 2.0*wEe
    WEI = wEI + 2.0*wEi
    WIE = wIE + 2.0*wIe
    WII = wII + 2.0*wIi

    DEE = wEe
    DEI = wEi
    DIE = wIe
    DII = wIi

    alpha = kwargs["alpha"]
    amplitude = kwargs["Amplitude"]
    rI0 = kwargs["rI0"]
    rE0 = kwargs["rE0"]

    # This is now ordinary frequency f_r, not wavenumber k_r.
    fr_previous = float(
        kwargs.get("psfrE", 0.0)
    )

    response_values = []

    frequency_values = [fr_previous]
    frequency_values.extend(
        np.arange(
            fr_previous - 1.3,
            fr_previous + 0.5,
            0.01,
        )
    )
    frequency_values = sorted(frequency_values)

    iEt = alpha*amplitude
    iIt = (1.0-alpha)*amplitude

    if (1.0-rE0**2) == 0:
        A0 = 0.0
    else:
        A0 = 1.0/(1.0-rE0**2)

    if (1.0-rI0**2) == 0:
        B0 = 0.0
    else:
        B0 = 1.0/(1.0-rI0**2)

    for frequency in frequency_values:
        # Convert cycles/unit to radians/unit.
        k = 2.0*np.pi*frequency

        A = np.array([
            [
                A0-WEE+k**2*DEE,
                WEI-k**2*DEI,
            ],
            [
                -WIE+k**2*DIE,
                B0+WII-k**2*DII,
            ],
        ])

        Ai = np.array([
            [
                iEt,
                WEI-k**2*DEI,
            ],
            [
                iIt,
                B0+WII-k**2*DII,
            ],
        ])

        response = (
            np.linalg.det(Ai)
            / np.linalg.det(A)
        )

        response_values.append(response)

    index = np.argmax(
        np.asarray(response_values)
    )

    fr = frequency_values[index]
    return float(fr)

# LIB001 source lines 9548-9558
def cached_equilibrium(param_tuple, LB, rE_guess, rI_guess):
    """Cache root results per (params, LB, previous state)."""
    rE, rI = rErI_eq0_simulation(
        {'wEE': param_tuple[0], 'wEI': param_tuple[2],
         'wIE': param_tuple[4], 'wII': param_tuple[6],
         'wEe': param_tuple[1], 'wEi': param_tuple[3],
         'wIe': param_tuple[5], 'wIi': param_tuple[7],
         'Lb': LB, 'alpha': param_tuple[8], 'tauE': 1.0,
         'rE0': rE_guess, 'rI0': rI_guess}
    )
    return float(rE), float(rI)

# LIB001 source lines 9576-9595
def simulate_equilibria(params, xFit):
    param_tuple = tuple(
        np.asarray(params, dtype=float)
    )

    rE_last, rI_last = 0.0, 0.0
    rE_hist, rI_hist = [], []

    for LB in xFit:
        rE_last, rI_last = cached_equilibrium(
            param_tuple,
            float(LB),
            float(rE_last),
            float(rI_last),
        )

        rE_hist.append(rE_last)
        rI_hist.append(rI_last)

    return np.array(rE_hist), np.array(rI_hist)

# LIB001 source lines 9619-9625
def run_ISF_model_low(kwargs):
    a, b, c, wD0, wA0 = preferredk_r0_abc(kwargs)
    # safe sqrt with scimath to allow negative discriminant -> complex; then take real part
    disc   = np.lib.scimath.sqrt(b * b - 4 * a * c)
    arrayN = np.lib.scimath.sqrt((-b - disc) / (2 * a))
    knDW   = arrayN.copy()
    return np.real(knDW)

# LIB001 source lines 9627-9638
def run_ISF_model_high(kwargs):
    a, b, c, wD0, wA0 = preferredk_r0_abc(kwargs)
    # safe sqrt with scimath to allow negative discriminant -> complex; then take real part
    disc = np.lib.scimath.sqrt(b * b - 4 * a * c)
    arrayP = np.lib.scimath.sqrt((-b + disc) / (2 * a))
    # arrayN = np.lib.scimath.sqrt((-b - disc) / (2 * a))

    knUP = np.real(arrayP.copy())
    

        
    return knUP

# LIB001 source lines 9640-9669
def convert_psf_parameters_to_frequency(params):
    """
    Parameter order:
    [wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi, alpha]
    """
    params = np.asarray(params, dtype=float).copy()
    q = (2.0*np.pi)**2

    pairs = [
        (0, 1),  # wEE, wEe
        (2, 3),  # wEI, wEi
        (4, 5),  # wIE, wIe
        (6, 7),  # wII, wIi
    ]

    for local_index, lateral_index in pairs:
        local_old = params[local_index]
        lateral_old = params[lateral_index]

        lateral_new = lateral_old / q
        local_new = (
            local_old
            + 2.0*lateral_old
            - 2.0*lateral_new
        )

        params[local_index] = local_new
        params[lateral_index] = lateral_new

    return params

# LIB001 source lines 9692-9744
def simulate_psf_history(
    params,
    xFit,
    rE_hist,
    rI_hist,
):
    seed_kwargs = {
        "wEE": params[0],
        "wEe": params[1],
        "wEI": params[2],
        "wEi": params[3],
        "wIE": params[4],
        "wIe": params[5],
        "wII": params[6],
        "wIi": params[7],
        "alpha": params[8],
        "tauE": 1.0,
        "Amplitude": 1.0,
        "rE0": rE_hist[0],
        "rI0": rI_hist[0],
    }

    kr_seed = run_ISF_model_high(
        seed_kwargs
    )

    # Convert the initial wavenumber to ordinary frequency.
    fr_last = kr_seed/(2.0*np.pi)

    fr_hist = []

    for index, LB in enumerate(xFit):
        fr_last = simulate_PSF({
            "wEE": params[0],
            "wEe": params[1],
            "wEI": params[2],
            "wEi": params[3],
            "wIE": params[4],
            "wIe": params[5],
            "wII": params[6],
            "wIi": params[7],
            "Lb": float(LB),
            "alpha": params[8],
            "tauE": 1.0,
            "Amplitude": 1.0,
            "rE0": rE_hist[index],
            "rI0": rI_hist[index],
            "psfrE": fr_last,
        })

        fr_hist.append(fr_last)

    return np.asarray(fr_hist)

# LIB001 source lines 9754-9778
def model_psf_function(params, xFit):
    converted_params = (
        convert_psf_parameters_to_frequency(
            params
        )
    )

    rE_hist, rI_hist = simulate_equilibria(
        converted_params,
        xFit,
    )

    fr_predict = simulate_psf_history(
        converted_params,
        xFit,
        rE_hist,
        rI_hist,
    )

    scaled_xaxis = np.power(
        10.0,
        xFit/10.0,
    )

    return scaled_xaxis, fr_predict

