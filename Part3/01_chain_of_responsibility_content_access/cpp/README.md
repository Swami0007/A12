# Chain of Responsibility - Content Access Rule Chain (C++)

- Production code: `content_access.hpp`
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
- test result: **16/16**, median process time 1.9 ms
- source LOC (lizard NLOC, production files only): 86; max function CC: 6

## Language notes
Ownership of the chain via std::unique_ptr (each link owns the next); std::optional<Decision> as 'pass on' signal; virtual dispatch; header-only. Max-CC function: access::MaturityRule::evaluate.
