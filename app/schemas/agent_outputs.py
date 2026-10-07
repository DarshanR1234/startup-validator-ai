from pydantic import BaseModel, Field


class IdeaAnalysis(BaseModel):
    problem: str = Field(
        description="The main problem that the startup is trying to solve."
    )
    proposed_solution: str = Field(
        description="The proposed product or service that solves the problem."
    )
    target_industry: str = Field(
        description="The primary industry or domain of the startup."
    )
    target_customer: str = Field(
        description="The primary customer or user of the startup."
    )
    business_model: str = Field(
        description="The likely business model, such as B2B SaaS, B2C, marketplace, subscription, etc."
    )
    key_value_proposition: str = Field(
        description="The main value or benefit the startup provides to its customers."
    )
    assumptions: list[str] = Field(
        description="Important assumptions that need to be true for the startup idea to work."
    )


class MarketEvidence(BaseModel):
    claim: str = Field(
        description="The market finding or claim."
    )
    source: str = Field(
        default="",
        description="Source name or URL supporting the claim."
    )


class MarketResearch(BaseModel):
    market_demand: str = Field(
        description="Assessment of the current demand for the startup's proposed solution."
    )
    industry_trends: list[str] = Field(
        description="Important current trends relevant to the startup."
    )
    target_market: str = Field(
        description="Description of the primary market and customer segment."
    )
    growth_drivers: list[str] = Field(
        description="Factors that could drive growth in this market."
    )
    customer_problems: list[str] = Field(
        description="Important customer problems or pain points identified from research."
    )
    opportunities: list[str] = Field(
        description="Potential opportunities for the startup in the market."
    )
    evidence: list[MarketEvidence] = Field(
        description="Structured market evidence and its source."
    )


class Competitor(BaseModel):
    name: str = Field(
        description="Name of the competitor or competing product."
    )
    product: str = Field(
        description="Description of the competitor's product or solution."
    )
    pricing: str = Field(
        description="Publicly available pricing information. If pricing is not available, state 'Not publicly available'."
    )
    strengths: list[str] = Field(
        description="Important strengths of the competitor."
    )
    weaknesses: list[str] = Field(
        description="Important weaknesses or limitations of the competitor."
    )
    evidence: list[str] = Field(
        description="Evidence or findings supporting the competitor analysis."
    )


class CompetitorAnalysis(BaseModel):
    competitor_list: list[Competitor] = Field(
        description="List of relevant competitors identified for the startup."
    )
    market_gaps: list[str] = Field(
        description="Potential unmet needs or market gaps that the startup could address."
    )
    competitive_risks: list[str] = Field(
        description="Major competitive threats or risks for the startup."
    )


class CustomerPersona(BaseModel):
    name: str = Field(
        description="A clear name for the customer persona."
    )
    role: str = Field(
        description="The person's role or position."
    )
    business_type: str = Field(
        description="Type of business or organization they belong to."
    )
    goals: list[str] = Field(
        description="Main goals the persona wants to achieve."
    )
    pain_points: list[str] = Field(
        description="Main problems or frustrations faced by the persona."
    )
    needs: list[str] = Field(
        description="What the persona needs from a solution."
    )
    willingness_to_pay: str = Field(
        description="Assessment of the persona's likely willingness to pay and the reasoning."
    )


class CustomerPersonaAnalysis(BaseModel):
    personas: list[CustomerPersona] = Field(
        description="Two to four important customer personas for the startup."
    )


class SWOTAnalysis(BaseModel):
    strengths: list[str] = Field(
        description="Internal strengths of the startup idea."
    )
    weaknesses: list[str] = Field(
        description="Internal weaknesses or limitations of the startup idea."
    )
    opportunities: list[str] = Field(
        description="External opportunities available in the market."
    )
    threats: list[str] = Field(
        description="External threats and risks affecting the startup."
    )


class PricingTier(BaseModel):
    name: str = Field(
        description="Name of the pricing tier, such as Basic, Professional, or Enterprise."
    )
    price: str = Field(
        description="Recommended price for this tier, including currency and billing period."
    )
    target_customer: str = Field(
        description="Customer segment that this pricing tier is intended for."
    )
    included_features: list[str] = Field(
        description="Important features included in this pricing tier."
    )


class PricingAnalysis(BaseModel):
    pricing_model: str = Field(
        description="Recommended pricing model, such as subscription, usage-based, freemium, or one-time payment."
    )
    recommended_price: str = Field(
        description="Recommended starting price for the primary customer segment."
    )
    pricing_tiers: list[PricingTier] = Field(
        description="Recommended pricing tiers for the startup."
    )
    pricing_rationale: list[str] = Field(
        description="Reasons supporting the recommended pricing strategy."
    )
    pricing_risks: list[str] = Field(
        description="Potential risks or uncertainties associated with the proposed pricing."
    )


class MVPFeature(BaseModel):
    name: str = Field(
        description="Name of the MVP feature."
    )
    priority: int = Field(
        ge=0,
        description="Priority of the feature. Lower number means higher priority."
    )


class MVPRationale(BaseModel):
    reason: str = Field(
        description="Reason why this MVP decision was made."
    )


class MVPAnalysis(BaseModel):
    core_features: list[MVPFeature] = Field(
        description="Essential features that should be included in the first MVP."
    )
    future_features: list[MVPFeature] = Field(
        description="Features that should be considered after the initial MVP."
    )
    excluded_features: list[MVPFeature] = Field(
        description="Features intentionally excluded from the initial MVP."
    )
    development_priority: list[MVPFeature] = Field(
        description="Ordered development priorities for the MVP."
    )
    mvp_rationale: list[MVPRationale] = Field(
        description="Reasons supporting the selected MVP scope."
    )


class EvidenceItem(BaseModel):
    claim: str = Field(
        default="",
        description="The claim or finding supporting the criterion."
    )
    source_title: str = Field(
        default="",
        description="Title of the research source."
    )
    source_type: str = Field(
        default="",
        description="Source type, such as RAG research, Web research, or Startup analysis."
    )
    page: str = Field(
        default="",
        description="Page number or page label of the source."
    )
    doi: str = Field(
        default="",
        description="DOI of the source when available."
    )
    source: str = Field(
        default="",
        description="Source file path or URL."
    )


class CriterionScore(BaseModel):
    score: int = Field(
        ge=0,
        le=10,
        description="Score from 0 to 10."
    )
    reason: str = Field(
        default="",
        description="Reason supporting the score."
    )
    evidence: list[EvidenceItem] = Field(
        default_factory=list,
        description="Structured evidence supporting the criterion."
    )


class StartupEvaluation(BaseModel):
    market_demand: CriterionScore
    customer_need: CriterionScore
    competition: CriterionScore
    business_potential: CriterionScore
    pricing_potential: CriterionScore
    feasibility: CriterionScore
    mvp_clarity: CriterionScore