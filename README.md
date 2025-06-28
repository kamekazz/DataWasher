# DataWasher

A simple Flask application skeleton.

The project now contains a very small authentication system.  Users can log in
using the credentials `admin` / `secret`.  When logged in a session cookie is
set and the **Dashboard** and **1‑Hour Report** pages become available.  Logging
out clears the session and redirects back to the login page.

## Template structure

HTML templates are organized under `templates/`:

```
templates/
    pages/      # individual page templates
    elements/   # reusable elements such as header and footer
```
