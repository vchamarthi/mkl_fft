# Author notes: fix_ifft_real_input_strided_out

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/389
- commit: 4e84e7e1dbfa958a7b450b8136b046165a3f4924
- base: 5ace5e78fb5835a17aebf0b63814dacce6f16df9 (the fix's parent)
- subject: fix: respect `out` layout in real-input ifft and in rfft of cast input

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/_pydfti.pyx` (M)
- `mkl_fft/src/mklfft.c.src` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_fft1d.py`
- `mkl_fft/tests/test_fftnd.py`

## Authoring decisions

- #389 fixes two independent bugs; this task keeps only the C-backend one. `oracle.patch` is the
  `mkl_fft/src/mklfft.c.src` part of the PR (strided in-place conjugation helper, plus removal of the stale
  `out`-layout asserts and the ternary-precedence fix in the r2c assert); the `_pydfti.pyx` part belongs to
  `fix_rfft_cast_input_fortran_out`.
- `hidden/` = test_fft1d.py / test_fftnd.py as of #389 minus `test_rfft_out_fortran` / `test_rfftn_out_fortran`
  (the other bug's tests), so the whole files can be regression targets.
- At the base the null run crashes the interpreter (SIGABRT "corrupted double-linked list" / SIGSEGV) in 9 of
  the 27 inverse-transform cases, fails 10 and passes 8; all 27 forward cases pass. The instruction says so.
