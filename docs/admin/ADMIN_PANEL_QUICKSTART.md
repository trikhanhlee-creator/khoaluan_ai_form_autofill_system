# Admin Panel - Quick Start Guide

## ✅ System Status
All components integrated and tested successfully
- Database: ✓ Seeded with test accounts
- API: ✓ Connected to real database
- UI: ✓ Light/dark mode themes working
- Security: ✓ Password hashing and verification working

---

## 🔐 Account Credentials

### ADMIN Account
```
Email:    admin@example.com
Password: admin123
```
**Permissions:** Full access to admin panel, all management features

### REGULAR USER Account
```
Email:    user@example.com
Password: user123
```
**Permissions:** Limited to user-side features

---

## 🚀 How to Start

### 1. Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start Frontend
```bash
# Open in browser or start web server
# Usually on http://localhost:3000 or http://localhost
```

### 3. Admin Login
1. Navigate to login page
2. Enter: `admin@example.com`
3. Enter password: `admin123`
4. Click login

---

## 📊 Admin Dashboard Features

### Available Pages:
- **Dashboard** - Real-time statistics from database
- **Users Management** - View all users (4 total)
- **Forms Management** - Manage form templates
- **Activity Log** - Track user actions
- **Reports** - Generate reports from real data
- **Settings** - Admin settings

### What's Real Data vs Mock:
- ✓ User list comes from database
- ✓ Statistics computed from real data
- ✓ Activity logs stored in database
- ✓ Form count reflects actual forms
- ✓ Everything is now database-driven!

---

## 🧪 Test Data

### Existing Users (Pre-seeded)
1. **user_1** (user_1@autofill.local) - Regular user
2. **user_999** (user_999@autofill.local) - Regular user

### New Test Users (Newly Seeded)
3. **user** (user@example.com) - Regular user
4. **admin** (admin@example.com) - Administrator

---

## 🔍 Verify Everything Works

### Run Integration Tests
```bash
cd backend
python scripts/test_admin_api.py
```

Expected output:
```
✄ 4 users retrieved from database
✓ Found 3 regular users
✓ Found 1 admin user
✓ user@example.com + 'user123': VALID
✓ admin@example.com + 'admin123': VALID
✓ Database seeding completed successfully!
```

---

## 🎨 UI Themes

### Light Mode
- Click theme icon in top right
- Background: White/light colors
- Text: Dark (high contrast)
- Perfect for daytime use

### Dark Mode
- Click theme icon in top right
- Background: Dark colors
- Text: Light (high contrast)
- Perfect for nighttime use

**Note:** Theme preference is saved automatically

---

## 🛠️ Database Operations

### Check Database Users
```bash
cd backend
python scripts/test_admin_api.py
```

### Seed More Users (if needed)
```bash
cd backend
python scripts/seed_users.py
```

### Update Schema (if needed)
```bash
cd backend
python scripts/update_schema.py
```

---

## 🔐 Security Features

### Password Hashing
- Algorithm: Bcrypt with 12 rounds
- Format: $2b$ bcrypt standard
- Example hash: `$2b$12$gF/XDydihUtMp...`

### Password Verification
- Checked on every login
- Wrong passwords rejected
- Case-sensitive

### Role-Based Access
- `is_admin: true` → Admin features unlocked
- `is_admin: false` → User features only
- `is_active: true` → Account can login
- `is_active: false` → Account blocked

---

## 📈 What's New vs Old

### Before This Update:
- Admin pages showed hardcoded mock data
- Light mode had contrast issues
- No test accounts in database
- Admin panel UI looked pixelated in light mode

### After This Update:
- ✓ Admin pages display real database data
- ✓ Light/dark modes work perfectly
- ✓ 2 test accounts ready for use
- ✓ Clean, professional UI in both themes
- ✓ Full database integration complete
- ✓ Password hashing properly configured
- ✓ Login system fully functional

---

## 🆘 Troubleshooting

### Issue: "Cannot connect to database"
**Solution:** Make sure MySQL is running and `autofill_db` database exists

### Issue: "Admin login not working"
**Solution:** Check credentials are exactly:
- Email: `admin@example.com`
- Password: `admin123`

### Issue: "Page shows wrong theme colors in light mode"
**Solution:**
1. Clear browser cache (Ctrl+Shift+Del)
2. Refresh page (F5)
3. Try different browser

### Issue: "Stats page shows 0 users"
**Solution:** Run `python scripts/test_admin_api.py` to verify database has users

---

## 📞 Support

For issues or requests:
1. Check that backend server is running
2. Ensure MySQL database is accessible
3. Verify test accounts exist in database
4. Check browser console for errors (F12)

---

## ✅ Checklist for First-Time Setup

- [ ] MySQL server running
- [ ] Backend server started (`python -m uvicorn ...`)
- [ ] Frontend accessible in browser
- [ ] Successfully logged in with admin@example.com
- [ ] Can see real user list in Users page
- [ ] Theme toggle works properly (light/dark)
- [ ] Admin dashboard shows statistics
- [ ] All pages load without errors

Once all checked, you're ready to go! 🚀
