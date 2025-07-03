# DataWasher

A simple Flask application skeleton.

Authentication is backed by a small SQLite database.  Users can be created from
the **Create User** page and then sign in using the login form.  Once
authenticated the **Dashboard** and **1‑Hour Report** pages become available.
Logging out clears the session and redirects back to the login page.

The **1‑Hour Report** page now displays two summary tables when a CSV file is
uploaded.  The first table, **Tasks Per Transaction**, sums the ``No. Of task
details`` column for all rows.  A second table, **Assigned Status Tasks Per
Transaction**, summarises only those rows where the ``Status`` column value is
``Assigned`` and shows the count of transactions per type.

## Template structure

HTML templates are organized under `templates/`:

```
templates/
    pages/      # individual page templates
    elements/   # reusable elements such as header and footer
```

## Styling

The application includes a small custom CSS file under `static/styles/`. A color palette is defined in `static/styles/color-palette.css` using CSS variables. Import this file in your styles to access consistent colors across the UI. The templates already apply these variables via helper classes in `custom.css` to color links and tables.

## Shipment Tracking

Authenticated users can upload a CSV file containing FedEx tracking numbers on the **Track Shipments** page. The application reads the "Tracking Number" column, fetches the status for each number from the FedEx Track API, and shows the same table with a new "Status" column.

### FedEx API configuration

1. Sign up at the [FedEx Developer Portal](https://developer.fedex.com/) and create an application.
2. Enable the *Track* service for the app and note the provided **Client ID** and **Client Secret**.
3. Set environment variables `FEDEX_CLIENT_ID` and `FEDEX_CLIENT_SECRET` with these credentials before running the application.
4. When a file is uploaded, the app obtains an OAuth token and calls `https://apis.fedex.com/track/v1/trackingnumbers` to fetch statuses.

