# Author notes: fix_c2c_out_cast_or_padded_input

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/387
- commit: e2d358976ed82763bfae69dade8ba06ddb26d9e1
- base: 53cecd9861da064e1bef26539b6a1d275ad33b70 (the fix's parent)
- subject: fix: cast unsupported-dtype input to complex128 when `out=` is given

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/_pydfti.pyx` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_fft1d.py`
- `mkl_fft/tests/test_fftnd.py`

## Authoring decisions

- Whole PR #387 (two commits: 0566909 cast unsupported dtypes even with `out=`, 2417932 compare `out` strides
  with the array passed to MKL and raise for unsupported types). The two symptoms share one code path, so they
  are one task. Targets: the five test functions the PR added; regression: full test_fft1d.py, test_fftnd.py,
  test_interfaces.py.
- `test_fft_longdouble_unsupported` is skipped on platforms where long double == double.
