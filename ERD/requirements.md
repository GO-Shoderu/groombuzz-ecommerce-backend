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

### Booking
- booking_id (PK, UUID)
- service_id (FK → Service.service_id)
- client_id (FK → User.user_id)
- booking_date (DATE, NOT NULL)
- start_time (TIME, NOT NULL)
- status (ENUM: pending | confirmed | canceled | completed, NOT NULL)
- created_at (TIMESTAMP, DEFAULT current timestamp)

### Payment
- payment_id (PK, UUID)
- booking_id (FK → Booking.booking_id)
- amount (DECIMAL(10,2), NOT NULL)
- payment_date (TIMESTAMP, DEFAULT current timestamp)
- payment_method (ENUM: card | mobile_money | cash, NOT NULL)
- payment_status (ENUM: pending | completed | failed, NOT NULL)

### Review
- review_id (PK, UUID)
- booking_id (FK → Booking.booking_id)
- business_id (FK → Business.business_id)
- client_id (FK → User.user_id)
- rating (INT, CHECK 1–5, NOT NULL)
- comment (TEXT, NOT NULL)
- created_at (TIMESTAMP, DEFAULT current timestamp)

### Message
- message_id (PK, UUID)
- sender_id (FK → User.user_id)
- recipient_id (FK → User.user_id)
- business_id (FK → Business.business_id)
- message_body (TEXT, NOT NULL)
- sent_at (TIMESTAMP, DEFAULT current timestamp)

---

## Relationships & Cardinalities

| Relationship                              | Cardinality                         | FK Location                                          | Rationale |
| ----------------------------------------- | ----------------------------------- | --------------------------------------------------- | --------- |
| **User → Business (owns)**                | `User (1) —— (0..N) Business`       | `Business.owner_id → User.user_id`                   | A user may own zero or many businesses; each business has exactly one owner. |
| **Business → Service (lists/offers)**     | `Business (1) —— (0..N) Service`    | `Service.business_id → Business.business_id`         | A business can list zero or many services; each service belongs to one business. |
| **Category → Service (categorizes)**      | `Category (1) —— (0..N) Service`    | `Service.category_id → Category.category_id`         | A category can contain zero or many services; each service belongs to one category. |
| **User → Booking (makes)**                | `User (1) —— (0..N) Booking`        | `Booking.client_id → User.user_id`                   | A client can make zero or many bookings; each booking belongs to one client. |
| **Service → Booking (is booked)**         | `Service (1) —— (0..N) Booking`     | `Booking.service_id → Service.service_id`            | A service can be booked zero or many times; each booking is for one service. |
| **Booking → Payment (has)**               | `Booking (1) —— (1..N) Payment`     | `Payment.booking_id → Booking.booking_id`            | Every booking must have at least one payment; partial or split payments are allowed. |
| **Booking → Review (receives)**           | `Booking (1) —— (0..1) Review`      | `Review.booking_id → Booking.booking_id`             | A booking may have at most one review (after completion); each review relates to one booking. |
| **Business → Review (receives)**          | `Business (1) —— (0..N) Review`     | `Review.business_id → Business.business_id`          | A business can receive zero or many reviews; each review targets one business. |
| **User → Review (writes)**                | `User (1) —— (0..N) Review`         | `Review.client_id → User.user_id`                    | A user can write zero or many reviews; each review has one author (client). |
| **User → Message (sends)**                | `User (1) —— (0..N) Message`        | `Message.sender_id → User.user_id`                   | A user can send zero or many messages; each message has one sender. |
| **User → Message (receives)**             | `User (1) —— (0..N) Message`        | `Message.recipient_id → User.user_id`                | A user can receive zero or many messages; each message has one recipient. |
| **Business → Message (context)**          | `Business (1) —— (0..N) Message`    | `Message.business_id → Business.business_id`         | Messages are tied to a business context so client–business conversations can be grouped per business. |


