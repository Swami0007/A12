"""Single source of truth for the Part 1 pattern records of team A12.

Run from the A12 folder:  python3 Part1/evidence/part1_patterns.py
Writes data/patterns.csv and data/pattern_counts.csv (baseline rows).
Every location below was checked by hand against code/ (baseline commit
676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258). Dependency locations point into
node_modules of that commit's yarn.lock (versions listed in README.md).
"""
import csv
import os

SV = "original@676e5dd"

# Each record: pattern, category, instance, roles[(role, symbol, location)],
# intent/evidence text, concrete participant count (variable-role implementations).
PATTERNS = [
    dict(
        pattern="Chain of Responsibility", ptype="Behavioral (GoF); tRPC middleware idiom",
        instance="Authenticated Procedure Pipeline", origin="application (create-t3-app scaffold) on framework",
        roles=[
            ("Handler", "tRPC MiddlewareFunction created by t.middleware", "dependency @trpc/server@10.28.0"),
            ("ConcreteHandler", "enforceUserIsAuthed", "code/src/server/api/trpc.ts:109-119"),
            ("Chain assembly", "protectedProcedure = t.procedure.use(enforceUserIsAuthed)", "code/src/server/api/trpc.ts:129"),
            ("Terminal handler", "procedure resolvers e.g. profileRouter.getAll", "code/src/server/api/routers/profile.ts:7-15"),
            ("Client", "createNextApiHandler (tRPC HTTP entry point)", "code/src/pages/api/trpc/[trpc].ts:8-19"),
        ],
        evidence="Problem: every private procedure must reject anonymous callers. enforceUserIsAuthed inspects ctx.session and either throws TRPCError UNAUTHORIZED (stops the chain) or calls next({ctx}) with a narrowed session, passing the request to the next link. protectedProcedure attaches the handler once; 18 of 19 procedures in user/profile/icon/myList routers are built on it, so the check runs before each resolver without being repeated.",
        concrete=1,
    ),
    dict(
        pattern="Singleton", ptype="Creational (GoF)",
        instance="Shared Prisma Database Client", origin="application (create-t3-app scaffold)",
        roles=[
            ("Singleton", "prisma (PrismaClient instance)", "code/src/server/db.ts:9-14"),
            ("Instance holder", "globalForPrisma (globalThis cache)", "code/src/server/db.ts:5-7,16"),
            ("Client", "createInnerTRPCContext", "code/src/server/api/trpc.ts:47-52"),
            ("Client", "authOptions.adapter = PrismaAdapter(prisma)", "code/src/server/auth.ts:48"),
            ("Client", "getUserSubscriptionPlan", "code/src/lib/subscription.ts:6-53"),
            ("Client", "Stripe webhook POST", "code/src/app/api/webhooks/stripe/route.ts:8-76"),
        ],
        evidence="Problem: Next.js hot reload re-evaluates modules, which would open a new connection pool each time. db.ts reuses globalForPrisma.prisma if present (??) and only constructs PrismaClient once, then stores it on globalThis outside production. All server code imports the same `prisma` export.",
        concrete=1,
    ),
    dict(
        pattern="Singleton", ptype="Creational (GoF); ES-module singleton idiom",
        instance="Stripe API Client", origin="application",
        roles=[
            ("Singleton", "stripe (Stripe instance)", "code/src/lib/stripe.ts:4-7"),
            ("Client", "Stripe webhook POST", "code/src/app/api/webhooks/stripe/route.ts:8-76"),
            ("Client", "checkout/portal POST", "code/src/app/api/users/stripe/route.ts:14-115"),
            ("Client", "PlansPage", "code/src/app/(auth)/login/plans/page.tsx:17-60"),
            ("Client", "AccountPage", "code/src/app/(dashboard)/account/page.tsx:16-61"),
        ],
        evidence="One configured Stripe client (API key, apiVersion 2022-11-15) is created at module load and exported; the ES module cache guarantees a single instance per server process. Four call sites share it instead of constructing their own. No global guard as in db.ts, so it relies on module caching only (noted as weaker form).",
        concrete=1,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
        instance="Show Modal Selection", origin="application on dependency (zustand@4.3.8)",
        roles=[
            ("Subject", "zustand StoreApi (subscribe/setState) created by create()", "dependency zustand@4.3.8"),
            ("ConcreteSubject", "useModalStore", "code/src/stores/modal.ts:13-20"),
            ("Publisher (calls setState)", "ShowCard onClick", "code/src/components/shows-carousel.tsx:93-113"),
            ("ConcreteObserver", "ShowsContainer", "code/src/components/shows-container.tsx:22-65"),
            ("ConcreteObserver", "ShowModal", "code/src/components/show-modal.tsx:30-296"),
            ("ConcreteObserver", "Hero", "code/src/components/hero.tsx:17-102"),
            ("ConcreteObserver", "ShowsGrid", "code/src/components/shows-grid.tsx:13-48"),
        ],
        evidence="Selecting a poster calls useModalStore.setState({show, open, play}) (shows-carousel.tsx:105-109). Components that called useModalStore() are subscribed by the hook and re-render when state changes: ShowsContainer/ShowsGrid open ShowModal, ShowModal fetches the trailer for the new show (show-modal.tsx:45-74). Publisher and observers never reference each other.",
        concrete=4,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
        instance="Active Profile Selection", origin="application on dependency (zustand@4.3.8)",
        roles=[
            ("Subject", "zustand StoreApi", "dependency zustand@4.3.8"),
            ("ConcreteSubject", "useProfileStore", "code/src/stores/profile.ts:12-27"),
            ("Publisher", "ProfilesScreen profile button / SiteHeader menu / siteConfig sign-out", "code/src/components/screens/profiles-screen.tsx:86-91; code/src/components/layouts/site-header.tsx:150-155; code/src/config/site.ts:57"),
            ("ConcreteObserver", "ProfilesScreen", "code/src/components/screens/profiles-screen.tsx:24-144"),
            ("ConcreteObserver", "PinForm", "code/src/components/forms/pin-form.tsx:10-104"),
            ("ConcreteObserver", "ShowsContainer", "code/src/components/shows-container.tsx:22-65"),
            ("ConcreteObserver", "ShowModal", "code/src/components/show-modal.tsx:30-296"),
            ("ConcreteObserver", "SiteHeader", "code/src/components/layouts/site-header.tsx:35-261"),
            ("ConcreteObserver", "MyShows", "code/src/components/my-shows.tsx:16-54"),
        ],
        evidence="The selected profile and the PIN-gate flag live in one store. Setting {profile, pinForm} makes ProfilesScreen switch between profile picker, PinForm and the app shell (profiles-screen.tsx:43-143); ShowsContainer/ShowModal/MyShows re-query My List for the new profile id. Six components subscribe; three places publish.",
        concrete=6,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
        instance="Search Results Broadcast", origin="application on dependency (zustand@4.3.8)",
        roles=[
            ("Subject", "zustand StoreApi", "dependency zustand@4.3.8"),
            ("ConcreteSubject", "useSearchStore", "code/src/stores/search.ts:11-16"),
            ("Publisher", "SiteHeader.searchShowsByQuery", "code/src/components/layouts/site-header.tsx:51-55"),
            ("ConcreteObserver", "SiteHeader", "code/src/components/layouts/site-header.tsx:35-261"),
            ("ConcreteObserver", "ShowsContainer", "code/src/components/shows-container.tsx:22-65"),
            ("ConcreteObserver", "Hero", "code/src/components/hero.tsx:17-102"),
            ("ConcreteObserver", "MainNav", "code/src/components/layouts/main-nav.tsx:24-142"),
            ("ConcreteObserver", "MyShows", "code/src/components/my-shows.tsx:16-54"),
        ],
        evidence="SiteHeader writes query and results into useSearchStore; when query is non-empty ShowsContainer swaps carousels for ShowsGrid (shows-container.tsx:40-42) and Hero hides itself (hero.tsx:29-31); MainNav clears the query on navigation (main-nav.tsx:36-37). The search box does not know which views react.",
        concrete=5,
    ),
    dict(
        pattern="Decorator", ptype="Structural (GoF); Zustand middleware",
        instance="Persisted Profile Store", origin="application on dependency (zustand/middleware)",
        roles=[
            ("Component", "StateCreator<ProfileState>", "dependency zustand@4.3.8 (vanilla.d.ts)"),
            ("ConcreteComponent", "inline creator (set) => ({profile, setProfile, pinForm, setPinForm})", "code/src/stores/profile.ts:15-20"),
            ("ConcreteDecorator", "persist(..., {name, storage: sessionStorage})", "code/src/stores/profile.ts:14-25"),
            ("ConcreteDecorator", "devtools(...)", "code/src/stores/profile.ts:13-26"),
            ("Client", "create<ProfileState>()", "code/src/stores/profile.ts:12"),
        ],
        evidence="persist and devtools each take a StateCreator and return a StateCreator with the same shape, wrapping set/get to add sessionStorage persistence and Redux-devtools reporting. They are stacked devtools(persist(creator)); the modal and search stores use the undecorated creator, showing the behaviour is added per object without changing the creator.",
        concrete=3,
    ),
    dict(
        pattern="Adapter", ptype="Structural (GoF)",
        instance="NextAuth Prisma Persistence Adapter", origin="dependency (@next-auth/prisma-adapter@1.0.6) configured by application",
        roles=[
            ("Target", "Adapter (next-auth adapter interface)", "dependency next-auth@4.22.1 adapters.d.ts:57"),
            ("Adapter", "PrismaAdapter(p)", "dependency @next-auth/prisma-adapter@1.0.6 dist/index.js:206-264"),
            ("Adaptee", "prisma (PrismaClient)", "code/src/server/db.ts:9-14"),
            ("Client", "authOptions.adapter used by NextAuth handler", "code/src/server/auth.ts:38-64; code/src/pages/api/auth/[...nextauth].ts:4"),
        ],
        evidence="NextAuth persists users, accounts and sessions only through its Adapter interface (createUser, getUserByEmail, linkAccount, ...). PrismaAdapter returns an object implementing those methods by translating them to Prisma calls, e.g. createUser: (data) => p.user.create({data}) and getUserByEmail: (email) => p.user.findUnique({where:{email}}) (index.js:208-210). The app wires it with adapter: PrismaAdapter(prisma).",
        concrete=1,
    ),
    dict(
        pattern="Strategy", ptype="Behavioral (GoF)",
        instance="Sign-in Provider Strategy", origin="framework (next-auth@4.22.1) configured by application",
        roles=[
            ("Strategy", "Provider = OAuthConfig | EmailConfig | CredentialsConfig", "dependency next-auth@4.22.1 providers/index.d.ts:14"),
            ("ConcreteStrategy", "GoogleProvider({clientId, clientSecret})", "code/src/server/auth.ts:50-53"),
            ("Context", "NextAuth(authOptions) with providers[]", "code/src/server/auth.ts:38-64; code/src/pages/api/auth/[...nextauth].ts:4"),
        ],
        evidence="authOptions.providers is a list of interchangeable provider objects behind one Provider type; NextAuth selects the provider by id at sign-in and delegates the authorization/profile mapping to it. Only Google is configured; the commented block at auth.ts:54-62 documents adding more without changing NextAuth. Single concrete strategy, so variability is latent.",
        concrete=1,
    ),
    dict(
        pattern="Facade", ptype="Structural (GoF)",
        instance="TMDB Catalogue Facade", origin="application",
        roles=[
            ("Facade", "module lib/fetchers: getShows, getNewAndPopularShows, searchShows", "code/src/lib/fetchers.ts:5-77,82-122,124-142"),
            ("Subsystem", "TMDB REST endpoints (trending, top_rated, discover, popular, search/multi) + API key", "code/src/lib/fetchers.ts:15-41; code/src/env.mjs"),
            ("Client", "Home, MoviesPage, TVShowsPage", "code/src/app/(shows)/page.tsx:8-52; code/src/app/(shows)/movies/page.tsx:13-54; code/src/app/(shows)/tv-shows/page.tsx:12-51"),
            ("Client", "NewAndPopularPage", "code/src/app/(shows)/new-and-popular/page.tsx:12-39"),
            ("Client", "SiteHeader.searchShowsByQuery", "code/src/components/layouts/site-header.tsx:51-55"),
        ],
        evidence="Pages need categorised show lists, not URLs. getShows(mediaType) issues eight TMDB requests in parallel, checks all responses, parses JSON and returns one object of named rows; callers only call getShows('movie'). URL construction, API key, network errors and JSON shape are hidden behind three functions (module-level facade, no class).",
        concrete=1,
    ),
    dict(
        pattern="Composite", ptype="Structural (GoF); tRPC router tree",
        instance="API Router Tree", origin="application on framework (@trpc/server)",
        roles=[
            ("Component", "AnyRouter | AnyProcedure in ProcedureRouterRecord", "dependency @trpc/server@10.28.0"),
            ("Composite (root)", "appRouter", "code/src/server/api/root.ts:12-17"),
            ("Composite", "userRouter", "code/src/server/api/routers/user.ts:9-91"),
            ("Composite", "profileRouter", "code/src/server/api/routers/profile.ts:6-186"),
            ("Composite", "iconRouter", "code/src/server/api/routers/icon.ts:5-59"),
            ("Composite", "myListRouter", "code/src/server/api/routers/my-list.ts:6-184"),
            ("Leaf", "19 procedures e.g. profile.getAll", "code/src/server/api/routers/profile.ts:7-15"),
            ("Factory", "createTRPCRouter = t.router", "code/src/server/api/trpc.ts:97"),
        ],
        evidence="createTRPCRouter accepts a record whose values are procedures (leaves) or routers (composites); appRouter nests four routers that hold 19 procedures. Clients address any node uniformly by dotted path (api.profile.getAll), and the type AppRouter is the whole tree. The recursive DecoratedProcedureRecord type (src/@trpc/next-layout/server/createTrpcNextLayout.tsx:53-65) walks routers and procedures the same way.",
        concrete=5,
    ),
    dict(
        pattern="Proxy", ptype="Structural (GoF); remote proxy",
        instance="Pages-Router tRPC Client Proxy", origin="application on dependency (@trpc/next@10.28.0)",
        roles=[
            ("Subject", "AppRouter type", "code/src/server/api/root.ts:20"),
            ("RealSubject", "appRouter served by createNextApiHandler", "code/src/pages/api/trpc/[trpc].ts:8-19"),
            ("Proxy", "api = createTRPCNext<AppRouter>(...)", "code/src/lib/api/api.ts:21-54"),
            ("Transport", "loggerLink + httpBatchLink(/api/trpc)", "code/src/lib/api/api.ts:36-45"),
            ("Client", "ShowsContainer, ShowModal, ProfilesScreen, SiteHeader and 7 more components", "code/src/components/shows-container.tsx:32-36; code/src/components/show-modal.tsx:93-124"),
        ],
        evidence="Components call api.myList.getAll.useQuery(...) as if the server router were local. api is a JavaScript Proxy (createRecursiveProxy/createFlatProxy, @trpc/server dist index-4a823936.js:55,87) that turns each property path into an HTTP batch request to /api/trpc and returns typed results. Same typed interface as the real router (AppRouter).",
        concrete=1,
    ),
    dict(
        pattern="Proxy", ptype="Structural (GoF); remote proxy",
        instance="App-Router tRPC Client Proxy", origin="application (vendored src/@trpc/next-layout) on dependency",
        roles=[
            ("Subject", "AppRouter type", "code/src/server/api/root.ts:20"),
            ("RealSubject", "appRouter served by createNextApiHandler", "code/src/pages/api/trpc/[trpc].ts:8-19"),
            ("Proxy", "api = createTRPCNextBeta<AppRouter>(...)", "code/src/lib/api/client.ts:22-45"),
            ("Proxy factory", "createTRPCNextBeta -> createFlatProxy", "code/src/@trpc/next-layout/client/createTrpcNextBeta.tsx:48-93"),
            ("Provider", "TRPCProvider wraps RootLayout", "code/src/context/trpc-provider.tsx:7-9; code/src/app/layout.tsx:80-96"),
            ("Client", "AddProfileForm, EditProfileForm", "code/src/components/forms/add-profile-form.tsx:13; code/src/components/forms/edit-profile-form.tsx:15"),
        ],
        evidence="A second client proxy built with the vendored createTRPCNextBeta returns createFlatProxy((key) => ...) (createTrpcNextBeta.tsx:76-92): 'Provider' and 'useContext' are served locally, every other key is decorated into React-Query hooks that call the server. It also supplies the QueryClient used by the app. Two independent proxies for one Subject is recorded as a smell (duplicated getBaseUrl/links).",
        concrete=1,
    ),
    dict(
        pattern="Proxy", ptype="Structural (GoF); protection proxy",
        instance="Environment Secret Guard", origin="application (create-t3-app scaffold)",
        roles=[
            ("Subject", "MergedOutput (validated env shape)", "code/src/env.mjs:67-71"),
            ("RealSubject", "parsed.data (zod-validated variables)", "code/src/env.mjs:75-90"),
            ("Proxy", "env = new Proxy(parsed.data, {get})", "code/src/env.mjs:92-105"),
            ("Client", "10 modules importing env, e.g. lib/stripe.ts, lib/fetchers.ts, server/db.ts", "code/src/lib/stripe.ts:1-7; code/src/server/db.ts:3"),
        ],
        evidence="Server secrets (STRIPE_API_KEY, DATABASE_URL, ...) must never be read in browser bundles. Every module imports `env`, which is a Proxy whose get trap checks the caller side: on the client any non NEXT_PUBLIC_ key throws a descriptive error, otherwise the value is forwarded from the validated object (env.mjs:93-103). Same interface as the real object, access control added transparently.",
        concrete=1,
    ),
    dict(
        pattern="Read-Through Cache", ptype="Architecture (caching); React Query",
        instance="My List Query Cache", origin="application configuration on dependency (@tanstack/react-query@4.29.7)",
        roles=[
            ("Cache", "QueryClient created once per TRPCProvider", "code/src/@trpc/next-layout/client/createTrpcNextBeta.tsx:55-63"),
            ("Cache policy", "cacheTime: Infinity, staleTime: Infinity, refetchOnWindowFocus: false", "code/src/lib/api/client.ts:24-34"),
            ("Loader (data source)", "myListRouter.getAll", "code/src/server/api/routers/my-list.ts:7-12"),
            ("Reader", "ShowsContainer myShowsQuery", "code/src/components/shows-container.tsx:32-36"),
            ("Reader", "ShowModal myShowsQuery", "code/src/components/show-modal.tsx:98-102"),
            ("Invalidator", "ShowModal effect apiUtils.myList.getAll.invalidate()", "code/src/components/show-modal.tsx:127-130"),
        ],
        evidence="useQuery(key) returns cached data for the key (profile id) and only calls the loader on a miss or after invalidation; with staleTime Infinity, repeated renders of ShowsContainer and ShowModal share one fetch. After each add/remove mutation ShowModal invalidates the key so the next read reloads. Caller never talks to the data source directly.",
        concrete=1,
    ),
]


