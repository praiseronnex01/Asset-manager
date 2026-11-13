# Asset Lifespan Calculator & User Messaging System

## Overview
Two major features have been added to enhance asset tracking and user communication:

1. **Asset Lifespan Live Calculator** - Real-time display of asset depreciation with visual progress bars
2. **User-to-User Messaging System** - In-app messaging between users with notifications

---

## Feature 1: Asset Lifespan Live Calculator

### 🎯 Functionality
- Real-time calculation of remaining asset lifespan
- Visual depreciation progress bar (color-coded)
- Time remaining display in years, months, and days
- Expiration alerts and status indicators

### 📊 Components

#### Live Calculation
```
Purchase Date: 2023-06-04
Useful Life: 5 years
End Date: 2028-06-04
Today: 2026-06-04

Remaining: 2 years, 0 months, 0 days
Percentage Used: 40.0%
Percentage Remaining: 60.0%
```

#### Visual Progress Bar
- **Green (60-100%)**: Asset healthy, plenty of useful life remaining
- **Orange (25-60%)**: Asset in mid-life, monitor depreciation
- **Red (0-25%)**: Asset nearing end of useful life, plan replacement

#### Status Indicators
- ✓ **Active** - Asset has >25% lifespan remaining
- ⏳ **Nearing End** - Asset has 10-25% lifespan remaining
- ⚠️ **Expiring Soon** - Asset has <10% lifespan remaining
- ⚠️ **EXPIRED** - Asset has exceeded its useful life

### 📍 Display Locations

The lifespan calculator can be embedded in:
1. Dashboard (for all user assets overview)
2. Asset detail pages
3. Asset lists
4. Admin reports

### 🔧 Backend Implementation

**API Endpoint:**
```
GET /api/asset-lifespan/<asset_id>
```

**Request:**
- Requires login
- Asset must belong to user or user must be admin

**Response Example:**
```json
{
    "asset_name": "Office Desk",
    "purchase_date": "2023-06-04",
    "end_date": "2028-06-04",
    "total_years": 5,
    "total_months": 60,
    "remaining_years": 2,
    "remaining_months": 0,
    "remaining_days": 0,
    "percentage_remaining": 60.0,
    "percentage_used": 40.0,
    "is_expired": false
}
```

### 💻 Frontend Component

**Usage in Templates:**
```html
{% include 'asset_lifespan_component.html' %}
```

**or**

```html
<div class="asset-lifespan-widget" data-asset-id="{{ asset.id }}">
    <!-- Component loads automatically -->
</div>
```

### ⚙️ Features

✅ **Real-time Updates** - Refreshes every 60 seconds
✅ **Color-Coded Progress Bar** - Visual depreciation
✅ **Countdown Display** - Years, months, days remaining
✅ **Expiration Alerts** - Status indicators
✅ **Responsive Design** - Works on all devices
✅ **Auto-Refresh** - Background updates without manual refresh

### 📱 Display Example

```
┌─────────────────────────────────────┐
│ Office Desk              [Hardware] │
├─────────────────────────────────────┤
│                                     │
│ Purchase: 2023-06-04  End: 2028-06 │
│ Status: ✓ Active                    │
│                                     │
│ Progress Bar: ███████░░░░░░░░░░░░  │
│ Used: 40.0%         Remaining: 60% │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │  2          0          0        │ │
│ │ Years      Months     Days      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Total Useful Life: 5 years (60mo)  │
│ Purchased: 2023-06-04              │
│ Expires: 2028-06-04                │
│                                     │
└─────────────────────────────────────┘
```

---

## Feature 2: User-to-User Messaging System

### 💬 Functionality
- Send and receive direct messages between users
- Message history and conversations
- Read/unread message tracking
- Real-time message notifications
- Message timestamps and user display

### 📍 Pages

#### 1. Messages List (`/messages`)
- Shows all active conversations
- Unread message count for each conversation
- Last message timestamp
- Click to open conversation

#### 2. Message Thread (`/messages/<user_id>`)
- Full message history with a specific user
- Real-time message sending
- Auto-refresh every 3 seconds
- User information display

### 🔧 Backend Implementation

**Database Tables:**
```
user_messages
├── id
├── sender_id (FK: users)
├── recipient_id (FK: users)
├── message (TEXT)
├── is_read (BOOLEAN)
└── created_at (TIMESTAMP)
```

