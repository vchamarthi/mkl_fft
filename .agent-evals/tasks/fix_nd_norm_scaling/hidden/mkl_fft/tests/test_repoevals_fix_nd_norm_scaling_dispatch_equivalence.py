"""Cross-library equivalence checks for axis and axes dispatch.

``third_party/scipy/test_basic.py::test_fft_with_order`` already checks that
mkl_fft agrees with *itself* across C, Fortran, and non-contiguous layouts. It
does not compare against an external reference, so a dispatch change that is
consistently wrong in every layout passes it.

The defect recorded in ``_fft_utils._iter_complementary`` was exactly that
kind: values correct, but an element placed in the other half of the output
relative to NumPy. These tests therefore use NumPy's own implementation as
the reference.

Two deliberate choices:

* Every axis length differs, so an axis permutation cannot produce a
  correctly shaped result and hide behind a shape assertion.
* Output dtype is asserted alongside values, so a dispatch change cannot
  silently upcast.

These cover the paths that dispatch on *which* axes are requested: full-axes
transforms reach the batched N-D descriptor, strict subsets iterate the
complementary axes, and 1-D transforms of rank > 2 arrays are batched only for
the first and last axis.
"""

import itertools

import numpy as np

import pytest

from numpy.testing import assert_allclose

import mkl_fft

try:
    from numpy.fft import _pocketfft as npfft
except ImportError:  # numpy moved it
    import numpy.fft as npfft

if npfft.fftn.__module__.startswith("mkl_fft"):
    raise RuntimeError("reference is mkl_fft; these tests need real numpy.fft")

_SHAPE_3D = (8, 7, 13)

_SHAPE_4D = (4, 5, 6, 7)

_DTYPES = ["float32", "float64", "complex64", "complex128"]

_ORDERS = ["C", "F", "non-contiguous"]

def _cases(funcs, dtypes=_DTYPES):
    """(func, dtype) pairs, dropping the real-input transforms on complex."""
    return [
        (f, dt)
        for f in funcs
        for dt in dtypes
        if not (f.startswith("rfft") and np.dtype(dt).kind == "c")
    ]

_TOL = {
    "float32": 2e-5,
    "complex64": 2e-5,
    "float64": 1e-12,
    "complex128": 1e-12,
}

_NEG_AXES_3D = [
    (-1,),  # last axis
    (-2,),  # middle axis: per-vector path in the C backend
    (-3,),  # first axis
    (-2, -1),  # the fft2 default
    (-3, -1),
    (-1, -2),  # reversed: picks a different last axis for r2c
    (0, -1),  # mixed sign
    (-3, -2, -1),
]

_AXES_3D = (
    [ax for n in (1, 2, 3) for ax in itertools.combinations(range(3), n)]
    + _NEG_AXES_3D
    + [None]  # every axis
)

def _make(shape, dtype, seed=42):
    rng = np.random.default_rng(seed)
    dt = np.dtype(dtype)
    if dt.kind == "c":
        x = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    else:
        x = rng.standard_normal(shape)
    return x.astype(dt)

def _relayout(x, order):
    """Return *x* laid out as requested; data content may differ by order."""
    if order == "F":
        return np.asfortranarray(x)
    if order == "non-contiguous":
        return x[::-1]
    return np.ascontiguousarray(x)

def _check(got, want, dtype):
    assert got.dtype == want.dtype, f"dtype {got.dtype} != {want.dtype}"
    assert got.shape == want.shape, f"shape {got.shape} != {want.shape}"
    tol = _TOL[dtype]
    assert_allclose(
        got, want, rtol=tol, atol=tol * max(1.0, float(np.abs(want).max()))
    )

_UNITARY_CASES = [
    ((16, 18), (0,)),  # gh-336
    ((16, 18), (1,)),
    ((16, 18), (0, 1)),
    (_SHAPE_3D, (0,)),
    (_SHAPE_3D, (1,)),
    (_SHAPE_3D, (2,)),
    (_SHAPE_3D, (0, 2)),
    (_SHAPE_3D, None),
]

_UNITARY_RTOL = {"complex64": 1e-4, "complex128": 1e-10}

@pytest.mark.parametrize("func", ["fftn", "ifftn"])
@pytest.mark.parametrize("dtype", ["complex64", "complex128"])
@pytest.mark.parametrize("shape,axes", _UNITARY_CASES)
def test_ortho_preserves_norm(func, dtype, shape, axes):
    x = _make(shape, dtype)
    x /= np.sqrt((abs(x) ** 2).sum())
    got = getattr(mkl_fft, func)(x, axes=axes, norm="ortho")
    assert np.isclose(
        (abs(got) ** 2).sum(), 1.0, rtol=_UNITARY_RTOL[dtype]
    ), f"norm not preserved: {(abs(got) ** 2).sum()}"

@pytest.mark.parametrize("func", ["fftn", "ifftn"])
@pytest.mark.parametrize("dtype", ["float64", "complex128"])
@pytest.mark.parametrize("axes", _AXES_3D)
@pytest.mark.parametrize("norm", [None, "backward", "forward", "ortho"])
def test_fftn_axes_subset_norm(func, dtype, axes, norm):
    x = _make(_SHAPE_3D, dtype)
    got = getattr(mkl_fft, func)(x, axes=axes, norm=norm)
    want = getattr(npfft, func)(x, axes=axes, norm=norm)
    _check(got, want, dtype)

@pytest.mark.parametrize(
    "func,dtype", _cases(["rfftn", "irfftn"], ["float64", "complex128"])
)
@pytest.mark.parametrize("axes", _AXES_3D)
@pytest.mark.parametrize("norm", [None, "backward", "forward", "ortho"])
def test_rfftn_axes_subset_norm(func, dtype, axes, norm):
    """Includes ``axes=None``: for c2r the scale basis is the *output* length
    along the last transformed axis, so a full-axes irfftn is normalized over
    ``2 * (n - 1)`` rather than ``n``.
    """
    x = _make(_SHAPE_3D, dtype)
    got = getattr(mkl_fft, func)(x, axes=axes, norm=norm)
    want = getattr(npfft, func)(x, axes=axes, norm=norm)
    _check(got, want, dtype)

@pytest.mark.parametrize(
    "func,dtype",
    _cases(["fft2", "ifft2", "rfft2", "irfft2"], ["float64", "complex128"]),
)
@pytest.mark.parametrize("norm", [None, "backward", "forward", "ortho"])
def test_fft2_on_3d_norm(func, dtype, norm):
    """``fft2`` on a rank-3 array transforms 2 of 3 axes, so it is a subset
    transform even though the caller passed no ``axes``.
    """
    x = _make(_SHAPE_3D, dtype)
    got = getattr(mkl_fft, func)(x, norm=norm)
    want = getattr(npfft, func)(x, norm=norm)
    _check(got, want, dtype)