def roles_text(rec):
    return "; ".join(f"{r}={s}" for r, s, _ in rec["roles"])


def locs_text(rec):
    return "; ".join(f"{s}: {loc}" for _, s, loc in rec["roles"])


def main():
    os.makedirs("data", exist_ok=True)
    with open("data/patterns.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["source_version", "pattern_name", "pattern_type", "instance_name",
                    "participant_roles", "source_locations", "intent_and_evidence"])
        for rec in PATTERNS:
            w.writerow([SV, rec["pattern"], rec["ptype"], rec["instance"],
                        roles_text(rec), locs_text(rec), rec["evidence"]])
    counts = {}
    for rec in PATTERNS:
        counts[rec["pattern"]] = counts.get(rec["pattern"], 0) + 1
    with open("data/pattern_counts.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source_version", "summary", "pattern_name", "count"])
        for name, n in counts.items():
            w.writerow([SV, "per_pattern", name, n])
        w.writerow([SV, "total_pattern_types", "", len(counts)])
        w.writerow([SV, "total_pattern_instances", "", len(PATTERNS)])
    print("types", len(counts), "instances", len(PATTERNS),
          "concrete", sum(r["concrete"] for r in PATTERNS),
          "unique in-repo symbols", len(IN_REPO_SYMBOLS), "dependency symbols", len(DEP_SYMBOLS))


