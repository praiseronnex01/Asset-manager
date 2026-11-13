# Asset Management System

A web application built with Python (Flask) and SQLite for tracking, analyzing, and managing asset portfolios, user accounts, and activity logs.

## Features

- **Dashboard & Analytics**: Dynamic interactive charts powered by Chart.js (Asset Count, Valuation, Monthly Spend, Category breakdowns).
- **Asset Lifecycle Management**: Add, view, edit, and delete assets with quantity, unit valuation, total portfolio value calculation, and useful life tracking.
- **User Authentication**: Secure signup and login using Werkzeug password hashing.
- **Role-Based Access Control**: Standard Users and Administrators.
- **Admin Management Portal**: Search, monitor live online users, track detailed activity logs (24h history), suspend/unsuspend accounts, and delete users safely.
- **Password Reset**: Mobile SMS reset code integration with 15-minute verification token expiry.
- **Notifications & Messages**: In-app notifications and real-time direct messaging between registered users.
- **Theme & Profile Preferences**: Support for Light / Dark modes and custom profile image uploads.

## Prerequisites & Installation

1. **Python 3.9+** installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the local web server:

```bash
python run.py
```
Or run directly:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## Initial Setup & Credentials

- **Database**: Automatically created (`assets.db`) on first launch.
- **Default Admin Registration Code**: `ADMIN2026` (configurable via `ADMIN_SIGNUP_CODE` environment variable).
- **Secret Key**: Set `SECRET_KEY` in environment variables for production.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `asset-management-secret` | Flask session secret key |
| `ADMIN_SIGNUP_CODE` | `ADMIN2026` | Verification code required for registering Admin accounts |
| `HOST` | `127.0.0.1` | Web server host address |
| `PORT` | `5000` | Web server listening port |
