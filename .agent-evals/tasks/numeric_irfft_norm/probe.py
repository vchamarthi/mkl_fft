"""Numerical probe: mkl_fft.irfft / rfft / hfft family against numpy.fft. Lives in the task directory; the agent
never sees it. `candidate` imports mkl_fft inside the function so the agent's tree is what is measured."""
import numpy as np

NORMS = [None, "backward", "ortho", "forward"]
CASES = []
_rng = np.random.default_rng(12345)


def _add(id_, fn, x, **kw):
    CASES.append({"id": f"{id_}#{len(CASES)}", "fn": fn, "x": x, **kw})


for dtype, cdtype in ((np.float64, np.complex128), (np.float32, np.complex64)):
    tag = np.dtype(dtype).name
    for n_in in (2, 3, 8, 9, 64, 129):
        r = _rng.standard_normal(n_in).astype(dtype)
        spec = np.fft.rfft(r.astype(np.float64)).astype(cdtype)
        for norm in NORMS:
            _add(f"irfft_{tag}_m{spec.size}_{norm}", "irfft", spec, norm=norm, check_dtype=False)
            _add(f"irfft_{tag}_m{spec.size}_n{n_in}_{norm}", "irfft", spec, norm=norm, n=n_in, check_dtype=False)
            _add(f"rfft_{tag}_{n_in}_{norm}", "rfft", r, norm=norm, check_dtype=False)
        _add(f"irfft_{tag}_m{spec.size}_longer", "irfft", spec, norm="ortho", n=2 * n_in + 3, check_dtype=False)
# axis handling and non-contiguous input
_m = (_rng.standard_normal((5, 9)) + 1j * _rng.standard_normal((5, 9)))
_add("irfft_axis0_ortho", "irfft", _m, norm="ortho", axis=0, check_dtype=False)
_add("irfft_axis1_forward", "irfft", _m, norm="forward", axis=1, check_dtype=False)
_add("irfft_noncontig_ortho", "irfft", _m[:, ::2], norm="ortho", check_dtype=False)
_add("rfft_noncontig_forward", "rfft", _rng.standard_normal((6, 10))[::2, ::2], norm="forward", check_dtype=False)
# round trips stay exact for every norm
for norm in NORMS[1:]:
    _add(f"roundtrip_{norm}", "roundtrip", _rng.standard_normal(33), norm=norm, check_dtype=False)


def _args(case):
    kw = {k: case[k] for k in ("n", "axis", "norm") if k in case}
    return kw


def reference(case):
    kw = _args(case)
    if case["fn"] == "roundtrip":
        return np.asarray(case["x"], dtype=np.float64)
    return getattr(np.fft, case["fn"])(case["x"], **kw)


def candidate(case):
    import mkl_fft
    kw = _args(case)
    if case["fn"] == "roundtrip":
        spec = mkl_fft.rfft(case["x"], norm=case["norm"])
        return mkl_fft.irfft(spec, n=case["x"].size, norm=case["norm"])
    return getattr(mkl_fft, case["fn"])(case["x"], **kw)
