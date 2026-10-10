# Singleton - Shared Prisma Database Client (Java)

- Production code: `SharedDbClient.java`
- Test runner (kept separate): `Runner.java`
- Shared fixture and specification: `../test-cases/cases.tsv`, `../test-cases/spec.md`
- Runtime / compiler: javac 21.0.12.1 / openjdk version "21.0.12.1" 2026-08-18

## Run (working folder: this folder)
```
javac -d build *.java
java -cp build Runner ../test-cases/cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass.

## Result recorded in data/cross_language.csv
- test result: **9/9**, median process time 75.1 ms
- source LOC (lizard NLOC, production files only): 28; max function CC: 4

## Language notes
Holder is an explicit ProcessGlobals object (Java has no globalThis); idiomatic Java would use a static holder / enum singleton, which cannot be reset per test case. Max-CC function: DbModule::DbModule.
