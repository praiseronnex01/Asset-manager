# 🚨 CRITICAL: Python Installation Required

## Your system does NOT have Python installed yet.

### ⚠️ Before You Can Run the Flask App, You MUST:

---

## 🎯 Step 1: Install Python

### **Fastest Method: Microsoft Store**
1. Open **Microsoft Store** (Windows 11/10)
2. Search for **"Python"** (by Python Software Foundation)
3. Click **"Get"** or **"Install"**
4. Wait for installation to complete
5. Open Command Prompt and verify:
   ```
   python --version
   ```
   Should show: `Python 3.11.x` or similar

### **Alternative Method: Direct Download**
1. Visit: https://www.python.org/downloads/
2. Click **"Download Python 3.11"** (latest)
3. Run the installer
4. **✅ CRITICAL**: During installation:
   - ✅ Check: **"Add Python to PATH"** 
   - ✅ Check: **"Install for all users"** (optional)
   - Click **"Install Now"**
5. **Finish** and close installer

---

## ✅ Step 2: Verify Python is Installed

Open **Command Prompt** or **PowerShell** and run:

```bash
python --version
```

**Expected output:**
```
Python 3.11.9
```
(version number may vary)

If you see this ✅ → Continue to Step 3

If you see "not recognized" ❌ → Python is not in PATH, reinstall it

---

## 🚀 Step 3: Run the Flask App

Once Python is installed, simply:

**Double-click:** `START_APP.bat`

Or manually:
```bash
cd "c:\Users\praise\Desktop\BALEKE\NOBLE\Asset Management"
START_APP.bat
```

---

## 🌐 Step 4: Access in Browser

Once the app is running, open your browser and go to:

**Local Access:**
- http://localhost:5000
- http://127.0.0.1:5000

**Network Access (other computers):**
- http://<your-computer-ip>:5000
- Find your IP: Open PowerShell and run `ipconfig`

---

## 🐛 Troubleshooting

### ❌ "Python is not recognized as an internal or external command"
**Solution:**
- Python is NOT in your system PATH
- Reinstall Python and **MUST CHECK**: "Add Python to PATH"
- Restart Command Prompt after installation
- Verify: `python --version` in new Command Prompt window

### ❌ Still not working after reinstall?
**Manual PATH setup:**
1. Find Python installation folder (usually `C:\Users\[YourName]\AppData\Local\Programs\Python\Python311`)
2. Windows Settings → Environment Variables
3. Click "Edit Environment Variables for your account"
4. Click "New" and add Python path
5. Click "OK", restart Command Prompt

### ❌ "Module not found" errors
**Solution:**
- Flask app couldn't install dependencies
- Make sure pip is installed (comes with Python)
- Run in Command Prompt:
  ```bash
  python -m pip install --upgrade pip
  ```

### ❌ Database connection error
**Solution:**
- MySQL is not installed or not running
- See `SETUP_GUIDE.md` for MySQL setup
- Or create `.env` file with correct MySQL credentials

---

## 📋 Quick Checklist

- [ ] Python installed (verify with `python --version`)
- [ ] Python in PATH (shows version number)
- [ ] ✅ Run: `START_APP.bat`
- [ ] Flask app running (shows "Running on http://...")
- [ ] Open browser: `http://localhost:5000`
- [ ] See Flask app login page ✅

---

## 💡 Need Help?

1. **Can't install Python?**
   - Use Microsoft Store (easiest)
   - OR Download from https://www.python.org/downloads/

2. **Python installed but "not recognized"?**
   - Restart your computer
   - Open new Command Prompt
   - Run `python --version` again

3. **App starts but shows database error?**
   - You need MySQL installed and configured
   - See `SETUP_GUIDE.md` section: "Database Setup"

---

**Once you've installed Python and verified `python --version` works, run `START_APP.bat` and your Flask app will start!** 🎉
