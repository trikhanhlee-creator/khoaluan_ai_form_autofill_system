# 🌙 Global Theme Management System - Documentation

## Overview

The AutoFill AI System now has a **unified, synchronized light/dark mode system** that works across all pages and features. When users switch themes on any page, the change automatically applies system-wide and persists across browser sessions.

## Architecture

### Core Components

#### 1. **Theme Manager JavaScript** (`/static/js/theme-manager.js`)
- Single global instance: `themeManager`
- Manages all theme operations
- Handles cross-tab synchronization via localStorage events
- Persistent theme storage with key: `app-theme`

#### 2. **CSS Theme Support** (`/static/css/buttons.css`)
- Light mode class: `.light-mode` on body
- Dark mode class: `.dark-mode` on body (default)
- CSS variables for theme-aware styling
- Automatic responsive color adjustments

#### 3. **HTML Integration**
All HTML files include the script:
```html
<script src="/static/js/theme-manager.js"></script>
```

## How It Works

### 1. Initialization Flow
```
Page Load → theme-manager.js executes
          ↓
          Load saved theme from localStorage ('app-theme')
          ↓
          Apply theme to body element (light-mode or dark-mode class)
          ↓
          Update UI elements (icons, labels)
          ↓
          Listen for theme changes from other tabs
```

### 2. Theme Switching Process
```
User clicks theme toggle button
          ↓
          onclick="themeManager.toggleTheme()"
          ↓
          Switch between light/dark modes
          ↓
          Update body classes
          ↓
          Save to localStorage
          ↓
          Update all UI elements
          ↓
          Notify other browser tabs
          ↓
          Dispatch 'themeChanged' event
```

### 3. Cross-Tab Synchronization
- Uses `storage` event listener for localStorage changes
- Custom `app-theme-changed` event for real-time updates
- All tabs automatically sync when theme changes anywhere

## API Reference

### Global Object: `themeManager`

#### Methods

**`toggleTheme()`**
- Toggles between light and dark modes
- Persists to localStorage
- Notifies other tabs
```javascript
themeManager.toggleTheme();
```

**`setTheme(theme, notify = true)`**
- Sets specific theme: 'light' or 'dark'
- `notify` parameter controls cross-tab notification
```javascript
themeManager.setTheme('light', true);
```

**`getCurrentTheme()`**
- Returns current theme: 'light' or 'dark'
```javascript
const currentTheme = themeManager.getCurrentTheme(); // 'dark'
```

**`getSavedTheme()`**
- Returns saved theme from localStorage
```javascript
const savedTheme = themeManager.getSavedTheme(); // 'dark'
```

**`isLightMode()`**
- Boolean check for light mode
```javascript
if (themeManager.isLightMode()) { ... }
```

**`isDarkMode()`**
- Boolean check for dark mode
```javascript
if (themeManager.isDarkMode()) { ... }
```

**`getThemeColor(lightColor, darkColor)`**
- Get appropriate color for current theme
```javascript
const textColor = themeManager.getThemeColor('#1e293b', '#f1f5f9');
```

### Events

**`themeChanged`**
- Fired when theme changes
- Detail contains: `{ theme: 'light' or 'dark' }`
```javascript
window.addEventListener('themeChanged', (e) => {
    console.log('New theme:', e.detail.theme);
});
```

## Implementation Guide

### For Developers

#### 1. Adding Theme Toggle Button
```html
<button onclick="themeManager.toggleTheme()">
    <span id="themeIcon">🌙</span>
    <span id="themeLabel">Tối</span>
</button>
```

The `themeManager` automatically updates:
- `#themeIcon` → ☀️ (light) or 🌙 (dark)
- `#themeLabel` → "Sáng" (light) or "Tối" (dark)

#### 2. CSS Theme-Aware Styling
```css
body.light-mode {
    background: #ffffff;
    color: #000000;
}

body.dark-mode {
    background: #0f172a;
    color: #f1f5f9;
}

body.light-mode .component {
    background: #f0f9ff;
    border-color: #bfdbfe;
}

body.dark-mode .component {
    background: #1e293b;
    border-color: #334155;
}
```

#### 3. Listening to Theme Changes
```javascript
window.addEventListener('themeChanged', (event) => {
    const theme = event.detail.theme;
    console.log('Application theme changed to:', theme);
    
    // Update component styles if needed
    if (theme === 'light') {
        // Handle light mode
    } else {
        // Handle dark mode
    }
});
```

