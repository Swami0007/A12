# Strategy - Sign-in Provider Strategy (Java)

- Production code: `SignIn.java`
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
- test result: **10/10**, median process time 74.8 ms
- source LOC (lizard NLOC, production files only): 55; max function CC: 3

## Language notes
Strategy interface with three final classes; a Map<String, Supplier<Provider>> acts as the provider registry; Optional<String> separates 'no profile' from errors. Max-CC function: NextAuth::NextAuth.
