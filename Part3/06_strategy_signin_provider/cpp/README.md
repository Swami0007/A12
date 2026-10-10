# Strategy - Sign-in Provider Strategy (C++)

- Production code: `sign_in.hpp`
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
- test result: **10/10**, median process time 2.3 ms
- source LOC (lizard NLOC, production files only): 63; max function CC: 3

## Language notes
Abstract base + std::unique_ptr strategies in a std::map keyed by id; std::optional<std::string> for authorize(); std::regex for e-mail. Max-CC function: signin::NextAuth::NextAuth.
