# Chain of Responsibility - Content Access Rule Chain (Java)

- Production code: `ContentAccess.java`
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
- test result: **16/16**, median process time 81.7 ms
- source LOC (lizard NLOC, production files only): 69; max function CC: 5

## Language notes
Abstract class + final check() (template method); records for Show/Viewer/Decision; immutable Map.of/Set.of tables; static typing catches a wrong rule signature at compile time. Max-CC function: RegionRule::evaluate.
