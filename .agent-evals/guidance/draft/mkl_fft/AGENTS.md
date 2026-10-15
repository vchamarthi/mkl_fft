# AGENTS.md — mkl_fft/

Core package implementation for MKL-backed FFT operations.

## Key files
- `__init__.py` — public package API surface
- `_pydfti.pyx` — Cython bindings for DFTI interactions
- `_mkl_fft.py` — transform entry points (`fft` … `irfftn`) with NumPy-style signatures
- `_fft_utils.py` — shared argument checks (`_check_norm`, `_cook_nd_args`, `_init_nd_shape_and_axes`), pad/trim helpers, and the N-D drivers (`_c2c_fftnd_impl`, `_r2c_fftnd_impl`, `_c2r_fftnd_impl`)
- `_patch_numpy.py` — runtime swap of `numpy.fft` (`patch_numpy_fft`, `restore_numpy_fft`, `is_patched`, and the `mkl_fft` context decorator)
- `patch.py` — install/uninstall/status of the startup patch (`install_patch`, `uninstall_patch`, `check_status`)
- `with_patch.py` — runs a command with the NumPy patch applied; `__main__.py` — `python -m mkl_fft` entry point
- `interfaces/` — NumPy/SciPy adapter modules
- `src/` — C template backend (`*.c.src`)
- `tests/` — package tests (see local AGENTS in tests)

## Guardrails
- Preserve NumPy/SciPy-compatible behavior by default.
- Keep adapter, binding, and backend changes coordinated with tests.
- Treat interface wrappers as patch/integration points: behavior changes must stay explicit and reversible.
- Prefer minimal isolated edits around changed API paths.
