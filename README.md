# Projekat blok 4
## žabac na biciklu
![biciklo](https://github.com/lukardvn/pepe/blob/master/kermit.gif)

## Pokretanje

potrebno je imati instaliran PyQt5

pokreni Main.py

## Kontrole
| Taster(i) | Šta se desi |
| --------- | ----------- |
| Strelice | Kontrole igrača 1 (zeleni) |
| WASD | Kontrole igrača 2 (crveni) |
| ESC | Pause/Resume game |

## Objašnjenje mulitplayera preko mreže (neki podaci su zastareli)
![objasnjenje](https://github.com/lukardvn/pepe/blob/multiplayerV2/objasnjenjeMultiplayer.png)

*dodatno: klijent nema nikakvu logiku, samo prikazuje objekte onako kako se nalaze na serveru. ne dešava se nikakva provera kolizije 
niti bilo šta drugo (da li je žaba van ekrana ili ju je udario auto, to sve radi server). sve što klijent radi je da šalje input na server.

## Novo u V2
Salje podatke za objekte koji imaju speed != 0
i za zabe i lokvanje salje i sprite.
Igra moze da se pauzira na ESC (al ne kad se igra preko mreze)
Ako se server ugasi klijent nece pasti, vec ce se vratiti na glavni meni
