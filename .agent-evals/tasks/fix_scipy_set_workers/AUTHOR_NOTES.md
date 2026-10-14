# Author notes: fix_scipy_set_workers

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/183
- commit: 384fcb6e3e81402d7f8c223e3443953ae19a4e9a
- base: d3f7e2dfaf6111d5f772f9efd56fca47d458a7f7 (the fix's parent)
- subject: fix issues with `set_workers` (#183)

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/interfaces/README.md` (M)
- `mkl_fft/interfaces/_scipy_fft.py` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/third_party/scipy/test_repoevals_fix_scipy_set_workers_multithreading.py`: test_mixed_threads_processes, test_invalid_workers, test_set_get_workers, test_set_workers_invalid

## Commit message

* fix issues with set_workers

* address comment
