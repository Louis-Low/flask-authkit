# Password hashing

A hash is a one-way representation: the application can check a password without being able to read it back. Bcrypt also adds a salt and work factor, making guessing expensive.

```python
user.set_password(form.password.data)
if user.check_password(form.password.data):
    login_user(user)
```

The first line creates the hash; the second compares safely. Never use plain SHA-256 for passwords, never log passwords, and never compare hashes by hand.
