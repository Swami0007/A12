# Composite - API Router Tree (Java)

- Production code: `RouterTree.java`
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
- test result: **12/12**, median process time 93.0 ms
- source LOC (lizard NLOC, production files only): 68; max function CC: 3

## Language notes
Sealed interface Node permits Procedure and Router (Java 17+), so the type system knows the only two node kinds; records for leaves; LinkedHashMap keeps child order. Max-CC function: Router::resolve.