**API Endpoints:**

1. **Get Messages**
```
GET /messages
GET /messages/<user_id>
```

2. **Send Message**
```
POST /api/send-message/<recipient_id>
Content-Type: application/x-www-form-urlencoded

message=Hello%20there
```

**Response:**
```json
{
    "success": true,
    "message": "Message sent"
}
```

3. **Get Unread Count**
```
GET /api/unread-messages-count

Response: {"count": 3}
```

### 💻 Frontend Components

**Messages List:**
- Interactive conversation cards
- Hover effects
- Unread badge counter
- Last message preview with date

**Message Thread:**
- Scrollable message area
- Message bubbles (different color for sent/received)
- Timestamp on each message
- Message input box with send button
- Auto-scroll to latest message

### 🎨 UI/UX Features

✅ **Message Bubbles** - Sent (green) vs Received (gray)
✅ **Auto-Refresh** - Updates every 3 seconds
✅ **Unread Indicators** - Green badge with count
✅ **Timestamps** - HH:MM:SS format
✅ **User Names** - Display sender/recipient info
✅ **Responsive Design** - Mobile-friendly

### 📨 Display Example

**Conversations List:**
```
┌──────────────────────────────────────────────┐
│ 💬 Messages                                  │
├──────────────────────────────────────────────┤
│                                              │
│ John Doe              Last: 2026-06-04 ┌─┐ │
│ @john.d               Last msg: today  │2│ │
│                                        └─┘ │
│ Jane Smith            Last: 2026-06-04     │
│ @jane.s               Last msg: today      │
│                                            │
│ Bob Johnson           Last: 2026-06-03     │
│ @bob.j                Last msg: yesterday  │
│                                            │
└──────────────────────────────────────────────┘
```

**Message Thread:**
```
┌─────────────────────────────────────────────┐
│ 💬 Conversation with John Doe               │
│ @john.d                      ← Back to Chat │
├─────────────────────────────────────────────┤
│                                             │
│ [RECEIVED] Hello, how are you?              │
│           10:15 AM                          │
│                                             │
│                [SENT] Hi! I'm good!         │
│                      10:16 AM                │
│                                             │
│ [RECEIVED] Want to discuss the Q2 report?  │
│           10:17 AM                          │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Type your message...         [Send] 📤 │ │
│ └─────────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

### 🔔 Notifications

When a user receives a message:
1. A notification is created automatically
2. Unread badge appears on Messages link
3. Desktop notification (if browser supports)
4. Email notification (optional, can be configured)

**Notification Content:**
```
Title: "New Message"
Message: "[Sender Name] sent you a message"
Type: "message"
```

### 🔐 Security Features

✅ **Authentication Required** - Login required to view/send messages
✅ **Permission Checks** - Users can only view their own messages
✅ **Message Ownership** - Verify sender identity
✅ **SQL Injection Prevention** - Parameterized queries
✅ **XSS Prevention** - HTML encoding in templates

---

## Integration Points

### Navigation Bar
- **Messages Link** - Always visible for logged-in users
- **Unread Badge** - Shows count of unread messages
- **Auto-Update** - Badge refreshes every 30 seconds

### Dashboard
- Quick message count widget (optional)
- Recent conversations list (optional)

### Admin Features
- View/moderate messages (optional)
- Message history for user activity
- Message analytics

---

## Database Schema

### asset_alerts Table (Bonus Feature)
```sql
CREATE TABLE asset_alerts (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER (FK),
    user_id INTEGER (FK),
    alert_type TEXT,  -- 'expiring_soon', 'expired', 'maintenance_due'
    status TEXT DEFAULT 'active',
    created_at TEXT
)
```

### user_messages Table
```sql
CREATE TABLE user_messages (
    id INTEGER PRIMARY KEY,
    sender_id INTEGER (FK),
    recipient_id INTEGER (FK),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TEXT NOT NULL
)
```

---

## Usage Workflows

### For Users

**Viewing Asset Lifespan:**
1. Go to Dashboard
2. Asset cards show lifespan info automatically
3. Or navigate to specific asset page
4. Monitor progress bar for depreciation status
5. Take action when nearing expiration (renewal, disposal, etc.)

**Sending Messages:**
1. Click "Messages" in navigation
2. View existing conversations or start new one
3. Find user to message (or go directly via `/messages/<user_id>`)
4. Type message in text area
5. Click Send
6. Message appears in thread immediately
7. Recipient receives notification

**Receiving Messages:**
1. Notification badge appears on Messages link
2. Click Messages to view conversations
3. Click conversation to read full thread
4. Messages marked as read automatically
5. Badge count updates

---

## Testing

### Asset Lifespan Calculator
```javascript
// Test API
fetch('/api/asset-lifespan/1')
    .then(r => r.json())
    .then(data => console.log(data));

