# Normalization Exercise — Cars

The functional dependencies are identified, each normal form violation is explained, and the resulting table is shown at every step up to 3NF (Third Normal Form).

## Original table

| VIN | Make | Model | Year | Color | Owner ID | Owner Name | Owner Phone | Insurance Company | Insurance Policy |
|---|---|---|---|---|---|---|---|---|---|
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 101 | Alice | 123-456-7890 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 102 | Bob | 987-654-3210 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue | 103 | Claire | 555-123-4567 | DEF Insurance | Collision |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red | 104 | Dave | 111-222-3333 | GHI Insurance | Basic Legal |

**Key observation:** the same VIN (`1HGCM82633A`) appears twice, with two different owners (Alice and Bob) and two different insurance policies. This indicates a **many-to-many** relationship between cars and owners (a car can have more than one owner, each insuring it separately).

## Functional dependencies identified

- `VIN → Make, Model, Year, Color`
- `Owner ID → Owner Name, Owner Phone`
- `VIN, Owner ID → Insurance Company, Insurance Policy`
- `Model → Make` (every model always belongs to the same make in the data)

The primary key of the original table is **(VIN, Owner ID)**.

## Step 1 — First Normal Form (1NF)

All values are atomic and the composite key (VIN, Owner ID) uniquely identifies each row. The original table **is already in 1NF**.

## Step 2 — Second Normal Form (2NF)

Checking for partial dependencies on the composite key (VIN, Owner ID):

- `Make, Model, Year, Color` depend only on `VIN` → **partial dependency** → extracted into `Cars`.
- `Owner Name, Owner Phone` depend only on `Owner ID` → **partial dependency** → extracted into `Owners`.
- `Insurance Company, Insurance Policy` depend on the full key → remain in the intermediate `Car_Owners` table for now (revisited in Step 3).

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

Checking for transitive dependencies revealed **two problems missed in the first pass**, both flagged during instructor review:

**3a) `Cars`: `Model → Make` is a transitive dependency.** Every model always belongs to the same make (Accord/CR-V → Honda, Volt → Chevrolet), so `Make` depends on `Model`, not directly on `VIN`. Fix: extract `Model` into its own table.

**3b) Using the model name as the primary key of that new table is fragile.** A model name is just a text label — it isn't guaranteed to stay unique or unchanged, and it doesn't scale well if a make like Honda ends up with 100 models each needing to reference it. Fix: give `Models` a surrogate `Model ID`, and since `Make` also repeats once per model, extract it too into its own `Makes` table (`Model ID → Make ID → Make Name`), so the make name is stored exactly once instead of once per model.

**3c) `Car_Owners`: `Insurance Company` depends on `Insurance Policy`, not on the full key.** In the data, each policy is always tied to the same insurer — that's a transitive dependency (`VIN, Owner ID → Insurance Policy → Insurance Company`). Fix: extract policies into their own `Policies` table, keyed by a surrogate `Policy ID`.

**3d) A policy shouldn't be embedded as columns on `Car_Owners` at all — a single policy can cover more than one car.** Tying `Policy ID` directly into the `(VIN, Owner ID)` row would still assume a 1-to-1 relationship between an ownership record and a policy. In reality, this is a many-to-many relationship (one policy can cover several vehicles), so it needs its own junction table, `Policy_Coverage`, separate from `Car_Owners` (which now only represents *who owns which car*).

## Final schema (3NF)

**Makes** (PK: Make ID)

| Make ID | Make Name |
|---|---|
| 1 | Honda |
| 2 | Chevrolet |

**Models** (PK: Model ID, FK: Make ID → Makes)

| Model ID | Model Name | Make ID |
|---|---|---|
| 1 | Accord | 1 |
| 2 | CR-V | 1 |
| 3 | Volt | 2 |

**Cars** (PK: VIN, FK: Model ID → Models)

| VIN | Model ID | Year | Color |
|---|---|---|---|
| 1HGCM82633A | 1 | 2003 | Silver |
| 5J6RM4H79EL | 2 | 2014 | Blue |
| 1G1RA6EH1FU | 3 | 2015 | Red |

**Owners** (PK: Owner ID)

| Owner ID | Owner Name | Owner Phone |
|---|---|---|
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |

**Car_Owners** (PK: VIN + Owner ID, FKs: VIN → Cars, Owner ID → Owners) — pure ownership relation, no insurance data

| VIN | Owner ID |
|---|---|
| 1HGCM82633A | 101 |
| 1HGCM82633A | 102 |
| 5J6RM4H79EL | 103 |
| 1G1RA6EH1FU | 104 |

**Policies** (PK: Policy ID, FK: Owner ID → Owners) — each policy stored exactly once

| Policy ID | Owner ID | Insurance Company | Policy Type |
|---|---|---|---|
| P1 | 101 | ABC Insurance | Fire & Theft |
| P2 | 102 | XYZ Insurance | Full Cover |
| P3 | 103 | DEF Insurance | Collision |
| P4 | 104 | GHI Insurance | Basic Legal |

**Policy_Coverage** (PK: Policy ID + VIN, FKs: Policy ID → Policies, VIN → Cars) — which car(s) each policy covers

| Policy ID | VIN |
|---|---|
| P1 | 1HGCM82633A |
| P2 | 1HGCM82633A |
| P3 | 5J6RM4H79EL |
| P4 | 1G1RA6EH1FU |

If policy `P1` later also covered a second car owned by Alice, that would just be one more row in `Policy_Coverage` (`P1`, `<new VIN>`) — no duplication of the company or policy type data.

### Summary of fixes applied after instructor feedback

- `Insurance Company` and `Insurance Policy` were pulled out of `Car_Owners` into a dedicated `Policies` table, removing the transitive dependency between them.
- The policy-to-car relationship was modeled as its own many-to-many junction table (`Policy_Coverage`) instead of embedding it in the ownership record, since one policy can cover multiple vehicles.
- `Models` now uses a surrogate `Model ID` as its primary key instead of the model name.
- `Make` was extracted into its own `Makes` table referenced by `Models`, so the make name is never repeated once per model.
