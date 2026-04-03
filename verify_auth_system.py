#!/usr/bin/env python3
"""
Verification script to test the new authentication system
Run this after starting the backend to verify everything works
"""

import subprocess
import sys
import time
import requests
import json
from datetime import datetime

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def test_backend_running():
    """Check if backend is running"""
    print_header("Checking Backend Status")
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=2)
        if response.status_code == 200:
            print_success("Backend is running on http://localhost:8000")
            return True
        else:
            print_error(f"Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend at http://localhost:8000")
        print_info("Start the backend with: cd backend && python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print_error(f"Error checking backend: {e}")
        return False

def test_login_endpoint():
    """Test login functionality"""
    print_header("Testing Login Endpoint")
    
    # Test 1: Valid credentials with admin account
    print_info("Test 1: Login with admin/admin123")
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"Admin login successful: {data.get('user', {}).get('username')}")
                # Save session cookie
                admin_cookies = response.cookies
                return admin_cookies
            else:
                print_error(f"Login failed: {data.get('error', 'Unknown error')}")
                return None
        else:
            print_error(f"Login returned status {response.status_code}")
            print_info(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error testing login: {e}")
        return None

def test_check_auth(cookies):
    """Test authentication check"""
    print_header("Testing Auth Check Endpoint")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/auth/check-auth",
            cookies=cookies,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("authenticated"):
                user = data.get("user", {})
                print_success(f"Auth check passed: {user.get('username')} ({user.get('email')})")
                return True
            else:
                print_error("Auth check returned authenticated=false")
                return False
        else:
            print_error(f"Auth check returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error checking auth: {e}")
        return False

def test_session_endpoint(cookies):
    """Test session information endpoint"""
    print_header("Testing Session Endpoint")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/auth/session",
            cookies=cookies,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Session retrieved successfully")
            print_info(f"Username: {data.get('username')}")
            print_info(f"Email: {data.get('email')}")
            print_info(f"Login time: {data.get('login_time')}")
            return True
        else:
            print_error(f"Session endpoint returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error testing session endpoint: {e}")
        return False

def test_invalid_credentials():
    """Test login with invalid credentials"""
    print_header("Testing Invalid Credentials")
    
    print_info("Test: Login with wrong password")
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login",
            json={"username": "admin", "password": "wrongpass"},
            timeout=5
        )
        
        if response.status_code == 401:
            data = response.json()
            print_success(f"Correctly rejected: {data.get('error')}")
            return True
        else:
            print_error(f"Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error testing invalid credentials: {e}")
        return False

def test_logout(cookies):
    """Test logout functionality"""
    print_header("Testing Logout Endpoint")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/logout",
            cookies=cookies,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"Logout successful: {data.get('message')}")
                return True
            else:
                print_error(f"Logout failed: {data}")
                return False
        else:
            print_error(f"Logout returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error testing logout: {e}")
        return False

def test_auth_after_logout(cookies):
    """Verify auth fails after logout"""
    print_header("Testing Auth After Logout")
    
    print_info("Checking if auth is still valid after logout...")
    try:
        response = requests.get(
            "http://localhost:8000/api/auth/check-auth",
            cookies=cookies,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data.get("authenticated"):
                print_success("Auth correctly returns false after logout")
                return True
            else:
                print_error("Auth still returns true after logout - Session not cleared!")
                return False
        else:
            print_error(f"Auth check returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error testing post-logout auth: {e}")
        return False

def test_pages_accessible():
    """Test that pages are accessible"""
    print_header("Testing Page Accessibility")
    
    pages = [
        ("Menu page", "/"),
        ("Login page", "/login"),
    ]
    
    results = []
    for name, path in pages:
        try:
            response = requests.get(
                f"http://localhost:8000{path}",
                timeout=5
            )
            if response.status_code == 200:
                print_success(f"{name} is accessible")
                results.append(True)
            else:
                print_error(f"{name} returned status {response.status_code}")
                results.append(False)
        except Exception as e:
            print_error(f"Cannot access {name}: {e}")
            results.append(False)
    
    return all(results)

def test_static_files():
    """Test that static files are accessible"""
    print_header("Testing Static Files")
    
    files = [
        ("Menu HTML", "/static/menu.html"),
        ("Login HTML", "/static/login.html"),
    ]
    
    results = []
    for name, path in files:
        try:
            response = requests.get(
                f"http://localhost:8000{path}",
                timeout=5
            )
            if response.status_code == 200:
                print_success(f"{name} is accessible")
                results.append(True)
            else:
                print_error(f"{name} returned status {response.status_code}")
                results.append(False)
        except Exception as e:
            print_error(f"Cannot access {name}: {e}")
            results.append(False)
    
    return all(results)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🚀 AutoFill AI - Authentication System Test Suite")
    print("="*60)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {}
    
    # Test 1: Backend running
    if not test_backend_running():
        print_error("\nCannot proceed without running backend!")
        return False
    
    # Test 2: Login endpoint
    cookies = test_login_endpoint()
    results["Login"] = cookies is not None
    
    if not cookies:
        print_error("\nCannot proceed without valid session!")
        return False
    
    # Test 3: Check auth
    results["Auth Check"] = test_check_auth(cookies)
    
    # Test 4: Session endpoint
    results["Session Endpoint"] = test_session_endpoint(cookies)
    
    # Test 5: Invalid credentials
    results["Invalid Credentials"] = test_invalid_credentials()
    
    # Test 6: Logout
    results["Logout"] = test_logout(cookies)
    
    # Test 7: Auth after logout
    results["Auth After Logout"] = test_auth_after_logout(cookies)
    
    # Test 8: Pages accessible
    results["Pages Accessible"] = test_pages_accessible()
    
    # Test 9: Static files
    results["Static Files"] = test_static_files()
    
    # Print summary
    print_header("Test Summary")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Total: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print_success("All tests passed! ✨")
        print_header("Next Steps")
        print_info("1. Open browser: http://localhost:8000/")
        print_info("2. Try login with admin/admin123")
        print_info("3. Verify navbar displays user info")
        print_info("4. Test logout functionality")
        return True
    else:
        print_error(f"{total_tests - passed_tests} test(s) failed")
        print_header("What to Check")
        print_info("1. Backend is running: python -m uvicorn app.main:app --reload")
        print_info("2. Check error messages above")
        print_info("3. Review browser console (F12) for JavaScript errors")
        print_info("4. Check server logs for detailed error info")
        return False

if __name__ == "__main__":
    success = main()
    print("\n")
    sys.exit(0 if success else 1)
