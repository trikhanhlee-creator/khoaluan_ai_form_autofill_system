/**
 * Global Theme Manager - Synchronizes light/dark mode across entire system
 * Handles: localStorage persistence, cross-tab sync, DOM updates, event dispatching
 */

class ThemeManager {
    constructor() {
        this.STORAGE_KEY = 'app-theme';
        this.THEME_LIGHT = 'light';
        this.THEME_DARK = 'dark';
        this.EVENT_NAME = 'app-theme-changed';
        this.init();
    }

    /**
     * Initialize theme system
     */
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupTheme());
        } else {
            // DOM is already loaded
            this.setupTheme();
        }
    }

    /**
     * Setup theme after DOM is ready
     */
    setupTheme() {
        // Load saved theme or default to dark
        const savedTheme = this.getSavedTheme();
        this.setTheme(savedTheme, false);
        this.bindThemeToggleButtons();

        // Listen for storage changes from other tabs
        window.addEventListener('storage', (e) => {
            if (e.key === this.STORAGE_KEY) {
                this.setTheme(e.newValue || this.THEME_DARK, false);
            }
        });

        // Listen to custom theme changed events from other pages
        window.addEventListener(this.EVENT_NAME, (e) => {
            this.setTheme(e.detail.theme, false);
        });
    }

    /**
     * Get saved theme from localStorage
     */
    getSavedTheme() {
        const savedTheme = localStorage.getItem(this.STORAGE_KEY);
        if (savedTheme === this.THEME_LIGHT || savedTheme === this.THEME_DARK) {
            return savedTheme;
        }

        // Backward compatibility for legacy theme keys.
        const legacyKeys = ['admin-theme-mode', 'theme-mode', 'theme'];
        for (const key of legacyKeys) {
            const legacyTheme = localStorage.getItem(key);
            if (legacyTheme === this.THEME_LIGHT || legacyTheme === this.THEME_DARK) {
                localStorage.setItem(this.STORAGE_KEY, legacyTheme);
                return legacyTheme;
            }
        }

        return this.THEME_DARK;
    }

    /**
     * Get current theme
     */
    getCurrentTheme() {
        try {
            if (!document.body) return this.THEME_DARK;
            return document.body.classList.contains(this.THEME_LIGHT + '-mode')
                ? this.THEME_LIGHT
                : this.THEME_DARK;
        } catch (error) {
            return this.THEME_DARK;
        }
    }

    /**
     * Set theme globally
     * @param {string} theme - 'light' or 'dark'
     * @param {boolean} notify - Whether to notify other tabs
     */
    setTheme(theme, notify = true) {
        theme = theme === this.THEME_LIGHT ? this.THEME_LIGHT : this.THEME_DARK;

        // Update body classes - wait for body to exist
        if (!document.body) {
            // DOM not ready yet, try again later
            setTimeout(() => this.setTheme(theme, notify), 100);
            return;
        }

        // Update body classes
        document.body.classList.remove(this.THEME_LIGHT + '-mode', this.THEME_DARK + '-mode');
        document.body.classList.add(theme + '-mode');

        // Save to localStorage
        localStorage.setItem(this.STORAGE_KEY, theme);

        // Update theme icon and label globally
        this.updateThemeUI(theme);

        // Notify other tabs
        if (notify) {
            window.dispatchEvent(new CustomEvent(this.EVENT_NAME, {
                detail: { theme }
            }));
        }

        // Dispatch change event for custom handlers
        window.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme }
        }));
    }

    /**
     * Toggle between light and dark mode
     */
    toggleTheme() {
        try {
            const currentTheme = this.getCurrentTheme();
            const newTheme = currentTheme === this.THEME_LIGHT ? this.THEME_DARK : this.THEME_LIGHT;
            this.setTheme(newTheme, true);
        } catch (error) {
            console.error('Error toggling theme:', error);
        }
    }

    /**
     * Update all theme UI elements
     */
    updateThemeUI(theme) {
        // Safety check - ensure DOM elements exist
        if (!document.body) return;

        // Ensure all toggle buttons always work, even on pages without site-ui.js.
        this.bindThemeToggleButtons();

        // Update all theme toggle buttons
        const themeButtons = document.querySelectorAll('[data-theme-toggle]');
        themeButtons.forEach(btn => {
            this.updateThemeButton(btn, theme);
        });

        // Update theme icon and label in navbar
        const themeIcon = document.getElementById('themeIcon');
        const themeLabel = document.getElementById('themeLabel');

        if (themeIcon) {
            themeIcon.textContent = theme === this.THEME_LIGHT ? '☀️' : '🌙';
        }
        if (themeLabel) {
            themeLabel.textContent = theme === this.THEME_LIGHT ? 'Sáng' : 'Tối';
        }

        // Update all elements with theme-aware data attributes
        const themeElements = document.querySelectorAll('[data-light-text], [data-dark-text]');
        themeElements.forEach(el => {
            if (theme === this.THEME_LIGHT && el.dataset.lightText) {
                el.style.color = el.dataset.lightText;
            } else if (theme === this.THEME_DARK && el.dataset.darkText) {
                el.style.color = el.dataset.darkText;
            }
        });
    }

    /**
     * Update individual theme button
     */
    updateThemeButton(btn, theme) {
        const icon = btn.querySelector('[data-theme-icon]');
        const label = btn.querySelector('[data-theme-label]');

        if (!icon && !label) {
            btn.textContent = theme === this.THEME_LIGHT ? '☀️' : '🌙';
            btn.setAttribute('title', theme === this.THEME_LIGHT ? 'Chế độ sáng' : 'Chế độ tối');
            return;
        }

        if (icon) {
            icon.textContent = theme === this.THEME_LIGHT ? '☀️' : '🌙';
        }
        if (label) {
            label.textContent = theme === this.THEME_LIGHT ? 'Sáng' : 'Tối';
        }
    }

    /**
     * Bind click handlers to all theme toggle buttons once.
     */
    bindThemeToggleButtons() {
        const themeButtons = document.querySelectorAll('[data-theme-toggle]');
        themeButtons.forEach((btn) => {
            if (btn.dataset.themeBound === '1') {
                return;
            }

            btn.addEventListener('click', (event) => {
                event.preventDefault();
                this.toggleTheme();
            });

            btn.dataset.themeBound = '1';
        });
    }

    /**
     * Is light mode active?
     */
    isLightMode() {
        return this.getCurrentTheme() === this.THEME_LIGHT;
    }

    /**
     * Is dark mode active?
     */
    isDarkMode() {
        return this.getCurrentTheme() === this.THEME_DARK;
    }

    /**
     * Apply theme CSS variables dynamically
     */
    applyThemeVariables() {
        const theme = this.getCurrentTheme();
        const root = document.documentElement;

        if (theme === this.THEME_LIGHT) {
            root.style.setProperty('--bg-primary', '#f0f9ff');
            root.style.setProperty('--bg-secondary', '#ffffff');
            root.style.setProperty('--text-primary', '#1e293b');
            root.style.setProperty('--text-secondary', '#475569');
        } else {
            root.style.setProperty('--bg-primary', '#0f172a');
            root.style.setProperty('--bg-secondary', '#1e293b');
            root.style.setProperty('--text-primary', '#f1f5f9');
            root.style.setProperty('--text-secondary', '#cbd5e1');
        }
    }

    /**
     * Get color for current theme
     */
    getThemeColor(lightColor, darkColor) {
        return this.isLightMode() ? lightColor : darkColor;
    }
}

// Initialize global theme manager
const themeManager = new ThemeManager();

// Make it globally accessible
window.themeManager = themeManager;

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
