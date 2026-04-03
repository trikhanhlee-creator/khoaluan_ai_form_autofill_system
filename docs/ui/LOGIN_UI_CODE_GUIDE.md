# Login UI & Menu Integration - Complete Code Guide

## Overview
Complete implementation of authentication system with session-based login and redesigned horizontal navigation menu. This guide provides detailed code examples and explanations.

**Status**: ✅ **COMPLETE & TESTED**

---

## 1. Authentication Module (`backend/app/api/routes/auth.py`)

### Full Code Structure

```python
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

# In-Memory Storage
users_db = {
    "admin": {
        "username": "Admin User",
        "email": "admin@example.com",
        "password": "admin123"
    },
    "user": {
        "username": "Regular User",
        "email": "user@example.com",
        "password": "user123"
    }
}

sessions = {}  # {session_id: {username, email, login_time}}

def generate_session_id() -> str:
    """Generate unique session ID"""
    return str(uuid.uuid4())

@router.post("/login")
async def login(request: Request):
    """Login endpoint - validates credentials and creates session"""
    try:
        data = await request.json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        # Validate credentials
        if not username or not password:
            return JSONResponse(
                status_code=400,
                content={"error": "Username and password required"}
            )
        
        if username not in users_db:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid credentials"}
            )
        
        if users_db[username]["password"] != password:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid credentials"}
            )
        
        # Create session
        user_info = users_db[username]
        session_id = generate_session_id()
        sessions[session_id] = {
            "username": user_info["username"],
            "email": user_info["email"],
            "login_time": datetime.utcnow().isoformat()
        }
        
        # Set session cookie
        response = JSONResponse(
            status_code=200,
            content={
                "success": True,
                "user": {
                    "username": user_info["username"],
                    "email": user_info["email"]
                }
            }
        )
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=86400,  # 24 hours
            httponly=True,
            samesite="Lax"
        )
        return response
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Login failed"}
        )

@router.post("/logout")
async def logout(request: Request):
    """Logout endpoint - clears session and cookie"""
    try:
        session_id = request.cookies.get("session_id")
        if session_id and session_id in sessions:
            del sessions[session_id]
        
        response = JSONResponse(
            status_code=200,
            content={"success": True, "message": "Đã đăng xuất"}
        )
        response.delete_cookie("session_id")
        return response
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Logout failed"}
        )

@router.get("/check-auth")
async def check_auth(request: Request):
    """Check current authentication status"""
    try:
        session_id = request.cookies.get("session_id")
        
        if session_id and session_id in sessions:
            user_info = sessions[session_id]
            return JSONResponse(
                status_code=200,
                content={
                    "authenticated": True,
                    "user": {
                        "username": user_info["username"],
                        "email": user_info["email"]
                    }
                }
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"authenticated": False, "user": None}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=200,
            content={"authenticated": False, "user": None}
        )

@router.get("/session")
async def get_session(request: Request):
    """Get current session information"""
    try:
        session_id = request.cookies.get("session_id")
        
        if session_id and session_id in sessions:
            return JSONResponse(
                status_code=200,
                content=sessions[session_id]
            )
        else:
            return JSONResponse(
                status_code=401,
                content={"error": "No active session"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Session lookup failed"}
        )
```

### Key Implementation Details

**Session ID Generation**:
- Uses `uuid.uuid4()` for cryptographically strong random IDs
- Convert to string for storage in dictionary

**Password Validation**:
- Direct string comparison (for demo only)
- Non-production: Use bcrypt in real app
- Reject with generic "Invalid credentials" (no username enumeration)

**Cookie Security**:
- `httponly=True`: Prevents JavaScript access
- `max_age=86400`: 24-hour timeout
- `samesite=Lax`: CSRF protection
- No `secure=True` needed for localhost (set in production)

---

## 2. Login Page (`backend/app/static/login.html`)

### Key HTML Sections

```html
<!-- Login Form Container -->
<div class="login-container">
    <!-- Logo -->
    <div class="login-header">
        <div class="logo">🚀</div>
        <h1>AutoFill AI</h1>
        <h2>Document AutoComposer</h2>
    </div>
    
    <!-- Login Form -->
    <form id="loginForm" class="login-form">
        <input 
            id="username" 
            type="text" 
            placeholder="Username"
            data-username="admin"
            data-password="admin123"
            onclick="handleDemoClick(event)"
            required
        />
        
        <input 
            id="password" 
            type="password" 
            placeholder="Password"
            required
        />
        
        <label>
            <input type="checkbox" id="rememberMe" />
            Remember me
        </label>
        
        <button type="submit" id="loginBtn">Sign In</button>
    </form>
    
    <!-- Demo Credentials -->
    <div class="demo-credentials">
        <p>Try Demo Accounts:</p>
        <button 
            type="button" 
            data-username="admin" 
            data-password="admin123"
            onclick="handleDemoSelect(event)"
        >
            Admin Account (admin / admin123)
        </button>
        <button 
            type="button" 
            data-username="user" 
            data-password="user123"
            onclick="handleDemoSelect(event)"
        >
            User Account (user / user123)
        </button>
    </div>
    
    <!-- Messages -->
    <div id="message" class="message"></div>
    <div id="loadingIndicator" class="loading-indicator"></div>
</div>
```

