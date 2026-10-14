# Author notes: fix_irfft_real_input

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/180
- commit: 6bde33e7c2e1c47da84c2a07ba970e91202bd323
- base: 44d10a007c32a25fa2b0f2b80c8ea78733867181 (the fix's parent)
- subject: fix an issue for real inputs of `irfft` (#180)

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/_pydfti.pyx` (M)
- `mkl_fft/interfaces/_numpy_fft.py` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_repoevals_fix_irfft_real_input_fft1d.py`: test_irfft_dtype

## Commit message

* fix an issue for real inputs of irfft

* Update mkl_fft/tests/third_party/scipy/test_basic.py

Co-authored-by: Copilot <175728472+Copilot@users.noreply.github.com>

* Update mkl_fft/tests/test_fft1d.py

Co-authored-by: Anton <100830759+antonwolfy@users.noreply.github.com>

---------

Co-authored-by: Copilot <175728472+Copilot@users.noreply.github.com>
Co-authored-by: Anton <100830759+antonwolfy@users.noreply.github.com>