// Should return:
{
    "asset_name": "...",
    "purchase_date": "...",
    "end_date": "...",
    "remaining_years": 2,
    "remaining_months": 0,
    "remaining_days": 0,
    "percentage_remaining": 60.0,
    "percentage_used": 40.0,
    "is_expired": false
}
```

### Messaging System
```javascript
// Send message
const formData = new FormData();
formData.append('message', 'Hello!');
fetch('/api/send-message/2', {
    method: 'POST',
    body: formData
}).then(r => r.json());

// Get unread count
fetch('/api/unread-messages-count')
    .then(r => r.json());
    // Returns: {"count": 3}
```

---

## SQL Queries

### Asset Expiring Soon (Administrative)
```sql
SELECT a.*, u.full_name, u.email
FROM assets a
JOIN users u ON a.user_id = u.id
WHERE a.purchase_date < date('now', '-' || duration || ' months')
ORDER BY (a.purchase_date + (duration * 30) / 86400) ASC;
```

### User Conversation Count
```sql
SELECT COUNT(DISTINCT 
    CASE 
        WHEN sender_id = 1 THEN recipient_id
        WHEN recipient_id = 1 THEN sender_id
    END
) as conversation_count
FROM user_messages
WHERE sender_id = 1 OR recipient_id = 1;
```

### Unread Messages
```sql
SELECT COUNT(*) as unread_count
FROM user_messages
WHERE recipient_id = 1 AND is_read = FALSE;
```

---

## Future Enhancements

### Asset Lifespan
- [ ] Depreciation calculation methods (straight-line, declining-balance)
- [ ] Scheduled alerts before expiration
- [ ] Asset maintenance reminders
- [ ] Automatic disposal workflow
- [ ] Salvage value tracking
- [ ] Bulk asset renewal

### Messaging
- [ ] Group messaging/conversations
- [ ] Message search functionality
- [ ] Message attachments/files
- [ ] Message reactions/emoji
- [ ] Message editing/deletion
- [ ] Read receipts (typing, seen indicators)
- [ ] Archiving conversations
- [ ] Block user feature
- [ ] Message encryption (end-to-end)

---

## Performance Notes

- Asset lifespan calculated on-demand (cached for 60s)
- Messages paginated (load older messages on scroll)
- Unread count cached (updated every 30s)
- Auto-refresh uses efficient polling (every 3-30s)

---

## Security Considerations

- ✅ CSRF protection via Flask sessions
- ✅ Input validation on all message content
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS prevention (template auto-escaping)
- ✅ Authentication required for all features
- ✅ Authorization checks on sensitive operations
- ⚠️ Consider: Rate limiting on message API
- ⚠️ Consider: Message encryption for sensitive conversations

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Lifespan not updating | Refresh page or wait 60 seconds |
| Messages not appearing | Check browser console, verify recipient exists |
| Notification badge stuck | Clear browser cache, refresh page |
| Asset shows expired incorrectly | Verify purchase_date format (YYYY-MM-DD) |
| Messages not sending | Ensure valid recipient_id, check network tab |

---

## Summary

✅ **Asset Lifespan Calculator** - Production-ready with real-time updates
✅ **User Messaging System** - Fully functional peer-to-peer chat
✅ **Notifications Integration** - Automatic alerts for new messages
✅ **Security Measures** - All best practices implemented

**Total New Features:** 2 major + 1 bonus (alerts table)
**New Database Tables:** 2 (user_messages, asset_alerts)
**New API Endpoints:** 4 (lifespan, send-message, unread-count, message-list)
**New Pages:** 2 (messages, message-thread)

---

**Last Updated:** 2026-06-04
**Version:** 1.0.0
