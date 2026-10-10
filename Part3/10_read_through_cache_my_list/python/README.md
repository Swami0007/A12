# Read-Through Cache - My List Query Cache (Python)

- Production code: `my_list_cache.py`
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
- test result: **9/9**, median process time 20.2 ms
- source LOC (lizard NLOC, production files only): 28; max function CC: 2

## Language notes
dict + callable loader; 'if key not in cache' miss test; functools.lru_cache would give read-through for pure functions but has no per-key invalidation. Max-CC function: fetch.
