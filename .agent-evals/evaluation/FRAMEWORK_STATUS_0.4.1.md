# Status against repoevals 0.4.1

The items below were found with repoevals 0.2.0 (a stale local checkout). Re-checked against 0.4.1 (`origin/main`):

| item | status in 0.4.1 | action |
|---|---|---|
| 5 setup failure shows no excerpt | fixed upstream | none |
| 12 note, 25 pycache and history-mining false positives | mostly fixed upstream (noise globs, local `git log` allowed, skips in new test files allowed) | none |
| 25 `pytest.skip` inside a new test function of an existing file | still flagged, and upstream tests (`test_skip_in_new_test_file_is_not_tampering_but_in_existing_is`) say it should be | design question: agents add parametrized tests with a runtime skip for unsupported cases |
| 15 decoy keyword matches anywhere in the file | WRONG: decoys already match the finding text only | retracted |
| 24 workspace commit force-adds build output | still present | fixed on branch `fix/dogfood-mkl-fft` |
| 14 spam probe too short to be graded | still present ("x issue" is 7 characters) | fixed on branch |
| 11 `max_ulp` 0 for complex | still present | fixed on branch |
| 21, 22, 23, 26, 27, 28, 29, 32, 33 | still present | fixed on branch |
| 6, 16 failing-test detail in `check --json` | still present | fixed on branch (`null_detail`, `oracle_detail`) |
| 8 crash versus test failure in `check` summary | still present | fixed on branch |
| 3 shared environment, 4 build env, 7, 9, 10, 13, 17, 18, 19, 20, 30, 31 | still present | follow-ups, not fixed |
| 34 (new) example review patch fails on git 2.43 | `examples/minisci/.../review_seeded_softmax/review.patch` has an empty `new file` header; `git apply` 2.43 says "header lacks filename information". 7 upstream tests fail on Ubuntu 24.04 git | follow-up |
