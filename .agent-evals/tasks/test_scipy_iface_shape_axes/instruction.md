# Add unit tests for shape/axes handling in the SciPy interface

`mkl_fft/interfaces/_scipy_fft.py` validates and normalizes the `s`/`shape` and `axes` arguments of the N-D
transforms of the SciPy interface (`fftn`, `ifftn`, `rfftn`, `irfftn`, `hfftn`, `ihfftn` and the 2-D variants) in
the helper `_init_nd_shape_and_axes(x, shape, axes, invreal=False)`. It is adapted from SciPy's
`scipy.fft._pocketfft.helper._init_nd_shape_and_axes` and has no direct tests; it is only exercised indirectly
through a handful of transform calls.

Write tests for it in a new file `mkl_fft/tests/test_scipy_shape_axes.py`. Cover its observable behaviour:

- default `shape`/`axes`, negative and scalar `axes`, scalar and `-1` entries in `shape`, `shape` without `axes`;
- the return values (`shape` as a tuple, `axes` as a list) for each combination;
- every error it raises (axes out of range or repeated, non-integer `axes`/`shape`, mismatched lengths, `shape`
  longer than the array's dimensionality, non-positive lengths), including the message;
- the `invreal=True` mode used by the complex-to-real transforms (default length of the last transformed axis,
  and that an explicit `shape` is kept).

Tests may call the helper directly and through the public `mkl_fft.interfaces.scipy_fft` functions. Run them with
`python -m pytest -q mkl_fft/tests/test_scipy_shape_axes.py`. Do not change any library code under `mkl_fft/`
outside `mkl_fft/tests/`; the tests must pass on the current code.

End your answer with a JSON object naming your test file:

```json
{"targets": ["mkl_fft/tests/test_scipy_shape_axes.py"]}
```
