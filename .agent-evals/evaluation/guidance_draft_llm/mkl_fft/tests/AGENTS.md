# AGENTS.md — mkl_fft/tests/

Test suite for FFT API compatibility and regressions.

## Layout
- `test_fft1d.py`, `test_fftnd.py` — core `mkl_fft.*` 1-D and N-D transforms (dtypes, `n`/`s`, axes, `norm`, `out`, strided/non-contiguous inputs).
- `test_interfaces.py` — `mkl_fft.interfaces.numpy_fft` / `scipy_fft` adapters.
- `test_patch.py`, `test_cli.py` — NumPy patching and the CLI.
- `test_dispatch_equivalence.py` — consistency across dispatch paths.
- `helper.py` — shared markers (e.g. `requires_numpy_2`).
- `third_party/numpy/`, `third_party/scipy/` — copied from upstream NumPy/SciPy. **Do not modify**; they are the compatibility reference.

## Expectations
- Bug fixes and behavior changes add a regression test to the matching `test_*.py` above.
- Do not delete, skip, xfail, or relax existing assertions or tolerances to get a change to pass.
- Compare against `numpy.fft` / `scipy.fft` results as the reference; keep tests deterministic (seeded RNG) and free of timing assertions.

## Running
- `python -m pytest -q mkl_fft/tests`
- Single test: `python -m pytest -q mkl_fft/tests/test_fft1d.py -k <name>`
- SciPy-interface tests are skipped without `scipy` and `mkl-service`.
