Pendla v1.3.0
======

En liten applikation som visar kommande avgångar du faktiskt hinner till!

## Instruktioner

Kör './findstation.py' för att hitta din station, och kopiera ID-numret.
Skapa din egen konfigurations-fil från 'config.yml.sample' och skriv in
dina stationer och önskade linjer där. Kör sedan './pendla.py' för att visa
resultaten, eller 'pendla.py -l' för att uppdatera sökningen automatiskt
varje minut. Tryck Ctrl+C för att avbryta programmet.

För att söka alla avgångar från en station, gör såhär:
./pendla.py <namn på stationen> <linje> [<linje> ...]

Du kan även söka stationers ID-nummer snabbt genom att köra:
./findstation.py <namn på stationen>

## Versioner

### 1.3.0

- Gör det möjligt att loopa även vid snabbsökningar
- API-proxy som döljer API-nyckeln

### v1.2.0

NYHET! Sök alla avgångar direkt med:
./pendla.py <namn på station> <linje> [<linje> ...]

- Lägger till fler argument till findstation.py och pendla.py.
- Trafikslag är nu borttagen ur konfigurationen. Programmet matchar
  alla avgångar på vald linje, oavsett trafikslag.
- Mer felhantering i koden.
- Övergång till Git Flow i utvecklingen.

### v1.1.0

- Byter namn på huvudprogrammet till pendla.py
- Gör pendla.py exekverbar som standard
- Lägger till argument och instruktioner för korrekt användning.
- Ändrar standard-beteende till att visa resultaten och avsluta.
  Lägg till '-l' eller '--loop' för att uppdatera automatiskt.
- Bättre hantering av fel i både program och API.

#### v1.0.1

- Fixar en bugg där rubrikerna saknas i output

## v1.0.0

Full release av Pendla. Se instruktionerna för hur du skapar din konfiguration.

- Loopar automatiskt sökningen varje minut så att du alltid har den
  senaste informationen.
- Ny, finare konfigurations-fil som är enklare att läsa.
- Nytt verktyg för att hitta stationer och hämta ut deras SiteId.
- Fullt kompatibel med pep-0008

#### v1.0-RC3

Denna version gör en nästan total omskrivning av koden för detta projekt.

- Pendla läser ifrån en konfigurations-fil och filtrerar resultaten därefter

#### v1.0-RC2

- Det hände säkert något här... Men jag har glömt vad :)

#### v1.0-RC1

- Pendla kan nu visa när du måste gå för att hinna med en buss eller ett tåg
- Tar bort tunnelbana pga. bristfälligt API

#### v0.2

- Lägger till tunnelbana
- Skapar pendla.py och flyttar pendeltåg, bussar och tunnelbana till separata moduler
- Snyggar till output med färger och kolumner med rubriker

#### v0.1

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
