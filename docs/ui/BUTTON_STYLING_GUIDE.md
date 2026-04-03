# 🎨 Unified Button Styling Guide

## Overview
All buttons in the AutoFill AI System have been centralized and standardized using a unified CSS system. This ensures consistency, professionalism, and maintainability across all pages.

---

## CSS File Location
**File:** `/static/css/buttons.css`

**Include in your HTML:**
```html
<link rel="stylesheet" href="/static/css/buttons.css">
```

---

## Button Types & Classes

### 1. Primary Button
**Used for:** Main action buttons (Submit, Save, Continue)
```html
<button class="btn btn-primary">Primary Action</button>
```

### 2. Secondary Button
**Used for:** Alternative actions
```html
<button class="btn btn-secondary">Secondary Action</button>
```

### 3. Success Button
**Used for:** Positive actions (Approve, Complete)
```html
<button class="btn btn-success">✓ Confirm</button>
```

### 4. Danger Button
**Used for:** Destructive actions (Delete, Remove)
```html
<button class="btn btn-danger">🗑️ Delete</button>
```

### 5. Warning Button
**Used for:** Caution actions
```html
<button class="btn btn-warning">⚠️ Warning</button>
```

### 6. Info Button
**Used for:** Information/Help
```html
<button class="btn btn-info">ℹ️ More Info</button>
```

### 7. Outline Button
**Used for:** Secondary or cancellation actions
```html
<button class="btn btn-outline">Outline Button</button>
```

### 8. Default Button
**Used for:** Neutral actions (Reset, Cancel)
```html
<button class="btn btn-default">Default Action</button>
```

---

## Button Sizes

### Small (btn-sm)
```html
<button class="btn btn-primary btn-sm">Small Button</button>
```
Padding: 6px 12px | Font Size: 12px

### Medium (default)
```html
<button class="btn btn-primary">Medium Button</button>
```
Padding: 10px 20px | Font Size: 14px

### Large (btn-lg)
```html
<button class="btn btn-primary btn-lg">Large Button</button>
```
Padding: 14px 28px | Font Size: 16px

### Extra Large (btn-xl)
```html
<button class="btn btn-primary btn-xl">XL Button</button>
```
Padding: 16px 32px | Font Size: 16px

---

## Button Groups

### Horizontal Group (Default)
```html
<div class="button-group">
    <button class="btn btn-primary">Save</button>
    <button class="btn btn-default">Cancel</button>
</div>
```

### Vertical Group
```html
<div class="button-group vertical">
    <button class="btn btn-primary">Save</button>
    <button class="btn btn-default">Cancel</button>
</div>
```

### Full Width Buttons
```html
<div class="button-group fill">
    <button class="btn btn-primary">Save</button>
    <button class="btn btn-default">Cancel</button>
</div>
```

### Centered Group
```html
<div class="button-group center">
    <button class="btn btn-primary">Action</button>
</div>
```

### Right Aligned Group
```html
<div class="button-group right">
    <button class="btn btn-primary">Save</button>
    <button class="btn btn-default">Cancel</button>
</div>
```

### Left Aligned Group
```html
<div class="button-group left">
    <button class="btn btn-default">Back</button>
</div>
```

### Space Between
```html
<div class="button-group space-between">
    <button class="btn btn-default">Back</button>
    <button class="btn btn-primary">Next</button>
</div>
```

---

## Form Action Buttons
**Used for:** Form submission areas

```html
<div class="form-actions">
    <button type="submit" class="btn btn-primary">💾 Save</button>
    <button type="reset" class="btn btn-default">🔄 Clear</button>
</div>
```

**With Full Width:**
```html
<div class="form-actions fill">
    <button type="submit" class="btn btn-primary">💾 Save</button>
    <button type="reset" class="btn btn-default">🔄 Clear</button>
</div>
```

---

## Icon Buttons

### Standard Icon Button
```html
<button class="btn-icon" title="Toggle" onclick="toggle()">🌙</button>
```

### Large Icon Button
```html
<button class="btn-icon btn-icon-lg" title="Menu">☰</button>
```

### Small Icon Button
```html
<button class="btn-icon btn-icon-sm" title="Close">✕</button>
```

---

## Navigation Buttons

### Back Button
```html
<a href="/" class="btn btn-default">← Back</a>
```

```html
<button onclick="goBack()" class="btn btn-default">← Back</button>
```

---

## Modal Buttons

### OK Button
```html
<button class="modal-btn modal-btn-ok" onclick="confirm()">OK</button>
```

### Cancel Button
```html
<button class="modal-btn modal-btn-cancel" onclick="cancel()">Cancel</button>
```

### Close Button
```html
<button class="modal-close" onclick="closeModal()">✕</button>
```

