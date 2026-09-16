# Deployment

Use a production WSGI server such as Gunicorn behind HTTPS; do not expose `python run.py`. Set a strong secret through the host's secret manager, use PostgreSQL, enable secure cookies, and configure backups.

Before launch, add migrations, rate limiting, email delivery, security headers, observability, dependency updates, and a vulnerability-reporting process. Set `DEBUG` false and confirm errors do not reveal stack traces or account existence. Test password reset and logout in the deployed environment.
