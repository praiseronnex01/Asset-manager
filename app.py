import os
import sqlite3
import secrets
import string
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "asset-management-secret")

DB_PATH = "assets.db"
ADMIN_SIGNUP_CODE = os.getenv("ADMIN_SIGNUP_CODE", "ADMIN2026")

# Activity tracking middleware
@app.before_request
def track_user_activity():
    if "user_id" in session and "session_id" in session:
        update_session_activity()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def send_sms(mobile_number, message):
    """
    Send SMS to mobile number.
    In production, integrate with SMS service like Twilio, AWS SNS, etc.
    For now, this logs to console - replace with actual SMS sending.
    """
    try:
        # Log the SMS (in production, this would send actual SMS)
        print(f"SMS TO {mobile_number}: {message}")
        
        # Example integration with Twilio (uncomment and configure when ready):
        # from twilio.rest import Client
        # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=message,
        #     from_=os.getenv('TWILIO_PHONE_NUMBER'),
        #     to=mobile_number
        # )
        
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False


def column_exists(conn, table_name, column_name):
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(column["name"] == column_name for column in columns)


def migrate_existing_tables(conn):
    if not column_exists(conn, "users", "full_name"):
        conn.execute("ALTER TABLE users ADD COLUMN full_name TEXT DEFAULT 'User'")
    if not column_exists(conn, "users", "role"):
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    if not column_exists(conn, "users", "created_at"):
        conn.execute("ALTER TABLE users ADD COLUMN created_at TEXT")

    # Add password reset columns
    if not column_exists(conn, "users", "mobile_number"):
        conn.execute("ALTER TABLE users ADD COLUMN mobile_number TEXT")
    if not column_exists(conn, "users", "reset_token"):
        conn.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    if not column_exists(conn, "users", "reset_token_expiry"):
        conn.execute("ALTER TABLE users ADD COLUMN reset_token_expiry TEXT")

    # Suspension / active flags
    if not column_exists(conn, "users", "is_suspended"):
        conn.execute("ALTER TABLE users ADD COLUMN is_suspended BOOLEAN DEFAULT FALSE")
    if not column_exists(conn, "users", "is_active"):
        conn.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
    if not column_exists(conn, "users", "profile_image"):
        conn.execute("ALTER TABLE users ADD COLUMN profile_image TEXT")
    if not column_exists(conn, "users", "theme"):
        conn.execute("ALTER TABLE users ADD COLUMN theme TEXT DEFAULT 'light'")

    if not column_exists(conn, "assets", "purchase_value"):
        conn.execute("ALTER TABLE assets ADD COLUMN purchase_value REAL DEFAULT 0")
    if not column_exists(conn, "assets", "quantity"):
        conn.execute("ALTER TABLE assets ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1")
    if not column_exists(conn, "assets", "created_at"):
        conn.execute("ALTER TABLE assets ADD COLUMN created_at TEXT")
    if not column_exists(conn, "notifications", "action"):
        conn.execute("ALTER TABLE notifications ADD COLUMN action TEXT DEFAULT 'notification'")


