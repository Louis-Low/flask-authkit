# Flask-Login

Flask-Login remembers the current user after `login_user(user)`. `current_user` is available in routes and templates. The `user_loader` in `app/__init__.py` reloads a user from the session's ID.

```python
@app.get('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
```

The decorator checks authentication before the function runs. Without it, anyone could open the page. Common mistake: forgetting `UserMixin` or the `user_loader` callback.
