# 🛡️ InsecureGram: A Deliberately Vulnerable FastAPI API

Welcome to InsecureGram — a deliberately insecure RESTful API built using FastAPI to demonstrate real-world web application vulnerabilities, based on the [OWASP Top 10](https://owasp.org/www-project-top-ten/). It is meant for educational and research purposes only.

> ⚠️ This project is intentionally insecure. Do not deploy this in a production environment.

---

## 📦 Project Overview

This API mimics a realistic backend service similar to a social media app. It includes endpoints for:

- User registration and login with JWT
- User profiles and search
- Command execution
- File upload
- SSRF simulation
- External API interaction
- Legacy and admin routes

---

## 📁 Project Structure

```
InsecureGram/
│
├── app/
│   ├── main.py                  # FastAPI app initialization
│   ├── database.py              # SQLite DB setup and session handling
│   ├── models.py                # SQLAlchemy User model
│   ├── config.py                # Global config and JWT secret key
│   ├── dependencies.py          # Shared auth logic (get_current_user)
│   ├── routers/
│   │   ├── auth.py              # Login and registration endpoints
│   │   ├── users.py             # Search, profiles, legacy access
│   │   ├── upload.py            # File upload (unsafe mode)
│   │   ├── exec.py              # Remote command execution (RCE)
│   │   ├── proxy.py             # SSRF endpoint
│   │   ├── admin.py             # Admin-only data access
│   │   └── external.py          # External request simulation
│   ├── ssrf_target.py           # SSRF internal FastAPI server (optional)
│
├── static/uploads/              # Uploaded files
├── test.db                      # SQLite DB (created at runtime)
├── Dockerfile                   # Docker config
├── docker-compose.yml           # Compose config
├── README.md                    # You are here
```

---

## 🚨 Vulnerabilities Covered

This project contains examples of the following vulnerabilities:

| ID   | Category                     | Description |
|------|------------------------------|-------------|
| V1   | Broken Authentication        | Weak JWT management and no refresh logic |
| V2   | Sensitive Data Exposure      | Hardcoded secrets, leaked files |
| V3   | SQL Injection                | Raw query fallback in `/users/search` |
| V4   | Broken Access Control        | Users can access others' data |
| V5   | Security Misconfiguration    | SSRF, unrestricted internal access |
| V6   | Insecure Deserialization     | Arbitrary file upload with octet-stream |
| V7   | Using Components with Known Vulns | No dependency control |
| V8   | Insufficient Logging & Monitoring | No request audit logging |
| V9   | Remote Code Execution        | Via `/cmd/exec` route |
| V10  | SSRF                         | `/proxy` endpoint accesses arbitrary URLs |
| V11  | Insecure File Upload         | Unsafe flag allows overwrite |
| V12  | Open CORS Policy             | Missing origin validation allows API access from external domains |
| V13  | JWT Tampering                | JWT creation using exposed secret key |

---

## 🔐 JWT Example

### JWT Creation:
```python
from jose import jwt
token = jwt.encode({"sub": "alice", "is_admin": False}, "mysecret", algorithm="HS256")
```

### JWT Header (for curl):
```bash
-H "Authorization: Bearer <your_jwt_here>"
```

---

## 🧪 Example Endpoints and Test Commands

Here’s how you can interact with the API using `curl`:

### 🟢 Auth

🔐 Register
```bash
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" \
-d '{"username": "alice", "password": "alice123"}'
```

🔐 Login
```bash
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" \
-d '{"username": "alice", "password": "alice123"}'
```

---

### 🔎 User Search (SQLi vulnerable)
```bash
curl -G http://localhost:8000/users/search \
-H "Authorization: Bearer <JWT>" \
--data-urlencode "field=username" --data-urlencode "keyword=' OR 1=1 --"
```

---

### 📁 File Upload (Unsafe mode)
```bash
curl -X POST http://localhost:8000/upload?unsafe=true \
-F "file=@evil.py" \
-H "Authorization: Bearer <JWT>"
```

---

### 💣 Remote Command Execution (RCE)
```bash
curl -G http://localhost:8000/cmd/exec \
-H "Authorization: Bearer <JWT>" \
--data-urlencode "cmd=id"
```

---

### 🛰️ SSRF
```bash
curl -G http://localhost:8000/proxy \
-H "Authorization: Bearer <JWT>" \
--data-urlencode "url=http://127.0.0.1:8081/read?name=/etc/passwd"
```

---

### 🗂️ Admin Access (with API key)
```bash
curl -H "Authorization: Bearer <JWT>" \
-H "X-API-KEY: admin123" \
http://localhost:8000/admin/users
```

---

### 📡 Legacy API Endpoint
```bash
curl http://localhost:8000/v1/users/info
```

---

## 🐳 Running with Docker Compose

```bash
docker-compose up --build
```

This runs:
- `app`: The vulnerable API at http://localhost:8000
- `ssrf_target`: Internal server for SSRF testing at http://localhost:8081

---

## 🚫 Disclaimer

This project is for educational purposes only. Do not use it against real-world services or expose it publicly. You are fully responsible for any misuse.

---

## ✅ Credits

- Built using FastAPI + SQLAlchemy
- Inspired by OWASP Top 10
- Maintained by the security research community

---

## 💡 Contribution Ideas

- Add logging for audit
- Sanitize file uploads
- Parameterize raw SQL queries
- Improve CORS policy
- Add unit tests
