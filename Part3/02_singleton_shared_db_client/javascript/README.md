# Singleton - Shared Prisma Database Client (JavaScript)

- Production code: `sharedDbClient.js`
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
- test result: **9/9**, median process time 35.7 ms
- source LOC (lizard NLOC, production files only): 17; max function CC: 5

## Language notes
Closest to the source: ?? for reuse-or-create and an object standing in for globalThis; module cache gives the singleton in real code. Max-CC function: loadDbModule.
