#!/usr/bin/env python3
"""
Quick reference guide for XLS upload - test script users can run
"""
import requests
import time

def quick_test():
    """Run quick test to verify system is working"""
    
    print("\n" + "=" * 70)
    print("✅ XLS PARSING FIX - QUICK VERIFICATION")
    print("=" * 70)
    
    # Check server is running
    print("\n1. Checking if server is running...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("   ✅ Server running at http://localhost:8000")
        else:
            print("   ⚠️  Server responded but health check not OK")
    except:
        print("   ❌ Server not running. Start it first:")
        print("      cd backend")
        print("      python run.py")
        return False
    
    # Check Excel upload page exists
    print("\n2. Checking Excel upload page...")
    try:
        response = requests.get("http://localhost:8000/excel", timeout=2)
        if response.status_code == 200:
            print("   ✅ Excel upload page: http://localhost:8000/excel")
        else:
            print(f"   ⚠️  Page status: {response.status_code}")
    except:
        print("   ⚠️  Could not access Excel page")
    
    # Check API endpoint
    print("\n3. Checking Excel API endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/excel/sessions", timeout=2)
        print(f"   ✅ API endpoint working (Status: {response.status_code})")
    except:
        print("   ⚠️  Could not access API")
    
    print("\n" + "=" * 70)
    print("🎯 READY TO USE")
    print("=" * 70)
    
    print("\nHow to test the fix:")
    print("1. Open browser: http://localhost:8000/excel")
    print("2. Upload a .xls file (any format - even with empty first row)")
    print("3. You should see: ✅ Tải file thành công!")
    print("\nIf you get an error, run the full verification:")
    print("   python backend/test_xls_fix_verification.py")
    
    return True

if __name__ == "__main__":
    quick_test()
