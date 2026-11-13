# 🌐 ASSET MANAGER - Web Access Guide

## Running the Application

Your ASSET MANAGER application is now configured to be accessible via web URL.

### ⚠️ Prerequisite: Python Must Be Installed First

**Before proceeding, you MUST have Python installed:**

1. Check if Python is installed:
   ```bash
   python --version
   ```
   If this shows a version number, continue below.
   
2. If not installed, follow `PYTHON_INSTALLATION_REQUIRED.md` first.

### Step 1: Quick Start (Easiest)

Simply double-click: **`START_APP.bat`**

This automatically:
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Starts your Flask app
- ✅ Opens on http://localhost:5000

### Alternative: Manual Setup

If you prefer manual setup:

```bash
REM Navigate to project
cd "c:\Users\praise\Desktop\BALEKE\NOBLE\Asset Management"

REM Create virtual environment
python -m venv .venv

REM Activate it
.\.venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Run app
cd perpex
python app.py
```

### Step 1 (Old): Install Dependencies
```bash
cd perpex
pip install -r requirements.txt
```

### Step 2: Configure Database (Optional for Testing)

For full functionality, set up MySQL database.

**Quick test without database:**
- App will start but show database connection error
- You can still test the Flask setup

**For full setup:**

1. Install MySQL (if not already installed)
   - Download: https://dev.mysql.com/downloads/mysql/

2. Create `.env` file in the project root:
```env
FLASK_SECRET_KEY=your-secure-secret-key-here-change-this
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DB=asset_management
```

3. Import database schema:
   ```bash
   mysql -u root -p < perpex/database.sql
   ```

4. Update database credentials in app.py (lines 21-24) if needed

### Step 3: Run the Application

**Using START_APP.bat (Recommended):**
```bash
Double-click: START_APP.bat
```

**Or manually:**
```bash
cd perpex
python app.py
```

### Step 2 (Old): Configure Database
Before running, ensure your MySQL database is set up and update environment variables:

Create a `.env` file in the project root:
```env
FLASK_SECRET_KEY=your-secure-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DB=asset_management
```

### Step 3 (Old): Run the Application
```bash
cd perpex
python app.py
```

You should see output like:
```
============================================
Flask app is starting...
============================================

Open your browser and go to:
http://localhost:5000

Press Ctrl+C to stop the server
============================================

Running on http://0.0.0.0:5000
WARNING: This is a development server...
```

## Accessing the Application

### Local Access (Same Computer)
- **Browser URL**: `http://localhost:5000`
- **Other name**: `http://127.0.0.1:5000`

### Remote Access (Other Computers on Network)
Find your computer's IP address:

**On Windows (PowerShell)**:
```powershell
ipconfig
```
Look for "IPv4 Address" (usually 192.168.x.x or 10.x.x.x)

**Then access from another computer**:
```
http://<your-computer-ip>:5000
```

Example: `http://192.168.1.100:5000`

## Features Available at Web URL
✅ User Login & Registration  
✅ Dashboard with Asset Analytics  
✅ Add/Manage Assets  
✅ View Charts & Reports  
✅ Admin Panel (if admin user)  
✅ User Notifications  

## Troubleshooting

### "Connection refused" Error
- Ensure the Flask app is running
- Check firewall isn't blocking port 5000
- Verify MySQL is running and configured correctly

### "Cannot find IP address"
- Run `ipconfig` on Windows to find your IP
- Make sure both computers are on the same network
- Ping the IP to verify connectivity

### Database Connection Error
- Verify MySQL is running
- Check credentials in `.env` file
- Ensure `asset_management` database exists

## Production Deployment

For production environments, use a production WSGI server:

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress
```bash
pip install waitress
waitress-serve --host 0.0.0.0 --port 5000 app:app
```

## Security Notes
- Change `FLASK_SECRET_KEY` to a strong random value
- Set `debug=False` for production
- Use HTTPS with a reverse proxy (nginx/Apache)
- Keep MySQL password secure
- Use environment variables for sensitive data

---

For more help, ensure all dependencies are installed and MySQL database is properly configured.
