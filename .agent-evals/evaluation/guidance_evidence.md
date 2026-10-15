# Guidance evidence

72 graded runs; agents: claude-code; arms: guidance:none, guidance:raw.
Guidance files: .agent-evals/evaluation/guidance_draft_llm/AGENTS.md, .agent-evals/evaluation/guidance_draft_llm/CLAUDE.md, .agent-evals/evaluation/guidance_draft_llm/benchmarks/AGENTS.md, .agent-evals/evaluation/guidance_draft_llm/mkl_fft/AGENTS.md, .agent-evals/evaluation/guidance_draft_llm/mkl_fft/src/AGENTS.md, .agent-evals/evaluation/guidance_draft_llm/mkl_fft/tests/AGENTS.md, .github/AGENTS.md, .github/copilot-instructions.md, AGENTS.md, _vendored/AGENTS.md, benchmarks/AGENTS.md, conda-recipe/AGENTS.md, conda-recipe-cf/AGENTS.md, mkl_fft/AGENTS.md, mkl_fft/interfaces/AGENTS.md, mkl_fft/src/AGENTS.md, mkl_fft/tests/AGENTS.md.

## Suggestions

- `git stash pop` failed in 5 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `grep` failed in 5 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `git check-ignore` failed in 3 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `python -I` failed in 3 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `cat` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `find` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `pip install` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- `sed` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- 56% of runs looked up `mkl_fft/_fft_utils.py` before changing anything: say where things are and what they are for, so agents do not have to rediscover it.
- `protected_modified` happened in 78 run(s) despite the guidance: state the rule explicitly and say why it matters.
- `history_mining` happened in 8 run(s) despite the guidance: state the rule explicitly and say why it matters.
- `test_tampering` happened in 6 run(s) despite the guidance: state the rule explicitly and say why it matters.
- `source_access` happened in 1 run(s) despite the guidance: state the rule explicitly and say why it matters.
- `.agent-evals/evaluation/guidance_draft_llm/AGENTS.md` mentions `.c.src`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/AGENTS.md` mentions `.h`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/AGENTS.md` mentions `.pyx`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/AGENTS.md` mentions `_pydfti.c`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/AGENTS.md` mentions `build/<tag>/`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/benchmarks/AGENTS.md` mentions `benchmarks/__init__.py`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/mkl_fft/AGENTS.md` mentions `interfaces/`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/mkl_fft/src/AGENTS.md` mentions `build/<tag>/mklfft.c`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/mkl_fft/tests/AGENTS.md` mentions `third_party/numpy/`, which does not exist: update or remove it.
- `.agent-evals/evaluation/guidance_draft_llm/mkl_fft/tests/AGENTS.md` mentions `third_party/scipy/`, which does not exist: update or remove it.
- `.github/copilot-instructions.md` mentions `.c`, which does not exist: update or remove it.
- `benchmarks/AGENTS.md` mentions `.asv/`, which does not exist: update or remove it.
- `mkl_fft/src/AGENTS.md` mentions `.c`, which does not exist: update or remove it.

## Failing commands

| item | runs | share | sample_output |
|---|---|---|---|
| git stash pop | 5 | 0.07 | hem before you merge. Aborting On branch main Changes not staged for commit:   (use "git add <file>..." to update what will be committed)   (use "git restore <f |
| grep | 5 | 0.07 | Exit code 2 11:        'buildtype=release', 29:c_args = ['-DNDEBUG'] 73:    c_args: c_args + [ |
| git check-ignore | 3 | 0.04 | Exit code 1 # CMake build and local install directory build/ mkl_fft.egg-info/  # Byte-compiled / optimized / DLL files __pycache__/  # Virtual environments, te |
| python -I | 3 | 0.04 | =-1, fsc=fsc)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   File "mkl_fft/_pydfti.pyx", line 504, in mkl_fft._pydfti._c2c_fft1 |
| cat | 2 | 0.03 | Exit code 1 |
| find | 2 | 0.03 | ll     args: ["-L", "nd"]  # ignore "nd" used for n-dimensional     additional_dependencies:     - tomli  - repo: https://github.com/psf/black   rev: 26.5.1   h |
| pip install | 2 | 0.03 | ctory) 	modified:   build/cp312/.ninja_deps 	modified:   build/cp312/.ninja_log 	modified:   build/cp312/meson-logs/meson-log.txt 	modified:   build/cp312/meson |
| sed | 2 | 0.03 | Exit code 1 sed: -e expression #1, char 5: missing command |

## Rediscovered before the first edit

| item | runs | share |
|---|---|---|
| mkl_fft/_fft_utils.py | 40 | 0.56 |
| mkl_fft/_mkl_fft.py | 28 | 0.39 |
| mkl_fft/_pydfti.pyx | 22 | 0.31 |
| $ grep -80 | 21 | 0.29 |
| mkl_fft/tests/test_fft1d.py | 19 | 0.26 |
| mkl_fft/tests/test_fftnd.py | 15 | 0.21 |
| $ find . -50 | 14 | 0.19 |
| $ grep -40 | 14 | 0.19 |
| $ find . 2>/dev/null | 12 | 0.17 |
| $ grep -60 | 12 | 0.17 |

## Rule violations with guidance

| check | runs |
|---|---|
| protected_modified | 78 |
| history_mining | 8 |
| test_tampering | 6 |
| source_access | 1 |

## Stale references

| file | claim |
|---|---|
| .agent-evals/evaluation/guidance_draft_llm/AGENTS.md | .c.src |
| .agent-evals/evaluation/guidance_draft_llm/AGENTS.md | .h |
| .agent-evals/evaluation/guidance_draft_llm/AGENTS.md | .pyx |
| .agent-evals/evaluation/guidance_draft_llm/AGENTS.md | _pydfti.c |
| .agent-evals/evaluation/guidance_draft_llm/AGENTS.md | build/<tag>/ |
| .agent-evals/evaluation/guidance_draft_llm/benchmarks/AGENTS.md | benchmarks/__init__.py |
| .agent-evals/evaluation/guidance_draft_llm/mkl_fft/AGENTS.md | interfaces/ |
| .agent-evals/evaluation/guidance_draft_llm/mkl_fft/src/AGENTS.md | build/<tag>/mklfft.c |
| .agent-evals/evaluation/guidance_draft_llm/mkl_fft/tests/AGENTS.md | third_party/numpy/ |
| .agent-evals/evaluation/guidance_draft_llm/mkl_fft/tests/AGENTS.md | third_party/scipy/ |
| .github/copilot-instructions.md | .c |
| benchmarks/AGENTS.md | .asv/ |
| mkl_fft/src/AGENTS.md | .c |