### CSS Styling

```css
/* Main Container */
.login-container {
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

/* Login Card */
.login-form {
    background: white;
    border-radius: 12px;
    padding: 40px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Input Fields */
input[type="text"],
input[type="password"] {
    width: 100%;
    padding: 12px 16px;
    margin-bottom: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
    transition: all 0.3s;
}

input[type="text"]:focus,
input[type="password"]:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Sign In Button */
button[type="submit"] {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Loading Animation */
.loading-indicator {
    display: none;
    width: 40px;
    height: 40px;
    border: 4px solid #e0e0e0;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Message Display */
.message {
    margin-top: 16px;
    padding: 12px;
    border-radius: 6px;
    text-align: center;
    display: none;
}

.message.error {
    background: #fee;
    color: #c33;
    border: 1px solid #fcc;
    display: block;
}

.message.success {
    background: #efe;
    color: #3c3;
    border: 1px solid #cfc;
    display: block;
}
```

### JavaScript Functions

```javascript
// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    checkAuthOnLoad();
    document.getElementById("loginForm").addEventListener("submit", handleLogin);
});

// Check if already logged in
async function checkAuthOnLoad() {
    try {
        const response = await fetch("/api/auth/check-auth");
        const data = await response.json();
        
        if (data.authenticated) {
            // Already logged in, redirect to menu
            window.location.href = "/";
        }
    } catch (error) {
        console.error("Auth check failed:", error);
        // Continue to show login form
    }
}

// Handle login submission
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const rememberMe = document.getElementById("rememberMe").checked;
    const messageDiv = document.getElementById("message");
    const loginBtn = document.getElementById("loginBtn");
    const loadingIndicator = document.getElementById("loadingIndicator");
    
    // Validation
    if (!username || !password) {
        showMessage("Please enter username and password", "error");
        return;
    }
    
    // Show loading state
    loginBtn.disabled = true;
    loadingIndicator.style.display = "block";
    messageDiv.style.display = "none";
    
    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password,
                rememberMe: rememberMe
            }),
            credentials: "include"  // Important: include cookies
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showMessage("Login successful! Redirecting...", "success");
            setTimeout(() => {
                window.location.href = "/";
            }, 1000);
        } else {
            showMessage(data.error || "Login failed", "error");
            loginBtn.disabled = false;
            loadingIndicator.style.display = "none";
        }
    } catch (error) {
        console.error("Login error:", error);
        showMessage("Network error. Please try again.", "error");
        loginBtn.disabled = false;
        loadingIndicator.style.display = "none";
    }
}

// Handle demo account selection
function handleDemoSelect(event) {
    event.preventDefault();
    
    const button = event.target;
    const username = button.dataset.username;
    const password = button.dataset.password;
    
    document.getElementById("username").value = username;
    document.getElementById("password").value = password;
    
    // Focus password field for user to just press Enter
    document.getElementById("password").focus();
}

// Handle demo credentials click in input field
function handleDemoClick(event) {
    if (event.target.value === "") {
        event.target.value = event.target.dataset.username;
        document.getElementById("password").focus();
    }
}

// Show message to user
function showMessage(message, type) {
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = "block";
}
```

---

## 3. Menu with Navbar (`backend/app/static/menu.html`)

### Navbar HTML Structure

