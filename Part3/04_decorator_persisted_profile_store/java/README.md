# Decorator - Persisted Profile Store (Java)

- Production code: `ProfileStores.java`
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
- test result: **11/11**, median process time 93.9 ms
- source LOC (lizard NLOC, production files only): 71; max function CC: 2

## Language notes
Classic GoF form: interface + abstract forwarding decorator holding the wrapped component; storage/log injected as Map/List. Max-CC function: BasicStore::set.