---

## Login Buttons

### Login Form
```html
<div class="button-group fill">
    <button type="submit" class="btn btn-primary">Sign In</button>
    <button type="button" class="btn btn-outline" onclick="openSignup()">Sign Up</button>
</div>
```

---

## Disabled State
```html
<button class="btn btn-primary" disabled>Disabled Button</button>
```

---

## Loading State
```html
<button class="btn btn-primary loading" disabled>
    Processing
    <span class="loading"></span>
</button>
```

---

## Color Scheme
All buttons use a professional blue color scheme:

| Element | Color |
|---------|-------|
| Primary | #2563EB (Blue) |
| Primary Dark | #1e40af |
| Secondary | #6B7280 (Gray) |
| Success | #10B981 (Green) |
| Danger | #EF4444 (Red) |
| Warning | #F59E0B (Orange) |
| Info | #3B82F6 (Light Blue) |
| Default | #F3F4F6 (Light Gray) |

---

## Hover & Active Effects
- **Hover:** Translateupwardby 2px + Enhanced shadow
- **Active:** Return to original position
- **Disabled:** 60% opacity + not-allowed cursor

---

## Responsive Behavior
- **Desktop (> 768px):** Buttons display in original orientation
- **Tablet (768px):** Button groups stack vertically
- **Mobile (< 480px):** Full-width buttons by default

---

## Common Patterns

### Form with Multiple Action Buttons
```html
<div class="form-actions fill">
    <button type="reset" class="btn btn-default">🔄 Clear</button>
    <button type="submit" class="btn btn-primary">💾 Save</button>
    <button type="button" class="btn btn-secondary" onclick="preview()">👁️ Preview</button>
</div>
```

### Admin Action Row
```html
<div class="button-group right">
    <button class="btn btn-secondary btn-sm">📝 Edit</button>
    <button class="btn btn-danger btn-sm">🗑️ Delete</button>
</div>
```

### Dialog Actions
```html
<div class="button-group fill">
    <button class="modal-btn modal-btn-cancel" onclick="cancel()">Cancel</button>
    <button class="modal-btn modal-btn-ok" onclick="confirm()">Confirm</button>
</div>
```

---

## CSS Variables
You can customize colors by overriding CSS variables:

```css
:root {
    --btn-primary-bg: #2563EB;
    --btn-primary-bg-dark: #1e40af;
    --btn-padding-md: 10px 20px;
    --btn-radius: 8px;
    --btn-gap: 12px;
}
```

---

## Examples by Page Type

### Login Page
- Buttons should be full-width in smaller screens
- Use primary for login, outline for signup
- Maintain spacing of 30px from top

### Form Page
- Use form-actions class for consistency
- Primary for submit, default for reset
- Ensure 20px top padding/border

### Admin Pages
- Use small buttons in tables (btn-sm)
- Right-align action buttons
- Use danger for delete operations

### Modal Dialogs
- Centered button groups
- OK should be primary, Cancel secondary
- Use modal-btn class family

---

## Accessibility Features
- All buttons have clear labels
- Disabled state properly indicated
- High contrast colors for WCAG compliance
- Focus states visible for keyboard navigation
- Icons complemented with text labels

---

## Migration from Old Styles
If you find old button styles, migrate them:

### Old → New
- `.login-btn` → `.btn .btn-primary`
- `.signup-btn` → `.btn .btn-outline`
- `.btn-submit` → `.btn .btn-primary`
- `.btn-reset` → `.btn .btn-default`
- `.back-button` → `.btn .btn-default`
- `.template-actions button` → `.btn .btn-danger .btn-sm`

---

## Best Practices
1. **Always use class names**, never inline styles
2. **Group related buttons** using `.button-group`
3. **Use semantic colors**: Success=green, Danger=red, Warning=orange
4. **Keep icons + text** together for clarity
5. **Test responsive** behavior on all screen sizes
6. **Provide feedback** for disabled/loading states
7. **Maintain spacing** around button groups (12px gaps)

---

## Troubleshooting

### Button not styling correctly?
- Ensure `buttons.css` is linked
- Check for conflicting inline `style` attributes
- Verify correct class names used
- Clear browser cache

### Buttons not responsive?
- Ensure viewport meta tag present
- Check media queries in buttons.css
- Test on actual devices, not just browser DevTools

### Colors not matching?
- Verify you're using .btn class as base
- Check CSS color variable values
- Ensure no conflicting styles elsewhere

---

## Contact & Support
For questions about button styling:
- Check this guide first
- Review `/static/css/buttons.css`
- Check existing examples in HTML files
- Contact development team

---

**Last Updated:** March 18, 2026
**Version:** 1.0
**Status:** Production Ready ✅
