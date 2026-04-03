# 🎯 Admin API Testing & Quick Reference Guide

## 🌐 API Base URL
```
http://localhost:8000/api/admin
```

## 👤 Authentication
All endpoints require admin authentication. Include in header:
```
Authorization: Bearer <token>
```
(Currently using session-based auth, update logic in `backend/app/core/auth.py` for production)

---

## 📊 System Statistics

### Get System Stats
```bash
curl -X GET http://localhost:8000/api/admin/stats \
  -H "Authorization: Bearer admin_token"
```

**Response:**
```json
{
  "total_users": 25,
  "active_users": 23,
  "admin_users": 2,
  "inactive_users": 2,
  "total_forms": 45,
  "total_submissions": 156,
  "total_documents": 89,
  "active_last_7_days": 15,
  "new_users_30_days": 5,
  "timestamp": "2026-03-26T23:15:30.123456"
}
```

---

## 👥 User Management

### 1. Get All Users (with pagination & filters)
```bash
curl -X GET "http://localhost:8000/api/admin/users?skip=0&limit=10&search=&role=&status=active" \
  -H "Authorization: Bearer admin_token"
```

**Query Parameters:**
- `skip`: Skip N records (for pagination)
- `limit`: Limit results to N records
- `search`: Search by username or email
- `role`: Filter by 'admin' or 'user'
- `status`: Filter by 'active' or 'inactive'

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "is_admin": false,
      "is_active": true,
      "created_at": "2026-03-20T10:30:00",
      "last_login": "2026-03-26T15:45:00"
    }
  ],
  "total": 25,
  "skip": 0,
  "limit": 10
}
```

### 2. Get User Details
```bash
curl -X GET http://localhost:8000/api/admin/users/1 \
  -H "Authorization: Bearer admin_token"
```

**Response includes activity summary:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_admin": false,
  "is_active": true,
  "created_at": "2026-03-20T10:30:00",
  "last_login": "2026-03-26T15:45:00",
  "activity": {
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "form_entries": 45,
    "submissions": 12,
    "compositions": 8,
    "period_days": 7
  }
}
```

### 3. Create New User
```bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer admin_token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "SecurePass123!",
    "is_admin": false
  }'
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*...)

**Response:**
```json
{
  "id": 26,
  "username": "new_user",
  "email": "new_user@example.com",
  "is_admin": false,
  "is_active": true,
  "message": "User đã được tạo thành công"
}
```

### 4. Update User
```bash
curl -X PUT http://localhost:8000/api/admin/users/1 \
  -H "Authorization: Bearer admin_token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "updated_name",
    "is_active": true
  }'
```

### 5. Delete (Deactivate) User
```bash
curl -X DELETE http://localhost:8000/api/admin/users/1 \
  -H "Authorization: Bearer admin_token"
```

**Note:** Cannot delete self (current admin user)

**Response:**
```json
{
  "message": "User đã được xóa"
}
```

### 6. Toggle Admin Role
```bash
curl -X POST http://localhost:8000/api/admin/users/1/toggle-admin \
  -H "Authorization: Bearer admin_token"
```

**Response:**
```json
{
  "id": 1,
  "is_admin": true,
  "message": "Thêm quyền admin: john_doe"
}
```

---

## 📋 Form Management

### 1. Get All Forms
```bash
curl -X GET "http://localhost:8000/api/admin/forms?skip=0&limit=10&search=&form_type=" \
  -H "Authorization: Bearer admin_token"
```

**Query Parameters:**
- `search`: Search by form name
- `form_type`: Filter by 'word', 'excel', or 'standard'

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "user_id": 5,
      "form_name": "Customer Registration",
      "description": "Main registration form",
      "form_type": "standard",
      "is_template": false,
      "created_at": "2026-03-15T10:00:00"
    }
  ],
  "total": 45,
  "skip": 0,
  "limit": 10
}
```

### 2. Get Forms Statistics
```bash
curl -X GET http://localhost:8000/api/admin/forms/stats \
  -H "Authorization: Bearer admin_token"
```

**Response:**
```json
{
  "total_forms": 45,
  "word_forms": 12,
  "excel_forms": 18,
  "standard_forms": 15,
  "template_forms": 8,
  "total_submissions": 156
}
```

