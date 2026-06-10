# Zadaća: balansiranje jednostavnog humanoidnog trupa

## Cilj

Implementirati i analizirati upravljanje pojednostavljenim humanoidnim sustavom u MuJoCo simulatoru. Sustav je modeliran kao trup koji se rotira oko gležnja, odnosno kao obrnuto njihalo.

Zadaća završava s LQR regulatorom. Nema hoda, nema MPC-a i nema whole-body controla.

---

## Zadatak 1 — Upoznavanje modela

Pokrenuti:

```bash
python run_assignment.py --mode inspect
```

U izvješću odgovoriti:

1. Što predstavljaju `qpos[0]`, `qvel[0]` i `ctrl[0]`?
2. Je li `ctrl[0]` pozicijska referenca ili moment?
3. Koje su granice aktuatora?

---

## Zadatak 2 — Open-loop ponašanje

Pokrenuti:

```bash
python run_assignment.py --mode open_loop --duration 4 --viewer
```

Bez `--viewer` spremiti graf:

```bash
python run_assignment.py --mode open_loop --duration 4 --out-dir results
```

U izvješću kratko objasniti zašto sustav pada. Dovoljno je povezati početni nagib, gravitaciju i nestabilnu ravnotežu.

---

## Zadatak 3 — PD stabilizacija

U datoteci:

```text
walker_assignment/controllers.py
```

podesiti `Kp` i `Kd` u funkciji `pd_control()`.

Pokrenuti:

```bash
python run_assignment.py --mode pd --duration 5 --viewer
```

Napraviti tri slučaja:

1. premali `Kp`,
2. dobar odziv,
3. prevelik `Kp` ili premali `Kd`.

Za svaki slučaj komentirati odziv: brzina smirivanja, oscilacije i maksimalni moment.

---

## Zadatak 4 — LQR regulator

U `controllers.py` proučiti funkcije:

```python
lqr_matrices()
lqr_gain()
lqr_control()
```

Koristi se linearizirani model:

```text
x = [theta, theta_dot]^T
u = tau
```

Potrebno je:

1. definirati matrice `Q` i `R`,
2. izračunati LQR pojačanje `K`,
3. koristiti zakon upravljanja `u = -Kx`,
4. usporediti LQR s PD regulatorom.

Pokretanje:

```bash
python run_assignment.py --mode lqr --duration 5 --viewer
```

---

## Zadatak 5 — Smetnja i kratka usporedba

Pokrenuti:

```bash
python run_assignment.py --mode perturbation --duration 6 --viewer
```

U ovom modu sustav dobiva kratku smetnju u 2. sekundi.

U izvješću usporediti:

- open-loop,
- PD,
- LQR,
- LQR sa smetnjom.

---

## Zadatak 6 — Upravljanje humanoidom u cijelosti

Na 5. slajdu (Od naredbe korisnika do momenata zglobova) iz predavanja nalazi se shematski prikaz upravljanja humanoidom. Potrebno je riječima opisati ulaze i izlaze svakog pojedinog bloka kako bi se provjerilo cjelokupno razumijevanje upravljanja humanoidnim robotom.

---

## Predaja

Predaje se `.zip` koji sadrži:

1. kod,
2. grafove iz `results/`,
3. izvješće do 3 stranice,
4. kratki video ili screenshot.

