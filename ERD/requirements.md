# ERD Requirements
Designing an Entity–Relationship Diagram (ERD) for **GroomBuzz**, a two-sided service discovery and booking platform that supports users (clients/business owners/admin), business profiles, service listings, bookings, payments, reviews, and messaging. The ERD identifies entities, attributes, and relationships with clear cardinalities.

---

## Entities & Attributes

### User
- user_id (PK, UUID)
- first_name (TEXT, NOT NULL)
- last_name (TEXT, NOT NULL)
- email (TEXT, UNIQUE, NOT NULL)
- password_hash (TEXT, NOT NULL)
- phone_number (TEXT, NULL)
- role (ENUM: client | owner | admin, NOT NULL)
- is_active (BOOLEAN, DEFAULT true)
- created_at (TIMESTAMP, DEFAULT current timestamp)

### Business
- business_id (PK, UUID)
- owner_id (FK → User.user_id)
- name (TEXT, NOT NULL)
- description (TEXT, NULL)
- phone_number (TEXT, NULL)
- address (TEXT, NULL)
- city (TEXT, NULL)
- area (TEXT, NULL)
- rating_avg (DECIMAL(3,2), NULL)
- is_active (BOOLEAN, DEFAULT true)
- created_at (TIMESTAMP, DEFAULT current timestamp)
- updated_at (TIMESTAMP, auto-update)

### Category
- category_id (PK, UUID)
- name (TEXT, UNIQUE, NOT NULL)
- slug (TEXT, UNIQUE, NOT NULL)
- description (TEXT, NULL)
- is_active (BOOLEAN, DEFAULT true)
- created_at (TIMESTAMP, DEFAULT current timestamp)

### Service
- service_id (PK, UUID)
- business_id (FK → Business.business_id)
- category_id (FK → Category.category_id)
- name (TEXT, NOT NULL)
- description (TEXT, NULL)
- price (DECIMAL(10,2), NOT NULL)
- currency (TEXT, DEFAULT 'ZAR')
- duration_minutes (INT, NULL)
- is_available (BOOLEAN, DEFAULT true)
- created_at (TIMESTAMP, DEFAULT current timestamp)
- updated_at (TIMESTAMP, auto-update)


