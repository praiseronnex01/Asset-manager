# Feature Flow Diagrams

## Feature 1: Admin Clear History

```
┌─────────────────────────────────────────────────┐
│         Admin User Workflow                      │
│                                                  │
│  Step 1: Navigate to Activity Logs              │
│  ────────────────────────────────────────────┐  │
│                                              │  │
│  URL: /admin/user-activity                  │  │
│                                              ▼  │
│  ┌──────────────────────────────────────────┐  │
│  │  📋 Activity Logs Page                    │  │
│  │                                           │  │
│  │  [🔄 Refresh] [🗑️ Clear All History]    │  │
│  │                                           │  │
│  │  ┌─────────────────────────────────────┐ │  │
│  │  │ User    │ Action │ Details │ Time  │ │  │
│  │  │─────────┼────────┼─────────┼───────│ │  │
│  │  │ John    │ login  │ Via Web │ 10:25│ │  │
│  │  │ Jane    │ add... │ Asset   │ 10:30│ │  │
│  │  │ Bob     │ delete │ Asset   │ 10:35│ │  │
│  │  └─────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────┘  │
│         ▲                                       │
│         │                                       │
│  Step 2: Click Clear Button                    │
│  ────────────────────────────────────────────┐ │
│                                              │ │
│  Confirmation Dialog:                        │ │
│  "Are you sure you want to clear ALL        │ │
│   activity history? This action cannot      │ │
│   be undone."                               │ │
│                                              │ │
│  [Cancel] [OK]                              │ │
│         ▲                                     │ │
│         │                                     │ │
│  Step 3: Confirm Deletion                   │ │
│  ────────────────────────────────────────────┼─┘
│                                              │
│  Backend: DELETE FROM user_activity         │
│                                              ▼
│  ┌──────────────────────────────────────────┐
│  │  ✓ Success!                              │
│  │  "All activity history has been         │
│  │   cleared successfully"                  │
│  │                                          │
│  │  ┌──────────────────────────────────┐   │
│  │  │ Activity table is now empty:     │   │
│  │  │ No recent activity found.        │   │
│  │  └──────────────────────────────────┘   │
│  └──────────────────────────────────────────┘
│
└─────────────────────────────────────────────────┘
```

---

## Feature 2: Live Asset Counter with Refresh

