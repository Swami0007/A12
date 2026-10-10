# Facade - TMDB Catalogue Facade (JavaScript)

- Production code: `tmdbCatalogue.js`
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
- test result: **10/10**, median process time 32.4 ms
- source LOC (lizard NLOC, production files only): 34; max function CC: 3

## Language notes
Only async version: Promise.all over injected fetch-like client, exactly like the refactored source; template literals build URLs. Max-CC function: getShows.