# Distinct mapped symbols; a symbol shared by several instances (e.g. ShowsContainer,
# prisma, AppRouter) is listed once.
IN_REPO_SYMBOLS = """enforceUserIsAuthed protectedProcedure profile.getAll trpcApiHandler prisma
globalForPrisma createInnerTRPCContext authOptions getUserSubscriptionPlan webhookPOST stripe
checkoutPOST PlansPage AccountPage useModalStore ShowCard ShowsContainer ShowModal Hero ShowsGrid
useProfileStore ProfilesScreen SiteHeader siteConfig PinForm MyShows useSearchStore MainNav
profileStateCreator getShows getNewAndPopularShows searchShows Home MoviesPage TVShowsPage
NewAndPopularPage appRouter userRouter profileRouter iconRouter myListRouter myList.getAll
createTRPCRouter AppRouter api(lib/api/api.ts) api(lib/api/client.ts) createTRPCNextBeta
TRPCProvider RootLayout AddProfileForm EditProfileForm nextAuthHandler
env parsedEnvData MergedOutput""".split()
DEP_SYMBOLS = """MiddlewareFunction StoreApi StateCreator persist devtools Adapter PrismaAdapter
Provider GoogleProvider AnyRouter createRecursiveProxy/createFlatProxy QueryClient""".split()


if __name__ == "__main__":
    main()
