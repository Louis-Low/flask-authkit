# Getting started

A virtual environment keeps this project's packages separate from other Python projects. Run `python -m venv .venv`, activate it, then `pip install -r requirements.txt`. Copy `.env.example` to `.env`; this is where local configuration lives. Finally run `python run.py` and visit `http://127.0.0.1:5000`.

`SECRET_KEY` signs sessions and reset tokens, so replace the example value. `DATABASE_URL=sqlite:///authkit.db` creates a local file. Run `pytest` to execute the automated tests.

Never commit `.env` or the database file.
