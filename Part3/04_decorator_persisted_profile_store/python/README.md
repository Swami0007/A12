# Decorator - Persisted Profile Store (Python)

- Production code: `profile_stores.py`
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
- test result: **11/11**, median process time 15.3 ms
- source LOC (lizard NLOC, production files only): 37; max function CC: 2

## Language notes
Forwarding base class; decorators override only what they add; could also use __getattr__ delegation, kept explicit for parity. Max-CC function: set.
