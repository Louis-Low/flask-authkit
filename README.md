# Flask AuthKit

Flask AuthKit is a reusable, production-oriented authentication foundation for Flask applications. It includes registration, secure password hashing, sessions, CSRF-protected forms, Brevo template-based email verification, welcome emails, password recovery, and protected views.

## Features

- Email/username login with mandatory email verification
- Registration, logout, remember-me sessions, and resend verification
- Flask-Bcrypt password hashing and Flask-Login current-user handling
- Flask-WTF CSRF protection and WTForms validation
- SQLite default with a PostgreSQL-compatible SQLAlchemy URL
- Brevo templates for verification, welcome, and password-reset emails
- Signed, expiring verification and password-reset tokens
- Responsive accessible UI and pytest coverage

## Quick start

```bash
git clone https://github.com/prajapatiHardik2008/Flask-LogIn-Page.git
cd Flask-LogIn-Page
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Configure a verified Brevo sender, API key, and the three template IDs in `.env`. See [docs/email-delivery.md](docs/email-delivery.md).

## Routes

| Route | Purpose |
|---|---|
| `/register` | Create an account and send verification + welcome messages |
| `/verify-email/<token>` | Verify an email address |
| `/resend-verification` | Send a fresh verification message |
| `/login` | Sign in only after verification |
| `/forgot-password` | Request a Brevo password-reset message |
| `/reset-password/<token>` | Set a new password |
| `/logout` | End a session |
| `/profile` | Protected example page |

## Architecture

`app/routes/auth.py` owns account flows, `models.py` stores the verification state, and `app/services/email.py` contains the Brevo adapter. Brevo template IDs and secrets are environment configuration, while token creation remains server-side.

## Security

Passwords are hashed, forms use CSRF, cookies use secure defaults, tokens are signed and time-limited, login requires verification, and recovery/verification responses avoid identifying accounts. Add rate limiting, MFA, security headers, migrations, and monitoring before production. Read [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
