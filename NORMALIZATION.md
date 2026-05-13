# Database Normalization Report

## Original Functional Dependencies

### Categories Table
- category_id → category_name

### Products Table
- product_id → product_name, price, quantity, category_id

### Inventory Logs Table
- log_id → product_id, change_amount, note, created_at

---

## Potential Anomalies

### Update Anomaly
If category information were duplicated across multiple products, updating 
category names would require multiple updates.

### Insertion Anomaly
Without separate category storage, categories could not exist 
independently from products.

### Deletion Anomaly
Deleting the last product in a category could accidentally remove category 
information.

---

## Decomposition Steps

The database was decomposed into:
1. categories
2. products
3. inventory_logs

This separation reduced redundancy and improved data integrity.

---

## Third Normal Form Verification

### First Normal Form (1NF)
- All fields contain atomic values.

### Second Normal Form (2NF)
- All non-key attributes fully depend on the primary key.

### Third Normal Form (3NF)
- No transitive dependencies exist.

---

## Final Relational Schema

### categories
- category_id (PK)
- category_name

### products
- product_id (PK)
- product_name
- price
- quantity
- category_id (FK)

### inventory_logs
- log_id (PK)
- product_id (FK)
- change_amount
- note
- created_at
