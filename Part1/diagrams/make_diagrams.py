"""Writes editable PlantUML sources (*.puml) for Part 1 and renders PNGs.
Run from A12/:  python3 Part1/diagrams/make_diagrams.py
Needs java and plantuml.jar (path in PLANTUML_JAR, default ~/tools/plantuml.jar) + graphviz dot."""
import os
import subprocess

OUT = "Part1/diagrams"
HEAD = "@startuml\nskinparam classAttributeIconSize 0\nskinparam shadowing false\nhide empty members\n"

D = {}

D["00_architecture"] = """@startuml
skinparam shadowing false
skinparam componentStyle rectangle
title netflx-web @676e5dd - component view (Part 1 baseline)
actor Viewer
package "Browser (React client components)" {
  [Pages: (shows) / (dashboard) / (auth)] as UI
  [Zustand stores\\nmodal / profile / search] as Stores
  [tRPC client proxies\\nlib/api/api.ts, lib/api/client.ts] as Client
  [React Query cache\\n(QueryClient)] as RQ
}
package "Next.js 13 server (Vercel/Node)" {
  [App Router server components\\n(shows pages, plans, account)] as RSC
  [lib/fetchers.ts\\nTMDB facade] as Fetchers
  [lib/subscription.ts\\nplan resolution] as Sub
  [/api/trpc  (pages router)\\nappRouter: user, profile, icon, myList] as TRPC
  [tRPC middleware\\nenforceUserIsAuthed] as MW
  [/api/auth  NextAuth\\nGoogleProvider + PrismaAdapter] as Auth
  [/api/users/stripe  checkout] as Checkout
  [/api/webhooks/stripe] as Hook
  [Prisma client (singleton)] as Prisma
}
database "MySQL (relationMode = prisma)" as DB
cloud "TMDB API" as TMDB
cloud "Stripe" as Stripe
cloud "Google OAuth" as Google
Viewer --> UI
UI --> Stores : setState / subscribe
UI --> Client : api.x.y.useQuery()
Client --> RQ
RQ --> TRPC : HTTP batch
TRPC --> MW
MW --> Prisma
UI ..> RSC : navigation
RSC --> Fetchers
Fetchers --> TMDB
RSC --> Sub
Sub --> Prisma
RSC --> Auth : getServerSession
Auth --> Google
Auth --> Prisma
UI --> Checkout : fetch POST
Checkout --> Stripe
Stripe --> Hook : checkout.session.completed\\ninvoice.payment_succeeded
Hook --> Prisma
Prisma --> DB
@enduml
"""

D["01_cor_authenticated_procedure_pipeline"] = HEAD + """title Chain of Responsibility - Authenticated Procedure Pipeline
interface "MiddlewareFunction\\n<<@trpc/server>>" as H {
  +({ctx, next}) : Promise<MiddlewareResult>
}
class "enforceUserIsAuthed\\n<<trpc.ts:109-119>>" as A {
  +({ctx, next}) : throws UNAUTHORIZED | next({ctx: session})
}
class "protectedProcedure\\n<<trpc.ts:129>>" as P {
  = t.procedure.use(enforceUserIsAuthed)
}
class "procedure resolver\\n(e.g. profile.getAll)" as R {
  +({ctx, input})
}
class "createNextApiHandler\\n<<[trpc].ts:8-19>>" as C
H <|.. A
P o--> A : first link
A --> R : next()
C --> P : invokes
@enduml
"""

D["02_singleton_shared_prisma_client"] = HEAD + """title Singleton - Shared Prisma Database Client
class "db.ts module" as M <<singleton holder>> {
  -globalForPrisma : {prisma?: PrismaClient}
  +prisma : PrismaClient = globalForPrisma.prisma ?? new PrismaClient()
}
class PrismaClient <<@prisma/client>>
class createInnerTRPCContext
class "authOptions.adapter" as AO
class getUserSubscriptionPlan
class "webhook POST" as W
M --> "1" PrismaClient : creates once
createInnerTRPCContext ..> M : import prisma
AO ..> M
getUserSubscriptionPlan ..> M
W ..> M
@enduml
"""

D["03_singleton_stripe_client"] = HEAD + """title Singleton (module) - Stripe API Client
class "lib/stripe.ts" as S <<module singleton>> {
  +stripe : Stripe = new Stripe(key, {apiVersion: 2022-11-15})
}
class Stripe <<stripe@12>>
class "webhooks/stripe POST" as A
class "users/stripe POST" as B
class PlansPage
class AccountPage
S --> "1" Stripe
A ..> S
B ..> S
PlansPage ..> S
AccountPage ..> S
@enduml
"""

OBS_HEAD = HEAD + """interface "StoreApi<T>\\n<<zustand>>" as Subject {
  +getState() : T
  +setState(partial)
  +subscribe(listener) : unsubscribe
}
"""

