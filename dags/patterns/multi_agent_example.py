from airflow.sdk import dag, task, Param
from pydantic_ai import Agent
from include.agent_tools import (
    get_financial_data, calculate_financial_ratios, get_revenue_projections,
    get_industry_trends, analyze_market_size, get_consumer_sentiment,
    analyze_competitor_data, get_market_positioning, track_competitor_pricing,
    assess_business_risks, scenario_modeling, regulatory_compliance_check
)
import json

orchestrator_agent = Agent(
    "gpt-4o-mini",
    system_prompt="""
    You are a Senior Strategy Consultant orchestrating a comprehensive business analysis.
    
    Your role is to:
    1. Analyze the company context and strategic situation
    2. Determine key focus areas for analysis
    3. Create specific, actionable tasks for specialist agents
    4. Prioritize analysis areas based on strategic importance
    
    Based on the company information provided, you should output a JSON structure with:
    {
        "company_analysis": "Brief analysis of company situation and strategic context",
        "priority_focus_areas": ["area1", "area2", "area3"],
        "specialist_tasks": {
            "financial_analyst": "Specific task for financial analysis",
            "market_researcher": "Specific task for market research", 
            "competitive_analyst": "Specific task for competitive analysis",
            "risk_assessor": "Specific task for risk assessment"
        }
    }
    
    Be specific and actionable in your task assignments.
    """,
)


financial_analyst_agent = Agent(
    "gpt-4o-mini",
    system_prompt="""
    You are a Senior Financial Analyst specializing in corporate finance and valuation.
    
    Your expertise includes:
    - Financial statement analysis and ratio calculation
    - Revenue projections and growth modeling
    - Profitability and efficiency assessment
    - Capital structure and liquidity analysis
    
    Use your tools to gather financial data and provide detailed analysis with:
    - Key financial metrics and trends
    - Strengths and weaknesses in financial performance
    - Revenue growth opportunities and risks
    - Recommendations for financial optimization
    
    Always provide data-driven insights with specific numbers and actionable recommendations.
    """,
    tools=[get_financial_data, calculate_financial_ratios, get_revenue_projections],
)

market_research_agent = Agent(
    "gpt-4o-mini", 
    system_prompt="""
    You are a Market Research Specialist with expertise in industry analysis and consumer behavior.
    
    Your expertise includes:
    - Industry trends and market dynamics
    - Market sizing and segmentation
    - Consumer sentiment and behavior analysis
    - Growth opportunity identification
    
    Use your tools to analyze market conditions and provide insights on:
    - Market size, growth potential, and key trends
    - Consumer preferences and buying behavior
    - Market opportunities and threats
    - Strategic positioning recommendations
    
    Focus on actionable market insights that can drive strategic decisions.
    """,
    tools=[get_industry_trends, analyze_market_size, get_consumer_sentiment],
)

competitive_intelligence_agent = Agent(
    "gpt-4o-mini",
    system_prompt="""
    You are a Competitive Intelligence Expert specializing in market positioning and competitor analysis.
    
    Your expertise includes:
    - Competitor landscape mapping
    - Competitive advantage assessment  
    - Market positioning analysis
    - Pricing strategy evaluation
    
    Use your tools to analyze the competitive environment and provide:
    - Competitor strengths, weaknesses, and strategies
    - Market positioning opportunities
    - Competitive threats and defensive strategies
    - Differentiation and competitive advantage recommendations
    
    Provide strategic insights that help achieve competitive advantage.
    """,
    tools=[analyze_competitor_data, get_market_positioning, track_competitor_pricing],
)

risk_assessment_agent = Agent(
    "gpt-4o-mini",
    system_prompt="""
    You are a Risk Assessment Expert specializing in business risk analysis and scenario planning.
    
    Your expertise includes:
    - Business risk identification and assessment
    - Scenario modeling and planning
    - Regulatory compliance analysis
    - Risk mitigation strategy development
    
    Use your tools to evaluate risks and provide:
    - Key risk areas and probability/impact assessment
    - Scenario analysis with different business outcomes
    - Regulatory compliance risks and requirements
    - Risk mitigation strategies and contingency plans
    
    Focus on practical risk management recommendations that protect and enable business growth.
    """,
    tools=[assess_business_risks, scenario_modeling, regulatory_compliance_check],
)


synthesis_agent = Agent(
    "gpt-4o-mini",
    system_prompt="""
    You are a Senior Strategy Director responsible for synthesizing multiple analyses into actionable strategic recommendations.
    
    Your role is to:
    1. Integrate insights from financial, market, competitive, and risk analyses
    2. Identify strategic priorities and trade-offs
    3. Create a comprehensive strategic roadmap
    4. Provide clear, prioritized recommendations with timelines
    
    Create a strategic roadmap that includes:
    - Executive summary of key findings
    - Strategic priorities ranked by impact and feasibility
    - Specific action items with timelines and resource requirements
    - Key success metrics and milestones
    - Risk mitigation plans for top strategic initiatives
    
    Your output should be practical, actionable, and clearly prioritized for executive decision-making.
    """,
)


