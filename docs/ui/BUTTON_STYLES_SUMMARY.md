# Comprehensive Button Styles Summary
## AutoFill AI System - /backend/app/static HTML Files

**Generated:** March 18, 2026

---

## Table of Contents
1. [Overview](#overview)
2. [Centralized Button Styles (admin-styles.css)](#centralized-button-styles)
3. [File-by-File Button Styles](#file-by-file-button-styles)
4. [Inconsistencies & Patterns](#inconsistencies--patterns)
5. [Modal Button Styles](#modal-button-styles)
6. [Recommendations](#recommendations)

---

## Overview

The system contains button styles scattered across multiple HTML files with embedded `<style>` tags, plus a centralized CSS file for admin components. Total files analyzed: **15 HTML files** + **1 CSS file**.

**Button Style Categories Found:**
- Primary buttons (.btn-primary, .login-btn)
- Secondary buttons (.btn-secondary, .signup-btn)
- Action buttons (.btn-submit, .btn-reset, .btn-cancel, .btn-save)
- Specialized buttons (.btn-new-doc, .back-button, .theme-toggle-btn)
- Icon buttons (.btn-icon)
- Header buttons (.btn-header)
- Group containers (.button-group)
- Modal buttons (.modal-footer button)
- Table action buttons (.table-actions)

---

## Centralized Button Styles (admin-styles.css)

Located at: `/static/css/admin-styles.css`

These are the **standard button definitions** used across admin pages.

### Base Button Style (.btn)
```css
.btn {
    padding: var(--spacing-sm) var(--spacing-md);          /* 8px 16px */
    border: none;
    border-radius: var(--radius-md);                       /* 8px */
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);                         /* all 0.3s ease */
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);                                /* 8px */
    text-decoration: none;
    white-space: nowrap;
}
```

### Primary Button (.btn-primary)
```css
.btn-primary {
    background: var(--color-primary);                      /* #2563EB */
    color: white;
}

.btn-primary:hover {
    background: var(--color-secondary);                    /* #1e40af */
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);                          /* 0 4px 12px rgba(0, 0, 0, 0.15) */
}
```

### Secondary Button (.btn-secondary)
```css
.btn-secondary {
    background: var(--color-surface-light);                /* #334155 (dark) / white option */
    color: var(--color-text);
    border: 1px solid var(--color-border-color);           /* #475569 (dark) / #bfdbfe (light) */
}

.btn-secondary:hover {
    background: var(--color-primary);                      /* #2563EB */
    color: white;
    border-color: var(--color-primary);                    /* #2563EB */
}
```

### Success Button (.btn-success)
```css
.btn-success {
    background: var(--color-success);                      /* #10b981 */
    color: white;
}

.btn-success:hover {
    background: #059669;
}
```

### Warning Button (.btn-warning)
```css
.btn-warning {
    background: var(--color-warning);                      /* #f59e0b */
    color: white;
}

.btn-warning:hover {
    background: #d97706;
}
```

### Error Button (.btn-error)
```css
.btn-error {
    background: var(--color-error);                        /* #ef4444 */
    color: white;
}

.btn-error:hover {
    background: #dc2626;
}
```

### Size Variants
```css
.btn-sm {
    padding: var(--spacing-xs) var(--spacing-sm);          /* 4px 8px */
    font-size: 12px;
}

.btn-lg {
    padding: var(--spacing-md) var(--spacing-lg);          /* 16px 24px */
    font-size: 16px;
}

.btn-block {
    width: 100%;
}
```

### Icon Button (.btn-icon)
```css
.btn-icon {
    padding: var(--spacing-sm);                            /* 8px */
    background: var(--color-surface-light);                /* #334155 (dark) / #f0f0f0 (light) */
    color: var(--color-text-secondary);                    /* #94a3b8 (dark) / #64748b (light) */
    border: none;
    border-radius: var(--radius-md);                       /* 8px */
}

.btn-icon:hover {
    color: var(--color-accent);                            /* #60a5fa */
    background: var(--color-surface);                      /* #1e293b (dark) / white (light) */
}
```

---

## File-by-File Button Styles

### 1. login.html
**Location:** `/backend/app/static/login.html`

#### Login Button (.login-btn)
```css
.login-btn {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #2563EB 0%, #1e40af 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 30px;
}

.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
}

.login-btn:active {
    transform: translateY(0);
}
```

**Properties:**
- Full-width button
- Blue gradient background
- Hover: lift effect + shadow

#### Signup Button (.signup-btn)
```css
.signup-btn {
    padding: 12px;
    background: #f5f5f5;
    color: #2563EB;
    border: 2px solid #2563EB;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.signup-btn:hover {
    /* Hover styles incomplete in source */
}
```

**Properties:**
- Light gray background
- Blue text and border
- Secondary action style
- Outline/ghost style variant

#### Button Group (.button-group)
```css
.button-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 30px;
}
```

**Properties:**
- Two-column grid layout
- 12px gap between buttons

---

### 2. composer.html
**Location:** `/backend/app/static/composer.html`

#### Primary Button (.btn-primary)
```css
.btn-primary {
    background: #2563EB;
    color: #ffffff;
}

.btn-primary:hover {
    background: #1e40af;
    transform: translateY(-2px);
}
```

#### Secondary Button (.btn-secondary)
```css
.btn-secondary {
    background: rgba(37, 99, 235, 0.2);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.5);
}

.btn-secondary:hover {
    background: rgba(37, 99, 235, 0.3);
}
```

**Properties:**
- Transparent background with alpha
- Light blue text
- Subtle border

#### New Document Button (.btn-new-doc)
```css
.btn-new-doc {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #2563EB 0%, #1e40af 100%);
    color: #ffffff;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    margin-bottom: 15px;
}

.btn-new-doc:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}
```

**Properties:**
- Full-width
- Gradient background
- Bottom margin
- Lift effect on hover

#### Cancel Button (.btn-cancel)
```css
.btn-cancel {
    background: #444;
    color: #e8e8e8;
}
```

#### Save Button (.btn-save)
```css
.btn-save {
    background: #5a67d8;
    color: #1a1f3a;
}

.btn-save:hover {
    background: #667eea;
}
```

#### Suggestion Action Buttons (.suggestion-actions button)
```css
.suggestion-actions button {
    flex: 1;
    padding: 6px;
    border: 1px solid #334155;
    background: #334155;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s;
    color: #f1f5f9;
}

.suggestion-actions .accept {
    background: #10b981;
    color: white;
    border-color: #10b981;
}

.suggestion-actions .reject {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
}

.suggestion-actions button:hover {
    transform: translateY(-2px);
}
```

**Properties:**
- Flex: 1 (equal width in container)
- Accept button: green (#10b981)
- Reject button: red (#ef4444)
- Small padding and font size

---

### 3. form.html
**Location:** `/backend/app/static/form.html`

#### Submit Button (.btn-submit)
```css
.btn-submit {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-submit:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}
```

**Properties:**
- Purple/violet gradient
- Full width via flex: 1
- Lift effect on hover

#### Reset Button (.btn-reset)
```css
.btn-reset {
    background: #f0f0f0;
    color: #333;
    border: 2px solid #ddd;
}

.btn-reset:hover {
    background: #e8e8e8;
    border-color: #999;
}
```

**Properties:**
- Light gray background
- Dark text
- Border included
- Lighten on hover

---

### 4. excel-data-form.html
**Location:** `/backend/app/static/excel-data-form.html`

#### Base Button (.btn)
```css
.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    flex: 1;
}
```

#### Submit Button (.btn-submit)
```css
.btn-submit {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-submit:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}
```

#### Reset Button (.btn-reset)
```css
.btn-reset {
    background: #f0f0f0;
    color: #333;
}

.btn-reset:hover {
    background: #e0e0e0;
}
```

#### Clear Button (.btn-clear)
```css
.btn-clear {
    background: #ff6b6b;
    color: white;
}

.btn-clear:hover {
    background: #ff5252;
}
```

**Properties:**
- Red/coral background
- White text
- Darken on hover

#### Button Group
```css
.form-button-group {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}
```

---

### 5. excel-upload.html
**Location:** `/backend/app/static/excel-upload.html`

#### Back Button (.back-button)
```css
.back-button {
    background: rgba(102, 126, 234, 0.2);
    color: #5a67d8;
    border: 2px solid #5a67d8;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.back-button:hover {
    background: #5a67d8;
    color: #1a1f3a;
}
```

**Properties:**
- Outline style (light background + border)
- Indigo/purple theme
- Inline-block display
- Fill on hover

#### Theme Toggle Button (.theme-toggle-btn)
```css
.theme-toggle-btn {
    background: rgba(102, 126, 234, 0.2);
    color: #5a67d8;
    border: 1px solid #5a67d8;
    padding: 8px 15px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 5px;
}

.theme-toggle-btn:hover {
    background: #5a67d8;
    color: #1a1f3a;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
```

**Properties:**
- Flex container for icon + text
- Outline/ghost style
- Small padding
- Shadow on hover

#### Upload Button (.upload-button)
```css
.upload-button {
    background: linear-gradient(135deg, #5a67d8 0%, #667eea 100%);
    color: #1a1f3a;
    border: 2px solid #5a67d8;
    padding: 12px 30px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    width: 100%;
    margin-top: 20px;
}

.upload-button:hover {
    background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
    color: #1a1f3a;
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}
```

**Properties:**
- Full-width
- Gradient (indigo theme)
- Dark text (inverted)
- Lift + shadow on hover

---

### 6. word-upload.html
**Location:** `/backend/app/static/word-upload.html`

#### Back Button (.back-button)
```css
.back-button {
    background: rgba(102, 126, 234, 0.2);
    color: #5a67d8;
    border: 2px solid #5a67d8;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.back-button:hover {
    background: #5a67d8;
    color: #1a1f3a;
}
```

**(Same as excel-upload.html)**

#### Theme Toggle Button (.theme-toggle-btn)
**(Same as excel-upload.html)**

---

### 7. excel-form.html
**Location:** `/backend/app/static/excel-form.html`

#### Header Button (.btn-header)
```css
.btn-header {
    padding: 10px 20px;
    border: 2px solid white;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.btn-header:hover {
    background: white;
    color: #2563EB;
}
```

**Properties:**
- Transparent white background
- White border
- White text
- Invert colors on hover (white bg, blue text)

---

### 8. menu.html
**Location:** `/backend/app/static/menu.html`

*Note: This file does not have embedded button styles; uses centralized CSS variables and admin-styles.css*

---

### 9-15. Admin Pages (admin-dashboard.html, admin-users.html, admin-forms.html, admin-account.html, admin-reports.html, admin-audit-log.html)

**All admin pages use:** `/static/css/admin-styles.css` ✓

**Button styles used in admin pages:**
- `.btn .btn-primary`
- `.btn .btn-secondary`
- `.btn-icon`
- `.btn-sm`, `.btn-lg`

**Table action buttons in admin:**
```css
.table-actions {
    display: flex;
    gap: var(--spacing-sm);                                /* 8px */
}
```

Modal buttons appear in:
- User management modal
- Form management modal
- Settings modals

---

## Inconsistencies & Patterns

### ⚠️ Identified Inconsistencies

| Aspect | Issue | Files Affected |
|--------|-------|-----------------|
| **Button Padding** | Varies widely: 6px, 8px, 10px, 12px, 16px | Various inline styles |
| **Border Radius** | Ranges: 4px, 6px, 8px, 12px | Various inline styles |
| **Font Size** | Different bases: 13px, 14px, 16px | Various files |
| **Hover Effects** | Some use `transform`, others use`box-shadow` only | Composer vs Form |
| **Color Schemes** | Blue (#2563EB), Indigo (#5a67d8), Purple (#667eea) | Mix of themes |
| **Gradient Direction** | Both 135deg and other angles | Limited standardization |
| **Width** | Some full-width, some auto | Form-specific |

### ✅ Consistent Patterns

| Pattern | Details |
|---------|---------|
| **Transition** | All use `transition: all 0.3s ease` or similar |
| **Cursor** | All use `cursor: pointer` on interactive elements |
| **Text Color** | White on dark backgrounds, dark on light backgrounds |
| **Hover Effects** | Lift effect (`translateY(-2px)`) + shadow most common |
| **Border Styling** | `border: none` is standard for filled buttons |
| **Font Weight** | 600 (semibold) for most buttons, 500 for some |
| **Display** | Inline-flex common for button groups |

---

## Modal Button Styles

### Composer Modal Footer Buttons (.modal-footer button)
```css
.modal-footer button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
}
```

**In context:**
```css
.modal-footer {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}
```

### Admin Modal Buttons
From admin-styles.css:

```css
.modal-footer {
    display: flex;
    gap: var(--spacing-md);                                /* 16px */
    justify-content: flex-end;
    padding: var(--spacing-lg);                            /* 24px */
    border-top: 1px solid var(--color-border-color);
}
```

**Modal actions follow standard .btn pattern:**
- Primary actions: `.btn .btn-primary`
- Secondary/Cancel: `.btn .btn-secondary`

The admin modals in user management, form management include:
- "Lưu" (Save) - Primary button
- "Hủy" (Cancel) - Secondary button

---

## Button Group/Container Styles

### Two-Column Layout (login.html)
```css
.button-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 30px;
}
```

### Flex Layout (form.html)
```css
.form-button-group {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}
```

### Suggestion Actions (composer.html)
```css
.suggestion-actions {
    margin-top: 8px;
    display: flex;
    gap: 6px;
}
```

---

## Dark/Light Mode Button Styling

### composer.html & excel-upload.html

**Dark Mode (Default):**
```css
body.dark-mode .btn-primary {
    background: #2563EB;
    color: #ffffff;
}

body.dark-mode .btn-secondary {
    background: rgba(37, 99, 235, 0.2);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.5);
}
```

**Light Mode:**
```css
body.light-mode .btn-primary {
    background: #2563EB;
    color: #ffffff;
}

body.light-mode .btn-secondary {
    background: rgba(37, 99, 235, 0.2);
    color: #2563EB;
}
```

---

## Color System Overview

### Primary Colors Used
- **Blue:** `#2563EB` - Main CTAs (login, submit)
- **Dark Blue:** `#1e40af` - Hover state
- **Light Blue:** `#60a5fa` - Text/accent
- **Indigo:** `#5a67d8` - Upload pages
- **Purple:** `#667eea` - Secondary accent

### Status Colors
- **Success:** `#10b981` (Accept/approve)
- **Warning:** `#f59e0b` (Caution)
- **Error:** `#ef4444` (Cancel/delete/reject)
- **Info:** `#3b82f6` (Information)

### Semantic Backgrounds
- **Dark Mode Surface:** `#1e293b` (admin)
- **Light Mode Surface:** `#ffffff` (admin)
- **Borders:** `#334155` (dark) / `#bfdbfe` (light)

---

## Recommendations

### 1. **Standardize Button Styles**
   - Consolidate all button definitions into `admin-styles.css` or a new `buttons.css`
   - Remove redundant inline styles from individual HTML files
   - Create button style documentation/guide

### 2. **Establish Button Sizing Standards**
   ```
   - Small (.btn-sm): 4px 8px, 12px font
   - Medium (.btn): 8px 16px, 14px font (current default)
   - Large (.btn-lg): 16px 24px, 16px font
   ```

### 3. **Unify Color Scheme**
   - Choose one primary shade for consistency
   - Current: #2563EB (Microsoft Blue) - **RECOMMENDED**
   - Remove indigo/purple variants from upload pages
   - Use BrandColors defined in `admin-styles.css` `:root` CSS variables

### 4. **Create Button Variants Documentation**
   ```
   Solid variants:
   - .btn-primary (main action)
   - .btn-secondary (alternative action)
   - .btn-success (positive action)
   - .btn-warning (caution)
   - .btn-error (destructive)
   
   Ghost/Outline variants:
   - .btn-outline-primary
   - .btn-outline-secondary
   
   Icon-only:
   - .btn-icon (current)
   ```

### 5. **Improve Accessibility**
   - Add `:focus` states (currently only `:hover`)
   - Ensure sufficient color contrast
   - Add `aria-label` attributes
   - Consider disabled state styling

### 6. **Standardize Hover Effects**
   - Define base hover pattern:
     ```css
     transform: translateY(-2px);
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
     ```
   - Apply consistently across all buttons

### 7. **Create HTML Template/Usage Guide**
   Document proper button implementation:
   ```html
   <!-- Primary Action -->
   <button class="btn btn-primary">Save</button>
   
   <!-- Secondary Action -->
   <button class="btn btn-secondary">Cancel</button>
   
   <!-- With Icon -->
   <button class="btn btn-primary">
      <span>➕</span>
      <span>Add New</span>
   </button>
   ```

### 8. **Performance Optimization**
   - Use CSS custom properties (variables) for all values
   - Enable GPU acceleration for transforms
   - Consider reducing transition duration for mobile (300ms → 200ms)

### 9. **Test Coverage**
   - Verify button styles in light/dark modes
   - Test hover/focus/active states
   - Check responsive behavior
   - Validate keyboard navigation

### 10. **Migration Strategy**
   - Phase 1: Standardize admin pages (already using admin-styles.css) ✓
   - Phase 2: Migrate login.html to use centralized variables
   - Phase 3: Migrate upload/form pages
   - Phase 4: Update documentation

---

## File Summary Table

| File | Location | Button Styles | Status |
|------|----------|----------------|--------|
| admin-styles.css | `/css/` | Centralized ✓ | Standard |
| login.html | `/` | Embedded | Custom |
| composer.html | `/` | Embedded | Custom |
| form.html | `/` | Embedded | Custom |
| excel-data-form.html | `/` | Embedded | Custom |
| excel-upload.html | `/` | Embedded | Custom |
| word-upload.html | `/` | Embedded | Custom |
| excel-form.html | `/` | Embedded | Custom |
| menu.html | `/` | References CSS vars | Standard |
| admin-dashboard.html | `/admin-` | Centralized ✓ | Standard |
| admin-users.html | `/admin-` | Centralized ✓ | Standard |
| admin-forms.html | `/admin-` | Centralized ✓ | Standard |
| admin-account.html | `/admin-` | Centralized ✓ | Standard |
| admin-reports.html | `/admin-` | Centralized ✓ | Standard |
| admin-audit-log.html | `/admin-` | Centralized ✓ | Standard |
| form-autocomplete.html | `/` | Empty file | N/A |

---

## CSS Variables Reference (From admin-styles.css)

```css
:root {
    /* Primary Colors */
    --color-primary: #2563EB;              /* Action button */
    --color-secondary: #1e40af;            /* Hover state */
    --color-accent: #60a5fa;               /* Light accent */
    
    /* Status Colors */
    --color-success: #10b981;              /* Green */
    --color-warning: #f59e0b;              /* Orange */
    --color-error: #ef4444;                /* Red */
    --color-info: #3b82f6;                 /* Info blue */
    
    /* Spacing for button padding */
    --spacing-xs: 4px;
    --spacing-sm: 8px;                     /* .btn padding-left/right */
    --spacing-md: 16px;                    /* .btn padding-top/bottom */
    --spacing-lg: 24px;
    
    /* Border Radius */
    --radius-md: 8px;                      /* .btn border-radius */
    --radius-lg: 12px;
    
    /* Transitions */
    --transition: all 0.3s ease;           /* Standard button transition */
    
    /* Shadows */
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
    --shadow-lg: 0 10px 28px rgba(0, 0, 0, 0.2);
}
```

---

## Contact & Notes

- **Last Updated:** March 18, 2026
- **Scope:** Full system button style audit
- **Files Analyzed:** 17 files (15 HTML + 1 CSS + 1 empty)
- **Total Button Classes Found:** 25+
- **Recommendations:** 10 actionable items
- **Priority:** HIGH - For consistency and maintenance

