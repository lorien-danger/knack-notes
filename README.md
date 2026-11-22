# Notes

The keys of a piano and their names, for someone who has never played: see a key lit and say its name; see a name and
play that key. Every key from F3 to G5, white and black, under every name it usually goes by: 27 keys, 38 rows. A
dataset for [Knack](https://github.com/lorien-danger/knack): add it by this repo's link, or by its folder path.

It is the step before [knack-chords](https://github.com/lorien-danger/knack-chords): before you can play E♭ G B♭ you
have to know which key E♭ is. The thing learned is a key's name wherever the key is on the keyboard, so each name
comes up at every place it is on the keyboard (C in two octaves, F and G in three), and the only thing that stays the
same between them is the name.

| column | type | what it is |
|---|---|---|
| name | plain | the key's name: *C*, *F♯*, *G♭* |
| key | notes, `octave: false` | the key, lit on a keyboard from F3 to G5 at its own place, played on the app's piano. Answered by playing that note **in any octave**: any C is right for *C* |
| full name | plain | the name and the octave: *C4* (middle C), *F♯3*, *G♭3*. The title of a row; every row has its own |
| place | notes, `octave: true` | the same key, where only that very key is right: *C4* is not *C5* |

Suggested decks (a deck is asked every way round, so each of these is both directions):

- **Name the key:** see a key lit, say its name (both names, for a black key); see a name, play it anywhere.
- **Name the key and octave:** the same with the octave: see a key lit, say *C4*; see *G♭3*, play that very key.
  For later, once the names come without thinking.

There are no sounds of its own: the app's keyboard plays a key on its piano when it is shown or tapped.

## The keys

| | F3 to B3 | C4 to B4 | C5 to G5 |
|---|---|---|---|
| white | F G A B | C D E F G A B | C D E F G |
| black | F♯/G♭ G♯/A♭ A♯/B♭ | C♯/D♭ D♯/E♭ F♯/G♭ G♯/A♭ A♯/B♭ | C♯/D♭ D♯/E♭ F♯/G♭ |

The choices made, and why:

- **Which keys.** F3 to G5 is the keyboard of an FM-1 groovebox, so what is learned here is a real keyboard's
  layout, and it is nearly the stretch of knack-chords' keyboard (F♯3 to G5), so the two look alike. It is two octaves
  and a bit: 16 white keys, about 22 px each on a phone held upright, large enough to tap. Every name is in at least
  two octaves (C, D, E, A, B and the black keys between them in two; F, G and F♯/G♭ in three), so a name is never
  one place.
- **One row for each name.** A white key has one name. A black key has two, after the white keys on either side of
  it: the one below sharpened and the one above flattened (C♯ and D♭ are the same key). Each name is a row of its own,
  with the same key. So:
  - shown a black key lit, both names are right. Offered a few names to choose from, both are asked for: choosing
    both is right, one of them is partly right with the other marked *Missed*. Typed in the open, one name is taken
    and marked right (the app takes one value there). Either way both names are shown afterwards, each with the key;
  - shown *D♭*, you play that key; shown *C♯*, the same key. Each name is asked on its own, so each is learned on its
    own, not only as half of a pair;
  - the key column writes each row's key in its own spelling (`D♭4` in the D♭ row).

  The other way, one row per key with a column holding both names (`parts`), was weighed and not chosen: it can never
  show *D♭* alone and ask for the key, which is how a name is met in a chord or a song, so a learner would only ever
  see the pair.
- **Which names are left out.** E♯ (the F key), F♭ (E), B♯ (C), C♭ (B), and double sharps and flats. They are real
  but rare: met in a few keys' scales and in chord spellings, where knack-chords spells them with the key shown. Each
  names a white key that already has a plain name, so with them a beginner would be asked for two names for a white
  key before knowing one.
- **Which octave counts.** In *Name the key* the key column has `"octave": false`: the keys are written with their
  octaves (`C4`, `C5`) so that each is lit at its own place, but playing any C is right for *C*. So a C is shown at
  different places on different questions, and the name is learned wherever it is, not as one drawing.
- **The octave deck.** *Name the key and octave* uses `full name` and `place` (`"octave": true`): the same keys,
  where now the octave counts. Octaves are numbered as in the app and most music software: each octave starts on C,
  and middle C is C4. This keyboard has C4 in its middle, F3 to B3 below it and C5 to G5 above. It is a later step,
  so it is the second deck, and its columns are not in the first.

## How it behaves in the app

Checked in Knack at `0781e9d` (after #36 and #39) by practising both decks both ways, about 650 questions at phone
size (390×844) in Chromium and WebKit, answering from the theory and now and then wrongly on purpose. In *Name the
key* every one of the 27 keys came up lit, and every name was asked and played, in more than one octave.
`build/screenshots/` has what it looks like.

- Rows that share a name are one value: *C* is offered once, never twice, and a C played in any octave is right.
- Rows that show the same key are one question: a lit C♯4 asks for C♯ and D♭ together, and choosing both is right.
- Nothing was offered twice, and no right answer was marked partly right, *Missed* or wrong.
- Some of what the app does with this table is not what a learner should see. These are the app's to change, not
  the table's, and are written up with their causes on
  [knack-chords#2](https://github.com/lorien-danger/knack-chords/issues/2):
  - shown a name and offered a few keyboards, it says *Tap all that match* though only one is right;
  - while a question is asked, the keyboard writes *C4* and *C5* on the Cs, which answers every question about a C
    and every question of the octave deck;
  - after an answer, a key is named as most of the column spells it (*A♯*), not as the row asked (*B♭*): *B in place
    of A♯* for a question about B♭;
  - a right answer in another octave is shown at the row's key, not the key played (D5 played, D4 shown);
  - naming a black key in the open, only one of its names can be given.

## Checks

`build/check.py` uses nothing of `build.ts`. It lays out a piano's 88 keys again from scratch, as a keyboard is made:
white keys lettered A to G from the bottom key (A0), a black key between every two white keys except B–C and E–F,
each black key named after both of its neighbours, the octave number going up at every C, middle C the 40th key and
A4 the 49th at 440 Hz. Then it checks that:

- the rows are exactly the keys from F3 to G5, each once under each of its names, with no other spellings;
- each row's key is its name and octave, and that name is that key: its place among the 88 and its pitch, worked out
  from the name alone (whole and half steps from A4), agree;
- the two names of each black key are an enharmonic pair: the same key and pitch, a sharp and the flat of the next
  letter up;
- the full name is the name and octave, the place is the same key, and the columns and decks are as described here.

The last run gave:

    38 rows: the 27 keys from F3 (174.61 Hz) to G5 (783.99 Hz), 16 white with one name and 11 black with two
    names, keys, pitches, octaves, enharmonic pairs and columns checked against a keyboard laid out from A0
    all good

## Building it

    cd build && npm install
    npx tsx build.ts     # writes columns.json and rows.jsonl
    python3 check.py

The build needs only Node and tsx (no Knack checkout: there are no sounds to render), and has no randomness: building
again gives the same files. To change the range, change `LOWEST` and `HIGHEST` in `build.ts` and the range in
`check.py`.

## Licence

The rows, columns and the build and check scripts are dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
