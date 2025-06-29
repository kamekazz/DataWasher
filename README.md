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

## Environment variables

The application relies on a few environment variables:

- `SECRET_KEY` &mdash; secret key used by Flask for session management.
- `DEBUG` &mdash; set to `1` to enable debug mode when running locally.
- `HOST` &mdash; hostname to bind the development server to.
- `PORT` &mdash; port number for the server (defaults to `5000`).
- `DATABASE_URL` &mdash; optional SQLAlchemy database URI. If absent, a local
  SQLite database is used. Heroku populates this when a Postgres addon is
  attached.

For local development, create a `.env` file in the project root and define
these variables. Load them into your shell before starting the app so `app.py`
can read them via `os.getenv`.

## Running the app locally

Install the dependencies and start the server:

```bash
pip install -r requirements.txt
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