def notify_admins(title, message, type="info", action="notification"):
    conn = get_db()
    try:
        admins = conn.execute("SELECT id FROM users WHERE role = 'admin'").fetchall()
        for admin in admins:
            conn.execute(
                """
                INSERT INTO notifications (user_id, title, message, type, action, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    admin["id"],
                    title,
                    message,
                    type,
                    action,
                    datetime.utcnow().isoformat(),
                ),
            )
        conn.commit()
    except Exception as e:
        print(f"Error creating admin notification: {e}")
    finally:
        conn.close()


def create_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_suspended BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            profile_image TEXT,
            theme TEXT DEFAULT 'light',
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            duration INTEGER NOT NULL,
            purchase_value REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'info',
            action TEXT DEFAULT 'notification',
            is_read BOOLEAN DEFAULT FALSE,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            login_time TEXT NOT NULL,
            last_activity TEXT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TEXT NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (recipient_id) REFERENCES users (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS asset_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    migrate_existing_tables(conn)


def quarantine_corrupt_db(db_path):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{db_path}.corrupt_{timestamp}"
    os.replace(db_path, backup_path)
    return backup_path


def recovery_db_path(db_path):
    root, ext = os.path.splitext(db_path)
    return f"{root}_recovered{ext or '.db'}"


def init_db():
    global DB_PATH
    conn = None
    try:
        conn = get_db()
        quick_check = conn.execute("PRAGMA quick_check").fetchone()
        if quick_check and quick_check[0] != "ok":
            raise sqlite3.DatabaseError(f"Integrity check failed: {quick_check[0]}")
        create_schema(conn)
        conn.commit()
    except sqlite3.DatabaseError:
        if conn:
            conn.close()
            conn = None
        if os.path.exists(DB_PATH):
            try:
                backup_path = quarantine_corrupt_db(DB_PATH)
                print(
                    f"Detected corrupted SQLite database. Backed it up to '{backup_path}' and created a new database."
                )
            except PermissionError:
                old_path = DB_PATH
                DB_PATH = recovery_db_path(DB_PATH)
                print(
                    f"Detected corrupted SQLite database at '{old_path}', but it is locked by another process. "
                    f"Using a fresh database at '{DB_PATH}'."
                )
        conn = get_db()
        create_schema(conn)
        conn.commit()
    finally:
        if conn:
            conn.close()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access is required for this action.", "error")
            return redirect(url_for("dashboard"))
        return func(*args, **kwargs)

    return wrapper


def track_activity(action, details=None):
    """Decorator to track user activity"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user_id" in session:
                conn = get_db()
                try:
                    conn.execute(
                        """
                        INSERT INTO user_activity (user_id, action, details, ip_address, user_agent, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            session["user_id"],
                            action,
                            details,
                            request.remote_addr,
                            request.headers.get('User-Agent'),
                            datetime.utcnow().isoformat()
                        )
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Error tracking activity: {e}")
                finally:
                    conn.close()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def update_session_activity():
    """Update user's last activity timestamp"""
    if "user_id" in session:
        conn = get_db()
        try:
            conn.execute(
                """
                UPDATE user_sessions 
                SET last_activity = ? 
                WHERE user_id = ? AND session_id = ? AND is_active = TRUE
                """,
                (datetime.utcnow().isoformat(), session["user_id"], session["session_id"])
            )
            conn.commit()
        except Exception as e:
            print(f"Error updating session activity: {e}")
        finally:
            conn.close()


def get_current_user(conn):
    return conn.execute(
        "SELECT id, full_name, username, role FROM users WHERE id = ?",
        (session["user_id"],),
    ).fetchone()


@app.context_processor
def inject_user_settings():
    if session.get('user_id'):
        conn = get_db()
        user = conn.execute("SELECT profile_image, theme, full_name, username FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        conn.close()
        return dict(current_user_profile_image=(user['profile_image'] if user and user['profile_image'] else None), current_user_theme=(user['theme'] if user and user['theme'] else 'light'), current_user_full_name=(user['full_name'] if user else ''), current_user_username=(user['username'] if user else ''))
    return dict(current_user_profile_image=None, current_user_theme='light', current_user_full_name='', current_user_username='')


def verify_password(stored_password, candidate_password):
    if not stored_password:
        return False
    if stored_password.startswith(("pbkdf2:", "scrypt:")):
        return check_password_hash(stored_password, candidate_password)
    return stored_password == candidate_password


def summarize_assets(assets):
    total_assets = sum(int(asset["quantity"] or 1) for asset in assets)
    total_value = sum(
        float(asset["purchase_value"] or 0) * int(asset["quantity"] or 1) for asset in assets
    )
    total_quantity = max(total_assets, 1)
    average_life = (
        round(
            sum(int(asset["duration"]) * int(asset["quantity"] or 1) for asset in assets)
            / total_quantity,
            1,
        )
        if total_assets
        else 0
    )
    average_life_years = round(average_life / 12, 1) if average_life else 0
    return total_assets, total_value, average_life_years


def build_chart_data(assets):
    category_count = {}
    category_value = {}
    monthly_count = {}
    monthly_value = {}

    asset_name_money = {}
    asset_name_qty = {}
    
    items = []
    user_map = {}

    now_dt = datetime.utcnow()
    lifespan_health_counts = {
        "Healthy (>50%)": 0,
        "Mid-Life (25-50%)": 0,
        "Expiring Soon (<25%)": 0,
        "Expired": 0
    }
    lifespan_asset_map = {}

    for asset in assets:
        name = asset["name"] or "Unnamed Asset"
        category = asset["category"] or "Uncategorized"
        quantity = int(asset["quantity"] or 1)
        unit_price = float(asset["purchase_value"] or 0)
        money = round(unit_price * quantity, 2)
        purchase_date = asset["purchase_date"] or ""
        duration_months = int(asset["duration"] or 12)
        
        # Calculate percentage lifespan
        try:
            p_date_str = purchase_date[:10] if purchase_date else ""
            if p_date_str:
                p_dt = datetime.strptime(p_date_str, "%Y-%m-%d")
            else:
                p_dt = now_dt
            
            total_days = max(1, duration_months * 30)
            elapsed_days = max(0.0, (now_dt - p_dt).total_seconds() / 86400.0)
            remaining_days = max(0.0, total_days - elapsed_days)
            pct_remaining = max(0.0, min(100.0, (remaining_days / total_days) * 100.0))
            pct_used = round(100.0 - pct_remaining, 1)
            pct_remaining = round(pct_remaining, 1)
            is_expired = remaining_days <= 0.0
        except Exception:
            pct_remaining = 100.0
            pct_used = 0.0
            is_expired = False
            remaining_days = duration_months * 30
            total_days = duration_months * 30

        if is_expired or pct_remaining <= 0:
            health_status = "Expired"
            lifespan_health_counts["Expired"] += 1
        elif pct_remaining <= 25:
            health_status = "Expiring Soon (<25%)"
            lifespan_health_counts["Expiring Soon (<25%)"] += 1
        elif pct_remaining <= 50:
            health_status = "Mid-Life (25-50%)"
            lifespan_health_counts["Mid-Life (25-50%)"] += 1
        else:
            health_status = "Healthy (>50%)"
            lifespan_health_counts["Healthy (>50%)"] += 1

        lifespan_asset_map[name] = pct_remaining

        # User details if available
        user_keys = asset.keys()
        username = asset["username"] if "username" in user_keys else ""
        full_name = asset["full_name"] if "full_name" in user_keys else ""
        user_id = asset["user_id"] if "user_id" in user_keys else None

        # Category
        category_count[category] = category_count.get(category, 0) + quantity
        category_value[category] = round(category_value.get(category, 0) + money, 2)

        # Monthly
        month_key = purchase_date[:7] if purchase_date else "Unknown"
        monthly_count[month_key] = monthly_count.get(month_key, 0) + quantity
        monthly_value[month_key] = round(monthly_value.get(month_key, 0) + money, 2)

        # Asset Name -> Money aggregation
        asset_name_money[name] = round(asset_name_money.get(name, 0) + money, 2)
        asset_name_qty[name] = asset_name_qty.get(name, 0) + quantity

        item = {
            "id": asset["id"],
            "name": name,
            "category": category,
            "date": purchase_date,
            "quantity": quantity,
            "unit_price": unit_price,
            "money": money,
            "duration_months": duration_months,
            "pct_remaining": pct_remaining,
            "pct_used": pct_used,
            "health_status": health_status,
            "is_expired": is_expired,
            "remaining_days": int(remaining_days),
            "user_id": user_id,
            "username": username,
            "full_name": full_name or username or "User"
        }
        items.append(item)

        if user_id:
            if user_id not in user_map:
                user_map[user_id] = {
                    "id": user_id,
                    "name": full_name or username or f"User #{user_id}",
                    "username": username,
                    "total_money": 0,
                    "count": 0
                }
            user_map[user_id]["total_money"] = round(user_map[user_id]["total_money"] + money, 2)
            user_map[user_id]["count"] += quantity

    # Sort chronological for Line Graph
    items_by_date = sorted(items, key=lambda x: (x["date"] or "0000-00-00", x["id"]))

    # Sort asset names by money descending for Pie Chart
    sorted_assets = sorted(asset_name_money.items(), key=lambda x: x[1], reverse=True)
    pie_labels = [k for k, v in sorted_assets]
    pie_values = [v for k, v in sorted_assets]

    # Percentage Lifespan Pie labels and values
    sorted_lifespan = sorted(lifespan_asset_map.items(), key=lambda x: x[1], reverse=True)
    lifespan_pie_labels = [k for k, v in sorted_lifespan]
    lifespan_pie_values = [v for k, v in sorted_lifespan]

    # Line graph series
    line_labels = [f"{x['name']} ({x['date']})" if x['date'] else x['name'] for x in items_by_date]
    line_values = [x['money'] for x in items_by_date]
    
    # Cumulative money calculation
    running_total = 0
    line_cumulative = []
    for val in line_values:
        running_total = round(running_total + val, 2)
        line_cumulative.append(running_total)

    total_money = round(sum(pie_values), 2)
    top_asset = sorted_assets[0][0] if sorted_assets else "—"
    top_asset_money = sorted_assets[0][1] if sorted_assets else 0

    avg_lifespan = round(sum(x["pct_remaining"] for x in items) / max(len(items), 1), 1)

    return {
        "category_count": category_count,
        "category_value": category_value,
        "monthly_count": dict(sorted(monthly_count.items())),
        "monthly_value": dict(sorted(monthly_value.items())),
        "pie_labels": pie_labels,
        "pie_values": pie_values,
        "lifespan_pie_labels": lifespan_pie_labels,
        "lifespan_pie_values": lifespan_pie_values,
        "lifespan_health_labels": list(lifespan_health_counts.keys()),
        "lifespan_health_values": list(lifespan_health_counts.values()),
        "line_labels": line_labels,
        "line_values": line_values,
        "line_cumulative": line_cumulative,
        "items": items_by_date,
        "users": list(user_map.values()),
        "total_money": total_money,
        "total_count": len(items),
        "top_asset": top_asset,
        "top_asset_money": top_asset_money,
        "avg_money": round(total_money / max(len(items), 1), 2),
        "avg_lifespan": avg_lifespan
    }


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        mobile_number = request.form.get("mobile_number", "").strip()
        role = request.form.get("role", "user")
        admin_code = request.form.get("admin_code", "").strip()

        if not all([full_name, username, password, confirm_password]):
            flash("Please complete all required fields.", "error")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")
        if role == "admin" and admin_code != ADMIN_SIGNUP_CODE:
            flash("Invalid admin signup code.", "error")
            return render_template("register.html")

        conn = get_db()
        
        # Check if username already exists
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if existing:
            conn.close()
            flash("Username already exists. Choose another one.", "error")
            return render_template("register.html")
        
        # Check if mobile number already exists (if provided)
        if mobile_number:
            existing_mobile = conn.execute(
                "SELECT id FROM users WHERE mobile_number = ?",
                (mobile_number,),
            ).fetchone()
            if existing_mobile:
                conn.close()
                flash("Mobile number already registered.", "error")
                return render_template("register.html")

        conn.execute(
            """
            INSERT INTO users (full_name, username, password, mobile_number, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                full_name,
                username,
                generate_password_hash(password),
                mobile_number if mobile_number else None,
                "admin" if role == "admin" else "user",
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        
        # Create notifications for all admin users
        user_id = conn.lastrowid
        admins = conn.execute("SELECT id FROM users WHERE role = 'admin'").fetchall()
        for admin in admins:
            conn.execute(
                """
                INSERT INTO notifications (user_id, title, message, type, action, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    admin["id"],
                    "New User Registration",
                    f"New user '{full_name}' (username: {username}) has registered.",
                    "success",
                    "user_registration",
                    datetime.utcnow().isoformat(),
                ),
            )
        
        conn.commit()
        conn.close()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        conn.close()

        if not user or not verify_password(user["password"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        # Upgrade legacy plain text passwords to a secure hash after first successful login.
        if not user["password"].startswith(("pbkdf2:", "scrypt:")):
            conn = get_db()
            conn.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (generate_password_hash(password), user["id"]),
            )
            conn.commit()
            conn.close()

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        session["full_name"] = user["full_name"]        
        # Create session record for activity tracking
        conn = get_db()
        try:
            session_id = secrets.token_hex(16)
            conn.execute(
                """
                INSERT INTO user_sessions (user_id, session_id, ip_address, user_agent, login_time, last_activity, is_active)
                VALUES (?, ?, ?, ?, ?, ?, TRUE)
                """,
                (
                    user["id"],
                    session_id,
                    request.remote_addr,
                    request.headers.get('User-Agent'),
                    datetime.utcnow().isoformat(),
                    datetime.utcnow().isoformat()
                )
            )
            conn.commit()
            session["session_id"] = session_id
        except Exception as e:
            print(f"Error creating session record: {e}")
        finally:
            conn.close()

        notify_admins(
            title="User Logged In",
            message=f"User '{user['full_name']}' (username: {user['username']}) logged in.",
            type="info",
            action="user_login",
        )
        
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
@login_required
@track_activity("view_dashboard", "Viewed dashboard")
def dashboard():
    conn = get_db()
    user = get_current_user(conn)

    if session.get("role") == "admin":
        assets = conn.execute(
            """
            SELECT a.*, u.username, u.full_name
            FROM assets a
            JOIN users u ON u.id = a.user_id
            ORDER BY a.purchase_date DESC
            """
        ).fetchall()
        users_count = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
        all_users = conn.execute("SELECT id, full_name, username FROM users ORDER BY full_name ASC").fetchall()
    else:
        assets = conn.execute(
            """
            SELECT a.*, u.username, u.full_name
            FROM assets a
            JOIN users u ON u.id = a.user_id
            WHERE a.user_id = ?
            ORDER BY a.purchase_date DESC
            """,
            (session["user_id"],),
        ).fetchall()
        users_count = 1
        all_users = []

    total_assets, total_value, average_life = summarize_assets(assets)
    chart_data = build_chart_data(assets)
    
    # Get notification count
    notification_count = conn.execute("SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = FALSE", (session["user_id"],)).fetchone()["count"]
    
    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        assets=assets,
        total_assets=total_assets,
        total_value=total_value,
        average_life=average_life,
        users_count=users_count,
        all_users=all_users,
        chart_data=chart_data,
        notification_count=notification_count,
        current_date=datetime.now().strftime("%B %d, %Y"),
    )


@app.route("/api/assets")
@login_required
def api_assets():
    conn = get_db()
    if session.get("role") == "admin":
        rows = conn.execute(
            """
            SELECT a.*, u.username, u.full_name
            FROM assets a
            JOIN users u ON u.id = a.user_id
            ORDER BY a.purchase_date DESC
            """
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT a.*, u.username, u.full_name
            FROM assets a
            JOIN users u ON u.id = a.user_id
            WHERE a.user_id = ?
            ORDER BY a.purchase_date DESC
            """,
            (session["user_id"],),
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/chart-data")
@login_required
def api_chart_data():
    conn = get_db()
    if session.get("role") == "admin":
        assets = conn.execute(
            """
            SELECT a.*, u.username, u.full_name
            FROM assets a
            JOIN users u ON u.id = a.user_id
            ORDER BY a.purchase_date DESC
            """
        ).fetchall()
    else:
        assets = conn.execute(
            """
            SELECT a.*, u.username, u.full_name
            FROM assets a
            JOIN users u ON u.id = a.user_id
            WHERE a.user_id = ?
            ORDER BY a.purchase_date DESC
            """,
            (session["user_id"],),
        ).fetchall()
    conn.close()
    data = build_chart_data(assets)
    return jsonify(data)


@app.route("/add-asset", methods=["GET", "POST"])
@login_required
@track_activity("add_asset", "Added new asset")
def add_asset():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        purchase_date = request.form.get("purchase_date", "")
        quantity = request.form.get("quantity", "1")
        duration = request.form.get("duration", "0")
        purchase_value = request.form.get("purchase_value", "0")

        if not all([name, category, purchase_date, quantity, duration]):
            flash("Please fill in all required asset fields.", "error")
            return render_template("add_asset.html")

        try:
            quantity_value = int(quantity)
            duration_years = float(duration)
            val_purchase = float(purchase_value or 0)
        except ValueError:
            flash("Quantity must be a whole number, useful life must be valid, and purchase value must be numeric.", "error")
            return render_template("add_asset.html")

        if quantity_value < 1 or duration_years <= 0 or val_purchase < 0:
            flash("Quantity must be at least 1, useful life greater than 0, and purchase value non-negative.", "error")
            return render_template("add_asset.html")

        duration_value = max(1, int(round(duration_years * 12)))

        conn = get_db()
        conn.execute(
            """
            INSERT INTO assets (
                user_id, name, category, purchase_date, quantity, duration, purchase_value, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                name,
                category,
                purchase_date,
                quantity_value,
                duration_value,
                val_purchase,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

        notify_admins(
            title="New Asset Added",
            message=(
                f"User '{session.get('full_name', session.get('username'))}' added asset '{name}' "
                f"in category '{category}'."
            ),
            type="success",
            action="asset_added",
        )
        
        flash("Asset added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_asset.html")


@app.route("/edit-asset/<int:asset_id>", methods=["GET", "POST"])
@login_required
@track_activity("edit_asset", "Edited an asset")
def edit_asset(asset_id):
    conn = get_db()
    asset = conn.execute(
        "SELECT * FROM assets WHERE id = ?",
        (asset_id,),
    ).fetchone()

    if not asset:
        conn.close()
        flash("Asset not found.", "error")
        return redirect(url_for("dashboard"))

    if session.get("role") != "admin" and asset["user_id"] != session["user_id"]:
        conn.close()
        flash("You do not have permission to edit this asset.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        purchase_date = request.form.get("purchase_date", "")
        quantity = request.form.get("quantity", "1")
        duration = request.form.get("duration", "0")
        purchase_value = request.form.get("purchase_value", "0")

        if not all([name, category, purchase_date, quantity, duration]):
            conn.close()
            flash("Please fill in all required asset fields.", "error")
            return render_template("edit_asset.html", asset=asset)

        try:
            quantity_value = int(quantity)
            duration_years = float(duration)
            val_purchase = float(purchase_value or 0)
        except ValueError:
            conn.close()
            flash("Quantity must be a whole number, useful life must be numeric, and purchase value must be valid.", "error")
            return render_template("edit_asset.html", asset=asset)

        if quantity_value < 1 or duration_years <= 0 or val_purchase < 0:
            conn.close()
            flash("Quantity must be at least 1, useful life greater than 0, and purchase value non-negative.", "error")
            return render_template("edit_asset.html", asset=asset)

        duration_value = max(1, int(round(duration_years * 12)))

        conn.execute(
            """
            UPDATE assets
            SET name = ?, category = ?, purchase_date = ?, quantity = ?, duration = ?, purchase_value = ?
            WHERE id = ?
            """,
            (name, category, purchase_date, quantity_value, duration_value, val_purchase, asset_id),
        )
        conn.commit()
        conn.close()

        flash("Asset updated successfully.", "success")
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("edit_asset.html", asset=asset)


@app.route("/delete-asset/<int:asset_id>", methods=["POST"])
@login_required
@track_activity("delete_asset", "Deleted an asset")
def delete_asset(asset_id):
    conn = get_db()
    asset = conn.execute(
        "SELECT user_id FROM assets WHERE id = ?",
        (asset_id,),
    ).fetchone()

    if not asset:
        conn.close()
        flash("Asset not found.", "error")
        return redirect(url_for("dashboard"))

    if session.get("role") != "admin" and asset["user_id"] != session["user_id"]:
        conn.close()
        flash("You do not have permission to delete this asset.", "error")
        return redirect(url_for("dashboard"))

    conn.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    conn.commit()
    conn.close()
    flash("Asset deleted.", "success")
    return redirect(url_for("dashboard"))


@app.route("/admin/users")
@login_required
@admin_required
@track_activity("view_admin_users", "Viewed admin users page")
def admin_users():
    conn = get_db()
    # allow optional search by name or username
    q = request.args.get('q', '').strip()
    if q:
        q_param = f"%{q}%"
        users = conn.execute(
            """
            SELECT u.id, u.full_name, u.username, u.role, u.created_at, u.is_suspended, u.is_active, COUNT(a.id) AS asset_count
            FROM users u
            LEFT JOIN assets a ON a.user_id = u.id
            WHERE u.full_name LIKE ? OR u.username LIKE ?
            GROUP BY u.id
            ORDER BY u.created_at DESC
            """,
            (q_param, q_param),
        ).fetchall()
    else:
        users = conn.execute(
            """
            SELECT u.id, u.full_name, u.username, u.role, u.created_at, u.is_suspended, u.is_active, COUNT(a.id) AS asset_count
            FROM users u
            LEFT JOIN assets a ON a.user_id = u.id
            GROUP BY u.id
            ORDER BY u.created_at DESC
            """
        ).fetchall()
    conn.close()
    return render_template("admin_users.html", users=users, admin_signup_code=ADMIN_SIGNUP_CODE)


@app.route("/admin/user-action/<int:user_id>", methods=["POST"])
@login_required
@admin_required
@track_activity("admin_user_action", "Performed admin user action")
def admin_user_action(user_id):
    action = request.form.get('action')
    conn = get_db()
    user = conn.execute("SELECT id, username, full_name, role FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        flash("User not found.", "error")
        return redirect(url_for('admin_users'))

    if action == 'delete':
        if user['id'] == session.get('user_id'):
            conn.close()
            flash("You cannot delete your own active admin account.", "error")
            return redirect(url_for('admin_users'))
        # prevent deleting last admin
        if user['role'] == 'admin':
            admins = conn.execute("SELECT COUNT(*) as count FROM users WHERE role = 'admin'").fetchone()['count']
            if admins <= 1:
                conn.close()
                flash("Cannot delete the last admin account.", "error")
                return redirect(url_for('admin_users'))
        
        # Clean up dependent records before deleting user
        conn.execute("DELETE FROM assets WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM user_activity WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM user_messages WHERE sender_id = ? OR recipient_id = ?", (user_id, user_id))
        conn.execute("DELETE FROM asset_alerts WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        notify_admins("User Deleted", f"Admin deleted user '{user['username']}'.", type='error', action='user_deleted')
        flash("User deleted.", "success")
        return redirect(url_for('admin_users'))

    if action == 'suspend':
        if user['id'] == session.get('user_id'):
            conn.close()
            flash("You cannot suspend your own active admin account.", "error")
            return redirect(url_for('admin_users'))
        conn.execute("UPDATE users SET is_suspended = TRUE, is_active = FALSE WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        notify_admins("User Suspended", f"Admin suspended user '{user['username']}'.", type='warning', action='user_suspended')
        flash("User suspended.", "success")
        return redirect(url_for('admin_users'))

    if action == 'unsuspend':
        conn.execute("UPDATE users SET is_suspended = FALSE, is_active = TRUE WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        notify_admins("User Unsuspended", f"Admin reactivated user '{user['username']}'.", type='success', action='user_unsuspended')
        flash("User reactivated.", "success")
        return redirect(url_for('admin_users'))

    conn.close()
    flash("Unknown action.", "error")
    return redirect(url_for('admin_users'))


@app.route("/admin/online-users")
@login_required
@admin_required
@track_activity("view_online_users", "Viewed online users")
def admin_online_users():
    conn = get_db()
    
    # Get currently online users (active sessions within last 5 minutes)
    online_users = conn.execute(
        """
        SELECT DISTINCT u.id, u.full_name, u.username, u.role, 
               s.last_activity, s.ip_address, s.user_agent, s.login_time
        FROM users u
        JOIN user_sessions s ON u.id = s.user_id
        WHERE s.is_active = TRUE 
        AND datetime(s.last_activity) > datetime('now', '-5 minutes')
        ORDER BY s.last_activity DESC
        """
    ).fetchall()
    
    # Format timestamps for display
    formatted_users = []
    for user in online_users:
        user_dict = dict(user)
        if user_dict.get('last_activity'):
            try:
                dt = datetime.fromisoformat(user_dict['last_activity'])
                user_dict['formatted_last_activity'] = dt.strftime('%H:%M:%S')
            except (ValueError, TypeError):
                user_dict['formatted_last_activity'] = user_dict['last_activity']
        else:
            user_dict['formatted_last_activity'] = '-'
        
        if user_dict.get('login_time'):
            try:
                dt = datetime.fromisoformat(user_dict['login_time'])
                user_dict['formatted_login_time'] = dt.strftime('%m/%d %H:%M')
            except (ValueError, TypeError):
                user_dict['formatted_login_time'] = user_dict['login_time']
        else:
            user_dict['formatted_login_time'] = '-'
        
        formatted_users.append(user_dict)
    
    conn.close()
    return render_template("admin_online_users.html", online_users=formatted_users)


@app.route("/admin/user-activity")
@login_required
@admin_required
@track_activity("view_user_activity", "Viewed user activity logs")
def admin_user_activity():
    conn = get_db()
    
    # Get recent user activity (last 24 hours)
    activities = conn.execute(
        """
        SELECT a.*, u.full_name, u.username
        FROM user_activity a
        JOIN users u ON a.user_id = u.id
        WHERE datetime(a.timestamp) > datetime('now', '-1 day')
        ORDER BY a.timestamp DESC
        LIMIT 100
        """
    ).fetchall()
    
    # Format timestamps for display
    formatted_activities = []
    for activity in activities:
        activity_dict = dict(activity)
        if activity_dict.get('timestamp'):
            try:
                # Parse ISO timestamp and format for display
                dt = datetime.fromisoformat(activity_dict['timestamp'])
                activity_dict['formatted_timestamp'] = dt.strftime('%m/%d %H:%M:%S')
            except (ValueError, TypeError):
                activity_dict['formatted_timestamp'] = activity_dict['timestamp']
        else:
            activity_dict['formatted_timestamp'] = '-'
        formatted_activities.append(activity_dict)
    
    conn.close()
    return render_template("admin_user_activity.html", activities=formatted_activities)


@app.route("/admin/clear-history", methods=["POST"])
@login_required
@admin_required
@track_activity("clear_history", "Cleared all user activity history")
def admin_clear_history():
    """Clear all user activity logs"""
    conn = get_db()
    try:
        conn.execute("DELETE FROM user_activity")
        conn.commit()
        flash("All activity history has been cleared successfully.", "success")
    except Exception as e:
        flash(f"Error clearing history: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("admin_user_activity"))


@app.route("/api/user-asset-count/<int:user_id>")
@login_required
@admin_required
def get_user_asset_count(user_id):
    """API endpoint to get asset count for a user (for live refresh)"""
    conn = get_db()
    result = conn.execute(
        "SELECT COUNT(*) as count FROM assets WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return {"count": result["count"] if result else 0}


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    conn = get_db()
    user = conn.execute("SELECT id, profile_image, theme FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    if request.method == 'POST':
        theme = request.form.get('theme', 'light')
        file = request.files.get('profile_image')
        filename = None
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"profile_{session['user_id']}{ext}")
            upload_folder = os.path.join(app.static_folder, 'profile_images')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
        if filename:
            conn.execute("UPDATE users SET profile_image = ?, theme = ? WHERE id = ?", (filename, theme, session['user_id']))
        else:
            conn.execute("UPDATE users SET theme = ? WHERE id = ?", (theme, session['user_id']))
        conn.commit()
        conn.close()
        flash('Settings updated.', 'success')
        return redirect(url_for('settings'))
    conn.close()
    return render_template('settings.html', user=user)


@app.route("/logout")
def logout():
    # Mark session as inactive
    if "user_id" in session and "session_id" in session:
        conn = get_db()
        try:
            conn.execute(
                """
                UPDATE user_sessions 
                SET is_active = FALSE, last_activity = ? 
                WHERE user_id = ? AND session_id = ?
                """,
                (datetime.utcnow().isoformat(), session["user_id"], session["session_id"])
            )
            conn.commit()
        except Exception as e:
            print(f"Error updating session on logout: {e}")
        finally:
            conn.close()
    
    session.clear()
    return redirect(url_for("login"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        mobile_number = request.form.get("mobile_number", "").strip()
        
        if not mobile_number:
            flash("Please enter your mobile number.", "error")
            return render_template("forgot_password.html")
        
        conn = get_db()
        user = conn.execute(
            "SELECT id, username FROM users WHERE mobile_number = ?",
            (mobile_number,),
        ).fetchone()
        
        if user:
            # Generate reset token
            reset_token = ''.join(secrets.choice(string.digits) for _ in range(6))
            reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
            
            conn.execute(
                "UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?",
                (reset_token, reset_token_expiry.isoformat(), user["id"])
            )
            conn.commit()
            
            # Send SMS with reset code
            sms_message = f"Your Asset Management password reset code is: {reset_token}. This code expires in 15 minutes."
            sms_sent = send_sms(mobile_number, sms_message)
            
            if sms_sent:
                flash("Password reset code sent to your mobile number.", "success")
                conn.close()
                return redirect(url_for('reset_password', token=reset_token))
            else:
                flash("Failed to send SMS. Please try again.", "error")
                conn.close()
                return render_template("forgot_password.html")
        else:
            conn.close()
            flash("Mobile number not found.", "error")
    
    return render_template("forgot_password.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "POST":
        new_password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        if not new_password or not confirm_password:
            flash("Please fill in all fields.", "error")
            return render_template("reset_password.html", token=token)
        
        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("reset_password.html", token=token)
        
        conn = get_db()
        user = conn.execute(
            "SELECT id FROM users WHERE reset_token = ? AND reset_token_expiry > ?",
            (token, datetime.utcnow().isoformat())
        ).fetchone()
        
        if user:
            conn.execute(
                "UPDATE users SET password = ?, reset_token = NULL, reset_token_expiry = NULL WHERE id = ?",
                (generate_password_hash(new_password), user["id"])
            )
            conn.commit()
            conn.close()
            flash("Password reset successfully! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            conn.close()
            flash("Invalid or expired reset token.", "error")
            return redirect(url_for("forgot_password"))
    
    return render_template("reset_password.html", token=token)


@app.route("/api/verify-reset-token/<token>")
def verify_reset_token(token):
    """API endpoint to verify if reset token is valid (for real-time checking)"""
    conn = get_db()
    user = conn.execute(
        "SELECT id FROM users WHERE reset_token = ? AND reset_token_expiry > ?",
        (token, datetime.utcnow().isoformat())
    ).fetchone()
    conn.close()
    
    return {"valid": user is not None}


@app.route("/notifications")
@login_required
def notifications():
    conn = get_db()
    user_notifications = conn.execute(
        "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    
    # Mark notifications as read
    conn.execute(
        "UPDATE notifications SET is_read = TRUE WHERE user_id = ? AND is_read = FALSE",
        (session["user_id"],)
    )
    conn.commit()
    conn.close()
    
    return render_template("notifications.html", notifications=user_notifications)


@app.route("/api/notifications/count")
@login_required
def get_notification_count():
    conn = get_db()
    count = conn.execute(
        "SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = FALSE",
        (session["user_id"],)
    ).fetchone()["count"]
    conn.close()
    return {"count": count}


@app.route("/api/notifications/mark-read", methods=["POST"])
@login_required
def mark_notifications_read():
    conn = get_db()
    conn.execute(
        "UPDATE notifications SET is_read = TRUE WHERE user_id = ? AND is_read = FALSE",
        (session["user_id"],)
    )
    conn.commit()
    conn.close()
    return {"success": True}


@app.route("/api/asset-lifespan/<int:asset_id>")
@login_required
def get_asset_lifespan(asset_id):
    """API endpoint to get real-time asset lifespan information"""
    conn = get_db()
    asset = conn.execute(
        "SELECT id, user_id, name, purchase_date, duration FROM assets WHERE id = ?",
        (asset_id,)
    ).fetchone()
    
    if not asset:
        conn.close()
        return {"error": "Asset not found"}, 404
    
    if asset['user_id'] != session['user_id'] and session.get('role') != 'admin':
        conn.close()
        return {"error": "Unauthorized"}, 403
    
    # Calculate lifespan
    try:
        purchase_dt = datetime.fromisoformat(asset['purchase_date'])
        total_months = asset['duration']
        total_days = total_months * 30
        
        end_date = purchase_dt + timedelta(days=total_days)
        today = datetime.utcnow()
        
        remaining_seconds = (end_date - today).total_seconds()
        remaining_days = max(0, int(remaining_seconds / 86400))
        remaining_months = remaining_days // 30
        remaining_years = remaining_months // 12
        remaining_months = remaining_months % 12
        
        percentage_remaining = max(0, min(100, (remaining_seconds / (total_days * 86400)) * 100))
        percentage_used = 100 - percentage_remaining
        
        is_expired = remaining_seconds <= 0
        
        conn.close()
        return {
            "asset_name": asset['name'],
            "purchase_date": asset['purchase_date'][:10],
            "end_date": end_date.isoformat()[:10],
            "total_years": total_months // 12,
            "total_months": total_months,
            "remaining_years": remaining_years,
            "remaining_months": remaining_months,
            "remaining_days": remaining_days,
            "percentage_remaining": round(percentage_remaining, 1),
            "percentage_used": round(percentage_used, 1),
            "is_expired": is_expired
        }
    except Exception as e:
        conn.close()
        return {"error": str(e)}, 400


@app.route("/messages")
@login_required
def messages():
    """View user messages"""
    conn = get_db()
    
    # Get conversations (distinct users who have messaged)
    conversations = conn.execute(
        """
        SELECT DISTINCT u.id, u.full_name, u.username, 
               MAX(m.created_at) as last_message_time,
               COUNT(CASE WHEN m.is_read = FALSE AND m.recipient_id = ? THEN 1 END) as unread_count
        FROM (
            SELECT sender_id as user_id, created_at, is_read, recipient_id 
            FROM user_messages WHERE recipient_id = ?
            UNION
            SELECT recipient_id as user_id, created_at, is_read, recipient_id
            FROM user_messages WHERE sender_id = ?
        ) m
        JOIN users u ON u.id = m.user_id
        GROUP BY u.id
        ORDER BY last_message_time DESC
        """,
        (session['user_id'], session['user_id'], session['user_id'])
    ).fetchall()
    
    conn.close()
    return render_template("messages.html", conversations=conversations)


@app.route("/messages/<int:user_id>")
@login_required
def message_thread(user_id):
    """View message thread with specific user"""
    conn = get_db()
    
    # Verify user exists
    other_user = conn.execute(
        "SELECT id, full_name, username FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    
    if not other_user:
        conn.close()
        flash("User not found.", "error")
        return redirect(url_for('messages'))
    
    # Get messages in thread
    messages = conn.execute(
        """
        SELECT id, sender_id, recipient_id, message, is_read, created_at
        FROM user_messages
        WHERE (sender_id = ? AND recipient_id = ?) OR (sender_id = ? AND recipient_id = ?)
        ORDER BY created_at ASC
        """,
        (session['user_id'], user_id, user_id, session['user_id'])
    ).fetchall()
    
    # Mark as read
    conn.execute(
        """
        UPDATE user_messages 
        SET is_read = TRUE 
        WHERE recipient_id = ? AND sender_id = ? AND is_read = FALSE
        """,
        (session['user_id'], user_id)
    )
    conn.commit()
    conn.close()
    
    return render_template("message_thread.html", 
                         other_user=other_user, 
                         messages=messages)


@app.route("/api/send-message/<int:recipient_id>", methods=["POST"])
@login_required
def send_message(recipient_id):
    """API endpoint to send message"""
    conn = get_db()
    
    # Verify recipient exists
    recipient = conn.execute(
        "SELECT id FROM users WHERE id = ?",
        (recipient_id,)
    ).fetchone()
    
    if not recipient:
        conn.close()
        return {"success": False, "error": "Recipient not found"}, 404
    
    message_text = request.form.get('message', '').strip()
    
    if not message_text:
        conn.close()
        return {"success": False, "error": "Message cannot be empty"}, 400
    
    try:
        conn.execute(
            """
            INSERT INTO user_messages (sender_id, recipient_id, message, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (session['user_id'], recipient_id, message_text, datetime.utcnow().isoformat())
        )
        conn.commit()
        
        # Create notification for recipient
        full_name = conn.execute(
            "SELECT full_name FROM users WHERE id = ?",
            (session['user_id'],)
        ).fetchone()['full_name']
        
        conn.execute(
            """
            INSERT INTO notifications (user_id, title, message, type, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (recipient_id, "New Message", f"{full_name} sent you a message", "message", 
             datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Message sent"}
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}, 500


@app.route("/api/unread-messages-count")
@login_required
def get_unread_messages_count():
    """Get count of unread messages"""
    conn = get_db()
    count = conn.execute(
        "SELECT COUNT(*) as count FROM user_messages WHERE recipient_id = ? AND is_read = FALSE",
        (session['user_id'],)
    ).fetchone()['count']
    conn.close()
    return {"count": count}


@app.route("/api/check-auth")
def check_auth():
    """API endpoint to check if user is authenticated"""
    if "user_id" in session:
        return {"authenticated": True, "user_id": session["user_id"]}, 200
    return {"authenticated": False}, 401


@app.route("/api/user-theme", methods=["GET", "POST"])
@login_required
def user_theme():
    """API endpoint to get or set user theme preference"""
    conn = get_db()
    
    if request.method == "GET":
        user = conn.execute(
            "SELECT theme FROM users WHERE id = ?",
            (session['user_id'],)
        ).fetchone()
        conn.close()
        
        if user and user['theme']:
            return {"theme": user['theme']}, 200
        return {"theme": "blue-light"}, 200
    
    elif request.method == "POST":
        try:
            data = request.get_json()
            theme = data.get('theme', 'blue-light')
            
            # Validate theme (ensure it's one of the allowed themes)
            allowed_themes = [
                'light', 'dark',
                'blue-light', 'blue-dark',
                'green-light', 'green-dark',
                'pink-light', 'pink-dark'
            ]
            
            if theme not in allowed_themes:
                conn.close()
                return {"success": False, "error": "Invalid theme"}, 400
            
            conn.execute(
                "UPDATE users SET theme = ? WHERE id = ?",
                (theme, session['user_id'])
            )
            conn.commit()
            conn.close()
            
            return {"success": True, "theme": theme}, 200
        except Exception as e:
            conn.close()
            return {"success": False, "error": str(e)}, 500


init_db()

if __name__ == "__main__":
    app.run(debug=True)
