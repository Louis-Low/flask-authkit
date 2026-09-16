# CSRF

Cross-site request forgery tricks a logged-in browser into submitting an action from another site. Flask-WTF places a secret token in each form and checks it on the server.

```html
<form method="post">{{ form.hidden_tag() }}</form>
```

The hidden tag is not decoration: without it, POST requests fail when CSRF is enabled. Do not disable CSRF in production; tests disable it only to keep test setup focused.
