# API Documentation

Base URL:

http://127.0.0.1:8000

---

## Authentication

### Register

**POST**

`/auth/register`

Creates a new user account.

Request:

```json
{
  "email": "user@example.com",
  "password": "123456",
  "full_name": "Mohamed Ayman"
}