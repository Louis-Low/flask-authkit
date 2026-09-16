# Database

SQLAlchemy lets Python code describe tables. `User` has a unique username and email, a password hash, timestamps, and an active flag. `db.session.add(user)` stages a record; `commit()` saves it.

The default SQLite URL is convenient locally. A PostgreSQL URL can be supplied through `DATABASE_URL` without rewriting models. In a larger application, use migrations (such as Alembic/Flask-Migrate) instead of relying on `create_all()`.

Never store passwords or reset tokens as ordinary columns in plaintext.
