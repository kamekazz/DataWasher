# DataWasher

A simple Flask application skeleton.

Authentication is backed by a small SQLite database.  Users can be created from
the **Create User** page and then sign in using the login form.  Once
authenticated the **Dashboard** and **1‑Hour Report** pages become available.
Logging out clears the session and redirects back to the login page.

## Template structure

HTML templates are organized under `templates/`:

```
templates/
    pages/      # individual page templates
    elements/   # reusable elements such as header and footer
```