@dag(
    params={
        "company_name": Param(
            type="string",
            default="TechCorp Solutions",
        ),
        "industry": Param(
            type="string", 
            default="Software Technology",
        ),
        "company_description": Param(
            type="string",
            default="A mid-size B2B software company specializing in enterprise solutions with 200 employees and $50M annual revenue",
        ),
    },
    tags=["Pattern Example"]
)
def multi_agent_example():

    @task
    def prepare_company_context(**context) -> str:
        """Prepare the company context for analysis."""
        params = context["params"]
        company_context = {
            "company_name": params["company_name"],
            "industry": params["industry"], 
            "description": params["company_description"]
        }
        
        print(f"🏢 Preparing strategic analysis for: {params['company_name']}")
        print(f"📊 Industry: {params['industry']}")
        print(f"📝 Description: {params['company_description']}")
        
        return json.dumps(company_context)

    @task.agent(agent=orchestrator_agent)
    def orchestrate_analysis(company_context: str) -> str:
        """Orchestrator analyzes context and creates tasks for specialist agents."""
        return f"Analyze this company and create specific tasks for our specialist team: {company_context}"

    @task.agent(agent=financial_analyst_agent)
    def financial_analysis(orchestrator_output: str, company_context: str) -> str:
        """Financial analyst performs financial health and projection analysis."""
        context_data = json.loads(company_context)
        orchestrator_data = json.loads(orchestrator_output)
        
        task = orchestrator_data.get("specialist_tasks", {}).get("financial_analyst", 
                                                                "Perform comprehensive financial analysis")
        
        return f"""
        Company: {context_data['company_name']}
        Industry: {context_data['industry']}
        Task: {task}
        
        Please perform detailed financial analysis using your tools.
        """

    @task.agent(agent=market_research_agent) 
    def market_analysis(orchestrator_output: str, company_context: str) -> str:
        """Market researcher analyzes industry trends and opportunities."""
        context_data = json.loads(company_context)
        orchestrator_data = json.loads(orchestrator_output)
        
        task = orchestrator_data.get("specialist_tasks", {}).get("market_researcher",
                                                                "Analyze market trends and opportunities")
        
        return f"""
        Company: {context_data['company_name']}
        Industry: {context_data['industry']}
        Task: {task}
        
        Please analyze market conditions and opportunities using your research tools.
        """

    @task.agent(agent=competitive_intelligence_agent)
    def competitive_analysis(orchestrator_output: str, company_context: str) -> str:
        """Competitive analyst examines competitive landscape and positioning."""
        context_data = json.loads(company_context)
        orchestrator_data = json.loads(orchestrator_output)
        
        task = orchestrator_data.get("specialist_tasks", {}).get("competitive_analyst",
                                                                "Analyze competitive landscape and positioning")
        
        return f"""
        Company: {context_data['company_name']}
        Industry: {context_data['industry']}
        Task: {task}
        
        Please analyze the competitive environment using your intelligence tools.
        """

    @task.agent(agent=risk_assessment_agent)
    def risk_analysis(orchestrator_output: str, company_context: str) -> str:
        """Risk assessor evaluates business risks and scenarios.""" 
        context_data = json.loads(company_context)
        orchestrator_data = json.loads(orchestrator_output)
        
        task = orchestrator_data.get("specialist_tasks", {}).get("risk_assessor",
                                                                "Assess business risks and scenarios")
        
        return f"""
        Company: {context_data['company_name']}
        Industry: {context_data['industry']}
        Task: {task}
        
        Please evaluate business risks and scenarios using your assessment tools.
        """

    @task.agent(agent=synthesis_agent)
    def synthesize_strategy(
        orchestrator_output: str,
        financial_analysis: str, 
        market_analysis: str,
        competitive_analysis: str,
        risk_analysis: str,
        company_context: str
    ) -> str:
        """Synthesis agent combines all analyses into strategic roadmap."""
        context_data = json.loads(company_context)
        
        return f"""
        Company: {context_data['company_name']}
        
        Please synthesize the following specialist analyses into a comprehensive strategic roadmap:
        
        ORCHESTRATOR INSIGHTS:
        {orchestrator_output}
        
        FINANCIAL ANALYSIS:
        {financial_analysis}
        
        MARKET RESEARCH:
        {market_analysis}
        
        COMPETITIVE INTELLIGENCE: 
        {competitive_analysis}
        
        RISK ASSESSMENT:
        {risk_analysis}
        
        Create a prioritized strategic roadmap with clear recommendations and action items.
        """

    @task
    def finalize_strategic_report(synthesis_result: str, company_context: str) -> dict:
        """Final task to format and present the strategic analysis results."""
        context_data = json.loads(company_context)
        
        result = {
            "company": context_data["company_name"],
            "industry": context_data["industry"],
            "strategic_roadmap": synthesis_result,
            "analysis_type": "Multi-Agent Business Strategy Analysis",
            "word_count": len(synthesis_result.split()),
            "character_count": len(synthesis_result)
        }
        
        print(f"✅ Strategic analysis completed for {context_data['company_name']}")
        print(f"📊 Roadmap generated with {result['word_count']} words")

        # write to include as a markdown file
        with open("include/strategic_analysis.md", "w") as f:
            f.write(synthesis_result)
        
        return result

    company_ctx = prepare_company_context()
    orchestrator_result = orchestrate_analysis(company_ctx)
    
    financial_result = financial_analysis(orchestrator_result, company_ctx)
    market_result = market_analysis(orchestrator_result, company_ctx)
    competitive_result = competitive_analysis(orchestrator_result, company_ctx)
    risk_result = risk_analysis(orchestrator_result, company_ctx)
    
    strategy_synthesis = synthesize_strategy(
        orchestrator_result,
        financial_result,
        market_result, 
        competitive_result,
        risk_result,
        company_ctx
    )
    
    finalize_strategic_report(strategy_synthesis, company_ctx)


multi_agent_example()