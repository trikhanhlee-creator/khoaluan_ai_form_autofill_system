# 🎨 Global Theme System - Quick Reference

## One-Line Summary
**Single global theme manager syncs light/dark mode across all pages in real-time**

---

## Essential Setup

### For Every HTML File
Add one line in `<head>`:
```html
<script src="/static/js/theme-manager.js"></script>
```

### Theme Toggle Button
```html
<button onclick="themeManager.toggleTheme()">
    <span id="themeIcon">🌙</span>
    <span id="themeLabel">Tối</span>
</button>
```

---

## Core API (Copy & Paste)

| Function | Purpose | Example |
|----------|---------|---------|
| `toggleTheme()` | Switch theme | `themeManager.toggleTheme()` |
| `setTheme(t)` | Set specific | `themeManager.setTheme('light')` |
| `getCurrentTheme()` | Get current | `const t = themeManager.getCurrentTheme()` |
| `isLightMode()` | Is light? | `if (themeManager.isLightMode()) {}` |
| `isDarkMode()` | Is dark? | `if (themeManager.isDarkMode()) {}` |
| `getThemeColor(l, d)` | Get color | `themeManager.getThemeColor('#000', '#fff')` |

---

## CSS Styling

### Light/Dark Mode Classes
```css
/* Dark mode (default) */
body.dark-mode { background: #0f172a; color: #f1f5f9; }

/* Light mode */
body.light-mode { background: #ffffff; color: #1e293b; }
```

### Component Styling
```css
/* Automatic light/dark support */
.my-component {
    background: var(--btn-default-bg);
}

body.light-mode .my-component {
    background: #e5e7eb;
}

body.dark-mode .my-component {
    background: #1e293b;
}
```

---

## Events

### Listen for Theme Changes
```javascript
window.addEventListener('themeChanged', (e) => {
    console.log('Theme is now:', e.detail.theme); // 'light' or 'dark'
});
```

---

## Storage

- **Key**: `app-theme`
- **Values**: `'light'` or `'dark'`
- **Persists**: Yes (across sessions)
- **Scope**: Per domain
- **Sync**: Yes (across tabs/windows)

```javascript
localStorage.getItem('app-theme'); // Check current
```

---

## Common Use Cases

### 1. Custom Component Styling
```html
<div id="myChart"></div>

<script>
const bgColor = themeManager.getThemeColor('#f0f9ff', '#1e293b');
initChart(bgColor);

// Update when theme changes
window.addEventListener('themeChanged', () => {
    const newBg = themeManager.getThemeColor('#f0f9ff', '#1e293b');
    updateChart(newBg);
});
</script>
```

### 2. Conditional Logic
```javascript
if (themeManager.isDarkMode()) {
    // Dark mode specific code
    loadDarkModeImages();
} else {
    // Light mode specific code
    loadLightModeImages();
}
```

### 3. Dynamic Colors
```javascript
const accentColor = themeManager.getThemeColor(
    '#2563EB', // light mode blue
    '#60A5FA'  // dark mode light blue
);
canvas.strokeStyle = accentColor;
```

---

## Updated Pages

✅ **All feature pages**: menu, excel-upload, word-upload, composer, form, login
✅ **All admin pages**: dashboard, account, users, forms, reports, audit-log
✅ **All synchronized**: Theme changes apply system-wide instantly

---

## Testing Checklist

- [ ] Theme toggle button works
- [ ] Icon changes (☀️ ↔️ 🌙)
- [ ] Label changes (Sáng ↔️ Tối)
- [ ] Colors update instantly
- [ ] Persists after refresh
- [ ] Works across multiple tabs
- [ ] Works on all pages

---

## Troubleshooting

### Issue: Theme not saving
```javascript
// Verify storage is working
console.log(localStorage.getItem('app-theme'));
```

### Issue: Icons not updating
```javascript
// Check elements exist
console.log(document.getElementById('themeIcon'));
```

### Issue: Theme not syncing across tabs
- Enable localStorage (browser privacy settings)
- Check browser console for errors
- Verify script loaded: `console.log(themeManager)`

---

## Real-World Examples

### Menu with Theme Toggle
```html
<nav>
    <h1>AutoFill AI</h1>
    <button onclick="themeManager.toggleTheme()" class="theme-btn">
        <span id="themeIcon">🌙</span>
        <span id="themeLabel">Tối</span>
    </button>
</nav>
```

### Admin Dashboard
```html
<body class="dark-mode"> <!-- Auto-initialized -->
    <header>
        <button id="themeToggle" onclick="themeManager.toggleTheme()">
            🌙
        </button>
    </header>
    <main>Content</main>
</body>
```

### Custom Component
```javascript
class DataChart {
    constructor() {
        this.bgColor = themeManager.getThemeColor('#f0f9ff', '#1e293b');
        this.render();
        
        window.addEventListener('themeChanged', () => this.updateColors());
    }
    
    updateColors() {
        this.bgColor = themeManager.getThemeColor('#f0f9ff', '#1e293b');
        this.render();
    }
}
```

---

## File Locations

| File | Purpose |
|------|---------|
| `/static/js/theme-manager.js` | Core theme engine |
| `/static/css/buttons.css` | Button + theme styles |
| `GLOBAL_THEME_SYSTEM_DOCS.md` | Full documentation |
| `GLOBAL_THEME_QUICK_REFERENCE.md` | This file |

---

**Version**: 1.0 | **Status**: ✅ Production Ready | **Date**: March 2026
