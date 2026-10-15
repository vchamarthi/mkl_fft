# AGENTS.md  -  mkl_fft

Entry point for agent context in this repo.

## What this project is
`mkl_fft` is a NumPy/SciPy-compatible FFT interface backed by Intel® oneMKL.
It provides accelerated FFT transforms while aiming to preserve upstream API behavior.

## Key components
- **Package:** `mkl_fft/`
- **Cython bindings:** `mkl_fft/_pydfti.pyx`
- **Template-based C backend:** `mkl_fft/src/*.c.src`
- **Interface adapters:** `mkl_fft/interfaces/`
- **Tests:** `mkl_fft/tests/`
- **Vendored helpers:** `_vendored/`
- **Packaging:** `conda-recipe/`, `conda-recipe-cf/`
- **Benchmarks:** `benchmarks/`

## Build/runtime basics
- Build system: `pyproject.toml` + `meson.build`
- Build deps: `cython>=3.1.0`, `numpy`, `mkl-devel`, `meson-python`, `cmake`, `ninja`
- Runtime deps: `numpy`, `mkl-service`

## Development guardrails
- Preserve NumPy/SciPy FFT API compatibility unless change is explicitly requested.
- Edit template sources (`*.c.src`), not generated C artifacts.
- Pair behavior changes with tests and keep diffs minimal.
- If interface-level patching/wrapping behavior is changed, keep it explicit, reversible, and documented.
- Avoid hardcoding mutable versions/matrices/channels in docs.

## Where truth lives
- Build/config: `pyproject.toml`, `meson.build`
- Dependencies: `pyproject.toml`, `conda-recipe*/meta.yaml`
- CI/workflows: `.github/workflows/*.{yml,yaml}`
- Public API: `mkl_fft/__init__.py`, `mkl_fft/interfaces/` (including wrapper/patch adapter modules)
- Tests: `mkl_fft/tests/`

For behavior policy, see `.github/copilot-instructions.md`.

## Directory map
Use nearest local `AGENTS.md` when present:
- `.github/AGENTS.md`  -  CI workflows and automation policy
- `mkl_fft/AGENTS.md`  -  package-level implementation context
- `mkl_fft/interfaces/AGENTS.md`  -  NumPy/SciPy interface adapters
- `mkl_fft/src/AGENTS.md`  -  C template backend rules
- `mkl_fft/tests/AGENTS.md`  -  test scope/conventions
- `conda-recipe/AGENTS.md`  -  Intel-channel conda packaging
- `conda-recipe-cf/AGENTS.md`  -  conda-forge recipe context
- `_vendored/AGENTS.md`  -  vendored tooling boundaries
- `benchmarks/AGENTS.md`  -  ASV performance suite

## Notes from evaluation runs

- TODO: `git stash pop` failed in 5 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `grep` failed in 5 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `git check-ignore` failed in 3 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `python -I` failed in 3 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `cat` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `find` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `pip install` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: `sed` failed in 2 run(s): document the correct way to run it (arguments, environment variables, working directory).
- TODO: 55% of runs looked up `mkl_fft/_fft_utils.py` before changing anything: say where things are and what they are for, so agents do not have to rediscover it.
- TODO: `protected_modified` happened in 78 run(s) despite the guidance: state the rule explicitly and say why it matters.
- TODO: `history_mining` happened in 8 run(s) despite the guidance: state the rule explicitly and say why it matters.
- TODO: `test_tampering` happened in 6 run(s) despite the guidance: state the rule explicitly and say why it matters.
- TODO: `source_access` happened in 1 run(s) despite the guidance: state the rule explicitly and say why it matters.
- TODO: `.github/copilot-instructions.md` mentions `.c`, which does not exist: update or remove it.
- TODO: `benchmarks/AGENTS.md` mentions `.asv/`, which does not exist: update or remove it.
- TODO: `mkl_fft/src/AGENTS.md` mentions `.c`, which does not exist: update or remove it.
- TODO: AGENTS.md exists but CLAUDE.md does not: Claude Code may not read the guidance. Add a CLAUDE.md that imports it (`@AGENTS.md`).
