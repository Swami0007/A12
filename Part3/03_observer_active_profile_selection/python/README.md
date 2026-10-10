# Observer - Active Profile Selection (Python)

- Production code: `profile_selection.py`
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
- test result: **11/11**, median process time 40.7 ms
- source LOC (lizard NLOC, production files only): 30; max function CC: 3

## Language notes
Protocol-free duck typing: any object with notify(); dict-as-ordered-set (dict.fromkeys) keeps order and uniqueness; observers are small classes. Max-CC function: set_state.
