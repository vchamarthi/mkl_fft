# Author notes: fix_rfft_cast_input_fortran_out

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

- #389 fixes two independent bugs; this task keeps only the Cython one (`_r2c_fft1d_impl` checks the layout of
  the original `x` instead of the cast copy, and the cast copy was forced C-contiguous). `oracle.patch` is the
  `_pydfti.pyx` part of the PR only.
- `hidden/` = test_fft1d.py / test_fftnd.py as of #389 minus the strided real-input tests of the sibling task
  `fix_ifft_real_input_strided_out`.
- Null run: 8 of 16 target cases fail (i8/f2/g input, axis 0 and 2, and rfftn/rfft2 with i8); f8 cases pass.
