Pendla
======

En liten applikation som visar kommande avgångar du faktiskt hinner till!

## Instruktioner

Gå till sl.se eller valfri tjänst som nyttjar deras APIer. Gör en sökning på en hållplats och notera ID-numret (syns vanligtvis i URLen). Editera sedan "pendla.py" med korrekt data för respektive trafikslag.

## Versioner

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
