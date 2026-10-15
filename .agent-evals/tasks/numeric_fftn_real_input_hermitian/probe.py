"""Probe: mkl_fft N-D complex transforms of real input against NumPy's pocketfft.

Each case builds its input deterministically from the case dict, so the candidate and the reference processes see
identical data. Tolerances are norm-wise (max abs error relative to max abs reference value), with rtol/atol taken
from mkl_fft's own test helper (mkl_fft/tests/test_fftnd.py: reps = 2**11 * eps, atol = 2**9 * eps).
"""

import zlib

import numpy as np

_EPS = {"float32": float(np.finfo(np.float32).eps), "float64": float(np.finfo(np.float64).eps)}


def _cases():
    cases = []
    layouts = {
        "C": dict(shape=(5, 6, 7)),
        "F": dict(shape=(5, 6, 7), order="F"),
        "strided": dict(shape=(10, 12, 14), slc=(slice(None, None, 2), slice(None, None, 2), slice(None, None, 2))),
        "negstride": dict(shape=(5, 6, 7), slc=(slice(None, None, -1),) * 3),
    }
    # (shape, axes) pairs: 1-D control, 2-D with short and longer leading axes, 3-D full and subsets
    geometries = [
        ((16,), None),
        ((15,), None),
        ((2, 6), None),
        ((1, 9), None),
        ((3, 5), None),
        ((4, 6), None),
        ((9, 8), None),
        ((5, 6, 7), None),
        ((4, 3, 8), None),
        ((5, 6, 7), (1, 2)),
        ((5, 6, 7), (0, 2)),
        ((5, 6, 7), (0, 1)),
        ((6, 7), (0,)),
        ((3, 4, 5, 6), None),
    ]
    for dt in ("float32", "float64"):
        for func in ("fftn", "ifftn"):
            for shape, axes in geometries:
                cases.append(dict(func=func, dtype=dt, shape=shape, axes=axes, scale=1.0))
        for func in ("fft2", "ifft2"):
            for shape in ((3, 5), (8, 9), (5, 6, 7)):
                cases.append(dict(func=func, dtype=dt, shape=shape, axes=None, scale=1.0))
        for name, lay in layouts.items():
            for func in ("fftn", "ifftn"):
                cases.append(dict(func=func, dtype=dt, axes=None, scale=1.0, layout=name, **lay))
        for func in ("fftn", "ifftn"):
            # very large and very small magnitudes (float32 range is narrower)
            big, small = (1e30, 1e-30) if dt == "float32" else (1e150, 1e-290)
            cases.append(dict(func=func, dtype=dt, shape=(6, 10), axes=None, scale=big))
            cases.append(dict(func=func, dtype=dt, shape=(6, 10), axes=None, scale=small))
            # non-finite values propagate the same way as in NumPy
            cases.append(dict(func=func, dtype=dt, shape=(4, 6), axes=None, scale=1.0, special="nan"))
        for norm in ("ortho", "forward"):
            cases.append(dict(func="fftn", dtype=dt, shape=(5, 6, 7), axes=None, scale=1.0, norm=norm))
            cases.append(dict(func="ifftn", dtype=dt, shape=(5, 6, 7), axes=(0, 1), scale=1.0, norm=norm))
    # complex input of the same shapes: a control that does not use the real-input path
    for func in ("fftn", "ifftn"):
        cases.append(dict(func=func, dtype="complex128", shape=(5, 6, 7), axes=None, scale=1.0))
    for i, c in enumerate(cases):
        c["id"] = "{}-{}-{}-{}{}{}{}".format(
            c["func"], c["dtype"], "x".join(map(str, c["shape"])),
            "all" if c["axes"] is None else "".join(map(str, c["axes"])),
            "-" + c["layout"] if "layout" in c else "",
            "-scale%g" % c["scale"] if c["scale"] != 1.0 else "",
            ("-" + c["special"]) if "special" in c else ("-" + c["norm"] if "norm" in c else ""),
        ) + "-%d" % i
    return cases


CASES = _cases()


def _input(case):
    rng = np.random.default_rng(zlib.crc32(case["id"].encode()))
    shape = tuple(case["shape"])
    if case["dtype"].startswith("complex"):
        x = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    else:
        x = rng.standard_normal(shape)
    x = (x * case["scale"]).astype(case["dtype"])
    if case.get("special") == "nan":
        x[(1,) * x.ndim] = np.nan
    if case.get("order") == "F":
        x = np.asfortranarray(x)
    if case.get("slc") is not None:
        x = x[tuple(case["slc"])]
    return x


def _kwargs(case):
    kw = {}
    if case["axes"] is not None:
        kw["axes"] = tuple(case["axes"])
    if "norm" in case:
        kw["norm"] = case["norm"]
    return kw


def candidate(case):
    import mkl_fft

    return getattr(mkl_fft, case["func"])(_input(case), **_kwargs(case))


def reference(case):
    # numpy.fft could be patched by mkl_fft; take the pocketfft implementation directly
    from numpy.fft import _pocketfft as npfft

    return getattr(npfft, case["func"])(_input(case), **_kwargs(case))


def compare(case, got, want):
    got, want = np.asarray(got), np.asarray(want)
    res = {"dtype": str(want.dtype), "got_dtype": str(got.dtype)}
    if got.shape != want.shape:
        return dict(res, ok=False, why=f"shape {got.shape} != {want.shape}")
    if got.dtype != want.dtype:
        return dict(res, ok=False, why=f"dtype {got.dtype} != {want.dtype}")
    real = "float32" if want.dtype == np.complex64 else "float64"
    rtol, atol = 2**11 * _EPS[real], 2**9 * _EPS[real]
    g, w = got.astype(np.complex128), want.astype(np.complex128)
    # Non-finite outputs must be at the same elements. Which of the real/imaginary parts of such an element is
    # NaN depends on the order of operations (MKL and pocketfft differ), so compare per complex element.
    if not np.array_equal(np.isfinite(g), np.isfinite(w)):
        return dict(res, ok=False, why="non-finite positions differ")
    fin = np.isfinite(g) & np.isfinite(w)
    if not fin.any():
        return dict(res, ok=True, max_rel_err=0.0)
    scale = float(np.abs(w[fin]).max())
    err = float(np.abs(g[fin] - w[fin]).max())
    rel = err / scale if scale > 0 else err
    return dict(res, ok=bool(err <= atol * scale + rtol * scale or err == 0.0), max_rel_err=rel,
                rtol=rtol, atol=atol)
