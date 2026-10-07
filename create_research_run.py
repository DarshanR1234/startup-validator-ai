from pathlib import Path

from app.agents.idea_agent import analyze_startup_idea
from app.agents.market_agent import research_market
from app.agents.competitor_agent import analyze_competitors
from app.agents.persona_agent import generate_customer_personas
from app.agents.swot_agent import analyze_swot
from app.agents.pricing_agent import recommend_pricing
from app.agents.mvp_agent import recommend_mvp
from app.utils.run_cache import save_run, load_run


startup_idea = """
I want to build an AI-powered platform that helps
small restaurants predict food demand and reduce food waste.
"""

run_name = "restaurant_food_waste"

run_data = {
    "startup_idea": startup_idea.strip()
}


# ---------------------------------------------------------
# Load previous checkpoint if it exists
# ---------------------------------------------------------

try:
    existing_run = load_run(run_name)
    run_data.update(existing_run)

    print("\nExisting checkpoint found.")
    print("Resuming from saved progress...\n")

except FileNotFoundError:
    print("\nNo existing checkpoint found.")
    print("Starting a new research run...\n")


# ---------------------------------------------------------
# 1. IDEA ANALYSIS
# ---------------------------------------------------------

if "idea_analysis" not in run_data:

    print("[1/7] Analyzing idea...")

    idea_analysis = analyze_startup_idea(
        startup_idea
    )

    run_data["idea_analysis"] = idea_analysis.model_dump()

    save_run(run_name, run_data)

    print("Idea analysis saved.\n")

else:

    print("[1/7] Idea analysis already available. Skipping.")


# ---------------------------------------------------------
# 2. MARKET RESEARCH
# ---------------------------------------------------------

if "market_research" not in run_data:

    print("\n[2/7] Researching market...")

    market_research = research_market(
        startup_idea,
        run_data["idea_analysis"]
    )

    run_data["market_research"] = market_research.model_dump()

    save_run(run_name, run_data)

    print("Market research saved.\n")

else:

    print("[2/7] Market research already available. Skipping.")


# ---------------------------------------------------------
# 3. COMPETITOR ANALYSIS
# ---------------------------------------------------------

if "competitor_analysis" not in run_data:

    print("\n[3/7] Analyzing competitors...")

    competitor_analysis = analyze_competitors(
        startup_idea,
        run_data["idea_analysis"],
        run_data["market_research"]
    )

    run_data["competitor_analysis"] = competitor_analysis.model_dump()

    save_run(run_name, run_data)

    print("Competitor analysis saved.\n")

else:

    print("[3/7] Competitor analysis already available. Skipping.")


# ---------------------------------------------------------
# 4. CUSTOMER PERSONAS
# ---------------------------------------------------------

if "persona_analysis" not in run_data:

    print("\n[4/7] Generating customer personas...")

    persona_analysis = generate_customer_personas(
        startup_idea,
        run_data["idea_analysis"],
        run_data["market_research"],
        run_data["competitor_analysis"]
    )

    run_data["persona_analysis"] = persona_analysis.model_dump()

    save_run(run_name, run_data)

    print("Customer personas saved.\n")

else:

    print("[4/7] Customer personas already available. Skipping.")


# ---------------------------------------------------------
# 5. SWOT
# ---------------------------------------------------------

if "swot_analysis" not in run_data:

    print("\n[5/7] Performing SWOT analysis...")

    swot_analysis = analyze_swot(
        startup_idea,
        run_data["idea_analysis"],
        run_data["market_research"],
        run_data["competitor_analysis"],
        run_data["persona_analysis"]
    )

    run_data["swot_analysis"] = swot_analysis.model_dump()

    save_run(run_name, run_data)

    print("SWOT analysis saved.\n")

else:

    print("[5/7] SWOT analysis already available. Skipping.")


# ---------------------------------------------------------
# 6. PRICING
# ---------------------------------------------------------

if "pricing_analysis" not in run_data:

    print("\n[6/7] Creating pricing strategy...")

    pricing_analysis = recommend_pricing(
        startup_idea,
        run_data["idea_analysis"],
        run_data["market_research"],
        run_data["competitor_analysis"],
        run_data["persona_analysis"]
    )

    run_data["pricing_analysis"] = pricing_analysis.model_dump()

    save_run(run_name, run_data)

    print("Pricing strategy saved.\n")

else:

    print("[6/7] Pricing strategy already available. Skipping.")


# ---------------------------------------------------------
# 7. MVP
# ---------------------------------------------------------

if "mvp_analysis" not in run_data:

    print("\n[7/7] Designing MVP...")

    mvp_analysis = recommend_mvp(
        startup_idea,
        run_data["idea_analysis"],
        run_data["market_research"],
        run_data["competitor_analysis"],
        run_data["persona_analysis"],
        run_data["swot_analysis"],
        run_data["pricing_analysis"]
    )

    run_data["mvp_analysis"] = mvp_analysis.model_dump()

    save_run(run_name, run_data)

    print("MVP analysis saved.\n")

else:

    print("[7/7] MVP analysis already available. Skipping.")


# ---------------------------------------------------------
# FINAL STATUS
# ---------------------------------------------------------

print("\n========================================")
print("RESEARCH RUN STATUS")
print("========================================")

stages = [
    "idea_analysis",
    "market_research",
    "competitor_analysis",
    "persona_analysis",
    "swot_analysis",
    "pricing_analysis",
    "mvp_analysis"
]

for stage in stages:

    status = "DONE" if stage in run_data else "PENDING"

    print(f"{stage:25} : {status}")


file_path = Path("data/runs") / f"{run_name}.json"

print("\nCheckpoint file:")
print(file_path)