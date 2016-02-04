Pendla
======

En liten applikation som visar kommande avgångar du faktiskt hinner till!

## Instruktioner

Kör 'python findstation.py' för att hitta din station, och kopiera ID-numret.
Skapa din egen konfigurations-fil från config.yml.sample och skriv in
dina stationer och önskade linjer där. Kör sedan 'python main.py' för att
uppdatera sökningen automatiskt varje minut. Tryck Ctrl+C för att avbryta
programmet.

## Versioner

#### 1.0.1

- Fixar en bugg där rubrikerna saknas i output

### 1.0.0

Full release av Pendla. Se instruktionerna för hur du skapar din konfiguration.

- Loopar automatiskt sökningen varje minut så att du alltid har den
  senaste informationen.
- Ny, finare konfigurations-fil som är enklare att läsa.
- Nytt verktyg för att hitta stationer och hämta ut deras SiteId.
- Fullt kompatibel med pep-0008

#### 1.0-RC3

Denna version gör en nästan total omskrivning av koden för detta projekt.

- Pendla läser ifrån en konfigurations-fil och filtrerar resultaten därefter

#### 1.0-RC2

- Det hände säkert något här... Men jag har glömt vad :)

#### 1.0-RC1

- Pendla kan nu visa när du måste gå för att hinna med en buss eller ett tåg
- Tar bort tunnelbana pga. bristfälligt API

#### 0.2

- Lägger till tunnelbana
- Skapar pendla.py och flyttar pendeltåg, bussar och tunnelbana till separata moduler
- Snyggar till output med färger och kolumner med rubriker

#### 0.1

- Första versionen

## Utveckling

För att köra tester behöver pip-paket installeras:

```
pip install -r requirements-test.txt
```

[PEP8](https://www.python.org/dev/peps/pep-0008/) syntax test:

```
make syntax-test
```
