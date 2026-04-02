# mobius-units

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19186394.svg)](https://doi.org/10.5281/zenodo.19186394)

**Fundamental constants and unit conversions from the eigenvalue tower — one measurement derives them all.**

```python
from mobius_units import alpha_inv, m_e, G, l_P

alpha_inv   # 137.03599917656376 (tower-derived, not CODATA lookup)
m_e         # 9.109383714e-31 kg (from tower alpha + R_inf)
G           # 6.67436e-11 m^3 kg^-1 s^-2 (tower-derived, 0.37 sigma)
l_P         # 1.61626e-35 m (tower-derived)
```

## The Problem

Existing unit libraries (`pint`, `astropy.units`, `scipy.constants`) carry 20+ empirical conversion factors from CODATA lookup tables. When CODATA updates, the tables must be refreshed. No algebraic relationship connects the constants — they are independent numbers from independent measurements.

## The Fix

Three algebraic equations produce three dimensionless quantities with zero measured inputs:

| Equation | Produces | Agreement with experiment |
|----------|----------|:------------------------:|
| `a^-1 + S*a = 4*pi^3 + pi^2 + pi` | alpha (fine structure constant) | 0.3 sigma |
| `6*pi^5 * (1 + a^2/(2*sqrt(2)) - (22/27)*a^4)` | mu (proton-electron mass ratio) | 0.03 sigma |
| `ln(mP/mp) = 14*pi + pi^2*sqrt(a)/28` | eta (Planck hierarchy) | 4.2 ppm |

Combined with five SI-exact constants (`c`, `h`, `e`, `k_B`, `N_A`) and **one measurement** (the Rydberg constant `R_inf`), these produce the entire CODATA table.

## Install

```
pip install mobius-units
```

Requires Python >= 3.9. One dependency: `mobius-constant`.

## Constants

Every alpha-dependent constant uses the tower value, not a CODATA lookup.

### Dimensionless (tower-derived)
| Name | Symbol | Value |
|------|--------|-------|
| `alpha_inv` | 1/alpha | 137.035999177 |
| `alpha` | alpha | 7.2973526e-3 |
| `mu` | mp/me | 1836.15267343 |
| `eta` | ln(mP/mp) | 44.0124 |

### Atomic scale (tower alpha + R_inf)
| Name | Symbol | Value | alpha-dep |
|------|--------|-------|-----------|
| `m_e` | electron mass | 9.109e-31 kg | alpha^-2 |
| `m_p` | proton mass | 1.673e-27 kg | alpha^-2 |
| `a_0` | Bohr radius | 5.292e-11 m | alpha^1 |
| `r_e` | classical e- radius | 2.818e-15 m | alpha^3 |
| `lambda_C` | Compton wavelength | 3.862e-13 m | alpha^2 |
| `mu_B` | Bohr magneton | 9.274e-24 J/T | alpha^2 |
| `E_h` | Hartree energy | 4.360e-18 J | alpha^0 (exact) |
| `sigma_T` | Thomson cross-section | 6.652e-29 m^2 | alpha^6 |

### Planck scale (tower hierarchy)
| Name | Symbol | Value | Agreement |
|------|--------|-------|:---------:|
| `G` | gravitational constant | 6.674e-11 | 0.37 sigma |
| `m_P` | Planck mass | 2.176e-8 kg | 0.36 sigma |
| `l_P` | Planck length | 1.616e-35 m | 0.38 sigma |
| `t_P` | Planck time | 5.391e-44 s | 0.37 sigma |
| `T_P` | Planck temperature | 1.417e32 K | 0.36 sigma |

## Unit Systems

Three natural unit systems, all algebraically connected:

```python
from mobius_units import AtomicUnits, PlanckUnits, ParticleUnits

# Atomic -> SI
AtomicUnits.to_si(1.0, 'energy')   # 1 Hartree in joules
AtomicUnits.to_si(1.0, 'length')   # 1 Bohr in metres
AtomicUnits.to_si(1.0, 'time')     # 1 atomic time in seconds

# SI -> Atomic
AtomicUnits.from_si(9.11e-31, 'mass')  # electron mass in atomic units (= 1)

# Planck -> SI
PlanckUnits.to_si(1.0, 'length')   # 1 Planck length in metres
PlanckUnits.to_si(1.0, 'temperature')  # 1 Planck temperature in kelvin

# Particle physics (SI-exact, no tower needed)
ParticleUnits.to_si(125.0, 'energy')  # 125 GeV in joules

# Cross-system
from mobius_units import atomic_to_planck
atomic_to_planck(1.0, 'energy')  # 1 Hartree in Planck energy units
```

## The Alpha Source

All alpha-dependent constants trace to `mobius-constant`:

```python
from mobius_constant import Alpha_inv
float(Alpha_inv)  # 137.03599917656376
```

This is the tower-derived value, not the CODATA adjusted average. It sits 0.3 sigma from the best measurement in physics (Fan et al., 2023). The ~4.5 sigma offset from CODATA 2018 adjusted constants traces entirely to the documented Cs-133 recoil anomaly.

## See Also

- [mobius-constant](https://github.com/JustNothingJay/mobius-constant) — Exact irrational constants (`sqrt(2)**2 == 2`, by construction)
- [mobius-number](https://github.com/JustNothingJay/mobius-number) — Complementary residue arithmetic (`0.1 + 0.2 = 0.3`, exactly)
- [mobius-integer](https://github.com/JustNothingJay/mobius-integer) — Dual-strand integer: machine i64 + exact BigInt (Rust)
- *One Measurement Derives Them All* — companion paper (Carpenter, 2026)

Same pattern. Same anatomy. Same fix. Different domain.

## License

MIT — Jay Carpenter, 2026
