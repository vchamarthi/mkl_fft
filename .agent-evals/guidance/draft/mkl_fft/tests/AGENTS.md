# AGENTS.md — mkl_fft/tests/

Test suite for FFT API compatibility and regressions.

## Expectations
- Behavior changes should include test updates in the same PR.
- Bug fixes require regression tests.
- Keep tests deterministic and avoid brittle performance-dependent assertions.

## Files
- `test_fft1d.py` — 1-D transforms
- `test_fftnd.py` — N-D transforms
- `test_interfaces.py` — NumPy/SciPy interface adapters
- `test_dispatch_equivalence.py` — checks that dispatch paths give equivalent results
- `test_patch.py` — global NumPy patch behavior
- `test_cli.py` — `python -m mkl_fft` CLI
- `helper.py` — shared test helpers; `third_party/` — vendored third-party test code

SciPy-dependent tests are skipped when SciPy or `mkl-service` is missing (see `CONTRIBUTING.md`).

## Entry point
- `pytest mkl_fft/tests`
