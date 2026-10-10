# Adapter - NextAuth Prisma Persistence Adapter (Python)

- Production code: `auth_adapters.py`
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
- source LOC (lizard NLOC, production files only): 37; max function CC: 3

## Language notes
Object adapter with plain dicts as the ORM's data/where arguments; returning None for 'no user'; duck typing means the Target is only a convention (could add typing.Protocol). Max-CC function: find_unique.
