# Decorator - Persisted Profile Store (JavaScript)

- Production code: `profileStores.js`
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
- test result: **11/11**, median process time 33.1 ms
- source LOC (lizard NLOC, production files only): 34; max function CC: 2

## Language notes
Zustand-style functional decorators: each is a function store -> store that spreads the inner object and overrides set/clearStorage; no classes needed. Max-CC function: basicStore.
