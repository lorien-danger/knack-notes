"""Checks the dataset against the piano keyboard itself, using nothing of build.ts.

    python3 check.py

It lays out a piano's 88 keys again from scratch, the way the keyboard is made: white keys lettered A B C D E F G
over and over from the bottom (A0), with a black key between every two neighbouring white keys except B and C, and
E and F (the gaps that make the groups of two and three black keys). A black key is named after both white keys
beside it: the one below sharpened and the one above flattened. Octave numbers start again at every C, and the
fourth C from the bottom is middle C, C4 (the 40th key; A4, the 49th, is 440 Hz). Then:
  - the rows are exactly the keys from F3 to G5, the 27 keys of an FM-1's keyboard, each once under each of its names: one row for
    a white key, two for a black key, and no other spellings (no E♯, F♭, B♯, C♭, double sharps or double flats);
  - each row's key is written as its name and octave, and is that key on the keyboard (its place in the 88, and its
    pitch in Hz, worked out from the note's name alone, with no table of semitones);
  - the two names of a black key are an enharmonic pair: the same key, the same pitch, a letter apart;
  - the full name is the name and the octave; the column for the octave deck holds the same key;
  - the columns say what the README says (which octave counts where), and every deck is made of real columns.
"""
import json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
problems = []
def bad(msg):
    problems.append(msg)

# ---- the keyboard, laid out from the bottom key up ------------------------------------------------------------
WHITE_CYCLE = 'ABCDEFG'
NO_BLACK_AFTER = {'B', 'E'}  # B–C and E–F are next to each other with no black key between
keys = []  # (number 1..88, names, is_black)
letter_i, octave = 0, 0
n = 0
while n < 88:
    letter = WHITE_CYCLE[letter_i % 7]
    if letter == 'C' and n > 0:
        octave += 1
    n += 1
    keys.append((n, [f'{letter}{octave}'], False))
    nxt = WHITE_CYCLE[(letter_i + 1) % 7]
    nxt_oct = octave + (1 if nxt == 'C' else 0)
    if letter not in NO_BLACK_AFTER and n < 88:
        n += 1
        keys.append((n, [f'{letter}♯{octave}', f'{nxt}♭{nxt_oct}'], True))
    letter_i += 1
assert keys[0][1] == ['A0'] and keys[-1][1] == ['C8'] and len(keys) == 88, 'the keyboard is laid out wrongly'
by_name = {name: k for k in keys for name in k[1]}
assert by_name['C4'][0] == 40 and by_name['A4'][0] == 49, 'middle C or A4 is in the wrong place'

def hz(number):
    return 440 * 2 ** ((number - 49) / 12)

def pitch_from_name(name):
    """the pitch of a written note, from its letter, sign and octave alone: steps of the major scale counted as
    whole and half tones (E–F and B–C are the half tones), from A4 at 440 Hz"""
    m = re.fullmatch(r'([A-G])([♯♭]?)(\d)', name)
    if not m:
        return None
    letter, sign, octv = m[1], m[2], int(m[3])
    # half tones from C up to each letter, counted step by step
    steps, semis = 'CDEFGAB', 0
    for a, b in zip(steps, steps[1:]):
        if a == letter:
            break
        semis += 1 if (a, b) in (('E', 'F'), ('B', 'C')) else 2
    semis += {'': 0, '♯': 1, '♭': -1}[sign]
    from_a4 = (octv - 4) * 12 + semis - 9
    return 440 * 2 ** (from_a4 / 12)

# ---- the files ------------------------------------------------------------------------------------------------
columns = json.loads((ROOT / 'columns.json').read_text())
rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip()]

spec = {c['name']: c for c in columns['columns']}
want = {'name': ('plain', None), 'key': ('notes', False), 'full name': ('plain', None), 'place': ('notes', True)}
if set(spec) != set(want):
    bad(f'columns are {sorted(spec)}, not {sorted(want)}')
for c, (t, octv) in want.items():
    if c in spec and (spec[c]['type'] != t or spec[c].get('octave') != octv):
        bad(f'column {c}: {spec[c]}')
if columns.get('title') not in spec:
    bad('the title is not a column')
for p in columns.get('practices', []):
    if not all(c in spec for c in p['columns']):
        bad(f'deck {p["name"]} names a column that is not there')
if [p['columns'] for p in columns.get('practices', [])] != [['name', 'key'], ['full name', 'place']]:
    bad('the decks are not the two the README describes')

# ---- the rows -------------------------------------------------------------------------------------------------
LOW, HIGH = by_name['F3'][0], by_name['G5'][0]
in_range = [k for k in keys if LOW <= k[0] <= HIGH]
if len(in_range) != 27:
    bad(f'F3 to G5 is {len(in_range)} keys, not 27')
expected = {name: k for k in in_range for name in k[1]}
seen = {}
for r in rows:
    full = r.get('full name')
    if full in seen:
        bad(f'{full} is in two rows')
    seen[full] = r
    if full not in expected:
        bad(f'{full}: not a name of a key from F3 to G5 (or a spelling left out)')
        continue
    number, names, black = expected[full]
    m = re.fullmatch(r'([A-G][♯♭]?)(\d)', full)
    if r.get('name') != m[1]:
        bad(f'{full}: name {r.get("name")}')
    for c in ('key', 'place'):
        if r.get(c) != full:
            bad(f'{full}: {c} is {r.get(c)}')
    p = pitch_from_name(full)
    if p is None or abs(1200 * math.log2(p / hz(number))) > 0.01:
        bad(f'{full}: {p} Hz from its name, but key {number} is {hz(number):.3f} Hz')
    want_id = full.lower().replace('♯', 's').replace('♭', 'b')
    if r.get('id') != want_id:
        bad(f'{full}: id {r.get("id")}')
for name in expected:
    if name not in seen:
        bad(f'{name} has no row')

# the two names of each black key: the same key and pitch, on neighbouring letters, one sharp and one flat
pairs = 0
for number, names, black in in_range:
    if not black:
        if len(names) != 1 or len(names[0]) != 2:
            bad(f'white key {number} has names {names}')
        continue
    sharp, flat = names
    a, b = seen.get(sharp), seen.get(flat)
    if not a or not b:
        continue
    pa, pb = pitch_from_name(sharp), pitch_from_name(flat)
    if abs(1200 * math.log2(pa / pb)) > 0.01:
        bad(f'{sharp} and {flat} are not one pitch')
    if (WHITE_CYCLE.index(flat[0]) - WHITE_CYCLE.index(sharp[0])) % 7 != 1 or '♯' not in sharp or '♭' not in flat:
        bad(f'{sharp} and {flat} are not a sharp and the flat of the next letter')
    pairs += 1

whites = sum(1 for k in in_range if not k[2])
if problems:
    print('\n'.join(problems))
    print(f'{len(problems)} problems')
    sys.exit(1)
print(f'{len(rows)} rows: the {len(in_range)} keys from F3 ({hz(LOW):.2f} Hz) to G5 ({hz(HIGH):.2f} Hz), '
      f'{whites} white with one name and {pairs} black with two')
print('names, keys, pitches, octaves, enharmonic pairs and columns checked against a keyboard laid out from A0')
print('all good')
