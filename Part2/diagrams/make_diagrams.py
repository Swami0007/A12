"""Updated UML for instances changed in Part 2 (state after CH03 unless named).
Run from A12/: python3 Part2/diagrams/make_diagrams.py"""
import os
import subprocess

OUT = "Part2/diagrams"
HEAD = "@startuml\nskinparam classAttributeIconSize 0\nskinparam shadowing false\nhide empty members\n"
D = {}

D["01_content_access_rule_chain_CH03"] = HEAD + """title Content Access Rule Chain (CoR, student-added CH01, extended CH02 + CH03)
abstract class AccessRule <<lib/access/rules.ts>> {
  -next : AccessRule | null
  +setNext(rule) : AccessRule
  +check(show, ctx) : AccessDecision
  #{abstract} evaluate(show, ctx) : AccessDecision | null
}
class RegionRule <<CH02>> {
  -licences : Record<id, RegionLicence>
  #evaluate() : REGION_BLOCKED / hidden
}
class MaturityRule <<CH03>> {
  -policies : Record<Maturity, MaturityPolicy>
  #evaluate() : MATURITY_BLOCKED / hidden
}
class PremiumContentRule <<CH01>> {
  -minTier = 3
  #evaluate() : PREMIUM_REQUIRED / locked
}
class "policy.ts" as Policy <<module>> {
  +buildAccessChain(rules)
  +contentAccessChain() : Region -> Maturity -> Premium
  +checkAccess(show, ctx, chain)
  +visibleShows(shows, ctx)
  +profileVisibleShows(shows, maturity)
}
class "AccessContext" as Ctx {
  planTier : number
  region : string
  maturity? : Maturity
}
AccessRule <|-- RegionRule
AccessRule <|-- MaturityRule
AccessRule <|-- PremiumContentRule
AccessRule o--> "0..1" AccessRule : next
Policy ..> AccessRule : links
Policy ..> Ctx
class "catalogue.checkAccess" as CA <<tRPC>>
class "toCategories (server rows)" as TC
class "myList.create" as ML
class "ShowsContainer / Hero" as UI <<client>>
CA --> Policy
TC --> Policy
ML --> Policy
UI --> Policy
@enduml
"""

D["02_content_access_sequence_CH03"] = """@startuml
skinparam shadowing false
title catalogue.checkAccess - request through both chains (CH03)
actor Viewer
participant ShowModal
participant "api (tRPC proxy)" as Api
participant enforceUserIsAuthed as A
participant attachSubscription as S
participant "checkAccess resolver" as R
participant RegionRule as RR
participant MaturityRule as MR
participant PremiumContentRule as PR
Viewer -> ShowModal : open title
ShowModal -> Api : catalogue.checkAccess({id, isPremium, genre_ids, profileId})
Api -> A : HTTP batch
alt no session
  A --> Api : UNAUTHORIZED
else signed in
  A -> S : next({session})
  S -> S : getUserSubscriptionPlan(userId, ctx.prisma)
  S -> R : next({planTier, maxProfiles})
  R -> R : load profile.maturityLevel (owner check)
  R -> RR : check(show, {planTier, region, maturity})
  alt licensed in region
    RR -> MR : next.check()
    alt suitable for profile
      MR -> PR : next.check()
      PR --> R : allowed | PREMIUM_REQUIRED (locked)
    else
      MR --> R : MATURITY_BLOCKED (hidden)
    end
  else
    RR --> R : REGION_BLOCKED (hidden)
  end
  R --> ShowModal : AccessDecision
end
ShowModal -> Viewer : Play | "Upgrade to watch"
@enduml
"""

D["03_template_method_access_rule_CH03"] = HEAD + """title Template Method - Access Rule Evaluation Template (student-added CH01)
abstract class AccessRule {
  +check(show, ctx) <<template method>>
  #{abstract} evaluate(show, ctx) <<primitive>>
}
note right of AccessRule
  check():
    denial = evaluate(show, ctx)
    if denial: return denial
    return next ? next.check() : ALLOW
end note
class RegionRule {
  #evaluate()
}
class MaturityRule {
  #evaluate()
}
class PremiumContentRule {
  #evaluate()
}
AccessRule <|-- RegionRule
AccessRule <|-- MaturityRule
AccessRule <|-- PremiumContentRule
@enduml
"""

