# 🎨 Blue Color Scheme - Quick Reference Guide
## Hướng Dẫn Nhanh - Chủ Đạo Xanh Dương

### 📱 Core Colors / Màu Cốt Lõi

```
Primary Blue:    #2563EB  (Modern, eye-catching)
Dark Blue:       #1e40af  (Buttons, hover states)
Accent Blue:     #60a5fa  (Secondary highlights)
Success Green:   #10b981  (Positive actions)
Warning Amber:   #f59e0b  (Cautions)
Error Red:       #ef4444  (Errors, destructive)
Info Sky:        #3b82f6  (Information)
```

### 🌓 Mode Backgrounds / Nền Chế Độ

**Light Mode** (Dịu, sạch)
```
Primary Background:    #f0f9ff  (Soft light blue)
Surface:               #ffffff  (Pure white)
Border:                #bfdbfe  (Light blue)
Text:                  #1e293b  (Dark slate)
```

**Dark Mode** (Hiện đại, nổi bật)
```
Primary Background:    #0f172a  (Very dark blue)
Surface:               #1e293b  (Dark blue)
Light Surface:         #334155  (Medium dark)
Border:                #475569  (Dark border)
Text:                  #f1f5f9  (Light blue-white)
```

### 💻 CSS Usage / Cách Dùng CSS

```css
/* Use variables from :root */
background: var(--color-primary);          /* #2563EB */
border: 1px solid var(--color-border-color);
color: var(--color-text);
```

### 🎯 Common Patterns / Mẫu Thường Dùng

**Button Primary**
```css
background: #2563EB;
color: white;

&:hover {
    background: #1e40af;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}
```

**Form Input Focus**
```css
border-color: #2563EB;
box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
```

**Link Hover**
```css
color: #2563EB;
background: rgba(37, 99, 235, 0.08);
```

**Badge Blue**
```css
background: rgba(37, 99, 235, 0.2);
color: #2563EB;  /* Light: this, Dark: #60a5fa */
```

### 📋 Files Using Blue Theme / Tập Tin Dùng Chủ Đề Xanh

1. ✅ menu.html
2. ✅ login.html
3. ✅ form.html
4. ✅ excel-form.html
5. ✅ composer.html
6. ✅ excel-upload.html
7. ✅ word-upload.html
8. ✅ excel-data-form.html
9. ✅ admin-styles.css (root variables)

### 🔄 Light/Dark Mode Implementation

**Auto-switch support** via CSS variables:
```css
body.light-mode {
    --color-bg: var(--color-bg-light);
    --color-surface: var(--color-surface-light-mode);
    --color-text: var(--color-text-dark);
}

body:not(.light-mode) {
    --color-bg: var(--color-bg-dark);
    --color-surface: var(--color-surface-dark);
    --color-text: var(--color-text-light);
}
```

### 🎨 Gradient Combinations / Kết Hợp Gradient

**Primary Gradient** (Buttons, headers)
```css
background: linear-gradient(135deg, #2563EB 0%, #1e40af 100%);
```

**Dark Gradient** (Page background)
```css
background: linear-gradient(135deg, #0f172a 0%, #1a2f4a 100%);
```

**Light Gradient** (Light mode background)
```css
background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
```

### ✨ Shadow & Effects / Bóng & Hiệu Ứng

**Soft Shadow** (Cards, buttons)
```css
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
```

**Medium Shadow** (Elevated elements)
```css
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
```

**Large Shadow** (Modals, heavy elements)
```css
box-shadow: 0 10px 28px rgba(0, 0, 0, 0.2);
```

**Blue Focus Glow**
```css
box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
```

### 🔗 Accessibility / Khả Năng Tiếp Cận

✅ Contrast ratios meet WCAG AA standards
✅ Light mode: Dark text on light background
✅ Dark mode: Light text on dark background
✅ Focus states clearly visible with blue highlight
✅ Color not sole indicator (icons + color)

### 📐 Sizing & Spacing / Kích Thước & Khoảng Cách

```css
--spacing-xs:   4px;
--spacing-sm:   8px;
--spacing-md:   16px;
--spacing-lg:   24px;
--spacing-xl:   32px;
--spacing-2xl:  48px;

--radius-sm:    4px;
--radius-md:    8px;
--radius-lg:    12px;
--radius-xl:    16px;
```

### 🚀 Creating New Components / Tạo Thành Phần Mới

**Template:**
```html
<div class="my-component light-mode">
    <h2 style="color: #2563EB">Title</h2>
    <p style="color: var(--color-text)">Content</p>
    <button style="background: var(--color-primary)">Action</button>
</div>
```

**CSS Template:**
```css
.my-component {
    background: var(--color-surface);
    border: 1px solid var(--color-border-color);
    color: var(--color-text);
    transition: all 0.3s ease;
}

.my-component:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-md);
}

body.light-mode .my-component {
    /* Override if needed */
}
```

### 🎬 Transitions / Chuyển Tiếp

Standard transition for all interactive elements:
```css
transition: all 0.3s ease;
```

Specific transitions:
```css
transition: background 0.3s ease, color 0.3s ease;
transition: transform 0.2s ease;
```

### 💡 Pro Tips / Mẹo Chuyên Nghiệp

1. **Always use CSS variables** for colors - easier maintenance
2. **Test both light/dark modes** when adding new features
3. **Use semantic color names** (primary, secondary, success, error)
4. **Maintain proper contrast** ratios for accessibility
5. **Use gradients sparingly** - for high-impact areas only
6. **Hover effects < 300ms** for responsive feel
7. **Focus states must be visible** - use blue outline/shadow

### 📞 Support / Hỗ Trợ

For questions about the blue color scheme:
1. Check BLUE_COLOR_SCHEME_DOCUMENTATION.md
2. Review CSS variables in admin-styles.css
3. Compare with existing components (menu.html, form.html)

---
**Version**: 1.0  
**Updated**: March 18, 2026  
**Status**: ✅ Ready for Development
