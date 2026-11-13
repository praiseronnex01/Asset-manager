# Code Snippets Reference

Quick reference for all code changes made to implement the three features.

---

## 1. ADMIN CLEAR HISTORY

### Backend Route (app.py)

```python
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
```

### Frontend Button (admin_user_activity.html)

```html
<form method="POST" action="{{ url_for('admin_clear_history') }}" 
      style="display:inline;" 
      onsubmit="return confirm('Are you sure you want to clear ALL activity history? This action cannot be undone.')">
    <button type="submit" class="danger-link">🗑️ Clear All History</button>
</form>
```

### Refresh Button

```html
<button id="refresh-btn" class="secondary-link" onclick="refreshActivityLogs()">🔄 Refresh</button>
```

### Auto-Refresh JavaScript

```javascript
// Auto-refresh every 30 seconds
setInterval(() => {
    fetch(window.location.href)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');
            const newTable = newDoc.getElementById('activity-table');
            const oldTable = document.getElementById('activity-table');
            if (newTable && oldTable) {
                oldTable.innerHTML = newTable.innerHTML;
            }
        })
        .catch(err => console.log('Auto-refresh failed:', err));
}, 30000);
```

---

## 2. LIVE ASSET COUNTER WITH REFRESH

### Backend API Endpoint (app.py)

```python
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
```

### Frontend Refresh Button (admin_users.html)

```html
<th>Assets <button id="refresh-assets-btn" class="secondary-link" 
                   onclick="refreshAssetCounts()" 
                   title="Refresh asset counts" 
                   style="background:none; border:none; cursor:pointer; padding:0; margin-left:4px;">
                   🔄</button></th>
```

### Asset Count Cell

```html
<td class="asset-count" data-user-id="{{ user.id }}">{{ user.asset_count }}</td>
```

### Refresh Function (JavaScript)

```javascript
async function refreshAssetCounts() {
    const btn = document.getElementById('refresh-assets-btn');
    btn.disabled = true;
    btn.style.opacity = '0.5';
    
    const cells = document.querySelectorAll('.asset-count');
    for (const cell of cells) {
        const userId = cell.dataset.userId;
        try {
            const response = await fetch(`/api/user-asset-count/${userId}`);
            const data = await response.json();
            cell.textContent = data.count;
            cell.style.transition = 'background-color 0.3s';
            cell.style.backgroundColor = '#ffffcc';
            setTimeout(() => {
                cell.style.backgroundColor = 'transparent';
            }, 1000);
        } catch (err) {
            console.error('Failed to refresh asset count for user', userId, err);
        }
    }
    
    setTimeout(() => {
        btn.disabled = false;
        btn.style.opacity = '1';
    }, 500);
}

// Auto-refresh asset counts every 60 seconds
setInterval(refreshAssetCounts, 60000);
```

---

## 3. SMS PASSWORD RESET WITH COUNTDOWN

### SMS Code Generation (app.py - forgot_password route)

```python
# Generate reset token (6-digit code)
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
```

### SMS Function (app.py)

```python
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
```

### Forgot Password Form (forgot_password.html)

```html
<form method="POST" class="form-grid" id="forgot-form">
    <div>
        <label for="mobile_number">Mobile Number</label>
        <input id="mobile_number" type="tel" name="mobile_number" required 
               placeholder="e.g., +265 999 123 456" 
               pattern="\+?[0-9\s\-\(\)]+">
    </div>
    <button type="submit" id="submit-btn" class="primary-btn">
        <span id="btn-text">📱 Send Verification Code</span>
        <span id="btn-loading" style="display: none;">⏳ Sending SMS...</span>
    </button>
</form>

<div id="sms-info" class="info-box" style="display: none; margin-top: 16px; padding: 12px; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;">
    <p><strong>✓ SMS Sent!</strong></p>
    <p style="margin: 8px 0 0 0; font-size: 0.9em;">Check your mobile phone for the verification code. The code expires in <strong>15 minutes</strong>.</p>
</div>
```

### Countdown Timer (reset_password.html)

```html
<div id="token-status" class="token-status" style="padding: 12px; background: #f5f5f5; border-radius: 6px; margin: 16px 0; text-align: center;">
    <span id="status-icon" style="font-size: 24px;">⏳</span>
    <span id="status-text" style="display: block; margin-top: 8px;">Verifying reset code...</span>
    <span id="countdown-timer" style="display: block; margin-top: 4px; font-size: 0.85em; color: #f44336;"></span>
</div>
```

### Countdown Timer JavaScript (reset_password.html)

```javascript
const token = '{{ token }}';
let isValidToken = false;
let tokenExpiry = null;
let countdownInterval = null;

function startCountdown() {
    if (countdownInterval) clearInterval(countdownInterval);
    
    countdownInterval = setInterval(() => {
        if (!tokenExpiry) return;
        
        const now = new Date();
        const diff = tokenExpiry - now;
        
        if (diff <= 0) {
            clearInterval(countdownInterval);
            document.getElementById('countdown-timer').textContent = 'Code expired!';
            document.getElementById('countdown-timer').style.color = '#d32f2f';
            isValidToken = false;
            document.getElementById('reset-form').style.display = 'none';
            verifyToken();
        } else {
            const minutes = Math.floor(diff / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            document.getElementById('countdown-timer').textContent = 
                `Expires in: ${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }, 1000);
}

