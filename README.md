# Payment_Sim (Django + DRF + Docker + Postgres + Redis + Celery)

A production‑grade backend simulation of a payment gateway built using Django, Django REST Framework, Docker, PostgreSQL, Redis, and Celery.

This project demonstrates real‑world backend architecture and patterns used by payment providers like Stripe, Razorpay, and PayPal.

---

# Features Implemented

## Core Features

- Merchant system with secure API keys
- Secret‑key based authentication
- Payment creation API
- Payment listing API
- Payment detail API
- Payment status lifecycle management
- Idempotency protection (prevents duplicate payments)
- Webhook system for event notifications

## Infrastructure

- Dockerized environment
- PostgreSQL database
- Redis message broker
- Celery async worker
- Environment‑based configuration

## Security Features

- Merchant isolation
- Secret key authentication
- Idempotency keys
- Scoped database access

---

# Tech Stack

Backend:

- Python 3.11
- Django 5
- Django REST Framework

Database:

- PostgreSQL

Async Processing:

- Celery
- Redis

DevOps:

- Docker
- Docker Compose

---

# Project Structure

```
Payement_Sim/
│
├── backend/
│   ├── requirements.txt
│   └── core/
│       ├── manage.py
│       ├── core/
│       │   ├── settings/
│       │   ├── urls.py
│       │   ├── celery_app.py
│       │
│       └── apps/
│           ├── merchants/
│           │   ├── models.py
│           │   ├── authentication.py
│           │   ├── views.py
│           │   ├── serializers.py
│           │
│           └── payments/
│               ├── models.py
│               ├── views.py
│               ├── serializers.py
│               ├── tasks.py
│
├── docker/
│   └── django/
│       └── Dockerfile
│
├── docker-compose.yml
├── .env
└── README.md
```

---

# Database Models

## Merchant

Represents a merchant using the payment gateway.

Fields:

- id (UUID)
- name
- email
- public_key
- secret_key
- webhook_url
- is_active
- created_at

## Payment

Represents a payment created by merchant.

Fields:

- id (UUID)
- merchant
- amount
- currency
- status
- created_at

Status lifecycle:

```
pending → success
pending → failed
```

## IdempotencyKey

Prevents duplicate payments.

Fields:

- key
- merchant
- payment
- created_at

---

# Authentication System

Uses secret key authentication.

Header format:

```
Authorization: Bearer sk_xxxxxxxxx
```

Authentication flow:

- Extract secret key
- Find merchant
- Attach merchant to request

---

# API Endpoints

Base URL:

```
http://localhost:8000/api/
```

---

## Merchant APIs

### Get merchant info

```
GET /api/merchants/me/
```

Header:

```
Authorization: Bearer sk_xxxx
```

---

## Payment APIs

### Create payment

```
POST /api/payments/
```

Headers:

```
Authorization: Bearer sk_xxxx
Idempotency-Key: unique-key
```

Body:

```
{
  "amount": 10000,
  "currency": "INR"
}
```

---

### List payments

```
GET /api/payments/list/
```

---

### Get payment detail

```
GET /api/payments/{payment_id}/
```

---

### Update payment status

```
PATCH /api/payments/{payment_id}/status/
```

Body:

```
{
  "status": "success"
}
```

---

# Webhook System

Merchants can configure webhook URL.

When payment status updates, webhook is sent.

Example webhook payload:

```
{
  "event": "payment.success",
  "payment_id": "uuid",
  "amount": 10000,
  "currency": "INR",
  "status": "success"
}
```

Webhook delivery handled by Celery worker.

---

# Idempotency System

Prevents duplicate payment creation.

Client sends:

```
Idempotency-Key: unique-key
```

Same key returns same payment.

---

# Environment Variables

File: `.env`

Example:

```
SECRET_KEY=dev-secret
DEBUG=True

DATABASE_URL=postgres://pguser:pgpass@db:5432/pgateway

REDIS_URL=redis://redis:6379/0
```

---

# Running the Project

## Start containers

```
docker compose up --build
```

Services started:

- Django API
- PostgreSQL
- Redis
- Celery worker

## Access admin

```
http://localhost:8000/admin/
```

---

# Access Database

Connect via Docker:

```
docker compose exec db psql -U pguser -d pgateway
```

---

# Testing using Postman

Example request:

POST /api/payments/

Headers:

```
Authorization: Bearer sk_xxxx
Idempotency-Key: test123
```

Body:

```
{
  "amount": 10000,
  "currency": "INR"
}
```

---

# Production Concepts Implemented

This project implements real‑world backend concepts:

- Authentication system
- API security
- Database relationships
- Idempotency
- Async processing
- Webhooks
- Docker infrastructure
- Background jobs

---

# Learning Goals Achieved

This project teaches:

- Production Django architecture
- Class‑based views
- DRF authentication
- Dockerized backend
- PostgreSQL integration
- Celery async tasks
- Payment system design

---

# Next Planned Features

- Payment processing simulation
- API rate limiting
- API key scopes
- Logging system
- Production deployment

---

# Author

Nishant Sinha

Backend Developer Project

---

# License

Open source for learning purposes.
