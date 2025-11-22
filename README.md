# StudentToDo

Enkel To-do app for studenter som ønsker å sortre gjøremål og holde oversikt over kommende frister. En kan legge til/fjerne, sorte blant ferdige/ufeerdige gjøremål samt se oppkommande frister i en kalender.

## FUNKSJONER
- Legg til og fjerne oppgaver 
- Markere oppgaver som Ferdig/Uferdig 
-filtrere visning mellom: alle/ferdige/uferdige 
-Varsling for frister som nærmer seg(standar 3 dager før)
-snooze; muligheten å utsette frist med en dag når den popper opp som varsling
-kalenderoversikt for di neste 3 vekene

## Mappestruktur
├── controllers/
│ └── app.py # Flask-ruter
├── models/
│ └── services.py # Logikk + DB-operasjoner
├── views/
│ └── index.html # UI / Jinja-template 
├── static/
│ └── style.css # Små tillegg til PicoCSS
├── run.py # Starter appen
├── oppgaver.db # SQLite-database
└── test_app.py # pytest-tester
## TEKNOLOGI
- **Backend:** Python 3.12 +Flask
-**Database:** SQLite 
- **Frontend:** HTML+ PicoCSS +liten egen "style.css"
- **Testing:** pytest 

## Kjør lokalt 
1. Installer avhengigheter: 
```bash
pip install flask pytest

start appen : python3 run.py 

kjør test slik: pytest 

## om prosjektet: 
prosjeket er utviklet som en del av INFO212, som er utviklet gjennom 4 agile sprint itterasjoner. 


