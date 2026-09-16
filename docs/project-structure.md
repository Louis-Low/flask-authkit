# Project structure

`app/__init__.py` creates the Flask application and connects extensions. `models.py` describes database data. `routes/auth.py` contains account actions; `routes/main.py` contains example application pages. `forms/auth_forms.py` validates submitted fields. Templates render HTML and static files provide CSS/JavaScript.

This separation matters: a route decides what should happen, a form checks input, a model stores data, and a template displays results. It prevents one giant file and makes the auth module easier to copy.
