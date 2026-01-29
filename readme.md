# 🏋️ Gym Ecosystem Backend

A **multi-tenant SaaS backend** for gym owners, trainers, staff, and fitness members — built to power a **full fitness ecosystem** under a single platform with **subdomain-based gym personalization**.

---

## 📌 Vision

To build a **unified digital ecosystem for fitness**, where:

- Gym owners manage everything from one place
- Members get a seamless fitness experience
- Trainers & staff operate within a structured system
- The platform scales to thousands of gyms using one backend

---

## 🧠 What This Backend Powers

### Gym Owners
- Gym profile & branding
- Member management
- Trainer & staff management
- Subscription plans
- Payments & billing
- Gym-level configurations
- Personalized gym website

### Members (Customers)
- Gym access
- Memberships & subscriptions
- Payments
- Assigned trainers
- Ecosystem services

### Trainers & Staff
- Assigned members
- Roles & permissions
- Gym-specific access

### Platform Admin
- Gym onboarding
- Global plans
- Platform analytics
- Policy enforcement

---

## 🌐 Domain & Subdomain Architecture

| Type | Example |
|----|--------|
| Main Platform | `platform.com` |
| Gym Dashboard | `goldsgym.platform.com` |
| Gym Public Website | `goldsgym.platform.com/home` |
| Admin Panel | `admin.platform.com` |
| Backend API | `api.platform.com` |

Each gym operates as an **isolated tenant** using its **subdomain**.

---

## 🧩 Core Architecture

- **Multi-tenant SaaS**
- **Subdomain-based tenant resolution**
- **Shared backend, isolated data**
- **Role-Based Access Control (RBAC)**
- **Modular & scalable structure**

---

## 🧠 Tenancy Model

- One gym = one tenant
- Tenant identified using:
  - Subdomain (`req.hostname`)
  - Tenant ID mapped internally
- Logical data isolation using `tenantId`

---

## 👥 User Roles

- `SUPER_ADMIN`
- `GYM_OWNER`
- `TRAINER`
- `STAFF`
- `MEMBER`

Permissions are enforced via RBAC middleware.

---

## 🏗️ Tech Stack (Planned)

- **Runtime:** Node.js
- **Framework:** Express / Fastify / NestJS
- **Database:** MongoDB or PostgreSQL
- **ORM/ODM:** Prisma / Mongoose
- **Authentication:** JWT + Refresh Tokens
- **Payments:** Razorpay / Stripe
- **Storage:** AWS S3 / Cloudflare R2
- **Caching:** Redis
- **Realtime:** WebSockets (future)
- **Queues:** BullMQ / RabbitMQ (future)

---

## 📂 Project Structure