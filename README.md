# Private Tutor Finder — Backend

The API behind Private Tutor Finder, a platform that connects students and parents with private tutors.

Clients (a student, or a parent looking on behalf of their child) post what they need — the class level, where the lessons should happen, a short description — and tutors browse those posts and build a profile that clients can look through.

This repository is the backend only. It's built with **FastAPI**, **SQLAlchemy 2**, **Alembic** and **PostgreSQL**, and uses **JWT** for authentication.

---

## What it can do so far

- **Accounts** — sign up as a client or a tutor, log in, and get a JWT token. Admin accounts can't be created through sign-up.
- **Profiles** — after signing up, each client or tutor creates their profile (school and location for clients; workplace, degree, experience level and a short summary for tutors).
- **Class levels** — KG1 to Grade 12 plus University, each grouped automatically into Preschool, Elementary, Intermediate, Secondary or Higher Education.
- **Client posts** — clients publish what they're looking for, including where the lessons should take place (at their home, at the tutor's, or either). They can edit, deactivate or delete their own posts.
- **Permissions** — every endpoint checks who you are and what role you have. Clients can only touch their own data, and a client's private profile is visible to admins only.

---

## Getting started

### What you need

- Python 3.13
- PostgreSQL (any recent version)

### 1. Get the code and install dependencies

```bash
git clone https://github.com/ahmadarmoush11/Private-Tutor-Finder-Backend.git
cd Private-Tutor-Finder-Backend/backend

python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Then install the packages:

```bash
pip install -r requirements.txt
```

### 2. Create the database

Create an empty PostgreSQL database, for example `PrivateTutorFinder`, using pgAdmin or psql:

```sql
CREATE DATABASE "PrivateTutorFinder";
```

### 3. Set up your `.env` file

Copy the example file and fill it in:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

| Setting | What it's for |
|---|---|
| `DATABASE_URL` | Connection string to your PostgreSQL database. |
| `JWT_SECRET_KEY` | The secret used to sign login tokens. Keep it private — anyone who has it can create valid tokens. |
| `JWT_ALGORITHM` | Signing algorithm. Leave it as `HS256`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | How long a login stays valid. Defaults to 60. |
| `API_PREFIX` | Optional. The prefix in front of every endpoint. Defaults to `/api/v1`. |

To generate a strong secret key, run this once and paste the result into `JWT_SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Use a different key for every environment (your machine, staging, production).

### 4. Create the tables

```bash
alembic upgrade head
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

That's it. Open **http://localhost:8000/docs** to explore and try the API.

---

## Using the API

Every endpoint lives under **`/api/v1`**, for example `POST /api/v1/auth/login`.

The interactive docs at `/docs` list every endpoint with its request and response format, and they're always up to date with the code — so that's the place to look rather than this file.

To call protected endpoints from the docs:

1. Call `POST /api/v1/auth/login` with an email and password.
2. Copy the `access_token` from the response.
3. Click **Authorize** at the top of the page and paste the token (without the word `Bearer`).

From your own frontend or Postman, send the token as a header:

```
Authorization: Bearer <your token>
```

### Errors

Every error comes back in the same shape, so the frontend can handle them in one place:

```json
{
  "error": {
    "code": "POST_NOT_FOUND",
    "message": "Post not found"
  }
}
```

Validation errors also include a `details` list telling you which field was wrong and why.

---

## Seed data

When the server starts, it fills in anything that's missing — it never duplicates rows, so restarting is always safe:

- **Class levels** — KG1–KG3, Grade 1–12 and University.
- **Development accounts**, so you can log in straight away:

| Role | Email | Password |
|---|---|---|
| Admin | `admin@tutorfinder.com` | `ahmad200317@` |
| Client | `client@tutorfinder.com` | `ahmad200317@` |
| Tutor | `tutor@tutorfinder.com` | `ahmad200317@` |

> ⚠️ **These accounts are for development only.** The password is written in the code, so anyone who reads it can log in as admin. Turn this seed off or change the password before deploying anywhere real.

You can also run the seeds by hand:

```bash
python -m app.db.seeds.run
```

---

## How the project is organised

The code is grouped **by feature**: everything about tutor profiles lives in one folder, everything about posts in another, and so on.

```
backend/
├── alembic/                  database migrations
├── app/
│   ├── main.py               creates the app, runs seeds on startup
│   ├── api/router.py         plugs every feature's router in under /api/v1
│   ├── core/                 settings, security (passwords, JWT), errors
│   ├── db/                   database session, unit of work, model registry, seeds
│   ├── shared/               small helpers used by several features
│   └── features/
│       ├── auth/             sign up, log in, current user, role checks
│       ├── users/
│       ├── client_profiles/
│       ├── tutor_profiles/
│       ├── class_levels/
│       └── client_posts/
└── requirements.txt
```

Inside a feature folder you'll usually find the same files:

| File | Its job |
|---|---|
| `model.py` | The database table. |
| `schemas.py` | What the API accepts and returns. |
| `repository.py` | Reads and writes the database. Nothing else talks to the database directly. |
| `service.py` | The business rules — who can do what, what has to exist first. |
| `dependencies.py` | Wires the repository and service together for FastAPI. |
| `router.py` | The HTTP endpoints. Kept thin: they just call the service. |

---

## Conventions

A few rules that keep the code predictable as it grows:

- **Repositories never commit.** They only stage changes (`flush`). Services decide when work is final by wrapping their writes in `with self.uow:` — if anything inside fails, everything inside is rolled back together.
- **Services raise errors from `app/core/exceptions.py`** (for example `PostNotFoundError`). They never build HTTP responses — the error handlers do that.
- **Routes check roles with type hints**: `current_user: ClientUser`, `TutorUser`, `AdminUser`, or `CurrentUser` for any logged-in user.
- **The JWT only holds the user id and role.** Everything else is loaded from the database on each request, so it's never stale.

### Adding a new feature

1. Create `app/features/<feature_name>/` with the files above.
2. Add the model to `app/db/models.py` so Alembic can see it.
3. Add the router to `app/api/router.py`.
4. Add any new errors to `app/core/exceptions.py`.
5. Create a migration (see below).

---

## Database migrations

After changing a model, generate a migration, check it, then apply it:

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

Always open the generated file and read it before applying. One known trap: **when you add a new enum column to an existing table, Alembic doesn't create the PostgreSQL enum type**, so the migration fails. In that case write the migration by hand and create the type first. `alembic/versions/7c4e2a9b1f30_add_lesson_location_to_client_posts.py` is a working example to copy from.

To undo the last migration:

```bash
alembic downgrade -1
```

---

## What's next

Things planned or worth adding as the project grows:

- Automated tests with pytest
- Docker setup (run `alembic upgrade head` before starting the server)
- Searching and filtering tutors and posts, with pagination
- Refresh tokens, email verification and password reset
- Bookings between clients and tutors
