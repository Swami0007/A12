# Observer - Active Profile Selection (JavaScript)

- Production code: `profileSelection.js`
- Test runner (kept separate): `testRunner.js`
- Shared fixture and specification: `../test-cases/cases.tsv`, `../test-cases/spec.md`
- Runtime / compiler: Node.js v22.22.0

## Run (working folder: this folder)
```
node testRunner.js ../test-cases/cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass.

## Result recorded in data/cross_language.csv
- test result: **11/11**, median process time 32.9 ms
- source LOC (lizard NLOC, production files only): 24; max function CC: 3

## Language notes
Closest to zustand: listeners are functions in a Set (insertion-ordered); subscribe returns an unsubscribe closure; no interface needed. Max-CC function: setState.
