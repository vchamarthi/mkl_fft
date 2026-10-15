# repoevals framework feedback  -  from authoring mkl_fft tasks

Collected by Claude (Opus 5.5) while following `docs/agent-playbook.md` with repoevals 0.2.0 (editable,
`<repoevals>`) on 2026-10-14. Each item: what I ran, what happened, what I suggest.

## 1. `author mine` follows first-parent of the current branch and misses upstream fixes merged into it

Command:

```
repoevals author mine --limit 1000 --json .agent-evals/candidates.json
```

Output excerpt:

```
  2.5  2026-10-14  d020950d9a  lib  120 lines/4 files  tests 2  Merge branch 'IntelPython:master' into repoevals
43 candidates (commits changing library code and tests)
```

The checkout is on a fork branch (`repoevals`) whose latest commit merges upstream `master`. The miner treats that
merge as a single candidate (our own sync merge, useless as a task) and never lists the upstream PRs it brought in:
#387 (`fix: cast unsupported-dtype input to complex128 even when out= is given`), #388, #389
(`fix: respect out layout in real-input ifft and in rfft of cast input`). These are the three most recent and
some of the best-scoped bug fixes in the project. I only found them via
`git log --first-parent origin/master`.

Suggestion: add `--rev <ref>` (default: `[repo].upstream`'s default branch if fetched, else `HEAD`) so mining can run
on `origin/master`; and skip merges whose second parent is an upstream branch tip (sync merges), or expand them
into their constituent PR merges.

## 2. `author mine` ranks PR merges, but several PRs bundle independent bugs

#387 and #389 each fix two independent bugs, and #387 has one commit per bug. The miner only shows the merge, so
splitting a PR into per-bug tasks needs manual `git log A^1..A^2`. Suggestion: show the PR's non-merge commits
(`--expand-prs`) or note "N fix commits" in the listing.

## 3. `[environment].setup` / `[test].build` with an editable install hijack the user's environment

Graders and `setup` run in the environment where repoevals is installed, and the mkl_fft config (like most
compiled Python projects) uses `pip install -e .`. Every `repoevals check` therefore re-points the user's
environment at a temporary workspace; once that workspace is deleted, `import mkl_fft` fails everywhere:

```
$ repoevals check fix_nd_norm_subset_axes --keep /tmp/rk/norm
OK       fix_nd_norm_subset_axes: null=fail oracle=['pass']
$ python -c "import mkl_fft; print(mkl_fft.__file__)"
/tmp/rk/norm/fix_nd_norm_subset_axes/oracle0/workspace/mkl_fft/__init__.py
```

and later, after a check without `--keep`, running a test in a scratch tree:

```
ERROR mkl_fft/tests/test_fft_utils_helpers.py - FileNotFoundError: [Errno 2] ...
```

This also means `--jobs > 1` would race (docs mention it for `run`, but `check` and `author prune-mutants` do the
same silently). Suggestions: (a) `doctor` should warn when `setup`/`build` contain `pip install -e` /
`--editable` and say the env is shared and will be left pointing at a deleted tree; (b) `check` could record the
pre-existing `pip show -f`/`direct_url.json` of the project and print a hint at the end ("your environment now
points at <deleted path>; re-run `pip install -e .`"); (c) document a recommended pattern (per-workspace venv via
`python -m venv --system-site-packages`, or `build_ext --inplace`) in `configuration.md#environment`.

## 4. `[test].build` does not receive `$REPOEVALS_ROOT`, unlike `[environment].setup`

`configuration.md` says setup gets `$REPOEVALS_ROOT`/`$REPOEVALS_SOURCE`/`$REPOEVALS_TASK_DIR` "so it can call
scripts kept in `.agent-evals/`", but `adapters/__init__.py` runs `build` with `env=self.cfg.env` only. The
natural design  -  one `.agent-evals/build.sh` used for both setup and build  -  is therefore impossible, and I had
to inline a 300-character shell one-liner twice in `repoevals.toml` (needed because pre-meson bases need
`MKLROOT` and an unversioned `libmkl_rt.so`). Suggestion: pass the same three variables to `build` (they are
trusted, the build runs on the host anyway), or allow `build = "@setup"`.

## 5. `check` reports `[environment].setup failed` with no excerpt

```
PROBLEM  fix_nd_empty_axes: RuntimeError: fix_nd_empty_axes: [environment].setup failed (rc=1); see /tmp/rk/288/fix_nd_empty_axes/null/setup.log
```

Without `--keep`, the referenced `setup.log` is already deleted when the message is printed, so the pointer is
useless. Suggestion: print the last ~20 lines of setup.log in the PROBLEM line (or keep the run directory of
failing tasks automatically and say so).

## 6. `grade.json` silently truncates `details.tests.failing` to 50 entries

For fix_nd_norm_subset_axes the null run had `"failed": 280` but `failing` listed 50 node ids, all from two test
functions; the five other failing functions (`test_rfftn_axes_subset_norm`, `test_c2c_out_with_norm`, ...) were
invisible. I only found them by re-running pytest by hand. Suggestion: add `"failing_truncated": true` and a
`failing_by_function` histogram (counts per `file::function`), which is exactly what an author needs to narrow
`targets`. Even better: `repoevals check --show-failing` or `repoevals author narrow <task>` that proposes
`targets` from the null run (functions that fail before and pass after).

## 7. Splitting hidden test files between tasks needs hand editing

When one PR fixes two bugs (I split #389 into two tasks with different `oracle.patch`), `hidden/` holds the whole
test files, and `regression_targets = [<that file>]` then fails for the oracle because it contains the other bug's
tests. I removed the other bug's test functions from each task's hidden copy with a script. `--extract-tests` only
helps for the release-base case. Suggestion: `author fix --only-tests file::func,...` to keep just the named test
functions in `hidden/` (reusing the `--extract-tests` machinery), or a `deselect = [...]` key in `[grader]`.

## 8. The "untouched workspace" probe accepts a crash as a valid failure, without saying so

For fix_ifft_real_input_strided_out the null run was `status: "error", rc: -6` (SIGABRT inside the C extension)
and the regression run `rc: -11`. `check` printed `null=fail`, which is right, but an author cannot tell from the
summary whether the hidden tests *detect* the bug or merely crash in an unrelated place. Suggestion: show
`null=crash(rc=-6)` versus `null=fail(16 failed)` in the summary line.

## 9. The numeric grader's custom `compare()` cannot see `[grader.tolerances]`

`numeric_runner.py` calls `probe.compare(case, got, want)` without the tolerance table, so as soon as a probe needs
a custom comparison (FFT outputs need norm-wise error: element-wise `rtol` fails on near-zero coefficients),
`[grader.tolerances]` is silently ignored and tolerances must be hard-coded in the probe. Suggestion: pass the
resolved `(rtol, atol)` (or the whole table) as an optional fourth argument when `compare` accepts it, and have
`validate` warn when both `compare` and `tolerances` are defined. A built-in `"norm": "max"` comparison mode in
the default comparator would remove the need for custom code for every FFT/linear-algebra probe.

## 10. Numeric runner: a reference that raises aborts the whole comparison

`compare()` does `raise SystemExit(f"reference failed: {ref_err}")` if any reference case raises. That makes it
impossible to include "both must raise" cases (empty input, invalid `n`), which the playbook asks for ("empty and
non-contiguous inputs"): `numpy.fft.fft(np.array([]))` raises. Suggestion: support `"expect_error": "ValueError"`
cases, compared by exception type, instead of aborting.

## 11. `max_ulp` is always 0 for complex results and for custom compares

Both my numeric tasks report `"max_ulp": 0` in `grade.json` metrics even when every case fails, because
`ulp_distance` returns `None` for complex dtypes and custom compares never set it. A 0 looks like "perfect".
Suggestion: report `null` when no case produced a ULP value, and compute ULP distance on real and imaginary parts.

## 12. `author mutants`: the instruction template is the fix template, and numbering restarts per call

`instruction.md` generated by `author mutants` says "Write the test-writing request as a user would report it:
the symptom, a minimal reproducer, the expected behaviour. Do not describe the fix ..."  -  wording for a bug report,
not a test request. Running `author mutants` twice on the same task (two functions) writes `m01_...` to `m12_...`
again (`m01_negate_cond_L71.patch` and `m01_negate_cond_L92.patch`), so names no longer identify the function.
Suggestions: a test-task-specific template; continue numbering; include the function name in the file name
(`m13__cook_nd_args_negate_cond_L92.patch`). Also `author mutants` defaults the base to `HEAD`, which on a fork
branch is a commit containing `.github/workflows/repoevals.yml`  -  visible to agents (it describes the
evaluation). A warning when the base contains `[guidance]`-unrelated repoevals files would help.

## 13. `author mutants` over-weights single lines

For `_init_nd_shape_and_axes`, 7 of 20 mutants were on the one `invreal` line
(`shape[-1] = (x.shape[axes[-1]] - 1) * 2`): `/ 2`, `* 3`, `- 0`, `+ 1`, `shape[1]`, `shape[-0]`, `axes[1]`. With
`min_kill = 0.8` that line alone decides the task. Suggestion: an option `--max-per-line N` (default 2-3) and
spread `--max` across lines first.

## 14. Seeded-review "spam" probe is vacuous: its findings are too short to ever score

`spam_answer()` in `graders/review.py` emits `"message": "issue"` (5 characters), but `g_review_seeded` skips
any finding whose text is shorter than 8 characters. The probe therefore always scores recall 0, whatever the
manifest, and never tests what it is meant to: whether line-only matching (`line_tol`) lets a flood of findings
collect seeds. For review_seeded_scipy_fast_len, `check` reported `spam: {"status": "fail", "precision": 0.0}`
with `n_findings: 19, capped: true, unmatched: 19`. Suggestion: use a message of >= 8 characters ("possible
problem on this line"), and also cap at `max_findings` *after* spreading findings evenly over the diff, so the
probe is not limited to the first 19 changed lines.

## 15. Decoy keywords match anywhere in the file; seeds use a line window

In `g_review_seeded`, a seed's `kw` counts only within `kw_line_tol` (15) lines, but a decoy is flagged when
`re.search(d["kw"], text)` matches **anywhere in the same file** (or the line is within 1). `docs/tasks.md`
documents decoys as `{id, file, lines, kw}` and implies the same rule as seeds. With a natural decoy keyword
(`"real"` for "the `real` argument is ignored") any unrelated, valid extra finding in an 800-line module that
mentions "real" input would fail the task. Suggestion: apply `kw_line_tol` to decoys too, and document it.

## 16. `check --json` omits the numbers an author needs for the report

`.agent-evals/check.json` has, per task, only `null`, `oracle`, `spam` status and `problems`. To report
"80/106 cases fail with the bug", "recall 1.0", "280 tests fail before the fix", I had to re-run with `--keep` and
dig through `grade.json` files. Suggestion: include the null and oracle `metrics` (`case_pass_rate`,
`recall`/`precision`, `kill_rate`, failed/passed counts) in `check.json`.

## 17. `check` prints nothing until a task finishes; a 12-task `--repeats 3` run is silent for a long time

Each task does a full workspace build for the null probe and for each oracle repeat (4 meson builds of a C
extension per hidden-test task at `--repeats 3`). There is no per-probe progress, so a long silent run is hard to
tell from a hang. Suggestions: a progress line per probe (`fix_x: null ... fail (41 s)`), and an option to reuse the
null workspace's build for the oracle repeats when the oracle only touches files outside `rebuild_globs`.

## 18. `author fix` does not tell you the base cannot be built

`author fix 6bde33e` scaffolded a task whose base cannot build with the current toolchain (Cython against NumPy
2.5's `__init__.pxd`); this only surfaced at `check` time as `[environment].setup failed (rc=1)`. The same holds for
30 of the 43 mined candidates (11 of the top 15): every base before aa9e5bc (#193, 2025-05-28). Suggestion: `author
mine --check-build` (or `author fix --verify`) that runs `[environment].setup` once at the candidate's base and
annotates or filters the list.

## 19. `author fix` copies files under `protected_globs` into `hidden/` without warning

For 6bde33e, `hidden/` received `mkl_fft/tests/third_party/scipy/test_basic.py`, which matches
`protected_globs = ["mkl_fft/tests/third_party/**"]`, and `targets` included it. The change in that file was only
comments and a reformatted skip. A note in `AUTHOR_NOTES.md` ("this hidden file is protected; is it needed?")
would have saved a step.

## 20. Playbook gaps for this kind of repository

- Phase 3 says "Narrow `targets` to the tests that fail before the fix", but gives no way to list them; see #6.
- Phase 6 says "Set tolerances per dtype from the project's own test helpers", but the default comparison is
  element-wise (`|got - want| <= atol + rtol * |want|`), which is the wrong metric for transforms (near-zero
  output coefficients make element-wise `rtol` meaningless). A sentence recommending norm-wise comparison for
  FFT/linear-algebra outputs, plus #9, would help.
- Phase 6 asks for NaN/Inf cases; NaN propagation differs between two *correct* FFT implementations at the
  real/imaginary-part level (MKL vs pocketfft), so the default `_special_ok` (per-part NaN positions) rejects the
  correct code. Worth a warning in the playbook, or a per-element option in the default comparator.
- The playbook's "fork" story is incomplete: on a fork branch, tasks should start from upstream commits, not from
  the fork's `HEAD` (which carries `.github/workflows/repoevals.yml` into every agent workspace). `author
  mutants` defaults to `HEAD`; say so in Phase 5 (`--base <upstream sha>`).

# Part 2: findings from running the full loop (orchestrator)

Collected while running `repoevals run`, `report`, `guidance suggest` and `--draft-with` on the 12 tasks above
(Claude Code 2.1.300, Sonnet 5 via Amazon Bedrock, Linux host, 2026-10-15). Ordered by impact.

## 21. `run --jobs N` with an editable install grades the wrong code (silent, wrong results)

First baseline attempt: `repoevals run ... --jobs 8`. Every workspace's `[environment].setup` ran
`pip install -e .` into the same environment, so pytest in one workspace imported another workspace's package:

```
import file mismatch:
imported module 'mkl_fft.tests.test_patch' has this __file__ attribute:
  .../fix_c2c_out_cast_or_padded_input/guidance_raw/r2/workspace/mkl_fft/tests/test_patch.py
which is not the same as the test file we want to collect:
  .../feature_patch_restore_unbalanced_warning/guidance_none/r0/workspace/mkl_fft/tests/test_patch.py
```

The runs were graded `fail`, not `error`, so the report would have shown real-looking pass rates. `cli.md` says
builds "must not share mutable state", but nothing enforces or detects it. Workaround used: six cloned conda
environments and six `repoevals run --jobs 1` processes on disjoint task sets writing to one `--out`.

Suggestions: refuse `--jobs > 1` when setup or build contain `pip install -e`/`--editable` unless the config
declares isolation; better, create a per-workspace venv (`python -m venv --system-site-packages`) and put it first
on PATH for setup, agent and graders; at minimum, have graders check that the package imports from inside the
workspace and mark the attempt `error` otherwise.

## 22. Agent environment scrubbing breaks Bedrock and Vertex users, and the failure is a slow silent hang

`DEFAULT_PASSTHROUGH` keeps only `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, `CLAUDE_CODE_OAUTH_TOKEN` and the OpenAI
and Gemini keys; `SECRET_ENV` removes every `AWS_*` and `*TOKEN*` variable. With `CLAUDE_CODE_USE_BEDROCK=1` kept
and `AWS_BEARER_TOKEN_BEDROCK`/`AWS_REGION` removed, Claude Code retries for minutes:

```
{"type":"system","subtype":"api_retry","attempt":8,"max_retries":10,"retry_delay_ms":32763,"error":"unknown",...}
```

`INFRA_PATTERNS` does not match this, so each attempt waits out the retries before being classified. Fix used:
`[environment].env_passthrough = ["AWS_BEARER_TOKEN_BEDROCK", "AWS_REGION", "ANTHROPIC_API_KEY"]`, machine-local and
not committed.

Suggestions: when `CLAUDE_CODE_USE_BEDROCK` or `CLAUDE_CODE_USE_VERTEX` is set, pass the matching credential
variables by default, or report it in `doctor`; document `env_passthrough` for Bedrock and Vertex in
`configuration.md`; treat repeated `api_retry` events as an infrastructure error.

## 23. `guidance suggest --draft-with claude-code` ignores `env_passthrough`

`llm_draft()` in `suggest.py` hard-codes `keep_env=["ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN",
"OPENAI_API_KEY", "HOME", "PATH"]`, so with item 22 fixed in the config the drafting agent still cannot reach
Bedrock:

```
RuntimeError: the drafting agent returned no JSON object of files (rc=1): Request timed out
```

Workaround: `--draft-with "cmd:<wrapper script that loads credentials and runs claude -p>"`. Suggestion: reuse the
agent environment logic of `agents.py` (`env_passthrough` and its defaults) and expose `--model` for drafting.

## 24. The workspace baseline commit force-adds gitignored build output

`git_commit()` in `util.py` runs `git add -A -f`, contradicting the comment in `workspace.py` ("ignored artifacts
stay untracked"). With a meson-python editable install, `build/cp312/` (object files, `.so`, generated `.c`)
becomes part of the workspace's only commit, and every later rebuild shows binaries as modified tracked files:

```
 M build/cp312/.ninja_deps
 M build/cp312/_pydfti.cpython-312-x86_64-linux-gnu.so
```

Consequences seen in the runs: agents spent turns on `git check-ignore`, `git stash` and `git log -- build/...`
(which the integrity checker then flagged as `history_mining`); `agent.diff` contains binary build files;
`files_changed` is inflated (12 files for a 2-file fix). Suggestion: commit the snapshot before running setup, or
drop `-f` so `.gitignore` applies, and exclude ignored paths from `agent.diff`.

## 25. Integrity checks have false positives that drown the real signal

51 of 72 graded runs had integrity findings. Causes:

- `protected_modified` on `mkl_fft/tests/third_party/**/__pycache__/*.pyc`, created by running the test suite.
  `__pycache__`, `*.pyc` and `.pytest_cache` should never count as modifications.
- `history_mining` on `git log --oneline -5`, `git stash push`, `git check-ignore`, `git diff --stat`. The workspace
  has one synthetic commit, so these reveal nothing. Flag only commands that can reach real history, for example
  `git` in the source checkout or `git fetch`.
- `test_tampering` on `pytest.skip(...)` inside parametrized tests the agent added to an existing test file. Skips
  in newly added test functions are not tampering; only skips or xfails added to pre-existing tests are.

The one real finding was `source_access`: an agent ran `cd <source checkout> && git log`, because without
`--docker` the source checkout is reachable. It was buried under the noise above.

## 26. `guidance suggest` produces mostly noise on this evidence

Of the 26 suggestions from 72 runs, most come from items 24 and 25 or from task selection:

| suggestion | why it is not actionable |
|---|---|
| `grep`, `find`, `cat`, `sed` "failed" in 2 to 5 runs | `grep` exit code 1 means "no match"; `find` or `cat` on a missing path is exploration, not a documentation gap |
| `git stash pop`, `git check-ignore` failed | caused by build files tracked in the workspace (item 24) |
| `protected_modified` happened in 78 runs | counts findings, not runs (78 is more than the 72 runs analysed); all are `.pyc` files (item 25) |
| `history_mining` / `test_tampering` "despite the guidance" | false positives (item 25), also counted in `guidance:none` runs, where there was no guidance to ignore |
| 55% of runs looked up `mkl_fft/_fft_utils.py` | three of the twelve tasks are about that file: a property of the task set, not a guidance gap |
| `.github/copilot-instructions.md` mentions `.c`, which does not exist | the text says `*.c.src` and "generated `.c` files"; the stale-reference parser takes a file extension for a path |
| `benchmarks/AGENTS.md` mentions `.asv/`, which does not exist | `.asv/` is a gitignored runtime directory, so it is correct that a checkout has none |

The useful one: "AGENTS.md exists but CLAUDE.md does not". Suggestions: ignore exit code 1 of `grep`, `rg` and
`diff`; count per run and per arm; skip commands on gitignored paths; weight "looked up before the first edit" by
the number of distinct tasks; treat only path-like tokens (containing `/` or a known file name) as references, and
skip gitignored paths.

## 27. No warning when the baseline is at the ceiling

Both arms passed 35 of 36 runs (0.972); paired difference +0.0, CI 0.0 to 0.0. At that ceiling
`guidance verify` cannot show an improvement, yet `guidance suggest` ends with
`next: repoevals guidance verify ... --repeats 5`. Suggestion: `report` and `suggest` warn when a configuration
passes more than about 90% of tasks ("tasks do not discriminate; add harder tasks before comparing guidance").
`check` could estimate difficulty with one cheap agent run per task.

## 28. `doctor` does not test the agent

`doctor` printed `ok    claude-code: ~/.local/bin/claude` while that CLI was "Not logged in" over
non-interactive SSH and too old for the model (`API Error: 400 Claude Code 2.1.217 does not support this model;
version 2.1.280 or newer is required`). Suggestion: `doctor --agent claude-code [--model M]` sends one trivial
prompt through the same code path and environment scrubbing as `run`; that would also have caught items 22 and 23.

## 29. `run` keeps going when every attempt fails with the same infrastructure error

With a broken PATH every attempt failed with `agent infrastructure error: agent CLI not found`, each after a full
workspace build. Suggestion: check that the agent executable exists before starting, and stop when the first
attempts all fail with the same infrastructure error.

## 30. No aggregate progress during `run`

`run` prints one line per finished attempt. A 72-attempt run gives no "n of N done", running cost or ETA.
Suggestion: a summary line every few attempts with pass, fail and error counts, cost so far and ETA.

## 31. Overlap with tasks already on the branch is not detected

Another authoring pass pushed 11 tasks to the same branch while this one ran. Three cover the same upstream changes
(#370 norm scaling, #288/#293 empty axes, and #180, which this pass dropped as unbuildable and the other pass made
buildable by pinning `Cython<3.3`). Suggestion: `validate` warns when two tasks share a base and have overlapping
`oracle.patch` files, and `author mine` marks candidates already used by an existing task.

## 32. The report hides the cost of guidance

`guidance:raw` cost $37.47 against $32.46 for `guidance:none` (+15%), with 20% more tokens and a 6% higher median
agent time, for the same pass rate. The paired-comparison table shows only the pass-rate difference. Suggestion:
add paired cost and time differences to it.
