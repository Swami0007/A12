# Strategy - Sign-in Provider Strategy (JavaScript)

- Production code: `signIn.js`
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
- test result: **10/10**, median process time 30.0 ms
- source LOC (lizard NLOC, production files only): 31; max function CC: 3

## Language notes
Like next-auth: each provider is a factory returning a config object {id, authorize}; the context only needs the shape (duck typing). Max-CC function: signIn.
