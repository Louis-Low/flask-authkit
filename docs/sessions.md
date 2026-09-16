# Sessions

HTTP does not remember previous requests. A session gives the browser a signed cookie that lets Flask recognize continuity. Flask-Login stores the authenticated user ID in that session. “Remember me” uses a separate persistent cookie so a user can return later.

AuthKit sets HTTP-only and SameSite cookie attributes. HTTP-only prevents JavaScript from reading cookies; Secure (enable it in production) requires HTTPS. Keep the secret key private because it protects cookie signatures.
