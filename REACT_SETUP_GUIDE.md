# Asset Management System - Setup Guide

This guide will help you set up and run the complete Asset Management System with React frontend and Flask backend.

## Project Structure

```
Asset Management/
├── perpex/                 # Flask backend
│   ├── app.py             # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── ...
├── frontend/              # React frontend (NEW)
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── ...
├── templates/             # HTML templates (legacy, kept for reference)
└── static/                # Static files (legacy, kept for reference)
```

## Prerequisites

- **Python 3.8+** - For Flask backend
- **Node.js 16+** - For React frontend
- **MySQL** - Database
- **Git** (optional)

## Installation & Setup

### Step 1: Set up the Flask Backend

1. Navigate to the backend directory:
```bash
cd perpex
```

2. Create a virtual environment (if not already created):
```bash
python -m venv ..\.venv
```

3. Activate the virtual environment:
```bash
# Windows
..\.venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Configure MySQL Database

1. Ensure MySQL is running
2. Create the database:
```sql
CREATE DATABASE IF NOT EXISTS asset_management;
USE asset_management;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(20) UNIQUE,
    reset_token VARCHAR(50),
    reset_token_expiry DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create assets table
CREATE TABLE IF NOT EXISTS assets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    property_type VARCHAR(100),
    purchase_date DATE,
    value DECIMAL(10, 2),
    total_usage_hours INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active',
    maintenance_needed BOOLEAN DEFAULT FALSE,
    last_maintenance DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

3. Set environment variables (optional):
```bash
# Windows PowerShell
$env:MYSQL_HOST = 'localhost'
$env:MYSQL_USER = 'root'
$env:MYSQL_PASSWORD = 'your-password'
$env:MYSQL_DB = 'asset_management'
$env:FLASK_SECRET_KEY = 'your-secret-key'
```

### Step 3: Set up the React Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. The frontend is configured to proxy API requests to `http://localhost:5000` (see `vite.config.js`)

## Running the Application

### Terminal 1: Start Flask Backend

```bash
cd perpex
.venv\Scripts\activate
python app.py
```

The Flask backend will be available at: `http://localhost:5000`

### Terminal 2: Start React Frontend

```bash
cd frontend
npm run dev
```

The React frontend will be available at: `http://localhost:3000`

## Building for Production

### Flask Backend
No special build needed - just ensure `app.py` runs with debug=False in production.

### React Frontend
```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized production files.

## Available Routes

### React Frontend Routes
- `/` - Landing page
- `/login` - Login page
- `/register` - Registration page
- `/forgot-password` - Password recovery
- `/reset-password/:token` - Password reset
- `/dashboard` - Asset dashboard (protected)
- `/charts` - Analytics dashboard (protected)
- `/settings` - User settings (protected)

### Flask API Routes
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/logout` - User logout
- `GET /api/check-auth` - Check authentication status
- `GET /api/assets` - Get user's assets
- `POST /api/add-asset` - Add new asset
- `POST /api/forgot-password` - Request password reset
- `POST /api/reset-password/<token>` - Reset password

## Troubleshooting

### Port Already in Use
If port 3000 or 5000 is already in use:

**React (3000):**
```bash
cd frontend
npm run dev -- --port 3001
```

Then update the API proxy in `vite.config.js` to use the correct backend URL.

**Flask (5000):**
```python
# In app.py, change:
app.run(host='0.0.0.0', port=5001, debug=True)
```

### CORS Issues
The Flask backend is configured to accept requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

To allow other origins, update `app.py`:
```python
CORS(app, supports_credentials=True, origins=['http://your-url:3000'])
```

### Database Connection Error
1. Verify MySQL is running
2. Check credentials in environment variables or `app.py`
3. Ensure database and tables are created

### Dependencies Not Found
Reinstall dependencies:
```bash
# Python
pip install -r requirements.txt

# Node
npm install
```

## Development Tips

### Hot Reload
- **React**: Changes to components automatically reload in the browser
- **Flask**: Debug mode enabled, but you may need to restart for some changes

### API Requests
The React frontend uses `fetch()` for API calls. All requests include `credentials: 'include'` to maintain sessions.

Example:
```javascript
const response = await fetch('/api/assets', {
  credentials: 'include'
})
```

### Database Debugging
Use a MySQL client like MySQL Workbench or DBeaver to inspect and modify the database directly.

## Next Steps

1. **Customize styling** - Edit CSS files in `frontend/src/`
2. **Add more features** - Create new React components
3. **Implement real SMS** - Replace demo token with actual SMS service
4. **Add authentication tokens** - Consider JWT for stateless auth
5. **Add unit tests** - Set up Jest for React and pytest for Flask

## Support

For issues or questions:
1. Check the error messages in browser console and terminal
2. Review the README files in `frontend/` and `perpex/`
3. Verify all prerequisites are installed
4. Check that both servers are running
