# Startup Validator AI

## Project Overview

Startup Validator AI is an AI-powered startup idea validation system.

The system takes a startup idea along with a target country and region, analyzes the idea using multiple AI analysis stages, retrieves supporting knowledge from a RAG knowledge base, and generates a structured startup validation report.

The goal is to help founders evaluate an idea before investing significant time and resources into building it.

---

# 1. Problem We Are Solving

Many startup ideas fail because founders do not properly evaluate:

- Whether a real market demand exists
- Whether customers actually have the identified problem
- Existing competitors
- Competitive gaps
- Pricing potential
- Business scalability
- Technical and operational feasibility
- MVP scope
- Major risks and threats

The project attempts to combine these evaluations into one AI-powered validation pipeline.

---

# 2. What The System Does

The user provides:

- Startup idea
- Target country
- Target region

Example:

> A subscription-based healthy meal delivery service for working professionals in Pune that provides affordable calorie-controlled home-style meals.

Target country:

> India

Target region:

> Maharashtra

The system then performs multiple analysis stages and produces:

1. Idea Analysis
2. Market Research
3. Competitor Analysis
4. Customer Buyer Personas
5. SWOT Analysis
6. Pricing Analysis
7. MVP Analysis
8. 7-Point Evaluation
9. Overall Validation Score
10. Research Sources

---

# 3. High-Level Architecture

```text
                    USER
                      |
                      v
             React Frontend
                      |
                      | HTTP POST
                      v
             FastAPI Backend
                      |
                      v
             Validation Pipeline
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
   Idea Analysis   Research      AI Agents
                      |
        +-------------+-------------+
        |
        v
       RAG
 Knowledge Base / Chroma
        |
        v
 Criterion Evidence
        |
        v
  7-Point Evaluation
        |
        v
 Final Validation Result
        |
        v
 React Dashboard