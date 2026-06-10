# STATE

## Projekt

- **Naziv**: humanoid_balance_assignment
- **Tip**: Seminar | Zadaća | Thesis
- **Kolegij**: humanoid_balance_assignment
- **LaTeX format**: FSB Seminar

## Trenutni fokus

- _Opišite što se trenutno radi._

## Bilješke

- _Napomene za agenta ili sebe (npr. "koristi IEEE stil za reference")._

---

## Obavezno prije pozivanja agenta

Popuni `.ai/config/project.yaml` — `latex_architect` čita metapodatke za
naslovnicu odatle (ne iz ovog fajla):

```yaml
author_name: "Ime Prezime"
course_name: "NAZIV KOLEGIJA"
seminar_title: "Puni naslov seminara"
seminar_title_short: "Kratki naslov za header"
professor_title: "Prof. dr. sc."
professor_name: "Ime Prezime"
```

Agent neće nastaviti dok ta 4 obavezna polja nisu popunjena:
`author_name`, `course_name`, `seminar_title`, `professor_name`.
