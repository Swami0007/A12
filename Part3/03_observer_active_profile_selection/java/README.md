# Observer - Active Profile Selection (Java)

- Production code: `ProfileSelection.java`
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
- test result: **11/11**, median process time 82.9 ms
- source LOC (lizard NLOC, production files only): 44; max function CC: 3

## Language notes
Observer interface + LinkedHashSet keeps subscription order and set semantics; Consumer-style callbacks would also work; observers need explicit classes or lambdas. Max-CC function: ProfileStore::setState.
