# Agent guidance: measured effect and recommended changes

Baseline: 12 draft tasks, Claude Code with Sonnet 5, 3 repeats per arm, run on 2026-10-15
(`baseline_report.md`).

| arm | pass rate | cost | tokens | median agent time |
|---|---|---|---|---|
| `guidance:none` | 35/36 (0.972) | $32.46 | 678,548 | 225 s |
| `guidance:raw` (current AGENTS.md files) | 35/36 (0.972) | $37.47 | 815,377 | 239 s |

The current guidance changes no outcome on these tasks and costs about 15% more. Both failures are the same
seeded-review task, where the agent flagged decoy `D1_real_ignored`. The tasks are at the ceiling for this model, so
this run cannot show whether any guidance change helps; `guidance verify` was not run for that reason.

## Files in this directory

| file | content |
|---|---|
| `guidance_evidence.md` | `repoevals guidance suggest` output for all 72 runs |
| `guidance_draft_deterministic_AGENTS.md` | the framework's default draft: current AGENTS.md plus a TODO list |
| `guidance_draft_llm/` | draft written by Claude Opus 5.5 from the evidence (`--draft-with`) |
| `repoevals.used.toml` | the config used for these runs (setup with MKLROOT and a libmkl_rt symlink) |

## Recommended changes

Ranked by evidence. The drafts' file and symbol references were checked against the tree.

1. Add `CLAUDE.md` containing `@AGENTS.md` at the root. Claude Code reads `CLAUDE.md`, not `AGENTS.md`. This is the
   only suggestion from `guidance suggest` that held up. It may also explain why the raw arm changed nothing.
2. Add a code map to the root `AGENTS.md`: public API in `__init__.py`, then `_mkl_fft.py` (norm scale), then
   `_fft_utils.py` (N-D logic), `_pydfti.pyx` (1-D and out validation), and `src/mklfft.c.src`. More than half of the
   runs read `_fft_utils.py` before their first edit. The LLM draft has this section.
3. State that editable installs rebuild on `import mkl_fft`, that build output (including generated `mklfft.c`)
   lives in gitignored `build/<tag>/`, and how to check that `mkl_fft.__file__` points into the checkout. Agents
   spent turns on build files (partly a framework artifact, see FRAMEWORK_FEEDBACK item 24).
4. Say explicitly in root `AGENTS.md` and `mkl_fft/tests/AGENTS.md`: never modify `mkl_fft/tests/third_party/**`,
   and never skip, xfail or loosen existing tests.
5. Shorten `.github/copilot-instructions.md`, which repeats root `AGENTS.md`.

Not recommended, although the framework suggested them: documenting `grep`, `find`, `cat`, `sed`, `git stash` or
`git check-ignore` usage, and the "stale" `.c` and `.asv/` references. These are false positives (see
FRAMEWORK_FEEDBACK items 25 and 26).

Before adopting, review `guidance_draft_llm/` for task hints. One borderline phrase: "`_float_utils.py` (float16
upcast / float128 downcast)" points toward the `numeric_numpy_iface_longdouble` task.

## To prove a change helps

Add harder tasks first, or use a weaker model, until the `guidance:none` pass rate is clearly below 0.9. Then:

```bash
repoevals guidance verify <draft dir> --agent claude-code --repeats 5 --exclude-tasks-in <evidence runs>
```
