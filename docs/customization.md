# Customization

To add a display name, add a nullable model column, a form field, and a template field. To protect a new page, use `@login_required`. To change branding, edit `base.html` and `static/css/app.css`.

For real recovery email, create a mail service adapter around `_reset_token()` and send the URL through a provider. Keep token creation in server code and never expose it in logs. Add migrations before changing deployed tables.
