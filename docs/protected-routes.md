# Protected routes

A protected route is a page that requires a signed-in user:

```python
from flask_login import login_required, current_user

@app.get('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
```

The decorator redirects anonymous visitors to the configured login view. `current_user` is the authenticated model object. Always enforce authorization on the server; hiding a navigation link is not protection.
