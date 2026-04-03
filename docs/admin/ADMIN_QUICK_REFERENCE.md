# 🎮 Admin Interface - Quick Start Guide

## 🌐 Access URLs

Admin có thể truy cập các trang sau qua URL:

| Giao Diện | URL | Tính Năng |
|-----------|-----|----------|
| **Dashboard Admin** | `/admin-dashboard.html` | Tổng quan hệ thống |
| **Quản Lí Người Dùng** | `/admin-users.html` | CRUD users, assign roles |
| **Quản Lí Biểu Mẫu** | `/admin-forms.html` | Quản lý forms, xóa, statistics |
| **Cài Đặt Tài Khoản** | `/admin-account.html` | Profile, password, security |
| **Báo Cáo & Thống Kê** | `/admin-reports.html` | Dashboard, charts, analytics |
| **Lịch Sử Hoạt Động** | `/admin-audit-log.html` | System audit trail, logs |

## 🚀 Cách Sử Dụng

### 1. Đăng Nhập
```
URL: /login
Username: admin
Password: admin123
```

### 2. Truy Cập Admin Panel
Sau đăng nhập, admin sẽ thấy menu admin trong sidebar hoặc nhấp vào "Admin Panel"

### 3. Các Chức Năng Chính

#### 📊 Bảng Điều Khiển (Dashboard)
- Xem tổng quan thống kê hệ thống
- Quick access links đến tất cả tính năng
- Hoạt động gần đây
- Thông tin hệ thống

**Hành động:**
- 🔄 Refresh statistics
- 🌙 Toggle dark/light mode
- ☰ Toggle sidebar (mobile)

#### 👥 Quản Lí Người Dùng
**Xem & Tìm Kiếm:**
- Danh sách tất cả người dùng
- Tìm kiếm theo tên/email
- Filter theo vai trò (Admin/User)
- Filter theo trạng thái

**Thêm Người Dùng:**
1. Click "➕ Thêm Người Dùng"
2. Điền form:
   - Tên Người Dùng
   - Email
   - Mật Khẩu
   - Vai Trò (Admin/User)
   - Trạng Thái
3. Click "Lưu"

**Chỉnh Sửa/Xóa:**
- ✎ Chỉnh sửa thông tin người dùng
- 🔒 Khóa/Mở khóa tài khoản
- 🗑️ Xóa người dùng

#### 📋 Quản Lí Biểu Mẫu
**Xem & Tìm Kiếm:**
- Danh sách tất cả forms
- Tìm kiếm theo tên
- Filter theo loại (Word/Excel/Custom)

**Hành Động:**
- 👁 Xem chi tiết form
- ✎ Chỉnh sửa
- 🗑️ Xóa form
- 📥 Xuất dữ liệu

**Xem Thống Kê:**
- Tổng forms, templates, bản gửi
- Top forms được sử dụng

#### ⚙️ Cài Đặt Tài Khoản
Menu bên trái với các tab:

**👤 Hồ Sơ**
- Cập nhật tên, email, số điện thoại
- Công ty, vị trí
- Click "💾 Lưu Thay Đổi"

**🔐 Thay Đổi Mật Khẩu**
- Nhập mật khẩu hiện tại
- Mật khẩu mới (với password strength indicator)
- Xác nhận mật khẩu
- Click "🔐 Cập Nhật Mật Khẩu"

**🛡️ Bảo Mật**
- Bật/tắt 2FA
- Đăng xuất tất cả phiên
- Xem lịch phiên đăng nhập

**🔔 Thông Báo**
- Toggle thông báo email hệ thống
- Cảnh báo hoạt động bất thường
- Báo cáo hàng tuần

**⚙️ Hệ Thống**
- Chế độ giao diện
- Ngôn ngữ
- Múi giờ

#### 📈 Báo Cáo & Thống Kê
**Xem Dữ Liệu:**
- Key statistics (Users, Forms, Submissions, Avg Time)
- Filter theo date range
- Charts (placeholders - ready for Chart.js)

**Bảng Dữ Liệu:**
- Biểu mẫu phổ biến nhất
- Hoạt động người dùng hàng ngày

