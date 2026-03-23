"""
mobius-units — Fundamental constants and unit conversions from the eigenvalue tower.

One measurement derives them all.

The eigenvalue tower produces three dimensionless quantities algebraically:
  - alpha (fine structure constant)
  - mu (proton-electron mass ratio)
  - eta (Planck hierarchy parameter)

Combined with five SI-exact definitions (c, h, e, kB, NA) and one
measured constant (R_inf), these reproduce the entire CODATA table
of fundamental constants.

Existing unit libraries carry ~20 empirical conversion factors.
This package carries three equations and one number.

    >>> from mobius_units import alpha_inv, m_e, G, l_P
    >>> alpha_inv
    137.03599917656376
    >>> from mobius_units import AtomicUnits, PlanckUnits
    >>> AtomicUnits.to_si(1.0, 'energy')  # 1 Hartree in joules
    4.359744722207...e-18

Jay Carpenter, 2026
"""

__version__ = "0.1.0"

# ─── Constants ─────────────────────────────────────────────────

from mobius_units._constants import (
    # Tower-derived dimensionless
    alpha_inv,
    alpha,
    pi,
    mu,
    eta,
    # SI 2019 exact
    c,
    h,
    hbar,
    e_charge,
    k_B,
    N_A,
    # The one measured input
    R_inf,
    R_inf_unc,
    # Derived atomic constants
    m_e,
    m_p,
    a_0,
    r_e,
    lambda_C,
    lambda_C_bar,
    mu_B,
    E_h,
    sigma_T,
    # Derived gravitational constants
    G,
    m_P,
    l_P,
    t_P,
    T_P,
    E_P,
)

# ─── Unit systems ─────────────────────────────────────────────

from mobius_units._systems import (
    AtomicUnits,
    ParticleUnits,
    PlanckUnits,
    atomic_to_planck,
    planck_to_atomic,
)

__all__ = [
    # Dimensionless
    "alpha_inv", "alpha", "pi", "mu", "eta",
    # SI exact
    "c", "h", "hbar", "e_charge", "k_B", "N_A",
    # Measured
    "R_inf", "R_inf_unc",
    # Atomic
    "m_e", "m_p", "a_0", "r_e", "lambda_C", "lambda_C_bar",
    "mu_B", "E_h", "sigma_T",
    # Gravitational / Planck
    "G", "m_P", "l_P", "t_P", "T_P", "E_P",
    # Unit systems
    "AtomicUnits", "ParticleUnits", "PlanckUnits",
    "atomic_to_planck", "planck_to_atomic",
]
