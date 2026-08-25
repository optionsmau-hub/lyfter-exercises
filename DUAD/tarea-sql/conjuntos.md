# Set Operations

Starting sets:

```
All  = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
Even = {2, 4, 6, 8, 10}
Odd  = {1, 3, 5, 7, 9}
```

---

## 1. Even ∪ Odd (Union)

The union gathers **every element that is in Even, in Odd, or in both**, without repeating elements.

**Step by step:**
1. Take all elements of Even: `{2, 4, 6, 8, 10}`
2. Add every element of Odd that isn't already in the result: `{1, 3, 5, 7, 9}`
3. Since Even and Odd share no elements, they simply combine.

**Result:**
```
Even ∪ Odd = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

Note: `Even ∪ Odd = All`, because Even and Odd fully partition All.

---

## 2. Even ∩ Odd (Intersection)

The intersection is the set of elements that are **in both** Even and Odd at the same time.

**Step by step:**
1. Go through each element of Even: `2, 4, 6, 8, 10`
2. Check whether each one also belongs to Odd:
   - 2 → is it in Odd? No
   - 4 → is it in Odd? No
   - 6 → is it in Odd? No
   - 8 → is it in Odd? No
   - 10 → is it in Odd? No
3. No number can be both even and odd, so there are no matches.

**Result:**
```
Even ∩ Odd = { } (empty set, ∅)
```

---

## 3. All − Odd (Difference)

The difference `All − Odd` is the set of elements that are in All but **not** in Odd.

**Step by step:**
1. Go through each element of All: `1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
2. Remove the ones that are also in Odd (`1, 3, 5, 7, 9`):
   - 1 → is in Odd → removed
   - 2 → not in Odd → kept
   - 3 → is in Odd → removed
   - 4 → not in Odd → kept
   - 5 → is in Odd → removed
   - 6 → not in Odd → kept
   - 7 → is in Odd → removed
   - 8 → not in Odd → kept
   - 9 → is in Odd → removed
   - 10 → not in Odd → kept

**Result:**
```
All − Odd = {2, 4, 6, 8, 10}
```

Note: `All − Odd = Even`, since removing the odd numbers from All leaves only the even ones.

---

## 4. C(Even) — Complement of Even with respect to All

The complement of Even with respect to All is the set of elements of All that **do not** belong to Even. That is, `C(Even) = All − Even`.

**Step by step:**
1. Go through each element of All: `1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
2. Remove the ones that are in Even (`2, 4, 6, 8, 10`):
   - 1 → not in Even → kept
   - 2 → is in Even → removed
   - 3 → not in Even → kept
   - 4 → is in Even → removed
   - 5 → not in Even → kept
   - 6 → is in Even → removed
   - 7 → not in Even → kept
   - 8 → is in Even → removed
   - 9 → not in Even → kept
   - 10 → is in Even → removed

**Result:**
```
C(Even) = {1, 3, 5, 7, 9}
```

Note: `C(Even) = Odd`.

---

## 5. C(Odd − All) — Complement of (Odd − All)

This exercise has two parts: first compute `Odd − All`, then take the complement of that result with respect to All.

**Step by step — Part A: `Odd − All`**
1. Go through each element of Odd: `1, 3, 5, 7, 9`
2. Remove the ones that are also in All. Since Odd is a subset of All, **every** element of Odd is in All:
   - 1 → is in All → removed
   - 3 → is in All → removed
   - 5 → is in All → removed
   - 7 → is in All → removed
   - 9 → is in All → removed
3. No elements remain.

```
Odd − All = { } (empty set, ∅)
```

**Step by step — Part B: `C(∅)`**
1. The complement of the empty set with respect to All is the set of elements of All that are not in `∅`.
2. Since `∅` has no elements, **none** of the elements of All get removed.

**Result:**
```
C(Odd − All) = C(∅) = All = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

---

## Summary of results

| Operation | Result |
|---|---|
| Even ∪ Odd | {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} |
| Even ∩ Odd | ∅ |
| All − Odd | {2, 4, 6, 8, 10} |
| C(Even) | {1, 3, 5, 7, 9} |
| C(Odd − All) | {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} |
