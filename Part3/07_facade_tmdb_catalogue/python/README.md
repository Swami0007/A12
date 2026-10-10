# Facade - TMDB Catalogue Facade (Python)

- Production code: `tmdb_catalogue.py`
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
- test result: **10/10**, median process time 14.4 ms
- source LOC (lizard NLOC, production files only): 25; max function CC: 6

## Language notes
Row specs as tuples; dict keeps insertion order; synchronous here (asyncio.gather would mirror Promise.all). Max-CC function: _fetch_rows.
