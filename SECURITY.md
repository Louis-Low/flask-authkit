# Security notes

AuthKit is a teaching and reuse-oriented foundation, not a guarantee of complete security. Review it against your threat model before deploying.

## Included protections

- Passwords are processed with Flask-Bcrypt and only the resulting hash is stored.
- Flask-WTF adds a CSRF token to state-changing forms.
- Flask-Login manages the authenticated user and login is blocked until `email_verified` is true.
- Verification and password-reset tokens are signed and time-limited.
- Brevo API credentials and template IDs are loaded from environment variables.
- Verification/resend/recovery messages avoid revealing whether an email exists.

## Production checklist

- Set a long random `SECRET_KEY` and `BREVO_API_KEY` outside source control.
- Verify the Brevo sender/domain and configure real template IDs; do not leave sample IDs in production.
- Add rate limiting to login, verification resend, and password recovery routes.
- Add database migrations before deploying the new `email_verified` column to an existing database.
- Use HTTPS, secure cookies, a production WSGI server, backups, monitoring, MFA, and security headers.
- Never log reset URLs, verification URLs, passwords, API keys, or secrets.

## Reporting vulnerabilities

Do not disclose a suspected vulnerability in a public issue. Contact the repository owner privately with reproduction steps, impact, and a safe contact method.
