# `set_workers` / `get_workers` in `mkl_fft.interfaces.scipy_fft` do not follow `scipy.fft` semantics

`scipy.fft.set_workers` rejects `0` and interprets negative values relative to the number of available threads. The `mkl_fft` SciPy interface does neither:

```python
import mkl
import mkl_fft.interfaces.scipy_fft as fft

print(mkl.get_max_threads())          # e.g. 2

with fft.set_workers(0):              # SciPy: ValueError: workers must not be zero
    print(fft.get_workers())          # prints the max thread count, no error

with fft.set_workers(-1):             # SciPy: -1 means "all threads"
    print(fft.get_workers())          # prints -1 instead of the max thread count
```

Expected, using `mkl.get_max_threads()` as the number of available threads (where SciPy uses `os.cpu_count()`), `T` below:

- `get_workers()` outside any context returns `T` (this default intentionally differs from SciPy's 1);
- `with set_workers(4)` makes `get_workers()` return 4, and nested contexts restore the outer value on exit;
- negative `n` means `T + n + 1`, so `set_workers(-1)` gives `T` and `set_workers(-T)` gives 1;
- `set_workers(0)` raises `ValueError` matching "workers must not be zero", and `set_workers(-T - 1)` raises `ValueError` matching "workers value out of range" (raised on entering the context);
- the same validation applies to the `workers=` argument of the transforms, e.g. `fft.fft(x, workers=-T - 1)` and `fft.fft(x, workers=0)` raise, while `fft.ifft([1], workers=-T)` works.

Do not weaken or delete existing tests.
