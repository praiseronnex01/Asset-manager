# Flask Asset Management - Setup Guide

## Quick Start (Windows)

### Option 1: Batch File (Simplest)
1. Make sure Python 3.10+ is installed and added to PATH
2. Double-click: `setup_and_run.bat`
3. The app will start at http://localhost:5000

### Option 2: PowerShell Script
1. Make sure Python 3.10+ is installed and added to PATH
2. Right-click `setup_and_run.ps1` → Run with PowerShell
3. Or run in terminal: `powershell -ExecutionPolicy Bypass -File setup_and_run.ps1`

### Option 3: Manual Setup
```powershell
# 1. Navigate to project folder
cd "c:\Users\praise\Desktop\BALEKE\NOBLE\Asset Management"

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install Flask==3.1.1 Flask-Bcrypt==1.0.1 Flask-MySQLdb==2.0.0 Flask-Cors==4.0.0 python-dateutil==2.9.0 Werkzeug==3.1.3

# 5. Run the app
cd perpex
python app.py
```

---

## Prerequisites

### Install Python (If Not Already Installed)

**Windows 11/10:**
1. Download from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Click "Disable path length limit" (optional but recommended)

**Verify Installation:**
```powershell
python --version
pip --version
```

### What Gets Installed

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.1.1 | Web framework |
| Werkzeug | 3.1.3 | WSGI utility library |
| Flask-Bcrypt | 1.0.1 | Password hashing |
| Flask-MySQLdb | 2.0.0 | MySQL database connection |
| Flask-Cors | 4.0.0 | Cross-origin resource sharing |
| python-dateutil | 2.9.0 | Date utilities |

---

## Database Setup

The Flask app connects to MySQL. You need to:

1. **Install MySQL Server** (if not already installed)
   - Download: https://dev.mysql.com/downloads/mysql/

2. **Login to MySQL:**
   ```bash
   mysql -u root -p
   ```

3. **Create Database:**
   ```sql
   CREATE DATABASE asset_management;
   USE asset_management;
   
   -- Import the schema from: perpex/database.sql
   SOURCE perpex/database.sql;
   ```

4. **Update Environment Variables:**
   Create a `.env` file in the root directory:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your-password
   MYSQL_DB=asset_management
   FLASK_SECRET_KEY=your-secret-key-here
   ```

---

## Running the Flask App

### Start the Server
```powershell
cd "c:\Users\praise\Desktop\BALEKE\NOBLE\Asset Management"
.\.venv\Scripts\Activate.ps1
cd perpex
python app.py
```

### Access in Browser
- **Local Access:** http://localhost:5000
- **Remote Access:** http://{your-computer-ip}:5000 (for devices on same network)

### Stop the Server
Press `Ctrl+C` in the terminal

---

## Troubleshooting

### Error: "python is not recognized"
**Solution:** Python is not in PATH
- Reinstall Python and check "Add Python to PATH"
- Or add Python manually to PATH:
  1. Settings → Environment Variables
  2. Add Python path (typically: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311`)

### Error: "MySQLdb connection not working"
**Solution:**
- MySQL server is not running or not installed
- Check MySQL credentials in code or `.env` file
- For MySQL on Windows: Start the service from Services panel

### Error: "Module not found"
**Solution:**
- Make sure virtual environment is activated (should see `(.venv)` in terminal)
- Reinstall dependencies: `pip install -r requirements.txt`

### App starts but page shows connection error
**Solution:**
- MySQL database not created or schema not imported
- Check database connection settings in `app.py`
- Verify MySQL is running

---

## Development Tips

### Using VS Code
1. Select Python interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
2. Choose `.\.venv` interpreter
3. Use the "Run Flask app" task from Tasks menu

### Debugging
Add breakpoints in VS Code and use Python debugger

### Deactivate Virtual Environment
```powershell
deactivate
```

### Add New Dependencies
```powershell
pip install package-name
pip freeze > requirements.txt
```

---

## Next Steps

1. Set up MySQL database
2. Run setup script
3. Open http://localhost:5000 in browser
4. Test user registration and login
5. Manage assets in the dashboard

Need help? Check the code comments in `perpex/app.py`
