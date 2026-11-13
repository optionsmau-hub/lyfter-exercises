# Fruit Store API - Authorization Exercise

Flask API that extends the guided JWT authentication exercise with role-based
authorization (`admin` / `user`), a product CRUD, a purchase flow and an
invoice listing. All database access goes through SQLAlchemy (repository
pattern), no raw SQL. Tokens are signed with **RS256**.

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # on Windows
pip install -r requirements.txt
```

1. Generate the RSA key pair used to sign/verify tokens (creates
   `private_key.pem` and `public_key.pem`):

   ```bash
   python generate_keys.py
   ```

2. Seed the first admin user (public `/register` always creates a `user`,
   never an `admin`):

   ```bash
   python seed_admin.py
   ```

   This prints the admin credentials (`admin` / `admin123`). The database
   file `app.db` (SQLite) is created automatically the first time any script
   imports `db.py`.

3. Run the server:

   ```bash
   python app.py
   ```

   The API is available at `http://127.0.0.1:5000`.

## Password hashing

Like in the guided exercise, passwords are hashed client-side with **MD5**
before being sent to the API (`password_generator.py` can generate a hash
for any plaintext password to use in request bodies).

## Roles

| Role  | Access                                                                 |
|-------|-------------------------------------------------------------------------|
| admin | Every endpoint, including the product CRUD.                             |
| user  | `/register`, `/login`, `/me`, `/refresh`, purchasing products, `/invoices`. |

## Endpoints

| Endpoint                          | Method | Auth           | Description                                   |
|------------------------------------|--------|----------------|------------------------------------------------|
| `/liveness`                        | GET    | No             | Confirms the service is running.                |
| `/register`                        | POST   | No             | Creates a `user` and returns tokens.             |
| `/login`                           | POST   | No             | Validates credentials and returns tokens.        |
| `/me`                              | GET    | Any role       | Returns the authenticated user's data.           |
| `/refresh`                         | POST   | No (refresh token in body) | Returns a new token pair.      |
| `/products`                        | POST   | admin          | Creates a product.                               |
| `/products`                        | GET    | admin          | Lists all products.                              |
| `/products/<id>`                   | GET    | admin          | Gets a single product.                           |
| `/products/<id>`                   | PUT    | admin          | Updates a product.                               |
| `/products/<id>`                   | DELETE | admin          | Deletes a product.                               |
| `/products/<id>/purchase`          | POST   | Any role       | Buys a product, decreases stock, creates an invoice. |
| `/invoices`                        | GET    | Any role       | Lists the invoices of the authenticated user.    |

## Testing with curl

Replace `<ADMIN_TOKEN>` / `<USER_TOKEN>` with the `access_token` received
from `/login`.

```bash
# Health check
curl http://127.0.0.1:5000/liveness

# Login as admin (password hash for "admin123")
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"0192023a7bbd73250516f069df18b500"}'

# Register a regular user (password hash for "user12345")
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"80ec08504af83331911f5882349af59d"}'

# Who am I
curl http://127.0.0.1:5000/me -H "Authorization: Bearer <TOKEN>"

# Admin creates a product
curl -X POST http://127.0.0.1:5000/products \
  -H "Authorization: Bearer <ADMIN_TOKEN>" -H "Content-Type: application/json" \
  -d '{"name":"Banana","price":0.5,"entry_date":"2026-11-01","quantity":100}'

# A regular user trying the same -> 403 Forbidden
curl -X POST http://127.0.0.1:5000/products \
  -H "Authorization: Bearer <USER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"name":"Banana","price":0.5,"entry_date":"2026-11-01","quantity":100}'

# User buys 5 units of product 1
curl -X POST http://127.0.0.1:5000/products/1/purchase \
  -H "Authorization: Bearer <USER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"quantity":5}'

# User lists their own invoices
curl http://127.0.0.1:5000/invoices -H "Authorization: Bearer <USER_TOKEN>"

# No token -> 401
curl -i http://127.0.0.1:5000/me

# Nonexistent product -> 404
curl http://127.0.0.1:5000/products/999 -H "Authorization: Bearer <ADMIN_TOKEN>"

# Buying more than available stock -> 400
curl -X POST http://127.0.0.1:5000/products/1/purchase \
  -H "Authorization: Bearer <USER_TOKEN>" -H "Content-Type: application/json" \
  -d '{"quantity":999999}'
```

All of the above cases were manually verified while building this exercise
(401 missing/invalid token, 403 wrong role, 404 missing resource, 400 bad
input / insufficient stock, 200/201/204 on success).
