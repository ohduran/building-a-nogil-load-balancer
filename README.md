# Building a NoGIL Load Balancer in 30 Minutes

The code for the talk presented at 2025 PyCon.

I used `pyenv` to switch between the normal build and the free-threaded (NoGIL) builds of Python.

- [Install pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#a-getting-pyenv)
- Run `pyenv install 3.14.0b1 3.14.0b1t`
- Wait (good things take time)
- You can now switch between one build or the other by running either `pyenv local 3.14.0b1` or `pyenv local 3.14.0b1t`.
- Feel free to test it out with `threaded_fibonacci.py`. See the docs in the file for more.
