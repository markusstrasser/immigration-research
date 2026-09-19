"""Clemens-Pritchett (2016/2019) epidemiological-case model.

Equations as parsed from the paper's own text (IZA DP 9730, Feb 2016):

  (2)  phi   = m / a                          stock share of unassimilated labour
  (3)  Atil  = A - (A - Alow) * tau*phi/(1-c*phi)
  (8)  m*    = (a - rho*tau*gtil) / (alpha*tau*gtil + c)
  (9)  T*    = (alpha*tau*gtil + c)/(a - rho*tau*gtil) * (beta - 1 - (1-gamma)**(1/(1-alpha)))

  gtil = (1-Alow) / (1 - Alow*beta**(alpha-1)),  Alow = 1 - gamma  (A normalised to 1)

Nothing here is repo- or Mexico-specific; see repo_inputs.py for parameters.
"""
import math

# Known parameters, paper section 5.3 "A benchmark calibration".
GAMMA = 0.8      # rich/poor TFP gap after human capital, Hall & Jones (1999a) Table 1
BETA = 6.0       # rest of world / high-income OECD population multiple
ALPHA = 0.6      # labour share, Gollin (2002); Guerriero (2012)
RHO = 0.05       # discount rate
M0 = 0.003       # observed migration rate, developing -> principal destinations


def gtil(gamma=GAMMA, beta=BETA, alpha=ALPHA):
    """Modified productivity gap gamma-tilde, footnote to eq. (8)."""
    alow = 1.0 - gamma
    return (1.0 - alow) / (1.0 - alow * beta ** (alpha - 1.0))


def mstar(a, tau, c, gamma=GAMMA, beta=BETA, alpha=ALPHA, rho=RHO):
    """Dynamically efficient migration rate, eq. (8)."""
    g = gtil(gamma, beta, alpha)
    return (a - rho * tau * g) / (alpha * tau * g + c)


def tstar(a, tau, c, gamma=GAMMA, beta=BETA, alpha=ALPHA, rho=RHO):
    """Optimal transition time, eq. (9). Infinite when m* <= 0."""
    m = mstar(a, tau, c, gamma, beta, alpha, rho)
    if m <= 0:
        return float("inf")
    return (beta - 1.0 - (1.0 - gamma) ** (1.0 / (1.0 - alpha))) / m


def tstar_footnote(m, gamma=GAMMA, beta=BETA, alpha=ALPHA):
    """Footnote 5 form: T ~ (1/m)(beta - 1 - (A/Alow)**(1/(alpha-1)))."""
    alow = 1.0 - gamma
    return (beta - 1.0 - (1.0 / alow) ** (1.0 / (alpha - 1.0))) / m


def tau_sign_flip(a, gamma=GAMMA, beta=BETA, alpha=ALPHA, rho=RHO):
    """tau at which m* crosses zero for a given a: tau = a/(rho*gtil)."""
    return a / (rho * gtil(gamma, beta, alpha))


def a_sign_flip(tau, gamma=GAMMA, beta=BETA, alpha=ALPHA, rho=RHO):
    """a at which m* crosses zero for a given tau: a = rho*tau*gtil."""
    return rho * tau * gtil(gamma, beta, alpha)


def a_for_mstar(m, tau, c, gamma=GAMMA, beta=BETA, alpha=ALPHA, rho=RHO):
    """Invert eq. (8) for a: the iso-m* contour of Figures 3 and 9."""
    g = gtil(gamma, beta, alpha)
    return m * (alpha * tau * g + c) + rho * tau * g


def half_life_assimilation(zeta, lam, mu):
    """Paper eq. (12): mu*t^2 + lam*t = -zeta/2, then a = ln2 / t_half.

    zeta is the (negative) foreign-born intercept, lam and mu the years-since-
    immigration linear and quadratic terms. Returns (t_half, a).
    """
    target = -zeta / 2.0
    # mu*t^2 + lam*t - target = 0 ; take the smaller positive root
    disc = lam * lam + 4.0 * mu * target
    if disc < 0:
        return float("nan"), float("nan")
    r = math.sqrt(disc)
    roots = [(-lam + r) / (2.0 * mu), (-lam - r) / (2.0 * mu)]
    pos = sorted(t for t in roots if t > 0)
    if not pos:
        return float("nan"), float("nan")
    t = pos[0]
    return t, math.log(2.0) / t


def initial_gap(zeta, lam, mu, years=5.0):
    """Paper: delta = 1 - exp(zeta + years*lam + years^2*mu)."""
    return 1.0 - math.exp(zeta + years * lam + years * years * mu)


def gen_rate(gap_early, gap_late, years):
    """Annual convergence rate implied by two generation-level gaps.

    Same exponential-decay convention as the paper's a = ln2/t_half:
    gap(t) = gap(0) * exp(-a t)  =>  a = -ln(gap_late/gap_early)/years.
    Sign of the gap is ignored (magnitudes only); a < 0 means divergence.
    """
    ge, gl = abs(gap_early), abs(gap_late)
    if ge <= 0 or gl <= 0:
        return float("nan")
    return -math.log(gl / ge) / years


def f(x, nd=6):
    """Fixed-precision formatting so reruns are byte-identical."""
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if isinstance(x, float) and math.isinf(x):
        return "inf"
    if isinstance(x, float) and math.isnan(x):
        return "nan"
    return f"{x:.{nd}f}"
