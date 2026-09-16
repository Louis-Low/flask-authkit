# Flask basics

Flask maps a URL to a Python function:

```python
@app.get('/hello')
def hello():
    return render_template('hello.html')
```

`@app.get` registers the route, and the function returns a response. Jinja templates turn Python data into HTML. A blueprint is a group of related routes; AuthKit's `auth_bp` keeps account routes separate. A request is what the browser sends; a response is what Flask sends back.

Common mistake: changing a route to POST only while linking to it with a normal GET link.
