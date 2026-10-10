# Part 1 - all candidates considered (scope: code/src, prisma/schema.prisma @ 676e5dd)

Method: for each of the seven case-study areas we listed the entry files, read them fully,
followed every import/call one hop (and into node_modules where a role is played by a
dependency), and only confirmed a pattern when intent, the role relationships and the
runtime delegation were all visible in code. Names, comments or an LLM claim alone were
never accepted. Line-range checks: `python3 Part1/evidence/verify_locations.py data/patterns.csv`
(log: `Part1/evidence/location_check.log`, 90 locations, 0 problems).

| Area | Files inspected |
|---|---|
| User management | server/api/routers/user.ts, profile.ts, icon.ts; components/forms/*; stores/profile.ts; app/(dashboard)/* |
| Video catalogue | lib/fetchers.ts; app/(shows)/*; components/shows-*.tsx, hero.tsx, show-modal.tsx; stores/modal.ts, search.ts |
| Subscription | config/subscriptions.ts, plans.ts; lib/subscription.ts, stripe.ts; app/api/users/stripe, app/api/webhooks/stripe; components/forms/billing-form.tsx, account-form.tsx |
| Recommendation | app/(shows)/page.tsx, new-and-popular/page.tsx, lib/fetchers.ts (only fixed TMDB lists exist) |
| Authentication | server/auth.ts; lib/session.ts; pages/api/auth/[...nextauth].ts; server/api/trpc.ts |
| Content access | server/api/trpc.ts; components/screens/profiles-screen.tsx; components/forms/pin-form.tsx; app/(shows)/layout.tsx |
| Caching | lib/api/api.ts, client.ts; @trpc/next-layout/*; components/show-modal.tsx; next.config.mjs |

Excluded: components/ui/* (shadcn primitives, generated UI kit), styles/, public/, app/(docs)
(static help/terms text), app/api/og (Open Graph image), node_modules except where a role is
mapped.

## Confirmed: 10 types, 14 instances (data/patterns.csv)

## Rejected (6)
| Candidate | Where | Reason |
|---|---|---|
| Caching Proxy for server components (createTRPCNextLayout) | src/@trpc/next-layout/server/createTrpcNextLayout.tsx:89-168 | Real proxy + QueryClient cache structure, but `grep -rn createTRPCNextLayout src` finds no importer: dead code at baseline, not part of any running collaboration. |
| Factory Method (createTRPCContext / createInnerTRPCContext) | server/api/trpc.ts:47-69 | Plain factory functions; no creator hierarchy or overridable creation step, so not GoF Factory Method. Recorded as simple-factory idiom only. |
| Repository | server/api/routers/*.ts | Routers call ctx.prisma.<model> directly; no repository abstraction exists. (Prisma itself is a data-mapper style ORM - dependency, not mapped.) |
| Template Method (nested layouts) | app/**/layout.tsx | Layouts compose children; no base algorithm with overridable steps. |
| Recommendation strategy / engine | app/(shows)/page.tsx:13-42, lib/fetchers.ts | Rows are fixed TMDB queries (trending, top rated, genre ids 28/35/27/10749/99). No user signal is used, so no recommendation pattern exists at baseline. |
| Debounce as a design pattern | components/debounced-input.tsx:44-50 | UI timing technique (setTimeout reset) - not a GoF/GRASP/architecture pattern. |

## Uncertain (4)
| Candidate | Where | Why uncertain |
|---|---|---|
| Observer / publish-subscribe via Stripe webhook | app/api/webhooks/stripe/route.ts:8-76 | Only the subscriber side is in the code; the subscription (endpoint registration) lives in Stripe dashboard config, and dispatch is an if-chain on event.type. Cannot confirm both roles from source. |
| Protection Proxy for profile PIN gate | components/screens/profiles-screen.tsx:43-143; forms/pin-form.tsx:16-26 | ProfilesScreen wraps children and decides whether to render them, but there is no shared interface with the protected object - it is conditional rendering. Also note: the PIN is sent to the browser and compared client-side (pin-form.tsx:19), so it is not a real access control. |
| Implicit server data cache (Next.js fetch) | lib/fetchers.ts:15-41 | Next 13 app router caches `fetch` by default, but the code sets no cache/revalidate option; behaviour comes entirely from the framework and was not observed at runtime here (no TMDB access in the sandbox). |
| Facade over session / subscription lookup | lib/session.ts:4-11; lib/subscription.ts:6-53 | Thin wrappers: getCurrentUser hides authOptions, getUserSubscriptionPlan joins DB fields with plan config and an expiry rule. Too small / single-subsystem to separate from ordinary helper functions. |

Observation scope: static reading of the baseline + typecheck; no runtime session with
real Stripe/TMDB/Google credentials was possible in the analysis environment.
