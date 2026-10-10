# Chain of Responsibility - Content Access Rule Chain (Python)

- Production code: `content_access.py`
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
- test result: **16/16**, median process time 40.1 ms
- source LOC (lizard NLOC, production files only): 68; max function CC: 5

## Language notes
ABC + @abstractmethod enforces evaluate(); frozen dataclasses; set intersection (show.genres & blocked) replaces the loop; links are checked only at run time. Max-CC function: evaluate.
