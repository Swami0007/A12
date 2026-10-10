# Singleton - Shared Prisma Database Client (Python)

- Production code: `shared_db_client.py`
- Test runner (kept separate): `test_runner.py`
- Shared fixture and specification: `../test-cases/cases.tsv`, `../test-cases/spec.md`
- Runtime / compiler: Python 3.13.16

## Run (working folder: this folder)
```
python3 test_runner.py ../test-cases/cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass.

## Result recorded in data/cross_language.csv
- test result: **9/9**, median process time 14.1 ms
- source LOC (lizard NLOC, production files only): 15; max function CC: 4

## Language notes
Module-level objects are already singletons via the import cache; the holder mirrors globalThis with a plain object; 'or' expresses ??. Max-CC function: __init__.
