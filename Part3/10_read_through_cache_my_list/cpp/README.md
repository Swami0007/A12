# Read-Through Cache - My List Query Cache (C++)

- Production code: `my_list_cache.hpp`
- Test runner (kept separate): `test_runner.cpp`
- Shared fixture and specification: `../test-cases/cases.tsv`, `../test-cases/spec.md`
- Runtime / compiler: g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 -std=c++17 -O2

## Run (working folder: this folder)
```
g++ -std=c++17 -O2 -Wall -o build/test_runner test_runner.cpp
./build/test_runner ../test-cases/cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass.

## Result recorded in data/cross_language.csv
- test result: **9/9**, median process time 1.7 ms
- source LOC (lizard NLOC, production files only): 42; max function CC: 2

## Language notes
Class template QueryCache<V> with std::function loader; std::map::try_emplace/find; values copied into the cache (value semantics give isolation for free). Max-CC function: mylist::QueryCache::fetch.
