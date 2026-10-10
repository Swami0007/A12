# Read-Through Cache - My List Query Cache (JavaScript)

- Production code: `myListCache.js`
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
- test result: **9/9**, median process time 38.7 ms
- source LOC (lizard NLOC, production files only): 33; max function CC: 4

## Language notes
Map-based cache with loader closures, the same shape as React Query's fetchQuery(key, fn); arrays copied with spread so the backend cannot mutate cached data. Max-CC function: add.
