from pydantic import BaseModel, Field


class StartupValidationRequest(BaseModel):
    startup_idea: str = Field(
        min_length=10,
        description="Startup idea provided by the user."
    )

    target_country: str = Field(
        default="India",
        description="Target country/market for the startup."
    )

    target_region: str = Field(
        default="",
        description="Optional state, city, or region within the target country."
    )


class ResearchSource(BaseModel):
    title: str = ""
    author: str = ""
    source_type: str = ""
    page: str = ""
    doi: str = ""
    source: str = ""
    category: str = ""


class StartupValidationResponse(BaseModel):
    startup_idea: str
    target_country: str
    target_region: str

    overall_score: float = Field(
        ge=0,
        le=100
    )

    verdict: str
    summary: str

    key_strengths: list[str]
    key_weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]

    market_research: dict
    competitor_analysis: dict
    persona_analysis: dict
    pricing_analysis: dict
    mvp_analysis: dict
    evaluation: dict

    research_sources: list[ResearchSource]