# Adapter - NextAuth Prisma Persistence Adapter (JavaScript)

- Production code: `authAdapters.js`
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
- test result: **9/9**, median process time 31.7 ms
- source LOC (lizard NLOC, production files only): 31; max function CC: 3

## Language notes
Like the real @next-auth/prisma-adapter: a factory returns an object literal whose methods translate to orm.user.create({data}) etc.; no class or interface. Max-CC function: findUnique.
