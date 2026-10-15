# Guidance evidence

16 graded runs; agents: claude-code; arms: guidance:none, guidance:raw.
Guidance files: .github/AGENTS.md, .github/copilot-instructions.md, AGENTS.md, _vendored/AGENTS.md, benchmarks/AGENTS.md, conda-recipe/AGENTS.md, conda-recipe-cf/AGENTS.md, mkl_fft/AGENTS.md, mkl_fft/interfaces/AGENTS.md, mkl_fft/src/AGENTS.md, mkl_fft/tests/AGENTS.md.

## Suggestions

- In 5 run(s): `timeout` is not available on the machine agents run on: name the right tool or how to install it.
- 75% of runs looked up `mkl_fft/_fft_utils.py` before changing anything: say where things are and what they are for, so agents do not have to rediscover it.
- 69% of runs looked up `mkl_fft/tests` before changing anything: say where things are and what they are for, so agents do not have to rediscover it.
- 50% of runs looked up `AGENTS.md` before changing anything: say where things are and what they are for, so agents do not have to rediscover it.
- 50% of runs looked up `mkl_fft/_mkl_fft.py` before changing anything: say where things are and what they are for, so agents do not have to rediscover it.
- `benchmarks/AGENTS.md` mentions `.asv/`, which does not exist: update or remove it.
- AGENTS.md exists but CLAUDE.md does not: Claude Code may not read the guidance. Add a CLAUDE.md that imports it (`@AGENTS.md`).

## Environment problems

| item | runs | share |
|---|---|---|
| `timeout` is not available on the machine agents run on: name the right tool or how to install it | 5 | 0.31 |

## Rediscovered before the first edit

| item | runs | share |
|---|---|---|
| mkl_fft/_fft_utils.py | 12 | 0.75 |
| mkl_fft/tests | 11 | 0.69 |
| AGENTS.md | 8 | 0.5 |
| mkl_fft/_mkl_fft.py | 8 | 0.5 |
| mkl_fft/__init__.py | 7 | 0.44 |
| mkl_fft/tests/test_fftnd.py | 6 | 0.38 |
| CHANGELOG.md | 5 | 0.31 |
| mkl_fft/AGENTS.md | 5 | 0.31 |
| mkl_fft/patch.py | 5 | 0.31 |
| mkl_fft/tests/AGENTS.md | 5 | 0.31 |

## Stale references

| file | claim |
|---|---|
| benchmarks/AGENTS.md | .asv/ |
