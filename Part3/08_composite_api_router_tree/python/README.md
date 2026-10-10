# Composite - API Router Tree (Python)

- Production code: `router_tree.py`
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
- test result: **12/12**, median process time 14.5 ms
- source LOC (lizard NLOC, production files only): 36; max function CC: 4

## Language notes
Two classes with the same methods (no common base needed at run time); dict keeps child order; recursion with generators would also fit paths(). Max-CC function: paths.
