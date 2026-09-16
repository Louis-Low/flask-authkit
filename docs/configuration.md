# Configuration

`.env` is loaded by `python-dotenv`. `SECRET_KEY` signs sessions and verification/reset tokens. `DATABASE_URL` selects SQLite or PostgreSQL. `SESSION_COOKIE_SECURE` should be true when the app is served over HTTPS.

Brevo uses `BREVO_API_KEY`, `MAIL_FROM_EMAIL`, and `MAIL_FROM_NAME`. The three template IDs tell Brevo which design to render:

- `BREVO_EMAIL_VERIFICATION_TEMPLATE_ID`
- `BREVO_WELCOME_TEMPLATE_ID`
- `BREVO_PASSWORD_RESET_TEMPLATE_ID`

Keep credentials out of Git, rotate compromised secrets, and use your deployment platform's secret manager. A secret in a client-side file is not secret.
