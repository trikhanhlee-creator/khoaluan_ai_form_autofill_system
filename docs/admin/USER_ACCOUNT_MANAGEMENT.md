# Quản Lý Tài Khoản - User Account Management Guide

## 📋 Tổng Quan (Overview)

After login, users can now access account management features through a convenient dropdown menu in the top right corner of the menu page.

## 🎯 Cách Sử Dụng (How to Use)

### Step 1: Đăng Nhập (Login)
- Navigate to `/login`
- Enter credentials
- Successfully logged in

### Step 2: Truy Cập Quản Lý Tài Khoản (Access Account Management)
- Go to home page (`/`)
- Look at top right corner - you'll see user avatar
- Click on user avatar to open dropdown menu
- Select "⚙️ Quản Lý Tài Khoản"

### Step 3: Manage Account
Choose from 4 main sections:

#### 1️⃣ 👤 Hồ Sơ (Profile)
- Update full name
- Change email address  
- Update phone number
- Enter company name
- Enter job position
- Click "💾 Lưu Thay Đổi" to save

#### 2️⃣ 🔐 Mật Khẩu (Password)
- Enter current password
- Enter new password (6+ characters)
- Password strength indicator shows: Yếu (Weak), Trung Bình (Medium), Mạnh (Strong)
- Confirm new password
- Click "🔐 Cập Nhật Mật Khẩu"

#### 3️⃣ 🛡️ Bảo Mật (Security)
- 2FA (Two-Factor Authentication) toggle
- View active sessions
- Logout from all sessions with one click

#### 4️⃣ 🔔 Thông Báo (Notifications)
- Email notifications toggle
- Security alerts toggle
- Weekly report emails toggle
- Click "💾 Lưu Thay Đổi" to save preferences

## 🔌 API Endpoints

### Check Current Session
```
GET /api/auth/session
```
Returns: Current user info if authenticated

### Update Profile
```
PUT /api/auth/update-profile
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+84 123 456 789",
  "company": "Tech Corp",
  "position": "Developer"
}
```

### Change Password
```
POST /api/auth/change-password
Content-Type: application/json

{
  "current_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

## 🎨 UI Components

### Navbar
- Fixed top navigation with AutoFill AI branding
- Theme toggle button (🌙/☀️)
- User avatar with dropdown menu

### Dropdown Menu
- "⚙️ Quản Lý Tài Khoản" - Account management link
- "🚪 Đăng Xuất" - Logout button (red text)

### Settings Layout
- Left sidebar menu (sticky on desktop)
- Four navigation items
- Right content area showing active section
- Form inputs with validation

### Forms
- Text inputs with labels and hints
- Password strength indicator (animated bar)
- Save/Cancel buttons
- Alert messages for success/error

## 🌐 Features

✅ **Session-Based Security**
- All actions require valid session
- Session checked before any page/API access

✅ **Form Validation**
- Password minimum 6 characters
- Email format validation
- Required field checks

✅ **User Feedback**
- Success messages with checkmark ✓
- Error messages with alert ✕
- Info messages with info icon ℹ
- Auto-dismiss alerts after 5 seconds

✅ **Responsive Design**
- Desktop: 2-column layout (menu + content)
- Mobile: Single column with horizontal menu
- Touch-friendly buttons and inputs

✅ **Theme Support**
- Dark mode (default) 🌙
- Light mode ☀️
- Toggle in navbar

## 📍 Page Locations

- User account page: `/user-account`
- Home page (with user menu): `/`
- Login page: `/login`

## 🔐 Security

- Session verification on every request
- Password confirmation for password change
- Current password validation
- No sensitive data stored in frontend
- HTTPS recommended for production

## 💡 Example Usage

```javascript
// In user-account.html, this is how profile is loaded:
fetch('/api/auth/session')
  .then(response => response.json())
  .then(data => {
    if (data.authenticated) {
      const user = data.user;
      document.getElementById('profileUsername').value = user.username;
      document.getElementById('profileEmail').value = user.email;
      // ... populate other fields
    }
  });
```

## ⚠️ Error Handling

| Error | Message | Solution |
|-------|---------|----------|
| Not logged in | "Bạn chưa đăng nhập" | Go to login page |
| Session expired | "Bạn chưa đăng nhập" | Login again |
| Wrong password | "Mật khẩu hiện tại không chính xác" | Check caps lock |
| Password too short | "Mật khẩu mới phải có ít nhất 6 ký tự" | Use longer password |
| Passwords don't match | "Mật khẩu xác nhận không khớp" | Make sure both match |

## 🚀 Quick Tips

1. **Use Strong Password**: Aim for "Mạnh" (Strong) indicator when changing password
2. **Update One Section at a Time**: Focus on one settings tab at a time
3. **Save Changes**: Don't forget to click save buttons
4. **Check Notifications**: Configure alerts to stay informed

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-26  
**Languages Supported**: Vietnamese (Tiếng Việt), English (UI framework ready)