```html
<!-- Fixed Navigation Bar -->
<nav class="navbar">
    <div class="navbar-container">
        <!-- Logo/Brand -->
        <div class="navbar-brand" onclick="window.location.href='/'">
            🚀 AutoFill AI
        </div>
        
        <!-- Menu Items -->
        <div class="navbar-menu">
            <a href="/" class="nav-link">🏠 Trang Chủ</a>
            <a href="/composer" class="nav-link">🤖 Soạn Thảo</a>
            <a href="/excel" class="nav-link">📊 Excel Upload</a>
            <a href="/form" class="nav-link">✏️ Điền Form</a>
        </div>
        
        <!-- Auth Section -->
        <div class="navbar-auth">
            <!-- User Info (visible when logged in) -->
            <div id="userInfo" class="user-info" style="display: none;">
                <div class="user-avatar" id="userAvatar"></div>
                <div class="user-details">
                    <div class="username" id="userName"></div>
                    <div class="email" id="userEmail"></div>
                </div>
            </div>
            
            <!-- Login Link (visible when logged out) -->
            <a id="loginLink" class="login-link" href="/login">
                Đăng Nhập
            </a>
            
            <!-- Logout Button (visible when logged in) -->
            <button id="logoutBtn" class="logout-btn" style="display: none;"
                    onclick="handleLogout()">
                Đăng Xuất
            </button>
        </div>
    </div>
</nav>

<!-- Main Content Area -->
<main class="main-content">
    <div class="welcome-section">
        <h1 id="welcomeMessage">Vui lòng đăng nhập để bắt đầu</h1>
        
        <!-- Menu Cards -->
        <div class="menu-grid">
            <div class="menu-card">
                <div class="card-icon">🤖</div>
                <h3>Soạn Thảo Tự Động</h3>
                <p>Sử dụng AI để soạn thảo và cải thiện tài liệu</p>
                <a href="/composer" class="card-link">Truy Cập</a>
            </div>
            
            <div class="menu-card">
                <div class="card-icon">📊</div>
                <h3>Tải Lên Excel</h3>
                <p>Tự động tạo biểu mẫu từ tệp Excel</p>
                <a href="/excel" class="card-link">Truy Cập</a>
            </div>
            
            <div class="menu-card">
                <div class="card-icon">✏️</div>
                <h3>Điền Biểu Mẫu</h3>
                <p>Tự động điền thông tin vào biểu mẫu</p>
                <a href="/form" class="card-link">Truy Cập</a>
            </div>
        </div>
    </div>
</main>
```

### Navbar CSS

```css
/* Fixed Navbar */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 80px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* Navbar Container (Flexbox Layout) */
.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 40px;
    max-width: 1400px;
    margin: 0 auto;
}

/* Brand/Logo */
.navbar-brand {
    font-size: 24px;
    font-weight: bold;
    color: white;
    cursor: pointer;
    transition: all 0.3s;
    flex-shrink: 0;
}

.navbar-brand:hover {
    transform: scale(1.05);
}

/* Menu Items */
.navbar-menu {
    display: flex;
    gap: 30px;
    flex: 1;
    margin-left: 60px;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-weight: 500;
    padding: 8px 12px;
    border-radius: 4px;
    transition: all 0.3s;
    display: inline-block;
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

/* Auth Section */
.navbar-auth {
    display: flex;
    align-items: center;
    gap: 20px;
    flex-shrink: 0;
}

/* User Info Display */
.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.1);
    padding: 8px 16px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    font-size: 16px;
    flex-shrink: 0;
}

.user-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.username {
    color: white;
    font-weight: 600;
    font-size: 14px;
}

.email {
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
}

/* Login Link */
.login-link {
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    transition: all 0.3s;
    font-weight: 500;
}

.login-link:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Logout Button */
.logout-btn {
    background: rgba(255, 255, 255, 0.25);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s;
}

.logout-btn:hover {
    background: rgba(255, 255, 255, 0.35);
    border-color: rgba(255, 255, 255, 0.4);
}

/* Main Content (Account for fixed navbar) */
.main-content {
    margin-top: 80px;
    padding: 40px 20px;
    min-height: calc(100vh - 80px);
}

/* Responsive Design */
@media (max-width: 768px) {
    .navbar-menu {
        margin-left: 30px;
        gap: 15px;
        font-size: 14px;
    }
    
    .user-details {
        display: none;
    }
}

@media (max-width: 480px) {
    .navbar-container {
        flex-wrap: wrap;
        padding: 10px 20px;
        height: auto;
        min-height: 80px;
    }
    
    .navbar-brand {
        font-size: 18px;
        order: 1;
    }
    
    .navbar-menu {
        width: 100%;
        order: 3;
        margin-left: 0;
        margin-top: 10px;
        flex-direction: column;
        gap: 5px;
    }
    
    .nav-link {
        width: 100%;
        text-align: center;
        padding: 10px;
    }
    
    .navbar-auth {
        order: 2;
        width: 100%;
        margin-top: 10px;
        justify-content: center;
    }
}
```

### Navbar JavaScript

