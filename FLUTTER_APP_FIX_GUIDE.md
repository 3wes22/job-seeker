# 🔧 Flutter App Configuration Fix

## 🚨 Issues Found & Solutions

### Issue 1: Wrong API Endpoint ❌
**Current:** Flutter app calls `http://10.0.2.2:8001//api/users/login/` (direct user service)
**Fix:** Change to `http://10.0.2.2:8000/api/users/login/` (unified API Gateway)

### Issue 2: Invalid Test Credentials ❌
**Current:** Flutter app tries `test@example.com` with `testpass123`
**Fix:** Use valid credentials created for testing

## ✅ Valid Test Credentials

### Job Seeker Test Account
- **Email:** `flutter@test.com`
- **Password:** `testpass123`
- **User Type:** `job_seeker`

### Alternative Test Account  
- **Email:** `test@example.com`
- **Password:** `testpass123` (password reset)
- **User Type:** `job_seeker`

## 🔧 Flutter Configuration Changes Needed

### 1. Update API Base URL
Change your Flutter app's API configuration from:
```dart
// ❌ WRONG - Direct service URL
baseUrl: 'http://10.0.2.2:8001/'

// ✅ CORRECT - Unified API Gateway  
baseUrl: 'http://10.0.2.2:8000/'
```

### 2. Remove Duplicate Slashes
Your logs show `http://10.0.2.2:8001//api/users/login/` (note the double slash)
Ensure your URL building doesn't create double slashes.

### 3. Use Valid Test Credentials
For testing, use these valid credentials:
```dart
// ✅ Valid test credentials
email: 'flutter@test.com'
password: 'testpass123'
```

## 📍 Android Emulator Network Notes

- `10.0.2.2` is the correct IP for Android emulator to access host `localhost`
- Port `8000` is the unified API Gateway (correct)
- Port `8001` is direct user service (bypass gateway - wrong for production)

## 🧪 Test the Fix

Once you update your Flutter app configuration:

1. **Login should work** with `flutter@test.com` / `testpass123`
2. **All API calls** should go through port `8000` (API Gateway)
3. **CORS headers** are configured for cross-origin requests
4. **JWT tokens** will be returned on successful login

## 🔍 Verification Commands

Test the endpoint manually to verify it works:

```bash
# Test login endpoint through API Gateway
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "flutter@test.com", "password": "testpass123"}'

# Should return:
# {"message":"Login successful","user":{...},"tokens":{...}}
```

## 📱 Expected Flutter Changes

Update these files in your Flutter app:

1. **API Configuration** - Change base URL to port 8000
2. **Network Service** - Fix double slash issue  
3. **Test Data** - Use valid credentials for testing

## ✅ Verification Checklist

- [ ] Change API base URL from port 8001 to 8000
- [ ] Fix double slash in URL construction  
- [ ] Use valid test credentials: `flutter@test.com` / `testpass123`
- [ ] Test login functionality
- [ ] Verify JWT token is received
- [ ] Confirm all API calls go through unified gateway

**🎯 After these changes, your Flutter app login should work successfully!**
