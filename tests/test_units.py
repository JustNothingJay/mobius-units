"""
Tests for mobius-units.

Organized by feature:
  1. Tower source — alpha comes from mobius-constant, not CODATA
  2. SI exact — h, c, e are exact by definition
  3. Dimensional ladder — atomic constants are alpha^n * R_inf * SI
  4. Planck scale — G and Planck units within measurement uncertainty
  5. Inter-constant relationships — algebraic predictions hold
  6. Unit system conversions — round-trip consistency
"""

import math
import pytest
from mobius_units import (
    alpha_inv, alpha, pi, mu, eta,
    c, h, hbar, e_charge, k_B, N_A,
    R_inf, R_inf_unc,
    m_e, m_p, a_0, r_e, lambda_C, mu_B, E_h, sigma_T,
    G, m_P, l_P, t_P, T_P, E_P,
    AtomicUnits, ParticleUnits, PlanckUnits,
    atomic_to_planck, planck_to_atomic,
)


# ═══════════════════════════════════════════════════════════════
# 1. Tower source
# ═══════════════════════════════════════════════════════════════

class TestTowerSource:
    """Alpha comes from mobius-constant, not a hardcoded CODATA value."""

    def test_alpha_inv_is_tower_value(self):
        from mobius_constant import Alpha_inv as MC_Alpha_inv
        assert alpha_inv == float(MC_Alpha_inv)

    def test_alpha_inv_not_codata_2018(self):
        # CODATA 2018 adjusted: 137.035999084
        assert alpha_inv != 137.035999084

    def test_alpha_times_alpha_inv(self):
        assert abs(alpha * alpha_inv - 1.0) < 1e-14

    def test_alpha_inv_near_137(self):
        assert 137.035 < alpha_inv < 137.036

    def test_mu_uses_tower_alpha(self):
        # Recompute mu from tower alpha to verify
        a = alpha
        expected = 6 * pi**5 * (1 + a**2 / (2 * math.sqrt(2)) - (22/27) * a**4)
        assert mu == expected


# ═══════════════════════════════════════════════════════════════
# 2. SI exact constants
# ═══════════════════════════════════════════════════════════════

class TestSIExact:
    """SI 2019 definitions are exact — test the exact values."""

    def test_c(self):
        assert c == 299_792_458.0

    def test_h(self):
        assert h == 6.62607015e-34

    def test_e_charge(self):
        assert e_charge == 1.602176634e-19

    def test_k_B(self):
        assert k_B == 1.380649e-23

    def test_N_A(self):
        assert N_A == 6.02214076e23

    def test_hbar_derived(self):
        assert abs(hbar - h / (2 * math.pi)) < 1e-50


# ═══════════════════════════════════════════════════════════════
# 3. Dimensional ladder
# ═══════════════════════════════════════════════════════════════

class TestDimensionalLadder:
    """Every atomic constant is alpha^n * R_inf * SI-exact factors."""

    def test_bohr_radius_formula(self):
        expected = alpha / (4 * math.pi * R_inf)
        assert abs(a_0 - expected) / a_0 < 1e-14

    def test_electron_mass_formula(self):
        expected = 2 * h * R_inf / (alpha**2 * c)
        assert abs(m_e - expected) / m_e < 1e-14

    def test_classical_radius_formula(self):
        expected = alpha**2 * a_0
        assert abs(r_e - expected) / r_e < 1e-14

    def test_compton_wavelength_formula(self):
        expected = alpha * a_0
        assert abs(lambda_C - expected) / lambda_C < 1e-14

    def test_proton_mass_formula(self):
        expected = mu * m_e
        assert abs(m_p - expected) / m_p < 1e-14

    def test_hartree_energy_alpha_independent(self):
        """Hartree energy = 2*h*c*R_inf — no alpha dependence."""
        expected = 2 * h * c * R_inf
        assert abs(E_h - expected) / E_h < 1e-10

    def test_bohr_radius_codata_range(self):
        """Tower a_0 within ~5 sigma of CODATA (expected Cs offset)."""
        codata = 5.29177210903e-11
        unc = 0.00000000080e-11
        sigma = abs(a_0 - codata) / unc
        assert sigma < 6  # Cs-offset expected ~4.5 sigma

    def test_electron_mass_codata_range(self):
        codata = 9.1093837015e-31
        unc = 0.0000000028e-31
        sigma = abs(m_e - codata) / unc
        assert sigma < 6

    def test_mu_codata_agreement(self):
        """Mass ratio agrees to <1 sigma."""
        codata = 1836.15267343
        unc = 0.00000011
        sigma = abs(mu - codata) / unc
        assert sigma < 1


# ═══════════════════════════════════════════════════════════════
# 4. Planck scale
# ═══════════════════════════════════════════════════════════════

