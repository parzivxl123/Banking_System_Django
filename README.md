# 🏦 Banking System API

A secure, full-featured banking backend built with **Django REST Framework** and **JWT authentication**. Supports account management, fund transfers, deposits, withdrawals, transaction history, and a full admin dashboard.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Guide](#authentication-guide)
- [Running Tests](#running-tests)
- [Roadmap](#roadmap)

---

## Features

| Area | Details |
|---|---|
| **Auth** | JWT access & refresh tokens, protected endpoints |
| **Users** | Register, update profile, hashed passwords, balance tracking |
| **Transfers** | Send money between users, self-transfer prevention, balance validation |
| **Deposits** | Deposit funds, full deposit history |
| **Withdrawals** | Withdraw funds, insufficient balance checks, withdrawal history |
| **Admin** | Django admin with search, filters, and full record management |
| **Testing** | Unit tests for users, auth flows, and transactions |

---

## Tech Stack

- **Runtime:** Python 3.x
- **Framework:** Django + Django REST Framework
- **Auth:** SimpleJWT
- **Database:** SQLite (development)
- **Testing:** Django TestCase
- **Tooling:** Postman, Git

---

## Project Structure

```
banking_project/
│
├── users/                  # User model, auth, deposits, withdrawals
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── transactions/           # Transfers and transaction history
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── banking_project/        # Django project settings
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd banking_project
```

### 2. Set up a virtual environment

```bash
python -m venv .venv
```

**Activate it:**

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.  
The admin panel is at `http://127.0.0.1:8000/admin/`.

---

## API Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login/` | Obtain access & refresh tokens |
| `POST` | `/refresh/` | Refresh an expired access token |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `GET` | `/users/` | Get current user details | ✅ |
| `POST` | `/users/` | Register a new user | ❌ |
| `PUT` | `/users/` | Update user details | ✅ |

### Transactions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/transactions/` | Transfer money to another user | ✅ |
| `GET` | `/transactions/history/` | View transaction history | ✅ |

### Deposits

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/users/deposit/` | Deposit funds into account | ✅ |
| `GET` | `/users/deposit/history/` | View deposit history | ✅ |

### Withdrawals

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/users/withdraw/` | Withdraw funds from account | ✅ |
| `GET` | `/users/withdraw/history/` | View withdrawal history | ✅ |

---

## Authentication Guide

### Step 1 — Login

```http
POST /login/
Content-Type: application/json

{
    "username": "john",
    "password": "John12345"
}
```

**Response:**

```json
{
    "refresh": "eyJ...",
    "access": "eyJ..."
}
```

### Step 2 — Use the token

Include the access token in the `Authorization` header on all protected requests:

```http
Authorization: Bearer eyJ...
```

### Step 3 — Refresh the token

When your access token expires, get a new one:

```http
POST /refresh/
Content-Type: application/json

{
    "refresh": "eyJ..."
}
```

---

## Running Tests

```bash
python manage.py test
```

Tests cover user creation, authentication flows, and transaction logic.

---

## Roadmap

- [x] Password reset via email
- [ ] Response pagination
- [ ] Docker support
- [ ] Rate limiting
- [ ] Structured logging
- [ ] Email notifications
- [ ] Expanded test coverage

---

## Author

**Parzival** — built with Django REST Framework.
