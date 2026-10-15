"""Probe: mkl_fft.interfaces.numpy_fft with long double input against NumPy's pocketfft.

The NumPy interface computes long double (`float128` / `complex256` on x86-64 Linux) input in double precision
and returns complex128 (or float64 for c2r transforms): the reference is pocketfft applied to the input converted
to float64 / complex128. float32 / float64 / complex128 inputs are controls.

Each case builds its input deterministically from the case dict. Tolerances are norm-wise (max abs error relative
to max abs reference value), rtol = 2**11 eps and atol = 2**9 eps of the result's real dtype, as in
mkl_fft/tests/test_fftnd.py.
"""

import zlib

import numpy as np

_EPS = {"float32": float(np.finfo(np.float32).eps), "float64": float(np.finfo(np.float64).eps)}

# function -> kind of input it takes
_FUNCS = {
    "fft": "complex",
    "ifft": "complex",
    "rfft": "real",
    "irfft": "complex",
    "hfft": "complex",
    "ihfft": "real",
    "fft2": "complex",
    "ifft2": "complex",
    "fftn": "complex",
    "ifftn": "complex",
    "rfftn": "real",
    "irfftn": "complex",
}
_ND = {"fft2", "ifft2", "fftn", "ifftn", "rfftn", "irfftn"}


def _cases():
    cases = []
    for func, kind in _FUNCS.items():
        shape = (6, 10) if func in _ND else (32,)
        dts = ["longdouble"] if kind == "real" else ["longdouble", "clongdouble"]
        for dt in dts:
            cases.append(dict(func=func, dtype=dt, shape=shape, data="normal"))
            # digits beyond single precision must survive
            cases.append(dict(func=func, dtype=dt, shape=shape, data="fine"))
            # magnitudes outside the float32 range
            cases.append(dict(func=func, dtype=dt, shape=shape, data="normal", scale=1e200))
            cases.append(dict(func=func, dtype=dt, shape=shape, data="normal", scale=1e-200))
        # strided input, explicit length, and norm variants for long double
        cases.append(dict(func=func, dtype=dts[-1], shape=tuple(2 * s for s in shape), data="normal", step=2))
        if func not in _ND:
            cases.append(dict(func=func, dtype=dts[-1], shape=shape, data="normal", n=20))
        for norm in ("ortho", "forward"):
            cases.append(dict(func=func, dtype=dts[-1], shape=shape, data="normal", norm=norm))
        # controls: supported precisions are unaffected
        for dt in (["float64", "float32"] if kind == "real" else ["complex128", "float64"]):
            cases.append(dict(func=func, dtype=dt, shape=shape, data="normal"))
    # NaN propagation
    for func in ("fft", "rfft", "fftn"):
        cases.append(dict(func=func, dtype="longdouble", shape=(6, 10) if func in _ND else (32,), data="nan"))
    for i, c in enumerate(cases):
        c["id"] = "{}-{}-{}-{}{}{}{}{}-{}".format(
            c["func"], c["dtype"], "x".join(map(str, c["shape"])), c["data"],
            "-scale%g" % c["scale"] if "scale" in c else "",
            "-step%d" % c["step"] if "step" in c else "",
            "-n%d" % c["n"] if "n" in c else "",
            "-" + c["norm"] if "norm" in c else "", i,
        )
    return cases


CASES = _cases()


def _input(case):
    rng = np.random.default_rng(zlib.crc32(case["id"].encode()))
    shape = tuple(case["shape"])
    dt = np.dtype(case["dtype"])
    if case["data"] == "fine":
        # 1 + small offsets: representable in double, lost in single precision
        re = 1.0 + rng.integers(1, 1000, size=shape) * 1e-12
        im = 1.0 - rng.integers(1, 1000, size=shape) * 1e-12
    else:
        re = rng.standard_normal(shape)
        im = rng.standard_normal(shape)
    x = re + 1j * im if dt.kind == "c" else re
    x = x.astype(dt)
    if "scale" in case:
        x = x * dt.type(case["scale"])
    if case["data"] == "nan":
        x[(2,) * x.ndim] = np.nan
    if "step" in case:
        x = x[(slice(None, None, case["step"]),) * x.ndim]
    return x


def _kwargs(case):
    kw = {}
    if "n" in case:
        kw["n"] = case["n"]
    if "norm" in case:
        kw["norm"] = case["norm"]
    return kw


def candidate(case):
    import mkl_fft.interfaces.numpy_fft as mfft

    return getattr(mfft, case["func"])(_input(case), **_kwargs(case))


def reference(case):
    # numpy.fft could be patched by mkl_fft; take the pocketfft implementation directly
    from numpy.fft import _pocketfft as npfft

    x = _input(case)
    if x.dtype == np.longdouble:
        x = x.astype(np.float64)
    elif x.dtype == np.clongdouble:
        x = x.astype(np.complex128)
    return getattr(npfft, case["func"])(x, **_kwargs(case))


def compare(case, got, want):
    got, want = np.asarray(got), np.asarray(want)
    res = {"dtype": str(want.dtype), "got_dtype": str(got.dtype)}
    if got.shape != want.shape:
        return dict(res, ok=False, why=f"shape {got.shape} != {want.shape}")
    if got.dtype != want.dtype:
        return dict(res, ok=False, why=f"dtype {got.dtype} != {want.dtype}")
    real = "float32" if want.dtype in (np.float32, np.complex64) else "float64"
    rtol, atol = 2**11 * _EPS[real], 2**9 * _EPS[real]
    wide = np.complex128 if want.dtype.kind == "c" else np.float64
    g, w = got.astype(wide), want.astype(wide)
    # non-finite outputs at the same elements; which part of a complex element is NaN depends on the order of
    # operations, so compare per element
    if not np.array_equal(np.isfinite(g), np.isfinite(w)):
        return dict(res, ok=False, why="non-finite positions differ")
    fin = np.isfinite(g) & np.isfinite(w)
    if not fin.any():
        return dict(res, ok=True, max_rel_err=0.0)
    scale = float(np.abs(w[fin]).max())
    err = float(np.abs(g[fin] - w[fin]).max())
    rel = err / scale if scale > 0 else err
    return dict(res, ok=bool(err <= (atol + rtol) * scale or err == 0.0), max_rel_err=rel, rtol=rtol, atol=atol)
