"""
Fake tools for Business Strategy Analysis Platform demo.
These tools simulate real data sources but return mock data for demonstration purposes.
"""

import random
from typing import Dict, List, Any
import json


# =============================================================================
# FINANCIAL ANALYSIS TOOLS
# =============================================================================

def get_financial_data(company_name: str, years: int = 3) -> Dict[str, Any]:
    """Simulate retrieving financial data from financial databases."""
    base_revenue = random.randint(50, 500) * 1000000  # $50M to $500M
    
    financial_data = {
        "company": company_name,
        "currency": "USD",
        "years_analyzed": years,
        "annual_data": []
    }
    
    for year in range(2024 - years + 1, 2025):
        # Simulate some growth/decline trends
        growth_factor = random.uniform(0.85, 1.25)
        revenue = int(base_revenue * growth_factor)
        base_revenue = revenue
        
        financial_data["annual_data"].append({
            "year": year,
            "revenue": revenue,
            "gross_profit": int(revenue * random.uniform(0.3, 0.7)),
            "operating_income": int(revenue * random.uniform(0.1, 0.3)),
            "net_income": int(revenue * random.uniform(0.05, 0.2)),
            "total_assets": int(revenue * random.uniform(1.2, 3.0)),
            "total_debt": int(revenue * random.uniform(0.2, 0.8))
        })
    
    return financial_data


