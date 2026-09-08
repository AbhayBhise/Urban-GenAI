"""Assemble backend/corpus/urban_planning.txt.

The MiniGPT trainer needs a reasonably large, stylistically consistent corpus.
Hand-writing 100 KB of planning prose is impractical, so we compose it from
vetted sentence templates over a grid of neighbourhood profiles. Every record
follows the same shape:

    Context: <situation>
    Recommendations:
    - <action>
    - <action>
    ...
    ===

Run:  python build_corpus.py
"""

import os
import random

random.seed(7)

OUT = os.path.join(os.path.dirname(__file__), "urban_planning.txt")

AREAS = [
    "a central ward", "a peri-urban ward", "an IT-corridor ward", "a riverside ward",
    "an industrial belt", "a heritage core", "a fast-growing suburban ward",
    "a hillside settlement", "a transit-station catchment", "a lakefront zone",
    "a market district", "a university precinct", "a floodplain-adjacent ward",
    "a low-income resettlement colony", "a mixed old-and-new ward",
]

BUILT = ["18%", "27%", "34%", "41%", "48%", "55%", "63%", "71%", "78%"]
GREEN = ["3%", "6%", "9%", "12%", "16%", "21%", "28%"]
ROADS = ["a sparse road grid", "a moderately connected road grid",
         "a dense but congested road grid", "a fragmented road network",
         "a well-connected arterial network"]
WATER = ["no mapped drainage", "a single choked nala", "two seasonal streams",
         "a canal along its edge", "a river frontage", "a lake in its catchment"]
POP = ["low", "moderate", "high", "very high"]

GREEN_ACTIONS = [
    "Raise tree-canopy cover toward 25% using native, low-water species along streets and in pocket parks.",
    "Convert at least one under-used plot per 400 m into a neighbourhood park within a 5-minute walk of every home.",
    "Protect all existing mature trees with a no-net-loss rule and a 3:1 compensatory planting ratio.",
    "Green the edges of every arterial road with a continuous 2 m planting verge.",
    "Create a linear greenway connecting fragmented open spaces into one continuous network.",
    "Require 20% of every large plot to be kept as permeable, planted ground.",
]
WATER_ACTIONS = [
    "Daylight and rehabilitate the natural drainage line with a vegetated buffer of at least 9 m on each bank.",
    "Mandate on-site rainwater harvesting and stormwater retention for all plots above 300 sq m.",
    "Replace impervious paving in public right-of-way with permeable surfaces where the water table allows.",
    "Reserve the floodplain as public open space and prohibit new habitable construction within it.",
    "Build decentralised sewage treatment and reuse treated water for landscape irrigation.",
    "Add bioswales and rain gardens along roads to slow and filter runoff before it reaches the drain.",
]
TRANSIT_ACTIONS = [
    "Concentrate the highest densities and mixed uses within 500 m of the transit station.",
    "Provide a continuous, shaded footpath network with safe crossings on every street.",
    "Add protected cycle lanes on all roads wider than 18 m and secure cycle parking at key destinations.",
    "Cap and price car parking; convert freed kerb space to footpath, planting, and cycle lanes.",
    "Run a high-frequency feeder bus connecting the ward to the nearest mass-transit corridor.",
    "Require new development to unbundle parking cost from housing and provide transit passes.",
]
DENSITY_ACTIONS = [
    "Allow gentle density (ground-plus-three to ground-plus-five) with active ground-floor frontages.",
    "Permit mixed use by right so shops, workspaces, and homes can share a street.",
    "Set a minimum share of small units and require a portion of affordable housing in large projects.",
    "Use form-based controls for street wall, height, and setback rather than use-segregating zoning.",
    "Phase additional floor-space ratio to the delivery of infrastructure and open space.",
    "Encourage incremental redevelopment of large plots into walkable blocks with through-streets.",
]
ENERGY_ACTIONS = [
    "Require rooftop solar readiness and shading design for all new buildings.",
    "Adopt a cool-roof and light-pavement standard to cut the local heat-island effect.",
    "Orient street grids and building masses to retain prevailing breezes and daytime shade.",
    "Set an energy-performance floor for new construction and a retrofit programme for public buildings.",
    "Site waste segregation and local composting within every cluster to cut haulage emissions.",
]
EQUITY_ACTIONS = [
    "Upgrade in situ rather than displace: provide tenure security, water, sanitation, and drainage to informal areas.",
    "Guarantee that every household is within 400 m of a park, a school, and a primary health centre.",
    "Involve residents in the design of public space through structured participatory workshops.",
    "Protect existing affordable rental stock and informal livelihoods during redevelopment.",
    "Publish plan drafts, data, and trade-offs openly and record how public comments changed the plan.",
]
HERITAGE_ACTIONS = [
    "Map and list heritage structures and precincts before any redevelopment approval.",
    "Keep the historic street pattern and plot rhythm; infill must respect scale and materials.",
    "Route heavy through-traffic around the heritage core and prioritise pedestrians within it.",
]

POOLS = [GREEN_ACTIONS, WATER_ACTIONS, TRANSIT_ACTIONS, DENSITY_ACTIONS,
         ENERGY_ACTIONS, EQUITY_ACTIONS, HERITAGE_ACTIONS]

PREAMBLES = [
    "UrbanGen AI drafts advisory recommendations for planner review; they are not approvals.",
    "Sustainable urban planning balances land, water, mobility, energy, and equity together, not one at a time.",
    "Every recommendation below is a starting point for professional and community review.",
    "Good plans protect ecological structure first, then arrange development around it.",
]

PUNE_NOTES = [
    "Context: Pune's PMC area is about 516 sq km with a population near 7.4 million in 2026, projected to reach 10 million by 2041.\nRecommendations:\n- Align ward plans with Pune Metro Phase 1 station catchments and the Mula-Mutha riverfront project.\n- Treat the Mula and Mutha river edges as a continuous ecological and public corridor, not a back boundary.\n- Direct growth pressure from the Hinjewadi IT corridor into transit-served, mixed-use nodes rather than car-dependent sprawl.\n- Protect the hill slopes and biodiversity parks that structure the city's drainage and microclimate.\n===\n",
    "Context: The Hinjewadi IT corridor draws large daily commuting flows into a car-oriented layout.\nRecommendations:\n- Add high-frequency mass transit and feeder buses before approving further office floor-space.\n- Require campuses to open through-streets, footpaths, and ground-floor amenities to the public.\n- Build worker housing within walking distance of employment to cut commute distance.\n- Retain and connect the remaining green and water features as a campus-scale greenway.\n===\n",
]


def make_record():
    area = random.choice(AREAS)
    built = random.choice(BUILT)
    green = random.choice(GREEN)
    roads = random.choice(ROADS)
    water = random.choice(WATER)
    pop = random.choice(POP)
    ctx = (f"Context: {area} with about {built} built-up area, roughly {green} green "
           f"cover, {roads}, {water}, and {pop} population density.")
    pools = random.sample(POOLS, k=random.randint(3, 5))
    actions = [random.choice(p) for p in pools]
    random.shuffle(actions)
    body = "\n".join(f"- {a}" for a in actions)
    return f"{ctx}\nRecommendations:\n{body}\n===\n"


def main():
    parts = []
    for p in PREAMBLES:
        parts.append(p + "\n===\n")
    parts.extend(PUNE_NOTES)
    # Enough records to give a char-level model ~120 KB to learn style from.
    for _ in range(420):
        parts.append(make_record())
    text = "\n".join(parts)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {OUT} ({len(text):,} chars, {len(set(text))} unique)")


if __name__ == "__main__":
    main()
