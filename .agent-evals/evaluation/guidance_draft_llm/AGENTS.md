# AGENTS.md — mkl_fft

Entry point for agent context in this repo. Behavior policy: `.github/copilot-instructions.md`.
Development workflow details: `CONTRIBUTING.md`.

## What this project is
`mkl_fft` is a NumPy/SciPy-compatible FFT interface backed by Intel® oneMKL (DFTI).
It aims to match `numpy.fft` / `scipy.fft` behavior while running on MKL.

## Code map (call order, top to bottom)
- `mkl_fft/__init__.py` — public API: `fft`, `ifft`, `fft2`, `ifft2`, `fftn`, `ifftn`, `rfft*`, `irfft*`, plus `patch_numpy_fft` / `restore_numpy_fft` / `is_patched` / `mkl_fft` context manager.
- `mkl_fft/interfaces/numpy_fft.py`, `scipy_fft.py` — public adapters; implementations live in `_numpy_fft.py`, `_scipy_fft.py` (SciPy adapter needs `scipy` + `mkl-service`), with helpers in `_float_utils.py` (float16 upcast / float128 downcast) and `_numpy_helper.py` (`fftshift`, `fftfreq`, ...).
- `mkl_fft/_patch_numpy.py`, `patch.py`, `with_patch.py`, `_patch_startup.py`, `__main__.py` — patching `numpy.fft` and the CLI.
- `mkl_fft/_mkl_fft.py` — thin public functions: compute the `norm` scale factor (`fsc`), then call the 1-D impls in `_pydfti` or the N-D impls in `_fft_utils`.
- `mkl_fft/_fft_utils.py` — pure-Python N-D logic: norm/scale (`_check_norm`, `_compute_fwd_scale`), shape/axes cooking, pad/trim, `out` handling, `_c2c_fftnd_impl` / `_r2c_fftnd_impl` / `_c2r_fftnd_impl`, iteration over non-transformed axes.
- `mkl_fft/_pydfti.pyx` — Cython: 1-D `_c2c_fft1d_impl`, `_r2c_fft1d_impl`, `_c2r_fft1d_impl`, `_direct_fftnd`, `_validate_out_array`, thread-local DFTI descriptor cache.
- `mkl_fft/src/mklfft.c.src` (+ `mklfft.h`, `multi_iter.h`) — C backend template, expanded by `_vendored/process_src_template.py` at build time.
- `mkl_fft/tests/` — tests (see `mkl_fft/tests/AGENTS.md`).
- Other: `_vendored/`, `benchmarks/` (ASV), `conda-recipe/`, `conda-recipe-cf/`, `.github/workflows/`.

Trace a behavior from the public entry point downward before editing; a fix usually belongs at one layer, and the layers above inherit it.

## Build and test
- Build system: `pyproject.toml` + `meson.build` (meson-python). Build deps: `cython>=3.1.0`, `numpy`, `mkl-devel`, `meson-python`, `cmake`, `ninja`. Runtime: `numpy`, `mkl-service` (optional, with `scipy`, for the SciPy interface).
- Editable install: `pip install -e . --no-build-isolation`. With pip-installed `mkl-devel` you may also need `MKLROOT=$(python -c 'import sys; print(sys.prefix)')` set.
- Editable installs rebuild the extension automatically on `import mkl_fft` when `.pyx`, `.c.src`, `.h` or `meson.build` change; you do not need to reinstall after editing them. Build output, including the generated `mklfft.c` and `_pydfti.c`, is under `build/<tag>/` (e.g. `build/cp312/`) and is gitignored. If the build is broken, `rm -rf build` and reinstall.
- Make sure you are testing this checkout: `python -c "import mkl_fft; print(mkl_fft.__file__)"` must point into the working tree.
- Tests: `python -m pytest -q mkl_fft/tests` (or a single file/test id). Lint: `pre-commit run --all-files` (black/isort, 80 cols; cython-lint for `.pyx`).

## Rules
- Preserve NumPy/SciPy FFT API compatibility unless a change is explicitly requested. NumPy is the reference: compare against `numpy.fft` / `scipy.fft` output when in doubt.
- **Never modify `mkl_fft/tests/third_party/**`.** These files are copied from upstream NumPy/SciPy test suites and are the compatibility contract; fix the library so they pass. Put new tests in `mkl_fft/tests/test_*.py`.
- Do not delete, skip, xfail, or loosen existing tests (tolerances, expected values, expected exceptions) to make a change pass. Add new regression tests instead.
- Work from the current source tree. Do not look up fixes in git history (`git log -p`, `git show` of other commits), fetch upstream, or read other installed/checked-out copies of `mkl_fft`; they may not match this tree.
- Edit `mkl_fft/src/*.c.src`, never generated C under `build/`.
- Keep diffs minimal and single-purpose; pair behavior changes with tests.
- Interface patching/wrapping changes must stay explicit, reversible, and documented.
- Do not hardcode mutable versions, CI matrices, or channels in docs; point to `pyproject.toml`, `conda-recipe*/meta.yaml`, `.github/workflows/`.

## Shell notes
- `grep` exits 1 when nothing matches and 2 on a bad path or pattern; `git check-ignore` exits 1 when a path is *not* ignored. Neither one is a build problem.
- `sed -n 40,80p file` needs the trailing `p`.
- Avoid `git stash` to compare before and after: the editable build rebuilds on import, and `git stash pop` aborts if the same files changed since. Use `git diff`, or `git stash push -- <paths>` and check `git stash list` before popping.

## Directory map
Use the nearest local `AGENTS.md` when present:
- `.github/AGENTS.md` — CI workflows
- `mkl_fft/AGENTS.md` — package implementation notes
- `mkl_fft/interfaces/AGENTS.md` — NumPy/SciPy adapters
- `mkl_fft/src/AGENTS.md` — C template backend
- `mkl_fft/tests/AGENTS.md` — test layout and conventions
- `conda-recipe/AGENTS.md`, `conda-recipe-cf/AGENTS.md` — packaging
- `_vendored/AGENTS.md` — vendored code-generation tooling
- `benchmarks/AGENTS.md` — ASV suite
