# Forms and validation

WTForms turns submitted fields into a form object and validators reject missing, malformed, short, or mismatched values. `validate_on_submit()` means the request is POST and all validators passed.

A custom validator checks uniqueness against the database. Validation improves user experience, but it is not a replacement for database unique constraints: two requests can race, so production code should also handle an integrity error.

Always render `form.hidden_tag()`; it includes the CSRF token.
