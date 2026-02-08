# GroomBuzz E-Commerce Backend (Project Nexus)

## Overview
GroomBuzz is a **service discovery and listing platform** that connects clients to grooming and self-care services. Similar to property listing or ride-hailing platforms, GroomBuzz allows users to **search, browse, and discover services** based on their needs, while service offerings are organized into structured listings.

This project is a **production-style backend** for GroomBuzz, focusing on a robust **catalog system** that supports managing categories and items (services/products), secure user authentication, and efficient discovery features such as **filtering, sorting, and pagination**.

The implementation is designed for seamless frontend integration.

---

## Tech Stack
- **Python / Django / Django REST Framework** — RESTful API development
- **PostgreSQL** — relational database design and optimization
- **JWT Authentication** — secure, stateless API access
- **Postman** — API documentation and testing
- **Docker** — containerized deployment
- **CI/CD (GitHub Actions)** — automated workflows

---

## Core Features (MVP)

### 1) Authentication
- User authentication using JWT (login & token refresh)
- Protected endpoints for authorized access

### 2) Catalog Management (CRUD)
- Create, read, update, and delete **Categories**  
  (e.g., Barbershop, Nail Salon, Skincare, Massage)
- Create, read, update, and delete **Items**  
  (services or products listed under categories)

### 3) Service Discovery
- Filter services by category
- Sort results (e.g., by price)
- Paginated responses for large datasets

---

## Planned API Endpoints

### Authentication
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`

### Categories
- `GET /api/categories/`
- `POST /api/categories/`
- `GET /api/categories/{id}/`
- `PUT/PATCH /api/categories/{id}/`
- `DELETE /api/categories/{id}/`

### Items (Services / Products)
- `GET /api/items/`
- `POST /api/items/`
- `GET /api/items/{id}/`
- `PUT/PATCH /api/items/{id}/`
- `DELETE /api/items/{id}/`

Filtering / Sorting / Pagination example:
- `/api/items/?category=<id>&ordering=price&page=1`

---

## Database & Performance
- Relational schema with well-defined foreign key relationships
- Database indexing for frequent queries (category, price, created_at)
- ORM optimizations using `select_related()` and `prefetch_related()`
- Pagination to limit query load and improve response times

---

## API Documentation
All endpoints will be documented using **Postman**, providing:
- Clear request and response examples
- Reusable collections for frontend integration
- Easy testing and validation of API behavior

---

## Roadmap
1. Initialize Django project and PostgreSQL configuration
2. Implement JWT authentication
3. Create Category and Item models
4. Build CRUD APIs
5. Add filtering, sorting, and pagination
6. Document APIs using Postman
7. Containerize with Docker and deploy
8. Add CI/CD checks

---

## Collaboration
This backend is designed to be consumed by a frontend application.
