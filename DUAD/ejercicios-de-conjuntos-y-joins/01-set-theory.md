# Set Theory Exercises

## Given sets

```
All  = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}     <- universal set
Even = {2, 4, 6, 8, 10}
Odd  = {1, 3, 5, 7, 9}
```

For the complement operations below, **All** is used as the universal set,
since the exercise does not define a separate universe and every element of
Even and Odd already belongs to All.

---

## 1. Even ∪ Odd (Union)

The union contains every element that belongs to Even, to Odd, or to both.

```
Even ∪ Odd = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

Note that this result is identical to **All**, because Even and Odd together
cover every element of the universal set.

---

## 2. Even ∩ Odd (Intersection)

The intersection contains only the elements that belong to **both** Even and
Odd at the same time.

```
Even ∩ Odd = ∅ (empty set)
```

No number can be even and odd simultaneously, so Even and Odd are
**disjoint sets**.

---

## 3. All − Odd (Difference)

The difference All − Odd contains every element of All that is **not**
in Odd.

```
All − Odd = {2, 4, 6, 8, 10}
```

This result is identical to **Even**, since removing every odd number from
All leaves exactly the even numbers.

---

## 4. C(Even) — Complement of Even

The complement of Even (relative to the universal set All) contains every
element of All that does **not** belong to Even.

```
C(Even) = All − Even = {1, 3, 5, 7, 9}
```

This result is identical to **Odd**.

---

## 5. C(Odd − All) — Complement of (Odd − All)

This operation must be solved in two steps.

**Step 1 — solve the inner operation (Odd − All):**

Odd − All contains every element of Odd that is **not** in All.
Since Odd is a subset of All (every odd number 1–9 is already inside All),
there is nothing left over.

```
Odd − All = ∅ (empty set)
```

**Step 2 — take the complement of that result:**

The complement of the empty set, relative to the universal set All, is All
itself (every element of All is "not in the empty set").

```
C(Odd − All) = C(∅) = All = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

---

## Summary table

| # | Operation      | Result                              | Equal to |
|---|----------------|--------------------------------------|----------|
| 1 | Even ∪ Odd     | {1,2,3,4,5,6,7,8,9,10}                | All      |
| 2 | Even ∩ Odd     | ∅                                     | —        |
| 3 | All − Odd      | {2,4,6,8,10}                          | Even     |
| 4 | C(Even)        | {1,3,5,7,9}                           | Odd      |
| 5 | C(Odd − All)   | {1,2,3,4,5,6,7,8,9,10}                | All      |
