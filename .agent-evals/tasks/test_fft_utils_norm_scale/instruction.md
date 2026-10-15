# Add unit tests for the normalization-scale and N-D argument helpers

Two small helpers in `mkl_fft/_fft_utils.py` decide how every transform of the `mkl_fft` package is scaled and
which lengths/axes an N-D transform uses, but they have no direct tests:

- `_compute_fwd_scale(norm, n, shape)` returns the forward scale factor for `norm` (`None`, `"backward"`,
  `"forward"`, `"ortho"`), using the lengths `n` (an int, NumPy integer, sequence or array) if given, else
  `shape`, and rejects any other `norm`;
- `_cook_nd_args(a, s=None, axes=None, invreal=False)` resolves the `s`/`axes` arguments of the N-D transforms
  (adapted from the `numpy.fft` helper of the same name), including the default output length of the last
  axis of complex-to-real transforms (`invreal=True`).

Write tests for both in a new file `mkl_fft/tests/test_fft_utils_helpers.py`. Cover every `norm` value and every
accepted form of `n`, the precedence of `n` over `shape`, zero lengths, all default/explicit combinations of `s`
and `axes`, the errors they raise, and the `invreal` mode. Tests may call the helpers directly and through the
public `mkl_fft` transforms (compare with `numpy.fft`). Run them with
`python -m pytest -q mkl_fft/tests/test_fft_utils_helpers.py`. Do not change any library code under `mkl_fft/`
outside `mkl_fft/tests/`; the tests must pass on the current code.

End your answer with a JSON object naming your test file:

```json
{"targets": ["mkl_fft/tests/test_fft_utils_helpers.py"]}
```
