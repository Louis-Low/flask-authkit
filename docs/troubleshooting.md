# Troubleshooting

**CSRF failed:** render `form.hidden_tag()` and do not reuse a stale page after restarting with a new secret. **Import errors:** activate `.venv` and reinstall requirements. **Database locked:** stop duplicate development processes. **Login always fails:** check that registration committed and that email comparison is lowercase. **Reset link unavailable:** AuthKit shows a development-only preview; production needs email delivery.

For unknown issues, inspect the Flask traceback locally, verify environment variables, and run `pytest -q`.
