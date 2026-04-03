# 🎯 Button Usage Quick Reference

## Immediate Copy-Paste Examples

### Login Page
```html
<div class="button-group fill">
    <button type="submit" class="btn btn-primary">« Đăng Nhập</button>
    <button type="button" class="btn btn-outline" onclick="openSignup()">Đăng Ký</button>
</div>
```

### Form Submission
```html
<div class="form-actions fill">
    <button type="reset" class="btn btn-default">🔄 Xóa Form</button>
    <button type="submit" class="btn btn-primary">💾 Lưu Dữ Liệu</button>
</div>
```

### Admin Actions
```html
<div class="button-group right">
    <button class="btn btn-secondary btn-sm" onclick="edit()">📝 Chỉnh Sửa</button>
    <button class="btn btn-danger btn-sm" onclick="delete()">🗑️ Xóa</button>
</div>
```

### Modal Dialog
```html
<div class="button-group fill">
    <button class="modal-btn modal-btn-cancel" onclick="close()">Hủy</button>
    <button class="modal-btn modal-btn-ok" onclick="confirm()">OK</button>
</div>
```

### Back Navigation
```html
<div class="button-group left">
    <button class="btn btn-default" onclick="goBack()">← Quay Lại</button>
</div>
```

### Theme Toggle
```html
<button class="btn-icon" id="themeToggle" onclick="toggleTheme()" title="Toggle Theme">🌙</button>
```

### Single Primary Action
```html
<button class="btn btn-primary" onclick="save()">💾 Lưu</button>
```

### Centered Action Group
```html
<div class="button-group center">
    <button class="btn btn-primary">🔄 Làm Mới</button>
    <button class="btn btn-info">📊 Xuất Báo Cáo</button>
</div>
```

### Full-Width Centered
```html
<div class="button-group fill center">
    <button class="btn btn-primary">Tiếp Tục</button>
</div>
```

### Inline Actions (Table Row)
```html
<div class="button-group">
    <button class="btn btn-info btn-sm">👁️ Xem</button>
    <button class="btn btn-secondary btn-sm">✏️ Sửa</button>
    <button class="btn btn-danger btn-sm">🗑️ Xóa</button>
</div>
```

---

## Size Reference

| Size | Class | Padding | Font-Size | Use Case |
|------|-------|---------|-----------|----------|
| Small | `.btn-sm` | 6px 12px | 12px | Tables, compact UI |
| Medium (default) | (none) | 10px 20px | 14px | Standard buttons |
| Large | `.btn-lg` | 14px 28px | 16px | Hero sections |
| XL | `.btn-xl` | 16px 32px | 16px | Main CTAs |

---

## Color Usage

| Color | Class | Use Case |
|-------|-------|----------|
| Blue | `.btn-primary` | Main actions |
| Gray | `.btn-secondary` | Alternative actions |
| Green | `.btn-success` | Confirmative actions |
| Red | `.btn-danger` | Destructive actions |
| Orange | `.btn-warning` | Caution actions |
| Light Blue | `.btn-info` | Information |
| Light Gray | `.btn-default` | Neutral actions |
| Outlined | `.btn-outline` | Secondary buttons |

---

## Layout Patterns

### Two Buttons Equal Width
```html
<div class="button-group fill">
    <button class="btn btn-primary">Save</button>
    <button class="btn btn-default">Cancel</button>
</div>
```

### Multiple Actions (Left & Right)
```html
<div class="button-group space-between">
    <button class="btn btn-default">← Back</button>
    <button class="btn btn-primary">Next →</button>
</div>
```

### Stack Vertically
```html
<div class="button-group vertical fill">
    <button class="btn btn-primary">Option 1</button>
    <button class="btn btn-secondary">Option 2</button>
</div>
```

### Compact Row (No Full Width)
```html
<div class="button-group">
    <button class="btn btn-sm">Small 1</button>
    <button class="btn btn-sm">Small 2</button>
</div>
```

---

## Icon + Text Combinations

```html
<!-- Primary with emoji --> 
<button class="btn btn-primary">💾 Lưu</button>

<!-- Danger action -->
<button class="btn btn-danger">🗑️ Xóa</button>

<!-- Info button -->
<button class="btn btn-info">ℹ️ Chi Tiết</button>

<!-- Success confirmation -->
<button class="btn btn-success">✓ Xác Nhận</button>

<!-- Warning caution -->
<button class="btn btn-warning">⚠️ Cảnh Báo</button>
```

---

## Disabled & Loading States

### Disabled Button
```html
<button class="btn btn-primary" disabled>Disabled</button>
```

### Loading Button
```html
<button class="btn btn-primary loading" onclick="submit()" id="submitBtn">
    Processing
    <span class="loading"></span>
</button>
```

### Dynamic Disable/Enable
```html
<button class="btn btn-primary" id="myBtn" onclick="submit()">Save</button>

<script>
    // Disable
    document.getElementById('myBtn').disabled = true;
    
    // Enable
    document.getElementById('myBtn').disabled = false;
</script>
```

---

## Common Mistakes ❌ → ✓

### Wrong → Right
```html
<!-- ❌ Wrong -->
<button style="background: blue; padding: 10px;">Button</button>

<!-- ✓ Right -->
<button class="btn btn-primary">Button</button>
```

```html
<!-- ❌ Wrong -->
<div>
    <button class="login-btn">Save</button>
    <button class="signup-btn">Cancel</button>
</div>

<!-- ✓ Right -->
<div class="button-group fill">
    <button class="btn btn-primary">Save</button>
    <button class="btn btn-default">Cancel</button>
</div>
```

```html
<!-- ❌ Wrong -->
<button class="btn" style="width: 100%;">Full Width</button>

<!-- ✓ Right -->
<div class="button-group fill">
    <button class="btn">Full Width</button>
</div>
```

---

## Testing Checklist

- [ ] All buttons inherit from `.btn` base class
- [ ] Colors match design (blue #2563EB primary)
- [ ] Hover effect works (translateY + shadow)
- [ ] Disabled state applies 60% opacity
- [ ] Responsive on mobile (stack vertically)
- [ ] Icon + text are aligned
- [ ] Spacing consistent (12px gaps)
- [ ] Focus state visible for accessibility

---

## Browser Support
✓ Chrome 90+
✓ Firefox 88+
✓ Safari 14+
✓ Edge 90+

---

**Need help?** Review [BUTTON_STYLING_GUIDE.md](BUTTON_STYLING_GUIDE.md) or check `/static/css/buttons.css`
