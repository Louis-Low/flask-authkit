# Authentication flow

The login path is:

```text
Browser → login form → WTForms validation → database user → bcrypt check → Flask-Login → session → protected page
```

The form checks shape and required fields. The database lookup finds a user. Bcrypt compares the submitted password with the stored hash. `login_user(user)` tells Flask-Login who is authenticated, and the browser receives a session cookie.

A failed lookup and a wrong password intentionally produce the same message. This prevents account enumeration. Registration follows the same pattern but stores only a hash.
