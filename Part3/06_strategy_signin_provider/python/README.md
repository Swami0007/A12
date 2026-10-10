# Strategy - Sign-in Provider Strategy (Python)

- Production code: `sign_in.py`
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
- test result: **10/10**, median process time 19.8 ms
- source LOC (lizard NLOC, production files only): 29; max function CC: 3

## Language notes
Strategies are small classes with the same method; could equally be plain functions in a dict; regex via re.fullmatch for the e-mail rule. Max-CC function: __init__.
