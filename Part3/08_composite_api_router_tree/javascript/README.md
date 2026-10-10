# Composite - API Router Tree (JavaScript)

- Production code: `routerTree.js`
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
- test result: **12/12**, median process time 31.8 ms
- source LOC (lizard NLOC, production files only): 36; max function CC: 3

## Language notes
Nodes are plain objects with the same methods, like tRPC's router records (procedures and routers mixed in one record); Map keeps order. Max-CC function: resolve.