#### 4. Theme-Aware JavaScript
```javascript
// Get current theme
const isDark = themeManager.isDarkMode();

// Get theme-appropriate color
const accentColor = themeManager.getThemeColor(
    '#2563EB', // light mode
    '#60A5FA'  // dark mode
);

// Use in canvas, charts, etc.
chart.setColor(accentColor);
```

## Integration Points

### Updated Files (with theme support)

#### Main Feature Pages
- `/static/menu.html` - Homepage with theme toggle
- `/static/excel-upload.html` - Excel upload page
- `/static/word-upload.html` - Word upload page
- `/static/composer.html` - Document composer
- `/static/form.html` - Form data entry
- `/static/login.html` - Login page

#### Admin Pages
- `/static/admin-dashboard.html` - Admin dashboard
- `/static/admin-account.html` - Account settings
- `/static/admin-users.html` - User management
- `/static/admin-forms.html` - Form management
- `/static/admin-reports.html` - Reports & analytics
- `/static/admin-audit-log.html` - Audit logging

### Storage Details

**LocalStorage Key**: `app-theme`
- Values: `'light'` or `'dark'`
- Default: `'dark'`
- Scope: Per domain
- Persists: Across sessions

Example:
```javascript
localStorage.getItem('app-theme'); // 'dark'
localStorage.setItem('app-theme', 'light');
```

## CSS Variables Available

### Color Variables (adapt by theme)
```css
:root {
    --btn-primary-bg: #2563EB;
    --btn-primary-bg-dark: #1e40af;
    --btn-secondary-bg: #6B7280;
    --btn-default-bg: #F3F4F6;
    --btn-text-white: #FFFFFF;
    /* ... more variables */
}

body.light-mode {
    --btn-default-bg: #E5E7EB;
}

body.dark-mode {
    /* Uses :root values */
}
```

## Testing the System

### Test Scenario 1: Single Page Theme Switch
1. Open `/menu`
2. Click theme toggle button
3. Page should switch between light/dark modes
4. Icon (☀️/🌙) and label (Sáng/Tối) should update

### Test Scenario 2: Cross-Tab Synchronization
1. Open `/menu` in Tab A
2. Open `/menu` in Tab B
3. Toggle theme in Tab A
4. Tab B should automatically update
5. Refresh Tab B → theme persists

### Test Scenario 3: Different Pages
1. Open `/excel-upload` (in dark mode)
2. Click theme toggle → switch to light mode
3. Navigate to `/word-upload`
4. Light mode should persist
5. Refresh page → light mode should remain

### Test Scenario 4: Admin Pages
1. Toggle theme on `/admin-dashboard`
2. Navigate to `/admin-users`
3. Theme should persist
4. Theme toggle should work on all admin pages

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Considerations

- Minimal CSS repaints (class-based switching)
- No JavaScript animations during theme change
- Instant cross-tab synchronization
- localStorage operations (~40KB max)
- Event listeners cleaned up on unload

## Troubleshooting

### Theme not persisting
```javascript
// Check localStorage
console.log(localStorage.getItem('app-theme'));

// Manually set theme
themeManager.setTheme('light', true);
```

### Icons not updating
```javascript
// Check if elements exist
console.log(document.getElementById('themeIcon'));
console.log(document.getElementById('themeLabel'));

// Manually trigger update
themeManager.updateThemeUI(themeManager.getCurrentTheme());
```

### Cross-tab sync not working
- Check localStorage is enabled
- Verify `app-theme` key in devtools
- Check browser isolation settings
- Look for blocked storage events

## Migration from Old System

### Old Implementation
```html
<!-- Individual pages stored theme separately -->
<button onclick="toggleTheme()">Toggle</button>
<script>
    function toggleTheme() {
        // Page-specific implementation
        localStorage.setItem('theme', 'light');
        // or
        localStorage.setItem('adminTheme', 'light');
    }
</script>
```

### New Implementation
```html
<!-- Global theme manager -->
<button onclick="themeManager.toggleTheme()">Toggle</button>
<script src="/static/js/theme-manager.js"></script>
<!-- That's it! -->
```

## Future Enhancements

- [ ] Scheduled theme switching (e.g., dark mode at night)
- [ ] System preference detection (prefers-color-scheme)
- [ ] Theme transition animations
- [ ] Custom color theme picker
- [ ] Per-component theme overrides
- [ ] Theme export/import functionality

## Support & Questions

For issues or questions about the theme system:
1. Check browser console for errors
2. Verify script is loaded: `console.log(themeManager)`
3. Check localStorage in DevTools
4. Review this documentation
5. Contact development team

---

**Last Updated**: March 2026
**Version**: 1.0
**Maintainer**: AutoFill AI Development Team
