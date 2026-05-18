uv python list
uv python pin 3.14
uv sync
Remove-Item .python-version -ErrorAction SilentlyContinue
requires-python = ">=3.12"   # Change to ">=3.14" or remove it
uv python pin 3.14
REM in dev use uv, for running just plain py ...
REM like: py vibrations_simulator_pro.py