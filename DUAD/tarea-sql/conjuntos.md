# Operaciones de Conjuntos

Conjuntos de partida:

```
All  = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
Even = {2, 4, 6, 8, 10}
Odd  = {1, 3, 5, 7, 9}
```

---

## 1. Even ∪ Odd (Unión)

La unión reúne **todos los elementos que están en Even, en Odd, o en ambos**, sin repetir elementos.

**Paso a paso:**
1. Tomamos todos los elementos de Even: `{2, 4, 6, 8, 10}`
2. Agregamos todos los elementos de Odd que aún no estén en el resultado: `{1, 3, 5, 7, 9}`
3. Como Even y Odd no comparten ningún elemento, simplemente se combinan.

**Resultado:**
```
Even ∪ Odd = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

Nota: `Even ∪ Odd = All`, porque Even y Odd particionan completamente a All.

---

## 2. Even ∩ Odd (Intersección)

La intersección son los elementos que están **al mismo tiempo** en Even y en Odd.

**Paso a paso:**
1. Recorremos cada elemento de Even: `2, 4, 6, 8, 10`
2. Verificamos si cada uno también pertenece a Odd:
   - 2 → ¿está en Odd? No
   - 4 → ¿está en Odd? No
   - 6 → ¿está en Odd? No
   - 8 → ¿está en Odd? No
   - 10 → ¿está en Odd? No
3. Ningún número puede ser par e impar a la vez, así que no hay coincidencias.

**Resultado:**
```
Even ∩ Odd = { } (conjunto vacío, ∅)
```

---

## 3. All − Odd (Diferencia)

La diferencia `All − Odd` son los elementos que están en All pero **no** están en Odd.

**Paso a paso:**
1. Recorremos cada elemento de All: `1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
2. Quitamos los que también estén en Odd (`1, 3, 5, 7, 9`):
   - 1 → está en Odd → se elimina
   - 2 → no está en Odd → se mantiene
   - 3 → está en Odd → se elimina
   - 4 → no está en Odd → se mantiene
   - 5 → está en Odd → se elimina
   - 6 → no está en Odd → se mantiene
   - 7 → está en Odd → se elimina
   - 8 → no está en Odd → se mantiene
   - 9 → está en Odd → se elimina
   - 10 → no está en Odd → se mantiene

**Resultado:**
```
All − Odd = {2, 4, 6, 8, 10}
```

Nota: `All − Odd = Even`, ya que quitarle los impares a All deja únicamente los pares.

---

## 4. C(Even) — Complemento de Even respecto a All

El complemento de Even respecto a All son los elementos de All que **no** pertenecen a Even. Es decir, `C(Even) = All − Even`.

**Paso a paso:**
1. Recorremos cada elemento de All: `1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
2. Quitamos los que estén en Even (`2, 4, 6, 8, 10`):
   - 1 → no está en Even → se mantiene
   - 2 → está en Even → se elimina
   - 3 → no está en Even → se mantiene
   - 4 → está en Even → se elimina
   - 5 → no está en Even → se mantiene
   - 6 → está en Even → se elimina
   - 7 → no está en Even → se mantiene
   - 8 → está en Even → se elimina
   - 9 → no está en Even → se mantiene
   - 10 → está en Even → se elimina

**Resultado:**
```
C(Even) = {1, 3, 5, 7, 9}
```

Nota: `C(Even) = Odd`.

---

## 5. C(Odd − All) — Complemento de (Odd − All)

Este ejercicio tiene dos partes: primero se calcula `Odd − All`, y luego se saca el complemento de ese resultado respecto a All.

**Paso a paso — Parte A: `Odd − All`**
1. Recorremos cada elemento de Odd: `1, 3, 5, 7, 9`
2. Quitamos los que también estén en All. Como Odd es un subconjunto de All, **todos** los elementos de Odd están en All:
   - 1 → está en All → se elimina
   - 3 → está en All → se elimina
   - 5 → está en All → se elimina
   - 7 → está en All → se elimina
   - 9 → está en All → se elimina
3. No queda ningún elemento.

```
Odd − All = { } (conjunto vacío, ∅)
```

**Paso a paso — Parte B: `C(∅)`**
1. El complemento del conjunto vacío respecto a All son los elementos de All que no están en `∅`.
2. Como `∅` no tiene elementos, **ningún** elemento de All se elimina.

**Resultado:**
```
C(Odd − All) = C(∅) = All = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

---

## Resumen de resultados

| Operación | Resultado |
|---|---|
| Even ∪ Odd | {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} |
| Even ∩ Odd | ∅ |
| All − Odd | {2, 4, 6, 8, 10} |
| C(Even) | {1, 3, 5, 7, 9} |
| C(Odd − All) | {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} |