async function verifyToken() {
    try {
        const res = await fetch(`/api/verify-reset-token/${token}`);
        const data = await res.json();
        const icon = document.getElementById('status-icon');
        const text = document.getElementById('status-text');
        const form = document.getElementById('reset-form');
        
        if (data.valid) {
            isValidToken = true;
            icon.textContent = '✅';
            text.textContent = 'Code verified — set your new password.';
            text.style.color = '#6ee7b7';
            form.style.display = 'grid';
            
            // Calculate expiry time (15 minutes from now)
            tokenExpiry = new Date(Date.now() + 15 * 60000);
            startCountdown();
        } else {
            isValidToken = false;
            icon.textContent = '❌';
            text.textContent = 'Invalid or expired code.';
            text.style.color = '#fca5a5';
            form.style.display = 'none';
        }
    } catch (err) {
        document.getElementById('status-text').textContent = 'Error verifying code.';
    }
}

verifyToken();
setInterval(verifyToken, 5000);
```

### Password Validation (reset_password.html)

```javascript
document.getElementById('reset-form').addEventListener('submit', function(e) {
    if (!isValidToken) { 
        e.preventDefault(); 
        const errorDiv = document.getElementById('error-message');
        const errorText = document.getElementById('error-text');
        errorDiv.style.display = 'block';
        errorText.textContent = 'Reset code is no longer valid. Please request a new one.';
        return; 
    }
    
    const p = document.getElementById('password').value;
    const cp = document.getElementById('confirm_password').value;
    
    if (p.length < 6) {
        e.preventDefault();
        const errorDiv = document.getElementById('error-message');
        const errorText = document.getElementById('error-text');
        errorDiv.style.display = 'block';
        errorText.textContent = 'Password must be at least 6 characters long.';
        return;
    }
    
    if (p !== cp) { 
        e.preventDefault(); 
        const errorDiv = document.getElementById('error-message');
        const errorText = document.getElementById('error-text');
        errorDiv.style.display = 'block';
        errorText.textContent = 'Passwords do not match!';
    }
});
```

---

## SQL Queries for Testing

### Check Activity Logs
```sql
SELECT COUNT(*) as total_activities FROM user_activity;
SELECT * FROM user_activity ORDER BY timestamp DESC LIMIT 10;
```

### Check Asset Counts
```sql
SELECT user_id, COUNT(*) as asset_count FROM assets GROUP BY user_id;
SELECT COUNT(*) FROM assets WHERE user_id = 1;
```

### Check Reset Codes
```sql
SELECT id, username, mobile_number, reset_token, reset_token_expiry 
FROM users 
WHERE reset_token IS NOT NULL;
```

### Check Expired Codes
```sql
SELECT id, username FROM users 
WHERE reset_token IS NOT NULL 
AND reset_token_expiry < datetime('now');
```

---

## Environment Variables (Optional)

For SMS production integration:

```bash
# .env file
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# Or set in your deployment environment
export TWILIO_ACCOUNT_SID="your_account_sid_here"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
export TWILIO_PHONE_NUMBER="+1234567890"
```

---

## Testing Code

### Test Clear History
```python
# In your test file
def test_admin_clear_history():
    client = app.test_client()
    
    # Login as admin
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin_password'
    }, follow_redirects=True)
    
    # Perform some actions to create activity logs
    client.get('/dashboard')
    
    # Clear history
    response = client.post('/admin/clear-history', follow_redirects=True)
    
    assert response.status_code == 200
    assert "cleared successfully" in response.data.decode()
```

### Test Asset Counter API
```python
# In your test file
def test_get_user_asset_count():
    client = app.test_client()
    
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin_password'
    })
    
    # Get asset count for user 1
    response = client.get('/api/user-asset-count/1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'count' in data
    assert isinstance(data['count'], int)
```

### Test SMS Reset Flow
```python
# In your test file
def test_password_reset_with_sms():
    client = app.test_client()
    
    # Request reset code
    response = client.post('/forgot-password', data={
        'mobile_number': '+265999123456'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert "reset" in response.data.decode().lower()
    
    # Verify token
    # Note: Extract token from database for testing
    # response = client.get('/api/verify-reset-token/<token>')
    # assert response.get_json()['valid'] == True
```

---

## Integration Checklist

- [ ] Copy code snippets from this file
- [ ] Verify all routes are added to app.py
- [ ] Verify all templates are updated
- [ ] Test clear history functionality
- [ ] Test asset counter refresh (manual and auto)
- [ ] Test password reset flow
- [ ] Verify SMS messages in console (demo mode)
- [ ] For production: Add Twilio integration
- [ ] For production: Set environment variables
- [ ] Run all tests
- [ ] Deploy to production

---

**Last Updated:** 2026-06-04
**Version:** 1.0.0