```
┌─────────────────────────────────────────────────────────┐
│         Asset Counter Workflow                          │
│                                                          │
│  Admin Views Users Page (/admin/users)                  │
│  ────────────────────────────────────────┐              │
│                                          │              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 👥 Registered Users                             │   │
│  │                                                 │   │
│  │ [Search Box] [Search] [Reset]                  │   │
│  │                                                 │   │
│  │ Name    │ Username │ Role   │ Status │ Assets │   │
│  │─────────┼──────────┼────────┼────────┼────────│   │
│  │ John    │ john.d   │ user   │ Active │  5  🔄│   │
│  │ Jane    │ jane.s   │ user   │ Active │  12 🔄│   │
│  │ Bob     │ bob.j    │ admin  │ Active │  8  🔄│   │
│  │                                                 │   │
│  │ [Refresh Button in Header ^]                   │   │
│  └─────────────────────────────────────────────────┘   │
│         ▲                                               │
│         │                                               │
│  Manual Refresh:                                        │
│  Admin clicks 🔄 button                                 │
│         │                                               │
│         ▼                                               │
│  ┌──────────────────────────────────────────────┐      │
│  │  JavaScript: Calls /api/user-asset-count/   │      │
│  │  for each user                              │      │
│  │                                             │      │
│  │  AJAX Request:                              │      │
│  │  GET /api/user-asset-count/1 → {count: 5} │      │
│  │  GET /api/user-asset-count/2 → {count: 12}│      │
│  │  GET /api/user-asset-count/3 → {count: 8} │      │
│  └──────────────────────────────────────────────┘      │
│         ▼                                               │
│  ┌──────────────────────────────────────────────┐      │
│  │  Update Display & Highlight in Yellow       │      │
│  │                                             │      │
│  │  Assets │                                  │      │
│  │─────────│                                  │      │
│  │  5   🟨 │ ← 1 second yellow highlight      │      │
│  │  12  🟨 │                                  │      │
│  │  8   🟨 │                                  │      │
│  │         │                                  │      │
│  │  (After 1 second, highlight fades)       │      │
│  └──────────────────────────────────────────────┘      │
│         ▲                                               │
│         │                                               │
│  Auto-Refresh: Every 60 seconds                        │
│  (Happens in background automatically)                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Feature 3: SMS Password Reset with Countdown Timer

```
┌────────────────────────────────────────────────────────────────────┐
│         SMS Password Reset Workflow                                 │
│                                                                     │
│ STEP 1: User Forgot Password                                       │
│ ─────────────────────────────────────────────────────────────────┐ │
│                                                                   │ │
│  Login Page                                                      │ │
│  ┌──────────────────────────────┐                              │ │
│  │ Username: [____________]     │                              │ │
│  │ Password: [____________]     │                              │ │
│  │ [Login]  [Forgot Password?]──┼──────────────────────────┐  │ │
│  └──────────────────────────────┘                          │  │ │
│                                                            ▼  │ │
│ STEP 2: Request Reset Code                                   │ │
│ ┌────────────────────────────────────────────────────────┐   │ │
│ │  Reset Password Page                                  │   │ │
│ │  (/forgot-password)                                   │   │ │
│ │                                                        │   │ │
│ │  Mobile Number: [+265 999 123 456]                    │   │ │
│ │  [📱 Send Verification Code]                          │   │ │
│ │  (shows: "⏳ Sending SMS...")                          │   │ │
│ └────────────────────────────────────────────────────────┘   │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ BACKEND:                                                      │ │
│  - Generate 6-digit code: 482056                             │ │
│  - Set expiry: +15 minutes                                   │ │
│  - Send SMS: "Your code is: 482056..."                       │ │
│  - Save to DB: reset_token, reset_token_expiry              │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ ┌────────────────────────────────────────────────────────┐   │ │
│ │  Success Message:                                     │   │ │
│ │  "✓ SMS Sent!"                                        │   │ │
│ │  Check your mobile for verification code.            │   │ │
│ │  Code expires in 15 minutes.                         │   │ │
│ │                                                        │   │ │
│ │  [← Request a new code] [Back to login]              │   │ │
│ └────────────────────────────────────────────────────────┘   │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ User's Phone (SMS received):                                 │ │
│ ┌────────────────────────────────────────────────────────┐   │ │
│ │ From: NOBLE ASSETS                                    │   │ │
│ │ Your Asset Management password reset code is:         │   │ │
│ │                                                        │   │ │
│ │           482056                                      │   │ │
│ │                                                        │   │ │
│ │ This code expires in 15 minutes.                      │   │ │
│ └────────────────────────────────────────────────────────┘   │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ STEP 3: Verify & Reset Password                              │ │
│ ┌────────────────────────────────────────────────────────┐   │ │
│ │  Reset Password Page                                  │   │ │
│ │  (/reset-password/482056)                             │   │ │
│ │                                                        │   │ │
│ │  ┌──────────────────────────────────────────────────┐ │   │ │
│ │  │ ⏳ Verifying reset code...                      │ │   │ │
│ │  └──────────────────────────────────────────────────┘ │   │ │
│ │         ▼ (after validation)                           │   │ │
│ │  ┌──────────────────────────────────────────────────┐ │   │ │
│ │  │ ✅ Code verified                                │ │   │ │
│ │  │ Expires in: 14:32 ⏱️                           │ │   │ │
│ │  │                                                 │ │   │ │
│ │  │ New Password: [__________]                     │ │   │ │
│ │  │ Confirm:     [__________]                     │ │   │ │
│ │  │                                                 │ │   │ │
│ │  │ [🔐 Reset Password]                            │ │   │ │
│ │  └──────────────────────────────────────────────────┘ │   │ │
│ └────────────────────────────────────────────────────────┘   │ │
│         │                                                      │ │
│         │ Countdown Timer Running:                            │ │
│         │ ┌─────────────────────────────────────────┐         │ │
│         │ │ Expires in: 14:32 → 14:31 → 14:30...  │         │ │
│         │ └─────────────────────────────────────────┘         │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ User enters password & clicks Reset                          │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ BACKEND VALIDATION:                                          │ │
│  - Check token validity ✓                                    │ │
│  - Check token not expired ✓                                 │ │
│  - Hash new password                                         │ │
│  - Update database                                           │ │
│         │                                                      │ │
│         ▼                                                      │ │
│ ┌────────────────────────────────────────────────────────┐   │ │
│ │  Success! Redirected to Login                         │   │ │
│ │  "Password reset successfully!                        │   │ │
│ │   Please log in."                                     │   │ │
│ │                                                        │   │ │
│ │  Username: [______________]                          │   │ │
│ │  Password: [______________] (NEW PASSWORD)           │   │ │
│ │  [Login] ← Now works with new password               │   │ │
│ └────────────────────────────────────────────────────────┘   │ │
│                                                               │ │
└───────────────────────────────────────────────────────────────┘ │
```

---

## Countdown Timer Details

```
┌──────────────────────────────────────────────────────┐
│  Countdown Timer Behavior                            │
│                                                      │
│  Timer Display: "Expires in: MM:SS"                 │
│                                                      │
│  Timeline:                                           │
│  ┌──────────────────────────────────────────────┐   │
│  │ 00:00  Code received                         │   │
│  │ ▼                                             │   │
│  │ 15:00  Timer starts (15 minutes remaining)   │   │
│  │ 14:59  Count down continues...               │   │
│  │ 14:58                                         │   │
│  │  :      (every second)                        │   │
│  │  :                                            │   │
│  │ 05:00  5 minutes remaining                   │   │
│  │ 04:00  4 minutes remaining                   │   │
│  │ 03:00  3 minutes remaining (⚠️ 20% time left)│   │
│  │ 02:00  2 minutes remaining                   │   │
│  │ 01:00  1 minute remaining 🔴                 │   │
│  │ 00:30  30 seconds remaining (RED TEXT)       │   │
│  │ 00:00  Code EXPIRED ❌                        │   │
│  │        Error: "Code expired!"                │   │
│  │        [← Request a new code]                │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Color Scheme:                                       │
│  15:00 - 01:00  → Normal (#f44336 red)             │   │
│  00:59 - 00:00  → Urgent (#d32f2f darker red)      │   │
│  EXPIRED        → Error state                       │   │
│                                                      │
│  User Actions Before Expiry:                        │
│  ✅ Can enter password & reset (works)             │   │
│  ✅ Submit before 15 mins = SUCCESS                │   │
│  ✅ If 15 mins pass, redirected to new code page  │   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Database Schema Changes

```
┌─────────────────────────────────────────────────────┐
│  Existing Tables Used (NO Changes Required)         │
│                                                     │
│  ┌─────────────────────────────────────┐            │
│  │  users TABLE                        │            │
│  ├─────────────────────────────────────┤            │
│  │ id INTEGER (PK)                     │            │
│  │ username TEXT UNIQUE                │            │
│  │ password TEXT                       │            │
│  │ mobile_number TEXT  ◄─────┐         │            │
│  │ reset_token TEXT ◄────────┤─ New Features       │
│  │ reset_token_expiry TEXT ◄─┤ Use These           │
│  │ role TEXT                 │         │            │
│  │ is_suspended BOOLEAN      │         │            │
│  │ is_active BOOLEAN         │         │            │
│  └─────────────────────────────────────┘            │
│                                                     │
│  ┌─────────────────────────────────────┐            │
│  │  user_activity TABLE                │            │
│  ├─────────────────────────────────────┤            │
│  │ id INTEGER (PK)                     │            │
│  │ user_id INTEGER (FK)                │            │
│  │ action TEXT      ◄──── Used by:     │            │
│  │ details TEXT          Clear History │            │
│  │ timestamp TEXT        Feature       │            │
│  │ ip_address TEXT                     │            │
│  │ user_agent TEXT                     │            │
│  └─────────────────────────────────────┘            │
│                                                     │
│  ┌─────────────────────────────────────┐            │
│  │  assets TABLE                       │            │
│  ├─────────────────────────────────────┤            │
│  │ id INTEGER (PK)                     │            │
│  │ user_id INTEGER (FK) ◄──── Used by: │            │
│  │ name TEXT                  Asset    │            │
│  │ category TEXT              Counter  │            │
│  │ purchase_date TEXT         Feature  │            │
│  │ quantity INTEGER                    │            │
│  │ duration INTEGER                    │            │
│  │ purchase_value REAL                 │            │
│  │ created_at TEXT                     │            │
│  └─────────────────────────────────────┘            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## API Endpoint Responses

```
┌──────────────────────────────────────────────────────┐
│  GET /api/user-asset-count/1                        │
│  ────────────────────────────────────────────────────│
│  Response:                                           │
│  {                                                   │
│    "count": 5                                        │
│  }                                                   │
│                                                      │
│  Status: 200 OK                                     │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  GET /api/verify-reset-token/482056                 │
│  ────────────────────────────────────────────────────│
│  Response (Valid):                                  │
│  {                                                   │
│    "valid": true                                     │
│  }                                                   │
│                                                      │
│  Response (Expired/Invalid):                        │
│  {                                                   │
│    "valid": false                                    │
│  }                                                   │
│                                                      │
│  Status: 200 OK                                     │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  POST /admin/clear-history                          │
│  ────────────────────────────────────────────────────│
│  Action: Deletes all records from user_activity    │
│                                                      │
│  Response: Redirect to /admin/user-activity        │
│           with flash: "All activity history has    │
│           been cleared successfully."              │
│                                                      │
│  Status: 302 Redirect                              │
└──────────────────────────────────────────────────────┘
```

---

## Summary

These diagrams show:

1. **Clear History Flow** - Admin confirmation workflow
2. **Asset Counter Flow** - Manual and auto-refresh process  
3. **SMS Reset Flow** - Complete password reset journey
4. **Countdown Timer** - Real-time expiration tracking
5. **Database Usage** - Existing schema utilization
6. **API Responses** - JSON payload examples

All features work together seamlessly in the Asset Management System!
