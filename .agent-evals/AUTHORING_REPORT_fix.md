# repoevals fix-task authoring report — mkl_fft

All tasks are drafts. Nothing could be executed on the authoring Mac (no x86 MKL): hidden tests were NOT run, `repoevals check` was NOT run. Everything below is reasoned from code/diffs. `repoevals validate --source .`: 6 tasks, 0 errors (only draft warnings). `author pin` run; `git apply --check oracle.patch` passes at each base.

## Tasks
| task | source | base | hidden tests (targets) | notes |
|---|---|---|---|---|
| fix_fftn_scale_fallback | PR #111 / gh-109 | 6335c594 (2024, setup.py build, old `shape=`/`forward_scale=` API) | test_gh109 (imports minimised) | int64 vs float32 `fftn(..., axes=(0,), forward_scale=1/3)` differ; fallback applied scale**(1/ndim) |
| fix_fft_empty_axes_typeerror | PR #288 | 1c0abc54 | test_empty_axes (parametrized vs numpy, strict dtype) | `fftn(x, axes=())` TypeError |
| fix_fft_empty_axes_identity | PR #293 | 5a5f1c25 | test_empty_axes_with_out, test_empty_axes_returns_same_object | returns input object, ignores out |
| fix_nd_norm_scaling | PR #370 (gh-336) | f83b9d41 | trimmed to test_ortho_preserves_norm, test_fftn_axes_subset_norm, test_rfftn_axes_subset_norm, test_fft2_on_3d_norm | subset-axes and irfftn norm scale; other 18 tests of the PR's new file removed (pass at base or test unrelated features) |
| fix_irfft_real_input | PR #180 (gh-176) | 44d10a00 | test_irfft_dtype | float32 real input to irfft returned float64 |
| fix_scipy_set_workers | PR #183 (gh-177) | d3f7e2df | test_invalid_workers, test_set_get_workers, test_set_workers_invalid | test_mixed_threads_processes removed |

Regression targets are narrow node ids (test_fftnd.py subsets, test_fft1d.py, test_threaded_same). Bases are pinned SHAs (merge first-parent for #111/#288/#293/#370; commit parent for squash PRs).

## Dropped candidates
| candidate | reason |
|---|---|
| #181 scipy shape/axes handling | refactor + docs; hidden tests are only un-skipped hfft/ihfft tests (xp fixtures) and I could not establish that any fail at base; no clean behaviour description |
| #138 "resolve a few issues" | four issues (#115/#116/#119/#135), 6 files, bundled tests; too multi-issue |
| #288 `test_empty_axes_with_out` (test only) | asserts `result is out`, contradicting #293; removed from hidden set |
| #183 `test_mixed_threads_processes` (test only) | fork + MKL threadpool, potential flakiness |

## Unverifiable assumptions / needs human attention
- Nothing executed. CI `repoevals check --repeats 3` must confirm: hidden tests fail at base, pass with oracle, regression targets pass at both.
- fix_fftn_scale_fallback: base is a July-2024 tree (setup.py, no pyproject; Cython code from that era). The configured `pip install --no-build-isolation -e .` and modern Cython/NumPy may not build it; highest risk of build failure. Drop if it does.
- Tests using `requires_numpy_2` / `assert_allclose(strict=True)` (180, 288, 293) assume NumPy >= 2 in the CI env; skipped hidden tests would fail the gate.
- fix_fft_empty_axes_identity: existing test `test_fftnd.py::test_empty_axes_with_out` asserts the OLD behaviour (`result is out`), conflicting with the fix. The instruction carves out an exception to "do not weaken existing tests" for it. Regression targets avoid that test. Reviewer may prefer to drop this task (it reverses a prior PR's behaviour).
- fix_scipy_set_workers: hardware-dependent: with os.cpu_count() == MKL max threads (MKL_NUM_THREADS=2 set in config), `test_invalid_workers` may pass at base, but `test_set_workers_invalid` and `test_set_get_workers` fail deterministically at base. The instruction states the (design-decided) semantic: T = mkl.get_max_threads(), default get_workers() == T.
- fix_nd_norm_scaling: hidden file reference `numpy.fft._pocketfft` import guard raises RuntimeError if numpy.fft is patched by mkl_fft; fine in plain env. Trimmed parametrizations include ones that pass at base (norm=None); file-level target still fails at base.
- Instructions for 288/293 slightly echo the PR's problem statement (TypeError text, identity/out semantics) which is the observable behaviour; no code locations named.

## Review checklist
- [ ] Instructions describe user-visible problems without solution
- [ ] Hidden tests match stated behaviour
- [ ] `repoevals check` OK in Linux CI; approve with `repoevals author approve`