def calculate_financial_ratios(financial_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate key financial ratios from financial data."""
    latest_year = financial_data["annual_data"][-1]
    
    ratios = {
        "gross_profit_margin": latest_year["gross_profit"] / latest_year["revenue"],
        "operating_margin": latest_year["operating_income"] / latest_year["revenue"],
        "net_profit_margin": latest_year["net_income"] / latest_year["revenue"],
        "debt_to_assets": latest_year["total_debt"] / latest_year["total_assets"],
        "revenue_growth_rate": random.uniform(-0.1, 0.3),  # -10% to +30%
        "liquidity_score": random.uniform(1.0, 4.0)  # Current ratio simulation
    }
    
    return ratios


def get_revenue_projections(company_name: str, projection_years: int = 3) -> Dict[str, Any]:
    """Generate revenue projections based on market trends."""
    current_revenue = random.randint(100, 600) * 1000000
    
    projections = {
        "company": company_name,
        "base_year_revenue": current_revenue,
        "projections": []
    }
    
    for year in range(1, projection_years + 1):
        # Simulate different growth scenarios
        optimistic_growth = random.uniform(0.15, 0.35)
        realistic_growth = random.uniform(0.05, 0.20)
        pessimistic_growth = random.uniform(-0.05, 0.10)
        
        projections["projections"].append({
            "year": 2024 + year,
            "optimistic": int(current_revenue * (1 + optimistic_growth) ** year),
            "realistic": int(current_revenue * (1 + realistic_growth) ** year),
            "pessimistic": int(current_revenue * (1 + pessimistic_growth) ** year)
        })
    
    return projections


# =============================================================================
# MARKET RESEARCH TOOLS
# =============================================================================

def get_industry_trends(industry: str) -> Dict[str, Any]:
    """Simulate market research data for industry trends."""
    trends = {
        "industry": industry,
        "market_size_usd": random.randint(5, 200) * 1000000000,  # $5B to $200B
        "annual_growth_rate": random.uniform(0.02, 0.25),
        "key_trends": [
            "Digital transformation accelerating",
            "Sustainability becoming critical differentiator",
            "AI/ML adoption increasing",
            "Supply chain resilience focus",
            "Customer experience optimization"
        ],
        "disruptive_factors": [
            "Emerging technology adoption",
            "Regulatory changes",
            "Changing consumer behavior",
            "New market entrants"
        ],
        "growth_drivers": random.sample([
            "Technology innovation", "Market expansion", "Product differentiation",
            "Cost optimization", "Strategic partnerships", "Customer retention"
        ], 3)
    }
    
    return trends


def analyze_market_size(industry: str, region: str = "global") -> Dict[str, Any]:
    """Analyze total addressable market and market segments."""
    total_market = random.randint(10, 500) * 1000000000  # $10B to $500B
    
    market_analysis = {
        "industry": industry,
        "region": region,
        "total_addressable_market": total_market,
        "serviceable_addressable_market": int(total_market * random.uniform(0.1, 0.4)),
        "serviceable_obtainable_market": int(total_market * random.uniform(0.01, 0.05)),
        "market_segments": [
            {"segment": "Enterprise", "share": random.uniform(0.4, 0.7)},
            {"segment": "SMB", "share": random.uniform(0.2, 0.4)},
            {"segment": "Consumer", "share": random.uniform(0.1, 0.3)}
        ],
        "geographic_breakdown": {
            "North America": random.uniform(0.3, 0.5),
            "Europe": random.uniform(0.2, 0.3),
            "Asia Pacific": random.uniform(0.2, 0.4),
            "Other": random.uniform(0.05, 0.15)
        }
    }
    
    return market_analysis


def get_consumer_sentiment(industry: str) -> Dict[str, Any]:
    """Analyze consumer sentiment and behavior patterns."""
    sentiment_data = {
        "industry": industry,
        "overall_sentiment_score": random.uniform(3.0, 4.5),  # Out of 5
        "purchase_intent": random.uniform(0.3, 0.8),
        "brand_loyalty": random.uniform(0.4, 0.9),
        "price_sensitivity": random.uniform(0.2, 0.8),
        "top_concerns": random.sample([
            "Data privacy", "Product quality", "Customer service",
            "Pricing", "Sustainability", "Innovation"
        ], 3),
        "emerging_preferences": [
            "Personalized experiences",
            "Sustainable products",
            "Digital-first interactions",
            "Transparent communication"
        ]
    }
    
    return sentiment_data


# =============================================================================
# COMPETITIVE INTELLIGENCE TOOLS
# =============================================================================

def analyze_competitor_data(company_name: str, industry: str) -> Dict[str, Any]:
    """Analyze competitor landscape and positioning."""
    competitors = [
        f"{industry.title()} Corp", f"Global {industry.title()}", f"{industry.title()} Solutions Inc",
        f"Premier {industry.title()}", f"{industry.title()} Technologies", f"Advanced {industry.title()} Group"
    ]
    
    competitor_analysis = {
        "target_company": company_name,
        "industry": industry,
        "direct_competitors": random.sample(competitors, 3),
        "market_leaders": random.sample(competitors, 2),
        "competitive_landscape": {
            "market_concentration": random.choice(["Fragmented", "Moderately Concentrated", "Highly Concentrated"]),
            "barriers_to_entry": random.choice(["Low", "Medium", "High"]),
            "competitive_intensity": random.choice(["Low", "Medium", "High"])
        },
        "competitor_strengths": [
            "Strong brand recognition",
            "Extensive distribution network", 
            "Technology leadership",
            "Cost advantage",
            "Customer relationships"
        ]
    }
    
    return competitor_analysis


def get_market_positioning(company_name: str) -> Dict[str, Any]:
    """Analyze market positioning and competitive advantages."""
    positioning_data = {
        "company": company_name,
        "market_position": random.choice(["Market Leader", "Strong Challenger", "Follower", "Niche Player"]),
        "competitive_advantages": random.sample([
            "Technology innovation", "Cost leadership", "Customer service excellence",
            "Brand strength", "Distribution network", "Product quality"
        ], 3),
        "value_proposition": random.choice([
            "Premium quality at competitive price",
            "Innovation and cutting-edge technology",
            "Comprehensive solutions and service",
            "Cost-effective and reliable"
        ]),
        "market_share": random.uniform(0.05, 0.25),
        "differentiation_factors": random.sample([
            "Product features", "Service quality", "Brand reputation",
            "Pricing strategy", "Distribution channels", "Customer experience"
        ], 2)
    }
    
    return positioning_data


def track_competitor_pricing(industry: str) -> Dict[str, Any]:
    """Track competitor pricing strategies and market dynamics."""
    base_price = random.randint(100, 10000)
    
    pricing_data = {
        "industry": industry,
        "price_range": {
            "low": base_price,
            "high": int(base_price * random.uniform(2.0, 5.0))
        },
        "pricing_strategies": random.sample([
            "Value-based pricing", "Competitive pricing", "Cost-plus pricing",
            "Penetration pricing", "Premium pricing", "Dynamic pricing"
        ], 3),
        "price_trends": random.choice(["Increasing", "Stable", "Decreasing"]),
        "price_sensitivity": random.uniform(0.3, 0.9)
    }
    
    return pricing_data


# =============================================================================
# RISK ASSESSMENT TOOLS
# =============================================================================

def assess_business_risks(company_name: str, industry: str) -> Dict[str, Any]:
    """Assess various business risks and their impact."""
    risk_categories = {
        "operational_risks": [
            "Supply chain disruption", "Key personnel loss", "Technology failures",
            "Quality control issues", "Regulatory compliance"
        ],
        "financial_risks": [
            "Cash flow volatility", "Credit risk", "Currency fluctuation",
            "Interest rate changes", "Investment losses"
        ],
        "strategic_risks": [
            "Market disruption", "Competitive threats", "Technology obsolescence",
            "Customer concentration", "Product lifecycle"
        ],
        "external_risks": [
            "Economic downturn", "Regulatory changes", "Political instability",
            "Natural disasters", "Cybersecurity threats"
        ]
    }
    
    risk_assessment = {
        "company": company_name,
        "industry": industry,
        "overall_risk_score": random.uniform(2.0, 4.0),  # Out of 5
        "risk_breakdown": {}
    }
    
    for category, risks in risk_categories.items():
        selected_risks = random.sample(risks, random.randint(2, 4))
        risk_assessment["risk_breakdown"][category] = [
            {
                "risk": risk,
                "probability": random.uniform(0.1, 0.7),
                "impact": random.uniform(0.2, 0.9),
                "risk_score": random.uniform(0.1, 0.6)
            }
            for risk in selected_risks
        ]
    
    return risk_assessment


def scenario_modeling(company_name: str, scenarios: List[str] = None) -> Dict[str, Any]:
    """Model different business scenarios and their outcomes."""
    if scenarios is None:
        scenarios = ["Base Case", "Optimistic", "Pessimistic", "Disruptive"]
    
    base_revenue = random.randint(100, 500) * 1000000
    
    scenario_results = {
        "company": company_name,
        "modeling_period": "3 years",
        "scenarios": {}
    }
    
    for scenario in scenarios:
        if scenario == "Optimistic":
            growth_multiplier = random.uniform(1.2, 1.8)
            probability = random.uniform(0.2, 0.3)
        elif scenario == "Pessimistic":
            growth_multiplier = random.uniform(0.6, 0.9)
            probability = random.uniform(0.2, 0.3)
        elif scenario == "Disruptive":
            growth_multiplier = random.uniform(0.3, 2.5)
            probability = random.uniform(0.1, 0.2)
        else:  # Base Case
            growth_multiplier = random.uniform(0.9, 1.3)
            probability = random.uniform(0.4, 0.6)
        
        scenario_results["scenarios"][scenario] = {
            "probability": probability,
            "projected_revenue": int(base_revenue * growth_multiplier),
            "market_share_change": random.uniform(-0.1, 0.15),
            "profitability_impact": random.uniform(-0.2, 0.3)
        }
    
    return scenario_results


def regulatory_compliance_check(industry: str, region: str = "US") -> Dict[str, Any]:
    """Check regulatory compliance requirements and risks."""
    compliance_data = {
        "industry": industry,
        "region": region,
        "compliance_score": random.uniform(3.5, 4.8),  # Out of 5
        "regulatory_requirements": random.sample([
            "Data privacy (GDPR, CCPA)", "Financial reporting (SOX)",
            "Industry-specific regulations", "Environmental compliance",
            "Labor law compliance", "Tax regulations"
        ], 4),
        "upcoming_changes": random.sample([
            "New data protection laws", "Environmental regulations",
            "Industry safety standards", "Financial reporting requirements"
        ], 2),
        "compliance_costs": {
            "annual_percentage_of_revenue": random.uniform(0.02, 0.08),
            "implementation_costs": random.randint(100000, 2000000)
        }
    }
    
    return compliance_data
