# Singleton - Shared Prisma Database Client (C++)

- Production code: `shared_db_client.hpp`
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
- test result: **9/9**, median process time 2.2 ms
- source LOC (lizard NLOC, production files only): 28; max function CC: 4

## Language notes
Holder owns the client through std::shared_ptr so identity (pointer equality) survives reloads; a function-local static (Meyers singleton) is the usual C++ form. Max-CC function: db::DbModule::DbModule.
