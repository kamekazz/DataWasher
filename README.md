# DataWasher

A simple Flask application skeleton.

Authentication is backed by a Heroku Postgres database.  Users can be created from
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

## Environment variables

The application relies on a few environment variables:

- `SECRET_KEY` &mdash; secret key used by Flask for session management.
- `DEBUG` &mdash; set to `1` to enable debug mode when running locally.
- `HOST` &mdash; hostname to bind the development server to.
- `PORT` &mdash; port number for the server (defaults to `5000`).
- `DATABASE_URL` &mdash; SQLAlchemy database URI. If unset, the application
  falls back to `sqlite:///data.db`. Heroku sets this variable automatically
  when a Postgres addon is attached.

For local development, create a `.env` file in the project root and define
these variables. The app uses **python-dotenv** to load them automatically
when `app.py` is executed.

## Running the app locally

Install the dependencies. To use SQLite instead of Postgres, set the database
URL and then start the server:

```bash
pip install -r requirements.txt
export DATABASE_URL=sqlite:///data.db  # optional
python app.py
```

The server will launch using the environment variables described above.

## Deploying to Heroku

The repository contains a `Procfile` configured for Heroku:

```Procfile
web: gunicorn app:app
```

Create a Heroku application, set the required environment variables (such as
`SECRET_KEY`) and push the code. Heroku will run the command from the Procfile
to serve the application.

## Database schema

The `User` model stores password hashes using Werkzeug's
`generate_password_hash` which can produce strings longer than 128
characters. The `password_hash` column therefore uses `String(255)` to
avoid truncation errors when inserting new users.
