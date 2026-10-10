# A12 - Design Pattern Analysis in a Next.js-Based Video Streaming Application

23CSE455 Design Patterns case study - OTT / video streaming application using React / Next.js.

| Roll number | Name | Batch |
|---|---|---|
| AM.SC.U4CSE23161 | Swaminathan A | CSE B |
| AM.SC.U4CSE23207 | Anna Ouseph | CSE C |
| AM.SC.U4CSE23230 | Leya Paul | CSE C |
| AM.SC.U4CSE23242 | Pooja Sathyan | CSE C |
| AM.SC.U4CSE23069 | Rahul Rajan | CSE A |

Report: `A12_Report.pdf` (source `A12_Report.tex`). Datasets: `data/`.

## Application and source
- Application: **netflx-web** - "An open source Netflix clone built using the new app router,
  server components, trpc, and everything new in Next.js 13" by sadmann7.
- URL: https://github.com/sadmann7/netflx-web (accessed 2026-10-10; 770 stars, 119 forks).
- Baseline commit: `676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258` (2024-06-12, "Merge pull request #11").
  Snapshot: `code/` (`git archive` of that commit).
- **Licence: the repository has no LICENSE file** (all rights reserved by default). The code is
  used here for academic analysis only; the course faculty approved this use for the case study.
- Evolved versions (Part 2) on branch `a12-evolution` of a local clone:

| Snapshot | Commit | Content |
|---|---|---|
| baseline | 676e5dd | original application |
| tests_only | d68c773 | vitest + characterization tests, no production change |
| CH01 | 3f79642 | premium content + Ultra plan |
| CH02 | e420dcf | regional restrictions |
| CH03 | f393031 | parental control (final; snapshot in `Part2/code/`) |

  Reproduce: `git clone https://github.com/sadmann7/netflx-web && cd netflx-web &&
  git checkout 676e5dd && git am <A12>/Part2/changes/patches/*.patch`.

## Environment (versions from `yarn.lock` / tools used)
Next.js 13.4.4 (`next ^13.3.1`), React 18.2.0, TypeScript 5.0.4, tRPC 10.28.0, NextAuth 4.22.1
(+ @next-auth/prisma-adapter 1.0.6), Prisma 4.14.1 (MySQL, `relationMode = "prisma"`),
Stripe 12.7.0, Zustand 4.3.8, @tanstack/react-query 4.29.7, Tailwind CSS 3.3.2.
Analysis machine: Node.js 22.22.0, yarn 1.22.22, vitest 1.6.0 (added in d68c773), lizard 1.24.1,
OpenJDK 21.0.12.1, Python 3.13.16, g++ 13.3.0, PlantUML (node-plantuml 0.9.0 jar) + Graphviz.

## Run / test commands
```
# application (needs .env from .env.example: MySQL URL, Google OAuth, TMDB key, Stripe keys)
cd Part2/code            # or code/ for the baseline
yarn install             # runs prisma generate
npx prisma db push       # create tables (CH03 adds Profile.maturityLevel)
yarn dev                 # http://localhost:3000
yarn stripe:listen       # forward Stripe webhooks (Stripe CLI)

# checks
yarn typecheck           # tsc --noEmit   (Part2/code only; baseline: npx tsc --noEmit)
yarn test                # vitest run     (Part2/code: 65/65)
```
Results in the analysis environment: `tsc --noEmit` passes for every snapshot; tests pass
(13/13 at d68c773, 29/29 CH01, 45/45 CH02, 65/65 CH03). `next build` could not be completed
there because the sandbox cannot reach Google Fonts (`next/font` download) - not a code error;
`yarn dev`/`yarn build` need to be run on a team machine with network access and the .env.
Prisma engines could not be downloaded in the sandbox either, so tests use an in-memory fake of
the Prisma client (`tests/helpers.ts`) and no MySQL instance was used.

## Scope
Inspected (Part 1): `src/server/**`, `src/lib/**`, `src/config/**`, `src/stores/**`,
`src/app/**` (except `(docs)` and `api/og`), `src/components/**` (except `ui/*`),
`src/@trpc/next-layout/**`, `src/env.mjs`, `prisma/schema.prisma`; dependency code only where a
pattern role lives there (next-auth, @next-auth/prisma-adapter, zustand, @trpc, react-query).
Excluded: `components/ui/*` (generated shadcn primitives), `styles/`, `public/`, `app/(docs)`
(static text), `app/api/og` (Open Graph image) - none touches the seven case-study areas.

## Measurement rules
- **Line ranges**: 1-based, inclusive, from the file in `code/` (baseline) or the snapshot named
  in `source_version`. Checked with `Part1/evidence/verify_locations.py` (start lines) and
  `Part2/evidence/locate.py` (bracket-balanced end lines).
- **Pattern counts**: one instance = one independent collaboration; two concrete classes in one
  collaboration are one instance. "Concrete participants" counts implementations of variable
  roles: ConcreteHandler, ConcreteObserver, ConcreteStrategy, ConcreteComponent/Decorator,
  Adapter, Singleton, Facade (module), Composite routers, Proxy, Cache, ConcreteClass.
- **LOC / complexity (Parts 2 and 3)**: lizard 1.24.1. LOC = lizard NLOC (no blank lines or
  comments). Part 2 scope = `src/` of each snapshot, `*.css` excluded, tests excluded
  (`Part2/evidence/run_snapshots.sh`). Part 3 scope = production snippet files only (runners
  excluded). Max CC = largest lizard cyclomatic complexity of a single function.
- **Timing (Part 3)**: compile first (not timed), then 1 warm-up and 5 measured runs of the test
  command on the same machine; reported value = median wall-clock time of the whole process
  (runtime start-up + reading the shared cases.tsv + running all cases). Raw times:
  `Part3/evidence/timings.csv`. Machine: Linux x86_64 cloud sandbox, shared CPU.

## Folder map
```
A12/
  README.md, A12_Report.tex, A12_Report.pdf, build_report.py (regenerates the .tex from data/)
  data/      patterns.csv, pattern_counts.csv, pattern_evolution.csv, cross_language.csv, llm.csv
  code/      original application source (676e5dd)
  test_result/baseline/   baseline typecheck/build/characterization logs
  Part1/     diagrams/ (PlantUML .puml + .png), evidence/ (scripts, candidates.md, checks), llm/
  Part2/     code/ (evolved source, CH03), changes/Change1..3 (requirement, diff, tests) + patches/,
             diagrams/, evidence/ (metrics, logs, scripts), llm/
  Part3/     NN_<pattern>_<problem>/{java,python,javascript,cpp,test-cases}/, evidence/, llm/, run_all.py,
             A12_slide.pdf (+ slides/A12_slide.tex)
```
The four CSVs are kept once in `data/` (the instructions ask not to repeat them inside Part folders).

## Limitations
- Static analysis + unit tests with a fake database; no end-to-end run with real Stripe / TMDB / Google.
- Region licences and premium titles are sample rules (originals row = premium; 3 licensed TMDB ids).
- The persisted (sessionStorage) profile keeps an old maturity rating until it is re-selected.
- Pre-existing issues reported, not fixed: client-side PIN check; profile/myList procedures do
  not check that a profileId belongs to the caller.
- lizard's TSX parsing is imperfect (see Part2/changes/Change1/README.md on the max-CCN artefact).
- Part 3 timings include runtime start-up and are machine-specific.
- LLM use: one Claude session generated most analysis code and text; see section 5 of the report
  and `data/llm.csv`. Human review entries must be completed by the team.
