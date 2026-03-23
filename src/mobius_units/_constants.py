"""
Fundamental constants derived from the eigenvalue tower.

Every constant that depends on alpha uses the tower-derived value,
not the CODATA adjusted average. Constants that are SI-exact carry
zero uncertainty. The only measured input is R_inf.

All values are plain floats. For the full-precision alpha, import
from mobius-constant directly.
"""

import math
from mobius_constant import Alpha_inv, Alpha, Pi

# ─── Tower-derived dimensionless constants ─────────────────────

alpha_inv: float = float(Alpha_inv)
"""Inverse fine structure constant. Tower-derived: 137.035999176..."""

alpha: float = float(Alpha)
"""Fine structure constant. Tower-derived: 7.29735256e-3."""

pi: float = math.pi
"""Pi. Full machine precision."""

# Proton-electron mass ratio: 6*pi^5 * (1 + alpha^2/(2*sqrt(2)) - (22/27)*alpha^4)
mu: float = 6 * pi**5 * (1 + alpha**2 / (2 * math.sqrt(2)) - (22 / 27) * alpha**4)
"""Proton-electron mass ratio. Tower-derived: 1836.15267343."""

# Planck hierarchy parameter: ln(mP/mp) = 14*pi + pi^2*sqrt(alpha)/28
eta: float = 14 * pi + pi**2 * math.sqrt(alpha) / 28
"""Planck hierarchy parameter. Tower-derived."""

# ─── SI 2019 exact definitions ─────────────────────────────────

c: float = 299_792_458.0
"""Speed of light in vacuum (m/s). Exact."""

h: float = 6.626_070_15e-34
"""Planck constant (J*s). Exact."""

hbar: float = h / (2 * pi)
"""Reduced Planck constant (J*s). Exact."""

e_charge: float = 1.602_176_634e-19
"""Elementary charge (C). Exact."""

k_B: float = 1.380_649e-23
"""Boltzmann constant (J/K). Exact."""

N_A: float = 6.022_140_76e23
"""Avogadro constant (mol^-1). Exact."""

# ─── The one measured input ────────────────────────────────────

R_inf: float = 10_973_731.568_157
"""Rydberg constant (m^-1). CODATA 2022. Uncertainty: 0.000012 m^-1."""

R_inf_unc: float = 0.000_012
"""Uncertainty in R_inf (m^-1)."""

# ─── Derived atomic constants (all use tower alpha) ────────────

m_e: float = 2 * h * R_inf / (alpha**2 * c)
"""Electron mass (kg). From tower alpha + R_inf."""

m_p: float = mu * m_e
"""Proton mass (kg). From tower mu * m_e."""

a_0: float = alpha / (4 * pi * R_inf)
"""Bohr radius (m). From tower alpha + R_inf."""

r_e: float = alpha**2 * a_0
"""Classical electron radius (m). alpha^3 dependence."""

lambda_C: float = alpha * a_0
"""Reduced Compton wavelength (m). alpha^2 dependence."""

lambda_C_bar: float = lambda_C
"""Alias: reduced Compton wavelength (m)."""

mu_B: float = e_charge * hbar / (2 * m_e)
"""Bohr magneton (J/T). alpha^2 dependence via m_e."""

E_h: float = alpha**2 * m_e * c**2
"""Hartree energy (J). Reduces to 2*h*c*R_inf (alpha-independent)."""

sigma_T: float = (8 * pi / 3) * r_e**2
"""Thomson scattering cross-section (m^2). alpha^6 dependence."""

# ─── Derived gravitational constants ───────────────────────────

G: float = hbar * c / (m_p**2 * math.exp(2 * eta))
"""Gravitational constant (m^3 kg^-1 s^-2). Tower-derived via hierarchy."""

m_P: float = math.sqrt(hbar * c / G)
"""Planck mass (kg). Tower-derived."""

l_P: float = math.sqrt(hbar * G / c**3)
"""Planck length (m). Tower-derived."""

t_P: float = l_P / c
"""Planck time (s). Tower-derived."""

T_P: float = m_P * c**2 / k_B
"""Planck temperature (K). Tower-derived."""

E_P: float = m_P * c**2
"""Planck energy (J). Tower-derived."""