D["04_observer_show_modal_selection"] = OBS_HEAD + """title Observer - Show Modal Selection
class "useModalStore\\n<<stores/modal.ts:13-20>>" as CS {
  open : boolean
  show : Show | null
  play : boolean
}
class "ShowCard.onClick\\n<<shows-carousel.tsx:93-113>>" as Pub
class ShowsContainer <<observer>>
class ShowModal <<observer>>
class Hero <<observer>>
class ShowsGrid <<observer>>
Subject <|.. CS
Pub --> CS : setState({show, open, play})
CS --> ShowsContainer : notify (re-render)
CS --> ShowModal : notify
CS --> Hero : notify
CS --> ShowsGrid : notify
@enduml
"""

D["05_observer_active_profile_selection"] = OBS_HEAD + """title Observer - Active Profile Selection
class "useProfileStore\\n<<stores/profile.ts:12-27>>" as CS {
  profile : ProfileWithIcon | null
  pinForm : boolean
}
class "publishers:\\nProfilesScreen button, SiteHeader menu,\\nsiteConfig sign-out" as Pub
class ProfilesScreen <<observer>>
class PinForm <<observer>>
class ShowsContainer <<observer>>
class ShowModal <<observer>>
class SiteHeader <<observer>>
class MyShows <<observer>>
Subject <|.. CS
Pub --> CS : setState({profile, pinForm})
CS --> ProfilesScreen
CS --> PinForm
CS --> ShowsContainer
CS --> ShowModal
CS --> SiteHeader
CS --> MyShows
@enduml
"""

D["06_observer_search_results_broadcast"] = OBS_HEAD + """title Observer - Search Results Broadcast
class "useSearchStore\\n<<stores/search.ts:11-16>>" as CS {
  query : string
  shows : Show[]
}
class "SiteHeader.searchShowsByQuery\\n<<site-header.tsx:51-55>>" as Pub
class SiteHeader <<observer>>
class ShowsContainer <<observer>>
class Hero <<observer>>
class MainNav <<observer>>
class MyShows <<observer>>
Subject <|.. CS
Pub --> CS : setQuery / setShows
CS --> SiteHeader
CS --> ShowsContainer
CS --> Hero
CS --> MainNav
CS --> MyShows
@enduml
"""

D["07_decorator_persisted_profile_store"] = HEAD + """title Decorator - Persisted Profile Store
interface "StateCreator<ProfileState>\\n<<zustand>>" as C {
  +(set, get, api) : ProfileState
}
class "profile creator\\n<<profile.ts:15-20>>" as CC
class "persist(creator, {sessionStorage})\\n<<zustand/middleware>>" as P {
  wraps set: write to storage
  +api.persist.clearStorage()
}
class "devtools(creator)\\n<<zustand/middleware>>" as DV {
  wraps set: report action
}
class "create<ProfileState>()\\n<<profile.ts:12>>" as Client
C <|.. CC
C <|.. P
C <|.. DV
P o--> C : wraps
DV o--> C : wraps
Client --> DV : devtools(persist(creator))
@enduml
"""

D["08_adapter_nextauth_prisma"] = HEAD + """title Adapter - NextAuth Prisma Persistence Adapter
interface "Adapter\\n<<next-auth adapters.d.ts:57>>" as T {
  +createUser(user)
  +getUserByEmail(email)
  +linkAccount(account)
  +createSession(session)
  ...()
}
class "PrismaAdapter(p)\\n<<@next-auth/prisma-adapter index.js:206-264>>" as A {
  createUser: p.user.create({data})
  getUserByEmail: p.user.findUnique({where:{email}})
}
class "PrismaClient (prisma)\\n<<db.ts:9-14>>" as Ad {
  +user.create()
  +user.findUnique()
  +account.create()
}
class "NextAuth(authOptions)\\n<<auth.ts:38-64>>" as Cl
T <|.. A
A --> Ad : translates calls
Cl --> T : adapter
@enduml
"""

D["09_strategy_signin_provider"] = HEAD + """title Strategy - Sign-in Provider Strategy
interface "Provider\\n<<next-auth providers/index.d.ts:14>>" as S {
  id, type
  authorization / token / profile()
}
class "GoogleProvider({clientId, clientSecret})\\n<<auth.ts:50-53>>" as G
class "(GitHub, Email, Credentials...)\\nnot configured" as O #eeeeee
class "NextAuth(authOptions)\\nproviders: Provider[]" as Ctx {
  +signIn(providerId)
}
S <|.. G
S <|.. O
Ctx o--> "1..*" S : selects by id
@enduml
"""

