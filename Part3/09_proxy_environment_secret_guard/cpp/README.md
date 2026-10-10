# Proxy - Environment Secret Guard (C++)

- Production code: `env_guard.hpp`
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
- test result: **10/10**, median process time 1.7 ms
- source LOC (lizard NLOC, production files only): 39; max function CC: 4

## Language notes
No run-time interception: the proxy is a class implementing the same abstract Env interface and forwarding to the real one; checks are compiled in. Max-CC function: envguard::EnvGuard::get.
