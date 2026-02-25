# Payement_Sim

> A production-grade backend simulation of a payment gateway built with Django, DRF, Docker, PostgreSQL, Redis, and Celery.

This project replicates real-world backend architecture used by payment providers like **Stripe, Razorpay, and PayPal**.

---

# 🚀 Live Features

## Core Payment System

- ✅ Merchant onboarding system
- ✅ Secure API key authentication
- ✅ Payment creation API
- ✅ Payment listing API
- ✅ Payment detail API
- ✅ Payment lifecycle management
- ✅ Idempotency protection
- ✅ Webhook system
- ✅ Async event processing using Celery

---

# 🏗 Architecture Overview

```
Client (Postman / Frontend)
        │
        ▼
Django REST API (Docker)
        │
        ├── PostgreSQL (Database)
        │
        ├── Redis (Message Broker)
        │
        └── Celery Worker (Async Tasks)
                │
                └── Webhook delivery
```

---

# 🧰 Tech Stack

## Backend

- Python 3.11
- Django 5
- Django REST Framework

## Database

- PostgreSQL

## Async Processing

- Celery
- Redis

## Infrastructure

- Docker
- Docker Compose

---

# 📁 Project Structure

```
Payement_Sim/

backend/
│
├── core/
│   ├── manage.py
│   │
│   ├── core/
│   │   ├── settings/
│   │   ├── urls.py
│   │   ├── celery_app.py
│   │
│   └── apps/
│       ├── merchants/
│       │   ├── models.py
│       │   ├── authentication.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │
│       └── payments/
│           ├── models.py
│           ├── serializers.py
│           ├── views.py
│           ├── tasks.py
│
├── docker/
├── docker-compose.yml
├── .env
└── README.md
```

---

# 🔐 Authentication System

Uses **secret-key based authentication**, similar to Stripe.

## Request Header

```
Authorization: Bearer sk_xxxxxxxxxxxxx
```

Authentication flow:

1. Extract secret key
2. Validate merchant
3. Attach merchant to request

---

# 💰 Payment Lifecycle

```
pending → success
pending → failed
```

All payments start in:

```
pending
```

---

# 🧠 Idempotency System

Prevents duplicate payments.

Client sends:

```
Idempotency-Key: unique-key
```

Same key → Same payment returned.

---

# 🔔 Webhook System

Async webhook delivery using Celery.

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

---

# 🌐 API Endpoints

Base URL:

```
http://localhost:8000/api/
```

---

## Merchant API

### Get merchant info

```
GET /api/merchants/me/
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

### Payment detail

```
GET /api/payments/{id}/
```

---

### Update payment status

```
PATCH /api/payments/{id}/status/
```

---

# ⚙️ Installation

## Clone repository

```
git clone https://github.com/YOUR_USERNAME/Payement_Sim.git
```

---

## Setup environment

Create `.env`

```
SECRET_KEY=dev-secret
DEBUG=True

DATABASE_URL=postgres://pguser:pgpass@db:5432/pgateway
REDIS_URL=redis://redis:6379/0
```

---

## Start services

```
docker compose up --build
```

---

# 🧪 Testing

Use Postman.

Example:

```
POST /api/payments/
```

Headers:

```
Authorization: Bearer sk_xxxx
Idempotency-Key: test123
```

---

# 🗄 Database Access

```
docker compose exec db psql -U pguser -d pgateway
```

---

# 🧱 Production Concepts Implemented

- API authentication
- Payment lifecycle
- Idempotency
- Async processing
- Webhooks
- Dockerized backend
- Background workers
- Merchant isolation

---

# 📈 Skills Demonstrated

- Production Django architecture
- Dockerized backend
- REST API design
- PostgreSQL integration
- Async processing with Celery
- Secure authentication systems

---

# 🧭 Roadmap

Upcoming features:

- Payment processing simulation
- Rate limiting
- API scopes
- Production deployment
- Monitoring

---

# 👨‍💻 Author

Nishant Sinha

Backend Developer

---

# ⭐ If you like this project

Give it a star on GitHub ⭐

---

# 📜 License

Open-source for learning and portfolio use.