D["10_facade_tmdb_catalogue"] = HEAD + """title Facade - TMDB Catalogue Facade
package "lib/fetchers.ts (Facade, module)" {
  class "getShows(mediaType)" as F1
  class "getNewAndPopularShows()" as F2
  class "searchShows(query)" as F3
}
package "Subsystem" {
  class "TMDB /trending, /top_rated" as T1
  class "TMDB /discover (genres, networks)" as T2
  class "TMDB /popular, /search/multi" as T3
  class "env.NEXT_PUBLIC_TMDB_API_KEY" as K
  class "fetch + JSON parse + error check" as J
}
class "Home / MoviesPage / TVShowsPage" as P1
class NewAndPopularPage
class "SiteHeader.searchShowsByQuery" as SH
P1 --> F1
NewAndPopularPage --> F2
SH --> F3
F1 --> T1
F1 --> T2
F1 --> J
F2 --> T3
F3 --> T3
F1 ..> K
F2 ..> K
F3 ..> K
@enduml
"""

D["11_composite_api_router_tree"] = HEAD + """title Composite - API Router Tree
interface "Router record entry\\nAnyRouter | AnyProcedure" as C
class "Router\\n(createTRPCRouter)" as R {
  _def.record : {key: Router | Procedure}
}
class "Procedure (leaf)" as L {
  query() / mutation()
}
C <|.. R
C <|.. L
R o--> "*" C : children
object "appRouter" as root
object "userRouter (4)" as u
object "profileRouter (7)" as p
object "iconRouter (4)" as i
object "myListRouter (4)" as m
root *-- u
root *-- p
root *-- i
root *-- m
@enduml
"""

PROXY = """class "AppRouter (type)\\n<<root.ts:20>>" as S
class "appRouter via createNextApiHandler\\n<<[trpc].ts:8-19>>" as RS
"""

D["12_proxy_pages_router_trpc_client"] = HEAD + """title Proxy - Pages-Router tRPC Client Proxy
""" + PROXY + """class "api = createTRPCNext<AppRouter>\\n<<lib/api/api.ts:21-54>>\\n(JS Proxy)" as P {
  +[router].[proc].useQuery()
  +[router].[proc].useMutation()
  +useContext()
}
class "httpBatchLink(/api/trpc)" as L
class "ShowsContainer, ShowModal,\\nProfilesScreen, ..." as Cl
S <|.. RS
S <|.. P : typed as
P --> L
L --> RS : HTTP
Cl --> P
@enduml
"""

D["13_proxy_app_router_trpc_client"] = HEAD + """title Proxy - App-Router tRPC Client Proxy
""" + PROXY + """class "api = createTRPCNextBeta<AppRouter>\\n<<lib/api/client.ts:22-45>>" as P
class "createFlatProxy(key => ...)\\n<<createTrpcNextBeta.tsx:76-92>>" as FP
class "TRPCProvider\\n<<context/trpc-provider.tsx>>" as Prov
class "AddProfileForm, EditProfileForm" as Cl
S <|.. RS
S <|.. P : typed as
P --> FP : built by
FP --> RS : hooks -> HTTP batch
Prov --> P : api.Provider
Cl --> P
@enduml
"""

D["14_cache_my_list_query_cache"] = HEAD + """title Read-Through Cache - My List Query Cache
class "QueryClient\\n<<createTrpcNextBeta.tsx:55-63>>" as Q {
  staleTime = Infinity, cacheTime = Infinity
  +fetchQuery(key, loader)
  +invalidateQueries(key)
}
class "ShowsContainer.myShowsQuery" as R1
class "ShowModal.myShowsQuery" as R2
class "ShowModal effect\\ninvalidate on mutation" as I
class "myList.getAll (loader)\\n<<my-list.ts:7-12>>" as L
R1 --> Q : useQuery(profileId)
R2 --> Q : useQuery(profileId)
I --> Q : invalidate
Q --> L : on miss / after invalidate
@enduml
"""

D["15_proxy_environment_secret_guard"] = HEAD + """title Proxy (protection) - Environment Secret Guard
interface "MergedOutput\\n<<env.mjs:67-71>>" as S {
  DATABASE_URL, STRIPE_API_KEY, ...
  NEXT_PUBLIC_TMDB_API_KEY, ...
}
class "parsed.data\\n(zod validated)" as RS
class "env = new Proxy(parsed.data, {get})\\n<<env.mjs:92-105>>" as P {
  get(target, prop): throw if client && !NEXT_PUBLIC_
}
class "lib/stripe.ts, server/db.ts,\\nlib/fetchers.ts ... (10 modules)" as C
S <|.. RS
S <|.. P
P --> RS : forwards allowed reads
C --> P : env.X
@enduml
"""


def main():
    jar = os.environ.get("PLANTUML_JAR", os.path.expanduser("~/tools/plantuml.jar"))
    for name, src in D.items():
        with open(os.path.join(OUT, name + ".puml"), "w", encoding="utf-8") as fh:
            fh.write(src)
    files = [os.path.join(OUT, n + ".puml") for n in D]
    subprocess.run(["java", "-jar", jar, "-tpng", *files], check=True)
    print("rendered", len(files))


if __name__ == "__main__":
    main()