**Xuất Dữ Liệu:**
- Click "📥 Xuất Báo Cáo"
- Tải file (CSV/PDF)

#### 📜 Lịch Sử Hoạt Động
**Xem & Tìm Kiếm:**
- Danh sách tất cả hành động hệ thống
- Tìm kiếm free text
- Filter theo hành động (Login, Create, Edit, Delete, Upload, Export)
- Thông tin: Thời gian, Người dùng, Hành động, Đối tượng, IP, Trạng thái

**Xem Chi Tiết:**
- Click 👁 để xem chi tiết hành động
- Modal popup với đầy đủ thông tin

**Xuất Nhật Ký:**
- Click "📥 Xuất Nhật Ký"
- Tải file log

## 🎨 Giao Diện & Tính Năng

### Theme
- 🌙 Dark Mode (mặc định) - Professional look
- ☀️ Light Mode - Bright & clean
- Toggle ở header

### Responsive
- Desktop: Full layout + sidebar
- Tablet: Adaptable
- Mobile: Collapsible sidebar ☰

### Components
- **Badges**: Status indicators (✓ Success, ✗ Error, ⚠ Warning)
- **Alerts**: Notifications (success, error, warning, info)
- **Modals**: Forms & dialogs
- **Tables**: Sortable, filterable
- **Cards**: Statistics & info containers

## 🔮 Keyboard Shortcuts (Optional)

```
Ctrl+K      - Open search
Esc         - Close modal
?           - Show help
```

## ⚠️ Chú Ý Quan Trọng

### Admin Privileges
- Chỉ admin mới có thể truy cập admin panel
- Tất cả hành động được log trong audit trail
- Khóa/xóa tài khoản không thể hoàn tác

### Data Safety
- Backup dữ liệu trước khi xóa forms/users
- Xóa người dùng sẽ xóa tất cả data liên quan (cascade delete)
- Export dữ liệu định kỳ

### Security
- Luôn sử dụng mật khẩu mạnh (8+ ký tự, mix chữ hoa/thường/số)
- Enable 2FA nếu có thể
- Đăng xuất khi dùng shared device
- Thay đổi mật khẩu định kỳ (30 ngày)

## 🆘 Troubleshooting

| Vấn Đề | Giải Pháp |
|--------|----------|
| Không thấy admin menu | Kiểm tra role là admin trong database |
| Form không save | Kiểm tra console log, validate input |
| Data không load | F5 refresh, kiểm tra API connection |
| UI bị lỗi | Clear cache, thử light mode |
| Không đăng xuất được | Clear cookies, try again |

## 📞 Developer Notes

### Files Location
```
backend/app/static/
├── admin-dashboard.html
├── admin-users.html
├── admin-forms.html
├── admin-account.html
├── admin-reports.html
├── admin-audit-log.html
└── css/
    └── admin-styles.css
```

### API Endpoints (To Be Implemented)
```
GET    /api/admin/stats
GET    /api/admin/users
POST   /api/admin/users
PUT    /api/admin/users/{id}
DELETE /api/admin/users/{id}
... (see ADMIN_INTERFACE_IMPLEMENTATION.md for full list)
```

### Customization
- Colors: Edit CSS variables in `admin-styles.css`
- Layout: Modify grid in main CSS
- Add pages: Duplicate existing HTML, update sidebar

## 📚 Related Documentation

- [Admin Interface Design](ADMIN_INTERFACE_DESIGN.md)
- [Admin Interface Implementation](ADMIN_INTERFACE_IMPLEMENTATION.md)
- [API Documentation](API_QUICK_REFERENCE.md)
- [System Architecture](SYSTEM_SUMMARY.md)

## 🎓 Training Tips

1. **Start with Dashboard** - Understand system overview
2. **Manage Users** - Practice CRUD operations
3. **Explore Reports** - Analyze system data
4. **Review Audit Log** - Monitor all activities
5. **Update Account** - Customize settings
6. **Practice Admin Tasks** - Maintain system health

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Author**: AutoFill AI System Development Team
