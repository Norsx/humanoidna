# Zadaća: jednostavno balansiranje humanoidnog trupa do LQR-a

Ovo je skraćena zadaća. Umjesto cijelog hoda, radi se samo stabilizacija pojednostavljenog humanoidnog trupa oko gležnja. Model je obrnuto njihalo u MuJoCo-u.

## Instalacija

```bash
pip install -r requirements.txt
```

## Pokretanje

```bash
python run_assignment.py --mode inspect
python run_assignment.py --mode open_loop --duration 4 --viewer
python run_assignment.py --mode pd --duration 5 --viewer
python run_assignment.py --mode lqr --duration 5 --viewer
python run_assignment.py --mode perturbation --duration 6 --viewer
```

Bez `--viewer` program sprema logove i grafove u `results/`:

```bash
python run_assignment.py --mode pd --duration 5 --out-dir results
python run_assignment.py --mode lqr --duration 5 --out-dir results
```

## Datoteke koje studenti mijenjaju

Najviše se mijenja:

```text
walker_assignment/controllers.py
```

Tamo su PD regulator, linearizirani model i LQR regulator.

## Predaja

Predati:

- kod,
- grafove za open-loop, PD, LQR i perturbation,
- kratko izvješće do 3 stranice,
- kratki video ili screenshot simulacije.