### 3. Delete Form
```bash
curl -X DELETE http://localhost:8000/api/admin/forms/1 \
  -H "Authorization: Bearer admin_token"
```

---

## 📜 Audit Logs

### Get Audit Logs
```bash
curl -X GET "http://localhost:8000/api/admin/audit-log?skip=0&limit=50&action=&object_type=&days=30" \
  -H "Authorization: Bearer admin_token"
```

**Query Parameters:**
- `action`: Filter by action (user_created, user_updated, user_deleted, form_deleted, etc.)
- `object_type`: Filter by 'user', 'form', 'admin', etc.
- `days`: Get logs from last N days (default: 30)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "admin_id": 1,
      "action": "user_created",
      "object_type": "user",
      "object_id": 26,
      "object_name": "new_user",
      "description": "Tạo user mới: new_user",
      "status": "success",
      "created_at": "2026-03-26T23:15:30"
    }
  ],
  "total": 125,
  "skip": 0,
  "limit": 50
}
```

**Possible Actions:**
- `user_created` - User account created
- `user_updated` - User info updated
- `user_deleted` - User deactivated
- `admin_role_granted` - Admin role added
- `admin_role_revoked` - Admin role removed
- `form_deleted` - Form deleted
- `admin_password_changed` - Admin password changed

---

## ⚙️ Admin Account Management

### Get Current Admin Info
```bash
curl -X GET http://localhost:8000/api/admin/account \
  -H "Authorization: Bearer admin_token"
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_active": true,
  "created_at": "2026-01-01T00:00:00",
  "last_login": "2026-03-26T23:15:30",
  "total_actions": 87,
  "recent_actions": [
    {
      "id": 87,
      "action": "user_created",
      "object_type": "user",
      "object_name": "new_user",
      "created_at": "2026-03-26T23:15:30"
    }
  ]
}
```

### Change Admin Password
```bash
curl -X POST http://localhost:8000/api/admin/account/change-password \
  -H "Authorization: Bearer admin_token" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "OldPass123!",
    "new_password": "NewPass456!"
  }'
```

**Response:**
```json
{
  "message": "Mật khẩu đã được cập nhật"
}
```

---

## 🧪 Testing Checklist

### Basic Functionality
- [ ] Can access `/admin-dashboard`
- [ ] Can access `/admin-users`
- [ ] Can access `/admin-forms`
- [ ] Can access `/admin-reports`
- [ ] Can access `/admin-audit-log`
- [ ] Can access `/admin-account`

### User Management
- [ ] Can retrieve user list
- [ ] Can search users by name/email
- [ ] Can filter users by role
- [ ] Can filter users by status
- [ ] Can create new user
- [ ] Can update user info
- [ ] Can deactivate user
- [ ] Can toggle admin role
- [ ] Cannot delete self (error handling)

### Form Management
- [ ] Can retrieve form list
- [ ] Can search forms
- [ ] Can get form statistics
- [ ] Can delete form

### Audit & Monitoring
- [ ] Can retrieve audit logs
- [ ] Can filter logs by action
- [ ] Can filter logs by date range
- [ ] Can view recent admin actions

### Security
- [ ] Admin access required (401 if not admin)
- [ ] User creation validates password strength
- [ ] Password changes require old password verification
- [ ] All changes logged in audit_logs

---

## 🐛 Common Issues & Solutions

### Error: "Admin access required"
- Ensure user is_admin = true
- Check authentication header

### Error: "User not found"
- Verify user_id exists
- Check user hasn't been truly deleted

### Error: "Email already exists"
- New user email must be unique
- Try different email

### Error: "Password is too weak"
- Password must meet strength requirements:
  - Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char

### Database Table Not Created
- Run: `python -c "from app.main import app; print('DB initialized')"`
- SQLAlchemy will auto-create tables

---

## 📝 Environment Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the app:
```bash
python run.py
```

3. Access API:
```bash
http://localhost:8000/api/admin/stats
```

4. Access Admin Dashboard:
```bash
http://localhost:8000/admin-dashboard
```

---

**Last Updated:** 2026-03-26
**Document Version:** 1.0
