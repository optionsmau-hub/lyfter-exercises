# Normalization Exercise — Cars

The functional dependencies are identified, each normal form violation is explained, and the resulting table is shown at every step up to 3NF (Third Normal Form).

## Original table

| VIN | Make | Model | Year | Color | Owner ID | Owner Name | Owner Phone | Insurance Company | Insurance Policy |
|---|---|---|---|---|---|---|---|---|---|
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 101 | Alice | 123-456-7890 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 102 | Bob | 987-654-3210 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue | 103 | Claire | 555-123-4567 | DEF Insurance | Collision |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red | 104 | Dave | 111-222-3333 | GHI Insurance | Basic Legal |

**Key observation:** the same VIN (`1HGCM82633A`) appears twice, with two different owners (Alice and Bob) and two different insurance policies. This indicates a **many-to-many** relationship between cars and owners (a car can have more than one owner, each with their own policy — for example, a car with co-owners who insure it separately).

## Functional dependencies identified

- `VIN → Make, Model, Year, Color` (the car's physical attributes depend only on the VIN)
- `Owner ID → Owner Name, Owner Phone` (the owner's data depends only on their ID)
- `VIN, Owner ID → Insurance Company, Insurance Policy` (the policy is specific to that car+owner combination)
- *(Additional dependency observed, see Step 3):* `Model → Make` — in the given data, every model always belongs to the same make (Accord and CR-V are always Honda, Volt is always Chevrolet).

The primary key of the original table is **(VIN, Owner ID)**.

## Step 1 — First Normal Form (1NF)

All values are atomic, and a key (VIN, Owner ID) already exists that uniquely identifies each row. The original table **is already in 1NF**.

## Step 2 — Second Normal Form (2NF)

Checking for partial dependencies on the composite key (VIN, Owner ID):

- `Make, Model, Year, Color` depend only on `VIN` → **partial dependency** → extracted into `Cars`.
- `Owner Name, Owner Phone` depend only on `Owner ID` → **partial dependency** → extracted into `Owners`.
- `Insurance Company, Insurance Policy` depend on the full key → remain in the intermediate `Car_Owners` table.

**Result after 2NF (intermediate tables):**

**Cars** (PK: VIN)

| VIN | Make | Model | Year | Color |
|---|---|---|---|---|
| 1HGCM82633A | Honda | Accord | 2003 | Silver |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red |

**Owners** (PK: Owner ID)

| Owner ID | Owner Name | Owner Phone |
|---|---|---|
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |

**Car_Owners** (PK: VIN + Owner ID)

| VIN | Owner ID | Insurance Company | Insurance Policy |
|---|---|---|---|
| 1HGCM82633A | 101 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | 102 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | 103 | DEF Insurance | Collision |
| 1G1RA6EH1FU | 104 | GHI Insurance | Basic Legal |

## Step 3 — Third Normal Form (3NF)

Checking for transitive dependencies:

- `Owners`: `Owner Name` and `Owner Phone` depend directly on `Owner ID`, with no transitive dependency between them. Already in 3NF.
- `Car_Owners`: `Insurance Company` and `Insurance Policy` depend on the full key (VIN, Owner ID). There's no evidence in the data that one determines the other. Already in 3NF.
- `Cars`: this one needs a closer look. In the data, **every `Model` always belongs to the same `Make`** (Accord → Honda, CR-V → Honda, Volt → Chevrolet). This is a transitive dependency: `VIN → Model → Make`. Strictly speaking, this violates 3NF because `Make` (a non-key attribute) depends on `Model` (another non-key attribute), rather than directly on the VIN.

**Design note:** this dependency reflects a real business rule (a car manufacturer doesn't reuse model names across different makes), so splitting `Make` into a separate models table is the strictly correct 3NF solution. However, many practical designs keep Make and Model together in the cars table, since the model list isn't managed as an independent, growing catalog. Both options are presented below:

### Option A — Strict 3NF (splitting Make out by Model)

**Models** (PK: Model)

| Model | Make |
|---|---|
| Accord | Honda |
| CR-V | Honda |
| Volt | Chevrolet |

**Cars** (PK: VIN, FK: Model → Models)

| VIN | Model | Year | Color |
|---|---|---|---|
| 1HGCM82633A | Accord | 2003 | Silver |
| 5J6RM4H79EL | CR-V | 2014 | Blue |
| 1G1RA6EH1FU | Volt | 2015 | Red |

### Option B — Practical 3NF (Make and Model kept together as a fixed pair)

**Cars** (PK: VIN)

| VIN | Make | Model | Year | Color |
|---|---|---|---|---|
| 1HGCM82633A | Honda | Accord | 2003 | Silver |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red |

Either option is defensible; the trade-off is documented here to make clear this was a conscious design decision, not a missed step.

## Final schema (3NF, using Option B as the base + Owners + Car_Owners)

- **Models** (optional, see Option A) — PK: Model
- **Cars** — PK: VIN
- **Owners** — PK: Owner ID
- **Car_Owners** — PK: (VIN, Owner ID), FKs: VIN → Cars, Owner ID → Owners

This resolves the many-to-many relationship between cars and owners, allows a car to have multiple owners with different policies, and removes all the redundancy from the original table (Make/Model/Year/Color repeated for the same VIN, and owner data repeated if they owned more than one car).