class TestPlanckScale:
    """Tower-derived G and Planck units within measurement uncertainty."""

    def test_G_within_1_sigma(self):
        G_codata = 6.67430e-11
        G_unc = 0.00015e-11
        sigma = abs(G - G_codata) / G_unc
        assert sigma < 1.0

    def test_planck_length_within_1_sigma(self):
        lP_codata = 1.616255e-35
        lP_unc = 0.000018e-35
        sigma = abs(l_P - lP_codata) / lP_unc
        assert sigma < 1.0

    def test_planck_mass_within_1_sigma(self):
        mP_codata = 2.176434e-8
        mP_unc = 0.000024e-8
        sigma = abs(m_P - mP_codata) / mP_unc
        assert sigma < 1.0

    def test_planck_time_within_1_sigma(self):
        tP_codata = 5.391247e-44
        tP_unc = 0.000060e-44
        sigma = abs(t_P - tP_codata) / tP_unc
        assert sigma < 1.0

    def test_planck_temperature_within_1_sigma(self):
        TP_codata = 1.416784e32
        TP_unc = 0.000016e32
        sigma = abs(T_P - TP_codata) / TP_unc
        assert sigma < 1.0

    def test_planck_mass_from_formula(self):
        """m_P = m_p * exp(eta)."""
        expected = m_p * math.exp(eta)
        assert abs(m_P - expected) / m_P < 1e-10

    def test_G_self_consistent(self):
        """G = hbar*c / m_P^2."""
        expected = hbar * c / m_P**2
        assert abs(G - expected) / G < 1e-14


# ═══════════════════════════════════════════════════════════════
# 5. Inter-constant relationships
# ═══════════════════════════════════════════════════════════════

class TestRelationships:
    """Algebraic relationships between constants hold."""

    def test_alpha_equation(self):
        """alpha^-1 + S*alpha = 4*pi^3 + pi^2 + pi."""
        S = 1/math.factorial(4) + 3/math.factorial(8)
        K = 4 * pi**3 + pi**2 + pi
        LHS = alpha_inv + S * alpha
        assert abs(LHS - K) < 1e-8

    def test_G_R_inf_squared(self):
        """G * R_inf^2 = c^3*alpha^4 / (8*pi*mu^2*h*exp(2*eta))."""
        LHS = G * R_inf**2
        RHS = c**3 * alpha**4 / (8 * pi * mu**2 * h * math.exp(2 * eta))
        assert abs(LHS / RHS - 1) < 1e-4

    def test_hierarchy_ratio(self):
        """m_P / m_p = exp(eta)."""
        ratio = m_P / m_p
        expected = math.exp(eta)
        assert abs(ratio / expected - 1) < 1e-10


# ═══════════════════════════════════════════════════════════════
# 6. Unit system conversions
# ═══════════════════════════════════════════════════════════════

class TestUnitSystems:
    """Round-trip conversion consistency."""

    def test_atomic_energy_round_trip(self):
        val = 1.0
        si = AtomicUnits.to_si(val, "energy")
        back = AtomicUnits.from_si(si, "energy")
        assert abs(back - val) < 1e-14

    def test_atomic_length_round_trip(self):
        val = 42.0
        si = AtomicUnits.to_si(val, "length")
        back = AtomicUnits.from_si(si, "length")
        assert abs(back - val) < 1e-12

    def test_planck_mass_round_trip(self):
        val = 3.14
        si = PlanckUnits.to_si(val, "mass")
        back = PlanckUnits.from_si(si, "mass")
        assert abs(back - val) < 1e-14

    def test_planck_length_is_l_P(self):
        assert PlanckUnits.length == l_P

    def test_atomic_energy_is_hartree(self):
        assert AtomicUnits.energy == E_h

    def test_particle_gev_exact(self):
        """GeV conversion is SI-exact."""
        assert ParticleUnits.GeV_to_J == 1.602176634e-10

    def test_cross_system_round_trip(self):
        """atomic -> planck -> atomic preserves value."""
        val = 5.0
        planck = atomic_to_planck(val, "energy")
        back = planck_to_atomic(planck, "energy")
        assert abs(back - val) / val < 1e-12

    def test_unknown_unit_raises(self):
        with pytest.raises(ValueError, match="Unknown"):
            AtomicUnits.to_si(1.0, "nonsense")

    def test_unknown_planck_unit_raises(self):
        with pytest.raises(ValueError, match="Unknown"):
            PlanckUnits.to_si(1.0, "nonsense")

    def test_unknown_particle_unit_raises(self):
        with pytest.raises(ValueError, match="Unknown"):
            ParticleUnits.to_si(1.0, "nonsense")
