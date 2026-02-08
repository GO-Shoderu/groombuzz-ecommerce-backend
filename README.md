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


