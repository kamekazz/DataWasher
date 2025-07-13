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

Authenticated users can either enter a single FedEx tracking number or upload a CSV file on the **Track Shipments** page. When uploading, the file must contain a column named "Tracking Number". The app reads every value in that column, fetches the status for each from the FedEx Track API, and displays a table with "Tracking Number" and "Status" columns.

### FedEx API configuration

1. Sign up at the [FedEx Developer Portal](https://developer.fedex.com/) and create an application.
2. Enable the *Track* service for the app and note the provided **Client ID** and **Client Secret**.
3. Set environment variables `FEDEX_CLIENT_ID` and `FEDEX_CLIENT_SECRET` with these credentials before running the application.
4. When a tracking number or file is submitted, the app obtains an OAuth token and calls `https://apis.fedex.com/track/v1/trackingnumbers` to fetch statuses.

## Live Camera Streaming

Set `CAMERA_IP` and `CAMERA_PASS` in a `.env` file to connect to the Reolink RTSP stream. Start the application using `./start-services.sh` and visit `/stream` to see the real-time video with barcode overlays. Use the on-page controls to start or stop detection. Each detected pallet is logged with timestamp and position.

