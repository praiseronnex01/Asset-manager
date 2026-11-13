# Quick Start Guide - New Features

## 🚀 How to Use the New Features

### Feature 1: Admin Clear History

**Access:** Admin Panel → Activity Logs (`/admin/user-activity`)

**Steps:**
1. Go to the Activity Logs page
2. Click the **🗑️ Clear All History** button
3. Confirm the action when prompted
4. All activity logs will be deleted
5. Success message will appear

**Note:** This action cannot be undone!

---

### Feature 2: Live Asset Counter with Refresh

**Access:** Admin Panel → Users (`/admin/users`)

**Features:**
- **View:** Automatic asset counts displayed for each user
- **Manual Refresh:** Click 🔄 button to instantly update all counts
- **Auto Refresh:** Counts update every 60 seconds automatically
- **Visual Feedback:** Cells highlight yellow when refreshed

**How to Use:**
1. Go to Users management page
2. Check the "Assets" column for asset counts
3. Click 🔄 **Refresh** button to update manually
4. Watch for auto-updates every minute

---

### Feature 3: SMS Password Reset with Countdown

**Access:** Forgot Password (`/forgot-password`)

**Step 1: Request Reset Code**
1. Click "Forgot Password" on login page
2. Enter your mobile number (e.g., +265 999 123 456)
3. Click "📱 Send Verification Code"
4. Check your phone for SMS with 6-digit code
5. Note: For demo, code appears in console/logs

**Step 2: Reset Password**
1. After SMS is sent, you'll be redirected to reset page
2. **Countdown Timer** shows how much time remains (max 15 minutes)
3. Enter your mobile number's 6-digit verification code (automatically)
4. Create your new password (min 6 characters)
5. Confirm the new password
6. Click "🔐 Reset Password"
7. You'll be redirected to login page
8. Log in with your new password

**Countdown Timer Details:**
- Shows format: `Expires in: MM:SS`
- Updates every second
- Turns red if code is about to expire
- If timer reaches 0, you must request a new code

---

## 🔧 For Developers

### API Endpoints Added

**1. Clear Activity History**
```
POST /admin/clear-history
Requires: Admin role
Returns: Redirect to activity page with success message
```

**2. Get User Asset Count**
```
GET /api/user-asset-count/<user_id>
Requires: Admin role
Returns: {"count": 5}
```

### New Database Queries
- No new tables created
- Uses existing columns: `mobile_number`, `reset_token`, `reset_token_expiry`
- Activity logs stored in `user_activity` table

---

## 📱 SMS Configuration (For Production)

To enable real SMS sending:

1. **Install Twilio:**
   ```bash
   pip install twilio
   ```

2. **Set Environment Variables:**
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

3. **Uncomment Code in `app.py`** (lines 41-50):
   - Uncomment the Twilio integration code in `send_sms()` function
   - Replace placeholder values with your credentials

4. **Test:**
   - Try password reset flow
   - SMS should be sent to provided number

---

## 🛡️ Security Notes

✅ All features require proper authentication
✅ Clear history requires admin role
✅ Asset counter requires admin role
✅ Reset codes expire after 15 minutes
✅ All actions are logged for audit trail
✅ Confirmation dialogs prevent accidents

---

## 🐛 Troubleshooting

**Issue:** SMS not appearing
- **Solution:** For demo mode, check server console/logs for SMS message

**Issue:** Reset code expired
- **Solution:** Request a new code from forgot password page

**Issue:** Asset counts not updating
- **Solution:** 
  - Manual refresh: Click 🔄 button
  - Wait for auto-refresh: 60 seconds
  - Check browser console for errors (F12 → Console tab)

**Issue:** Activity logs not showing
- **Solution:**
  - Activity is only logged after users perform actions
  - Wait for users to add assets or perform actions
  - Refresh page to see latest logs

---

## 📊 Live Data

### Auto-Refresh Intervals
- **Asset Counts:** Every 60 seconds
- **Activity Logs:** Every 30 seconds (if enabled)

### Expiration Times
- **Reset Codes:** 15 minutes
- **Activity Logs:** Last 24 hours shown

---

## ✨ UI/UX Highlights

✅ Clean, modern interface with icons
✅ Confirmation dialogs for destructive actions
✅ Real-time countdown timer
✅ Visual feedback (highlighting, loading states)
✅ Responsive design for mobile devices
✅ Auto-refresh without manual intervention
✅ Clear success/error messages

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Review `FEATURES_ADDED.md` for detailed documentation
3. Check browser console (F12) for JavaScript errors
4. Check server logs for backend errors

---

**Last Updated:** 2026-06-04
**Version:** 1.0.0
