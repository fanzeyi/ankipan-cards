# Ankipan decks

Shared decks for Ankipan. To add one, copy the link to a deck
file below, then in Ankipan tap **+ → Add a shared deck → From a link…** and paste it. You can also
download the file and open it with Ankipan.

## Japanese

Each deck has four card kinds: Recognition (word → reading and meaning), Production (meaning → type
the reading), Listening (hear the word) and Speaking (say the word).

| Deck | Words | Link |
|---|---|---|
| JLPT N5 Vocabulary | 718 | [japanese/jlpt-n5-vocabulary.ankipan](japanese/jlpt-n5-vocabulary.ankipan) |
| JLPT N4 Vocabulary | 668 | [japanese/jlpt-n4-vocabulary.ankipan](japanese/jlpt-n4-vocabulary.ankipan) |
| JLPT N3 Vocabulary | 2140 | [japanese/jlpt-n3-vocabulary.ankipan](japanese/jlpt-n3-vocabulary.ankipan) |
| JLPT N2 Vocabulary | 1905 | [japanese/jlpt-n2-vocabulary.ankipan](japanese/jlpt-n2-vocabulary.ankipan) |
| JLPT N1 Vocabulary | 2699 | [japanese/jlpt-n1-vocabulary.ankipan](japanese/jlpt-n1-vocabulary.ankipan) |

## Adding a deck with one link

On an iPhone with Ankipan installed, an `ankipan://import?url=…` link opens the deck's import preview
directly. [fanzeyi.github.io/ankipan-cards](https://fanzeyi.github.io/ankipan-cards/) has them as buttons;
GitHub doesn't make them tappable here, so on this page copy one into Safari's address bar:

```
JLPT N5: ankipan://import?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffanzeyi%2Fankipan-cards%2Fmain%2Fjapanese%2Fjlpt-n5-vocabulary.ankipan
JLPT N4: ankipan://import?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffanzeyi%2Fankipan-cards%2Fmain%2Fjapanese%2Fjlpt-n4-vocabulary.ankipan
JLPT N3: ankipan://import?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffanzeyi%2Fankipan-cards%2Fmain%2Fjapanese%2Fjlpt-n3-vocabulary.ankipan
JLPT N2: ankipan://import?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffanzeyi%2Fankipan-cards%2Fmain%2Fjapanese%2Fjlpt-n2-vocabulary.ankipan
JLPT N1: ankipan://import?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffanzeyi%2Fankipan-cards%2Fmain%2Fjapanese%2Fjlpt-n1-vocabulary.ankipan
```

To build one for any deck file, put its https address, URL-encoded, after `url=` (a GitHub `blob` page
link works too). Only http(s) addresses are accepted. A deck added from a link remembers where it came
from, so it can be updated from there later.

## Sources

- JLPT word lists: [tanos.co.uk](http://www.tanos.co.uk/jlpt/), via
  [jamsinclair/open-anki-jlpt-decks](https://github.com/jamsinclair/open-anki-jlpt-decks) (MIT,
  see `sources/jlpt/LICENSE-open-anki-jlpt-decks`). `sources/jlpt/build.py` rebuilds the decks from
  the CSVs.

Deck files keep their paths: Ankipan offers updates only for a file fetched again from the address
it was added from.
