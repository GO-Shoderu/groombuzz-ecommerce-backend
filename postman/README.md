# GroomBuzz API – Postman Testing & Documentation Guide

This document explains in detail how to test the GroomBuzz API using Postman.
It covers:

- Authentication (JWT login + refresh)
- Catalog endpoints (Categories, Businesses, Services)
- Transactions (Bookings, Payments)
- Engagement (Reviews, Messages)
- Validation scenarios
- Expected responses
- Common errors and troubleshooting

---

# 1 Prerequisites

## A. Start the API

```bash
cd backend
python manage.py runserver
```

API Base URL:

```
http://127.0.0.1:8000
```

---

## B. Seed the Database (Recommended)

If the database is empty, run:

```bash
cd backend
python manage.py seed --reset
```

This creates:
- Owners (owner1, owner2)
- Clients (client1, client2)
- Categories
- Businesses
- Services
- Bookings
- Payments
- Messages
- Reviews

---

# 2 Postman Setup

## Create Environment

Create an environment called **GroomBuzz Local** with:

| Variable        | Value                    |
|---------------|--------------------------|
| base_url      | http://127.0.0.1:8000    |
| access_token  |                          |
| refresh_token |                          |

---

# 3 IMPORTANT – Authentication Flow

⚠️ JWT access tokens expire.

Before testing protected endpoints, always:

1. Run **Auth → Token (Login)**
2. Then test other endpoints

If you get `401 Unauthorized`, your token likely expired.

Fix:
- Run **Refresh Token**, OR
- Run **Login** again

---

# 4 Test Users (Seeded)

| Role   | Username | Password   |
|--------|----------|------------|
| Owner  | owner1   | Pass1234!  |
| Owner  | owner2   | Pass1234!  |
| Client | client1  | Pass1234!  |
| Client | client2  | Pass1234!  |

---

# 5 AUTH TESTS

## 🔐 Login (Get Token)

POST
```
{{base_url}}/api/auth/token/
```

Body:
```json
{
  "username": "client1",
  "password": "Pass1234!"
}
```

Expected Response (200 OK):
```json
{
  "access": "<JWT_ACCESS_TOKEN>",
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```

---

## Refresh Token

POST
```
{{base_url}}/api/auth/token/refresh/
```

Body:
```json
{
  "refresh": "{{refresh_token}}"
}
```

Expected Response (200 OK):
```json
{
  "access": "<NEW_ACCESS_TOKEN>"
}
```

---

# 6 CATALOG TESTS

## 📂 List Categories (Public)

GET
```
{{base_url}}/api/categories/
```

Expected: 200 OK
Returns list of categories.

---

## 🏢 List Businesses (Public)

GET
```
{{base_url}}/api/businesses/
```

Expected: 200 OK
Returns list of businesses.

---

## 💇 List Services (Public)

GET
```
{{base_url}}/api/services/
```

Expected: 200 OK (Paginated)

Example Response:
```json
{
  "count": 20,
  "next": "...",
  "previous": null,
  "results": [ ... ]
}
```

---

## 🔍 Filter Services by Category

GET
```
{{base_url}}/api/services/?category=1
```

Expected: 200 OK
Only services under category id 1.

---

## 📊 Sort Services by Price

GET
```
{{base_url}}/api/services/?ordering=price
```

Expected: 200 OK
Sorted lowest → highest.

---

## ❌ Validation Test – Negative Price

POST
```
{{base_url}}/api/services/
```

Body:
```json
{
  "business": 1,
  "category": 1,
  "name": "Bad Service",
  "price": -10,
  "currency": "ZAR",
  "is_available": true
}
```

Expected: 400 Bad Request
```json
{
  "price": [
    "Ensure this value is greater than or equal to 0.01."
  ]
}
```

---

# 7️⃣ TRANSACTIONS TESTS

## 📅 List Bookings

GET
```
{{base_url}}/api/bookings/
```

Expected: 200 OK
Clients see their bookings.
Owners see bookings for their services.

---

## ➕ Create Booking

POST
```
{{base_url}}/api/bookings/
```

Body:
```json
{
  "service": 1,
  "scheduled_at": "2026-03-01T10:00:00Z",
  "status": "pending"
}
```

Expected: 201 Created

---

## ❌ Validation – Booking in Past

Expected: 400 Bad Request
```json
{
  "scheduled_at": [
    "scheduled_at must be in the future."
  ]
}
```

---

## 💳 Create Payment

POST
```
{{base_url}}/api/payments/
```

Body:
```json
{
  "booking": 1,
  "amount": 200,
  "payment_status": "completed",
  "payment_method": "card"
}
```

Expected: 201 Created

Auto sets:
```json
"payment_date": "2026-02-15T11:23:45.123456Z"
```

---

## ❌ Validation – Invalid Payment Amount

Expected: 400 Bad Request
```json
{
  "amount": [
    "Ensure this value is greater than or equal to 0.01."
  ]
}
```

---

# 8️⃣ ENGAGEMENT TESTS

## 💬 List Messages

GET
```
{{base_url}}/api/messages/
```

Expected: 200 OK
Only messages where user is sender or recipient.

---

## ✉️ Create Message

POST
```
{{base_url}}/api/messages/
```

Body:
```json
{
  "recipient": 1,
  "business": 1,
  "message_body": "Hi, do you have availability tomorrow?"
}
```

Expected: 201 Created
Sender is auto-set.

---

## ⭐ Create Review (Completed Booking Only)

POST
```
{{base_url}}/api/reviews/
```

Body:
```json
{
  "booking": 1,
  "rating": 5,
  "comment": "Great service!"
}
```

Expected: 201 Created

If booking not completed:
400 Bad Request

If booking already reviewed:
400 Bad Request

---

# 9️⃣ Common Errors

## 401 Unauthorized
Token expired.
Run Login or Refresh.

## Invalid pk "X" does not exist
Referenced object ID does not exist.
Run GET endpoint first to retrieve valid IDs.

---

# 🔟 Exporting Collection

1. Postman → Collection → Export
2. Choose Collection v2.1
3. Save as:

```
postman/groombuzz.postman_collection.json
```

---

# ✅ Final Notes

- Always login first.
- Use seeded accounts for consistent testing.
- Validate negative scenarios.
- Re-run seed if data becomes inconsistent.

This ensures GroomBuzz API is fully tested and presentation-ready.