D["04_cor_authenticated_pipeline_CH01"] = HEAD + """title Authenticated Procedure Pipeline - extended in CH01
interface "MiddlewareFunction <<@trpc/server>>" as H
class enforceUserIsAuthed <<trpc.ts>>
class "attachSubscription" as AS <<CH01>> {
  ctx.subscription, ctx.planTier, ctx.maxProfiles
}
class protectedProcedure
class "subscribedProcedure" as SP <<CH01>>
class "profile.create" as PC
class "catalogue.checkAccess" as CC <<CH01>>
class "other protected resolvers" as O
H <|.. enforceUserIsAuthed
H <|.. AS
protectedProcedure o--> enforceUserIsAuthed
SP o--> protectedProcedure : .use()
SP o--> AS
enforceUserIsAuthed --> AS : next()
AS --> PC : next()
AS --> CC : next()
enforceUserIsAuthed --> O : next()
@enduml
"""

D["05_composite_api_router_tree_CH01"] = HEAD + """title API Router Tree - extended in CH01
object "appRouter" as root
object "userRouter (4)" as u
object "profileRouter (7)" as p
object "iconRouter (4)" as i
object "myListRouter (4)" as m
object "catalogueRouter (1)\\n<<CH01>>" as c
object "checkAccess (leaf)" as ca
root *-- u
root *-- p
root *-- i
root *-- m
root *-- c
c *-- ca
@enduml
"""

D["06_observer_active_profile_selection_CH03"] = HEAD + """title Active Profile Selection - extended in CH03
class "useProfileStore" as CS {
  profile : ProfileWithIcon (+ maturityLevel)
  pinForm : boolean
}
class ProfilesScreen
class PinForm
class "ShowsContainer\\nfilters rows, search, My List" as SC
class "ShowModal\\nsends profileId to checkAccess" as SM
class SiteHeader
class MyShows
class "Hero <<new observer, CH03>>\\nselector: profile?.maturityLevel" as H #ffe4e1
CS --> ProfilesScreen
CS --> PinForm
CS --> SC
CS --> SM
CS --> SiteHeader
CS --> MyShows
CS --> H
@enduml
"""

D["07_facade_tmdb_refactored_CH02"] = HEAD + """title TMDB Catalogue Facade - after CH02 refactoring
package "lib/fetchers.ts (Facade)" {
  class "getShows(mediaType)" as G
  class "getNewAndPopularShows()" as N
  class "searchShows(query)" as S
  class "fetchRows(rows, errorMessage)" as FR <<private helper>>
  class "SHOW_ROWS (8) / NEW_AND_POPULAR_ROWS (4)" as Rows <<data>>
  class "tmdbUrl(path, query)" as U
}
G --> FR
N --> FR
G ..> Rows
N ..> Rows
FR --> U
FR --> "TMDB API" : Promise.all(fetch)
S --> "TMDB API"
class "Home / Movies / TV / New & Popular" as P
class "lib/catalogue.ts\\nGENRE_ROWS + toCategories" as C <<CH02>>
P --> G
P --> N
P --> C
@enduml
"""

D["08_plan_catalogue_refactor_CH01"] = HEAD + """title Plan data after CH01 refactoring (single source of truth)
class "config/plan-catalog.ts\\n(client-safe)" as PC {
  planCatalog : PlanCatalogEntry[5]
  PREMIUM_CONTENT_MIN_TIER = 3
  DEFAULT_MAX_PROFILES = 5
}
class "config/plans.ts (UI)\\nplansConfig" as UI
class "config/subscriptions.ts (server)\\nsubscriptionPlans" as SV
class "env (Protection Proxy)" as ENV
class BillingForm <<client>>
class "getUserSubscriptionPlan / checkout" as SRV <<server>>
UI --> PC : derive + icons
SV --> PC : derive + price ids
SV --> ENV : STRIPE_*_PRICE_ID
BillingForm --> UI
SRV --> SV
@enduml
"""


def main():
    jar = os.environ.get("PLANTUML_JAR", os.path.expanduser("~/tools/plantuml.jar"))
    files = []
    for name, src in D.items():
        path = os.path.join(OUT, name + ".puml")
        open(path, "w", encoding="utf-8").write(src)
        files.append(path)
    subprocess.run(["java", "-jar", jar, "-tpng", *files], check=True)
    print("rendered", len(files))


if __name__ == "__main__":
    main()
