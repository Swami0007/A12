# Proxy - Environment Secret Guard (JavaScript)

- Production code: `envGuard.js`
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
- test result: **10/10**, median process time 31.9 ms
- source LOC (lizard NLOC, production files only): 16; max function CC: 5

## Language notes
Identical mechanism to the source: new Proxy(target, {get}) traps property access on the plain object, so clients write env.NAME unchanged. Max-CC function: createEnv.