```javascript
// Initialize on page load
window.addEventListener("DOMContentLoaded", checkAuth);

// Check authentication status and update UI
async function checkAuth() {
    try {
        const response = await fetch("/api/auth/check-auth");
        const data = await response.json();
        
        if (data.authenticated && data.user) {
            displayUserInfo(data.user);
        } else {
            showLoginOption();
        }
    } catch (error) {
        console.error("Auth check failed:", error);
        showLoginOption();
    }
}

// Display logged-in user information
function displayUserInfo(user) {
    const userInfo = document.getElementById("userInfo");
    const logoutBtn = document.getElementById("logoutBtn");
    const loginLink = document.getElementById("loginLink");
    const welcomeMessage = document.getElementById("welcomeMessage");
    
    // Show user info
    userInfo.style.display = "flex";
    logoutBtn.style.display = "block";
    loginLink.style.display = "none";
    
    // Update user details
    document.getElementById("userAvatar").textContent = 
        user.username.charAt(0).toUpperCase();
    document.getElementById("userName").textContent = user.username;
    document.getElementById("userEmail").textContent = user.email;
    
    // Update welcome message
    welcomeMessage.textContent = `Chào ${user.username}! 👋`;
}

// Show login option (user not logged in)
function showLoginOption() {
    const userInfo = document.getElementById("userInfo");
    const logoutBtn = document.getElementById("logoutBtn");
    const loginLink = document.getElementById("loginLink");
    const welcomeMessage = document.getElementById("welcomeMessage");
    
    // Hide user info
    userInfo.style.display = "none";
    logoutBtn.style.display = "none";
    loginLink.style.display = "inline-block";
    
    // Show default message
    welcomeMessage.textContent = "Vui lòng đăng nhập để bắt đầu";
}

// Handle logout
async function handleLogout() {
    if (!confirm("Bạn chắc chắn muốn đăng xuất?")) {
        return;
    }
    
    try {
        const response = await fetch("/api/auth/logout", {
            method: "POST",
            credentials: "include"
        });
        
        if (response.ok) {
            // Clear user info and show login option
            showLoginOption();
            
            // Redirect after short delay
            setTimeout(() => {
                window.location.href = "/";
            }, 500);
        } else {
            alert("Logout failed. Please try again.");
        }
    } catch (error) {
        console.error("Logout error:", error);
        alert("Network error during logout.");
    }
}
```

---

## 4. Main App Updates (`backend/app/main.py`)

### Required Changes

```python
# 1. Add auth import to existing imports
from app.api.routes import suggestions, word, form_replacement, excel, composer, auth

# 2. Register auth router (should be first)
app.include_router(auth.router)

# 3. Register other routers
app.include_router(suggestions.router)
app.include_router(word.router)
app.include_router(form_replacement.router)
app.include_router(excel.router)
app.include_router(composer.router)

# 4. Add login route handler
@app.get("/login")
async def login_page():
    """Serve login.html when user visits /login"""
    return FileResponse("app/static/login.html", media_type="text/html")
```

---

## API Testing Examples

### Using cURL

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  -c cookies.txt

# Check authentication (using saved cookies)
curl -X GET http://localhost:8000/api/auth/check-auth \
  -b cookies.txt

# Logout
curl -X POST http://localhost:8000/api/auth/logout \
  -b cookies.txt
```

### Using Python

```python
import requests

# Create session
session = requests.Session()

# Login
response = session.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "admin", "password": "admin123"}
)
print("Login:", response.json())

# Check auth
response = session.get("http://localhost:8000/api/auth/check-auth")
print("Auth check:", response.json())

# Logout
response = session.post("http://localhost:8000/api/auth/logout")
print("Logout:", response.json())
```

### Using JavaScript Fetch

```javascript
// Login
fetch("/api/auth/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username: "admin", password: "admin123"}),
    credentials: "include"  // Include cookies
})
.then(r => r.json())
.then(data => console.log("Login:", data));

// Check auth
fetch("/api/auth/check-auth", {credentials: "include"})
    .then(r => r.json())
    .then(data => console.log("Auth:", data));

// Logout
fetch("/api/auth/logout", {
    method: "POST",
    credentials: "include"
})
.then(r => r.json())
.then(data => console.log("Logout:", data));
```

---

## Production Deployment Checklist

### Security Hardening

- [ ] Replace in-memory user store with database
- [ ] Implement BCrypt password hashing
- [ ] Add rate limiting on login endpoint
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set `secure=True` on cookies
- [ ] Implement CSRF token validation
- [ ] Add input sanitization
- [ ] Implement audit logging
- [ ] Add email verification
- [ ] Add password reset flow

### Session Management

- [ ] Move sessions to Redis or database
- [ ] Implement session cleanup task
- [ ] Add session monitoring dashboard
- [ ] Implement session timeout handling
- [ ] Add concurrent session limits

### Monitoring & Logging

- [ ] Add authentication event logging
- [ ] Monitor failed login attempts
- [ ] Set up alerts for suspicious activity
- [ ] Implement analytics tracking
- [ ] Add performance monitoring

---

**Last Updated**: 2024-01-15
**Status**: ✅ COMPLETE
**Version**: 1.0
