# Unbalanced `restore_numpy_fft()` is silently ignored

`mkl_fft.patch_numpy_fft()` and `mkl_fft.restore_numpy_fft()` are reference counted per thread. When
`restore_numpy_fft()` is called more times than `patch_numpy_fft()` in a thread, the extra call does nothing, and
the only sign of the mistake is a line printed to stdout when `verbose=True`. Library code that calls it with the
default arguments gets no signal at all, and the message cannot be caught, filtered or turned into an error with
the standard `warnings` machinery (for example `python -W error` or `pytest.warns`).

```python
import warnings
import mkl_fft

assert not mkl_fft.is_patched()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    mkl_fft.restore_numpy_fft()        # no matching patch_numpy_fft() call
print(len(w))                          # 0
```

Expected: an unbalanced `restore_numpy_fft()` call issues a `RuntimeWarning` whose message starts with
`restore_numpy_fft` and says it was called more times than `patch_numpy_fft` in this thread — regardless of
`verbose` — and still leaves the patch state unchanged. Balanced patch/restore sequences, nested use and the
`mkl_fft.mkl_fft()` context manager must behave as before, without warnings.

Do not weaken or delete existing tests.
