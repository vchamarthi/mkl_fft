# AGENTS.md — mkl_fft/

Core package. The module map and call order are in root `AGENTS.md`.

## Guardrails
- Put a fix at the lowest layer that owns the behavior (`_pydfti.pyx` for 1-D and DFTI, `_fft_utils.py` for N-D shape/axes/out logic, `interfaces/` for NumPy/SciPy-specific semantics); public wrappers in `_mkl_fft.py` stay thin.
- 1-D and N-D paths share helpers (`_validate_out_array`, scaling); check both when changing one.
- Treat interface wrappers as patch/integration points: behavior changes must stay explicit and reversible.
- Keep adapter, binding, and backend changes coordinated with tests.
