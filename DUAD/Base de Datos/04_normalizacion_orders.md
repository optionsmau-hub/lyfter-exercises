# Normalization Exercise — Orders

The functional dependencies are identified, each normal form violation is explained, and the resulting table is shown at every step up to 3NF (Third Normal Form).

## Original table

| Order ID | Customer Name | Customer Phone | Address | Item ID | Item Name | Price | Quantity | Special Request | Delivery Time |
|---|---|---|---|---|---|---|---|---|---|
| 001 | Alice | 123-456-7890 | 123 Main St | 101 | Cheeseburger | $8 | 2 | No onions | 6:00 PM |
| 001 | Alice | 123-456-7890 | 123 Main St | 102 | Fries | $3 | 1 | Extra ketchup | 6:00 PM |
| 002 | Bob | 987-654-3210 | 456 Elm St | 103 | Pizza | $12 | 1 | Extra cheese | 7:30 PM |
| 002 | Bob | 987-654-3210 | 4th Avenue | 102 | Fries | $3 | 2 | None | 7:30 PM |
| 003 | Claire | 555-123-4567 | 789 Oak St | 105 | Salad | $6 | 1 | No croutons | 12:00 PM |
| 004 | Claire | 555-123-4567 | 464 Georgia St | 106 | Water | $1 | 1 | None | 5:00 PM |

**Anomaly found in the data:** Order ID 002 shows up with two different addresses ("456 Elm St" and "4th Avenue") across its two rows. This is exactly the kind of inconsistency normalization is meant to prevent: by repeating the address on every product line, there's no way to know which address is actually correct for the order. It's a real example of an **update anomaly** caused by an unnormalized table. For this exercise, the address in the first row of the order is assumed to be the correct one ("456 Elm St"), but in a real scenario this should be clarified with the business before normalizing.

## Functional dependencies identified

- `Order ID → Customer Name, Customer Phone, Address, Delivery Time` (each order has exactly one customer, one delivery address, and one delivery time)
- `Customer Phone → Customer Name` (the phone number uniquely identifies the customer; the same phone/name pair repeats for Claire across orders 003 and 004)
- `Item ID → Item Name, Price` (the item catalog does not depend on the order)
- `Order ID, Item ID → Quantity, Special Request` (quantity and special request are specific to that product line within that order)

The primary key of the original table is the composite **(Order ID, Item ID)**, since that's what uniquely identifies each row (an order can contain several items).

## Step 1 — First Normal Form (1NF)

**Rule:** all values must be atomic (no lists or repeating groups), and a primary key must exist.

The original table already satisfies this: every cell holds a single value, there are no multi-valued fields. The composite primary key **(Order ID, Item ID)** is used. Therefore, the original table **is already in 1NF**, but not in 2NF (see next step).

## Step 2 — Second Normal Form (2NF)

**Rule:** there can be no partial dependencies — no non-key attribute can depend on only part of a composite key.

Since the key is composite (Order ID, Item ID), each attribute is checked:

- `Customer Name, Customer Phone, Address, Delivery Time` depend only on `Order ID` → **partial dependency** → extracted into an `Orders` table.
- `Item Name, Price` depend only on `Item ID` → **partial dependency** → extracted into an `Items` table.
- `Quantity, Special Request` depend on the full key (Order ID + Item ID) → remain in an intermediate `Order_Items` table.

**Result after 2NF (intermediate tables):**

**Orders** (PK: Order ID)

| Order ID | Customer Name | Customer Phone | Address | Delivery Time |
|---|---|---|---|---|
| 001 | Alice | 123-456-7890 | 123 Main St | 6:00 PM |
| 002 | Bob | 987-654-3210 | 456 Elm St | 7:30 PM |
| 003 | Claire | 555-123-4567 | 789 Oak St | 12:00 PM |
| 004 | Claire | 555-123-4567 | 464 Georgia St | 5:00 PM |

**Items** (PK: Item ID)

| Item ID | Item Name | Price |
|---|---|---|
| 101 | Cheeseburger | $8 |
| 102 | Fries | $3 |
| 103 | Pizza | $12 |
| 105 | Salad | $6 |
| 106 | Water | $1 |

**Order_Items** (PK: Order ID + Item ID)

| Order ID | Item ID | Quantity | Special Request |
|---|---|---|---|
| 001 | 101 | 2 | No onions |
| 001 | 102 | 1 | Extra ketchup |
| 002 | 103 | 1 | Extra cheese |
| 002 | 102 | 2 | None |
| 003 | 105 | 1 | No croutons |
| 004 | 106 | 1 | None |

## Step 3 — Third Normal Form (3NF)

**Rule:** there can be no transitive dependencies — no non-key attribute can depend on another attribute that is also not a key.

Looking at the `Orders` table: `Customer Phone → Customer Name` is a transitive dependency (`Order ID → Customer Phone → Customer Name`). The customer's name doesn't depend directly on the order — it depends on the customer's phone number. This is confirmed by the data: Claire appears twice with the same phone and same name across two different orders.

**Solution:** extract the customer data into its own `Customers` table, using the phone number as the key (it's the natural identifier available in the data).

`Items` and `Order_Items` are already in 3NF — there are no transitive dependencies among their attributes.

## Final schema (3NF)

**Customers** (PK: Customer Phone)

| Customer Phone | Customer Name |
|---|---|
| 123-456-7890 | Alice |
| 987-654-3210 | Bob |
| 555-123-4567 | Claire |

**Orders** (PK: Order ID, FK: Customer Phone → Customers)

| Order ID | Customer Phone | Address | Delivery Time |
|---|---|---|---|
| 001 | 123-456-7890 | 123 Main St | 6:00 PM |
| 002 | 987-654-3210 | 456 Elm St | 7:30 PM |
| 003 | 555-123-4567 | 789 Oak St | 12:00 PM |
| 004 | 555-123-4567 | 464 Georgia St | 5:00 PM |

**Items** (PK: Item ID)

| Item ID | Item Name | Price |
|---|---|---|
| 101 | Cheeseburger | $8 |
| 102 | Fries | $3 |
| 103 | Pizza | $12 |
| 105 | Salad | $6 |
| 106 | Water | $1 |

**Order_Items** (PK: Order ID + Item ID, FKs: Order ID → Orders, Item ID → Items)

| Order ID | Item ID | Quantity | Special Request |
|---|---|---|---|
| 001 | 101 | 2 | No onions |
| 001 | 102 | 1 | Extra ketchup |
| 002 | 103 | 1 | Extra cheese |
| 002 | 102 | 2 | None |
| 003 | 105 | 1 | No croutons |
| 004 | 106 | 1 | None |

**Note:** in a real-world design, an auto-generated `Customer ID` would be preferable over the phone number as the key (phone numbers can change), but since the exercise doesn't provide a customer ID, the phone number is documented as the natural key available in the data.
