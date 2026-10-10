# Chain of Responsibility - Content Access Rule Chain (JavaScript)

- Production code: `contentAccess.js`
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
- test result: **16/16**, median process time 34.8 ms
- source LOC (lizard NLOC, production files only): 60; max function CC: 3

## Language notes
ES2022 class with private #next field and static tables; 'abstract' evaluate() can only throw at run time; decisions are plain object literals. Max-CC function: check.
