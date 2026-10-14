# Author notes: review_replay_319

PR: https://github.com/IntelPython/mkl_fft/pull/319 — task: module CLI patching methods
Reviewed revision: abc566e188d48f8233ccde2e794398359d55a7de
Base: 38ed4cf9a1ede61bc2b73d45b58966d33efb9d4a

Edit gold.json: keep threads that ask for a change; remove praise, questions answered by the author, and
pure nits. Each remaining thread is a finding a good reviewer should make.

- `mkl_fft/__main__.py:28` (ndgrigorian): "I think we should use argparse here, dpctl is a good example\nhttps://github.com/IntelPython/dpctl/blob/master/dpctl/__main__.py\n\nit's a bit cleaner"
- `mkl_fft/patch.py:51` (antonwolfy): 'I guess it would be proper to have that as a warning, rather then default trace to the console.'
- `mkl_fft/patch.py:61` (antonwolfy): 'I believe it should be only traced under verbose mode'
- `mkl_fft/tests/test_cli.py:58` (antonwolfy): 'It should be warning raised at second installation and then we will verify that here through appropriate pytest i/f.'
- `mkl_fft/__main__.py:43` (antonwolfy): 'Why do we need the second `python` in the command? Is there any use case when we will run something different from python file?'
- `mkl_fft/tests/test_cli.py:61` (antonwolfy): 'Do we have a better way to check the patch is enabled through importing mkl_fft and checking `mkl_fft.is_patched()` result?'
- `mkl_fft/_patch_startup.py:1` (antonwolfy): 'Should we use the current year for new files?\n```suggestion\n# Copyright (c) 2026, Intel Corporation\n```'
- `mkl_fft/patch.py:63` (antonwolfy): 'Would it be better to handle through raising an exception?'
