# Facade - TMDB Catalogue Facade (Java)

- Production code: `TmdbCatalogue.java`
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
- test result: **10/10**, median process time 100.1 ms
- source LOC (lizard NLOC, production files only): 49; max function CC: 4

## Language notes
Facade class over an HttpClient interface; row specs are records in a List; LinkedHashMap keeps row order; synchronous (real code would use HttpClient.sendAsync + CompletableFuture.allOf). Max-CC function: Row::fetchRows.
