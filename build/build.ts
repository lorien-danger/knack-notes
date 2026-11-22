/**
 * Builds the dataset from nothing but this file: columns.json and rows.jsonl.
 *
 *     npx tsx build.ts
 *
 * One row for each name of each key from F3 to G5 (the keyboard of an FM-1): a white key has one name, a key between
 * two white keys has two (C♯ and D♭), and each name is a row of its own with the same key. Nothing is random:
 * building again gives the same files.
 */
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = join(import.meta.dirname, '..');

// ---------------------------------------------------------------------------------------------------------------
// The music

/** the white keys' letters, and how many semitones above C each is */
const LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
const NATURAL = [0, 2, 4, 5, 7, 9, 11];

/** a key as a MIDI number (middle C, C4, is 60), and the range: F3 to G5, the 27 keys of an FM-1's keyboard */
const LOWEST = 53; // F3
const HIGHEST = 79; // G5

/** a key's names: a white key its letter; a black key the letter below it sharpened, then the letter above it
 * flattened (C♯, D♭). Never the rarer spellings (E♯, F♭, B♯, C♭, double sharps and flats): see the README */
function namesOf(key: number): string[] {
	const pc = key % 12;
	const white = NATURAL.indexOf(pc);
	if (white >= 0) return [LETTERS[white]];
	return [LETTERS[NATURAL.indexOf(pc - 1)] + '♯', LETTERS[NATURAL.indexOf(pc + 1)] + '♭'];
}

/** the octave a key is in, as written after its name: each octave starts on C, and middle C is C4. (Only for the
 * names above, which never cross from one octave into another as B♯ and C♭ do.) */
const octaveOf = (key: number) => Math.floor(key / 12) - 1;

/** a name in ids: lower case, ♯ as s and ♭ as b (cs4, db4) */
const idOf = (name: string, octave: number) => name.toLowerCase().replace('♯', 's').replace('♭', 'b') + octave;

// ---------------------------------------------------------------------------------------------------------------
// Rows

const rows: Record<string, unknown>[] = [];
for (let key = LOWEST; key <= HIGHEST; key++) {
	const names = namesOf(key), octave = octaveOf(key);
	for (const name of names) {
		rows.push({
			id: idOf(name, octave),
			name,
			key: name + octave,
			'full name': name + octave,
			place: name + octave,
		});
	}
}
if (new Set(rows.map((r) => r.id)).size !== rows.length) throw new Error('Two rows with one id');

const columns = {
	name: 'Notes',
	item: 'key',
	items: 'keys',
	title: 'full name',
	practices: [
		{ name: 'Name the key', columns: ['name', 'key'] },
		{ name: 'Name the key and octave', columns: ['full name', 'place'] },
	],
	columns: [
		{ name: 'name', type: 'plain', label: 'Name' },
		{ name: 'key', type: 'notes', octave: false, label: 'Key' },
		{ name: 'full name', type: 'plain', label: 'Name and octave' },
		{ name: 'place', type: 'notes', octave: true, label: 'Key, in its octave' },
	],
};

writeFileSync(join(ROOT, 'columns.json'), JSON.stringify(columns, null, 1) + '\n');
writeFileSync(join(ROOT, 'rows.jsonl'), rows.map((r) => JSON.stringify(r)).join('\n') + '\n');
const black = rows.filter((r) => String(r.name).length > 1).length / 2;
console.log(`${rows.length} rows: ${HIGHEST - LOWEST + 1} keys from F3 to G5, ${HIGHEST - LOWEST + 1 - black} white with one name and ${black} black with two`);
