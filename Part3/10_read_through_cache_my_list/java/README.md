# Read-Through Cache - My List Query Cache (Java)

- Production code: `MyListCache.java`
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
- test result: **9/9**, median process time 87.8 ms
- source LOC (lizard NLOC, production files only): 37; max function CC: 2

## Language notes
Generic QueryCache<K,V> with Supplier<V> loader; HashMap.computeIfAbsent is a built-in read-through primitive; lists copied with List.copyOf to keep cached values immutable. Max-CC function: MyListStore::add.
