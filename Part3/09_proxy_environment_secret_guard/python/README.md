# Proxy - Environment Secret Guard (Python)

- Production code: `env_guard.py`
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
- test result: **10/10**, median process time 13.8 ms
- source LOC (lizard NLOC, production files only): 11; max function CC: 4

## Language notes
__getattr__ on a wrapper class intercepts attribute reads (env.STRIPE_API_KEY), the closest analogue of a property trap; object.__getattribute__ reaches the real data. Max-CC function: __getattr__.
