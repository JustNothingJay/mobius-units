"""
Unit system conversions.

Three natural-unit systems, all algebraically connected through the tower:
  - Atomic:  hbar = m_e = e = 4*pi*eps_0 = 1
  - Particle physics: hbar = c = 1, energy in GeV
  - Planck:  hbar = c = G = 1

Every conversion factor is either SI-exact, tower-derived, or
R_inf-derived. No CODATA lookup table.
"""

import math
from mobius_units._constants import (
    alpha, alpha_inv, mu, eta, pi,
    c, h, hbar, e_charge, k_B, N_A,
    R_inf,
    m_e, m_p, a_0, r_e, lambda_C, mu_B, E_h, sigma_T,
    G, m_P, l_P, t_P, T_P, E_P,
)


# ─── Atomic unit conversion factors ───────────────────────────

class AtomicUnits:
    """Conversion factors between atomic units and SI.

    In atomic units: hbar = m_e = e = 4*pi*eps_0 = 1.
    All conversions are algebraic in alpha and R_inf.
    """

    energy: float = E_h
    """1 Hartree in joules."""

    length: float = a_0
    """1 Bohr in metres."""

    time: float = hbar / E_h
    """1 atomic time unit in seconds."""

    mass: float = m_e
    """1 atomic mass unit (= m_e) in kg."""

    velocity: float = alpha * c
    """1 atomic velocity unit in m/s."""

    charge: float = e_charge
    """1 atomic charge unit in coulombs (= e, SI-exact)."""

    electric_field: float = E_h / (e_charge * a_0)
    """1 atomic electric field unit in V/m."""

    @classmethod
    def to_si(cls, value: float, unit: str) -> float:
        """Convert a value in atomic units to SI.

        Supported units: 'energy', 'length', 'time', 'mass', 'velocity'.
        """
        factor = getattr(cls, unit, None)
        if factor is None:
            raise ValueError(f"Unknown atomic unit: {unit!r}")
        return value * factor

    @classmethod
    def from_si(cls, value: float, unit: str) -> float:
        """Convert a value in SI to atomic units."""
        factor = getattr(cls, unit, None)
        if factor is None:
            raise ValueError(f"Unknown atomic unit: {unit!r}")
        return value / factor


# ─── Particle physics unit conversion factors ─────────────────

class ParticleUnits:
    """Conversion factors between particle physics units and SI.

    In particle physics: hbar = c = 1, energy in GeV.
    These conversions are SI-exact (no tower dependence).
    """

    GeV_to_J: float = 1.602_176_634e-10
    """1 GeV in joules. Exact from SI definition of e."""

    GeV_inv_to_m: float = hbar * c / 1.602_176_634e-10
    """1 GeV^-1 in metres. Exact from SI."""

    GeV_inv_to_s: float = hbar / 1.602_176_634e-10
    """1 GeV^-1 in seconds. Exact from SI."""

    GeV_to_kg: float = 1.602_176_634e-10 / c**2
    """1 GeV/c^2 in kg. Exact from SI."""

    @classmethod
    def to_si(cls, value: float, unit: str) -> float:
        """Convert particle physics value to SI.

        Supported units: 'energy' (GeV->J), 'length' (GeV^-1->m),
        'time' (GeV^-1->s), 'mass' (GeV/c^2->kg).
        """
        factors = {
            "energy": cls.GeV_to_J,
            "length": cls.GeV_inv_to_m,
            "time": cls.GeV_inv_to_s,
            "mass": cls.GeV_to_kg,
        }
        if unit not in factors:
            raise ValueError(f"Unknown particle unit: {unit!r}")
        return value * factors[unit]


# ─── Planck unit conversion factors ───────────────────────────

class PlanckUnits:
    """Conversion factors between Planck units and SI.

    In Planck units: hbar = c = G = 1.
    These conversions require the tower (via the hierarchy formula).
    """

    length: float = l_P
    """1 Planck length in metres."""

    time: float = t_P
    """1 Planck time in seconds."""

    mass: float = m_P
    """1 Planck mass in kg."""

    energy: float = E_P
    """1 Planck energy in joules."""

    temperature: float = T_P
    """1 Planck temperature in kelvin."""

    @classmethod
    def to_si(cls, value: float, unit: str) -> float:
        """Convert a value in Planck units to SI.

        Supported units: 'length', 'time', 'mass', 'energy', 'temperature'.
        """
        factor = getattr(cls, unit, None)
        if factor is None:
            raise ValueError(f"Unknown Planck unit: {unit!r}")
        return value * factor

    @classmethod
    def from_si(cls, value: float, unit: str) -> float:
        """Convert a value in SI to Planck units."""
        factor = getattr(cls, unit, None)
        if factor is None:
            raise ValueError(f"Unknown Planck unit: {unit!r}")
        return value / factor


# ─── Cross-system convenience ─────────────────────────────────

def atomic_to_planck(value: float, unit: str) -> float:
    """Convert from atomic units to Planck units."""
    si = AtomicUnits.to_si(value, unit)
    return PlanckUnits.from_si(si, unit)


def planck_to_atomic(value: float, unit: str) -> float:
    """Convert from Planck units to atomic units."""
    si = PlanckUnits.to_si(value, unit)
    return AtomicUnits.from_si(si, unit)
