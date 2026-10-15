# Author notes: fix_nd_norm_subset_axes

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/370
- commit: f9f45234b63fde855ad500a28e546a19ef5e567a
- base: f83b9d41f4e823880242519773d487d2091bf6d6 (the fix's parent)
- subject: fix: norm scaling

## Files changed by the fix

- `.pre-commit-config.yaml` (M)
- `CHANGELOG.md` (M)
- `mkl_fft/_fft_utils.py` (M)
- `mkl_fft/_mkl_fft.py` (M)
- `pyproject.toml` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_dispatch_equivalence.py`

## Authoring decisions

- `oracle.patch` keeps only `mkl_fft/_fft_utils.py` and `mkl_fft/_mkl_fft.py`; the PR's `pyproject.toml`
  (formatting) and `.pre-commit-config.yaml` changes were dropped — `pyproject.toml` is in `rebuild_globs` and
  would force a pointless rebuild.
- Two symptoms (CHANGELOG of #370): subset-of-axes scaling (gh-336) and `irfftn`/`irfft2` normalizing by the
  input length instead of `2 * (n - 1)` when `s` is not given (even over all axes). Both are described.
- Targets: the 7 test functions of the new test_dispatch_equivalence.py that fail at the base (280 failing cases);
  the remaining functions of that file pass at the base and are not targets.
