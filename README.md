# barbu-python

Python implementation of [Barbu](https://en.wikipedia.org/wiki/Barbu_(card_game)), a 4-player trick-taking card game.

Some of the game scores are different from the ones written on Wikipedia, but after any complete dealer the sum of the total scores is still zero.

## Scores

Listed below there are the scores used in this implementation.

### Atout

Every trick taken is worth +5.

### NoTricks

Every trick taken is worth -2.

### NoHearts

♥2, ♥3, ♥4, ♥5, ♥6, ♥7, ♥8, ♥9 are worth -2.

♥10, ♥J, ♥Q, ♥K, ♥A are worth -4.

### NoKingOfHearts

♥K is worth -20.

### NoLastTwo

The last two tricks are worth -12.

### NoQueens

Every Queen is worth -6.

### Domino

Points are assigned in order to players who run out of cards.

* First player gets +45.
* Second player gets +20.
* Third player gets +10.
* Last player gets -10.

## Aim

The ambition of this project is to create an Artificial Intelligence for the game, based on MCTS / UCT in addition to various heuristics.