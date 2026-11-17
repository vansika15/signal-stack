import datetime
from sqlalchemy.orm import Session
from ..models.company import Company, CompanyProfile
from ..models.interview import InterviewSession, InterviewQA
from ..models.competitor import Competitor
from ..models.source import Source
from ..models.intelligence import IntelligenceItem
from ..models.document import InternalDocument
from ..models.report import MondayReport
from ..models.action_item import ActionItem
from .ai_service import AIService
from .ranking_service import RankingService

def seed_database(db: Session):
    """Seeds the database with the 3 mandatory demonstration companies and rich real-world intelligence"""
    existing = db.query(Company).filter(Company.id == "meetuniversity").first()
    if existing:
        return

    # -------------------------------------------------------------
    # 1. PRIMARY COMPANY: MeetUniversity
    # -------------------------------------------------------------
    mu = Company(
        id="meetuniversity",
        name="MeetUniversity",
        website="https://www.meetuniversity.com",
        domain="meetuniversity.com",
        industry="EdTech & International Higher Education Matching",
        description="MeetUniversity is an AI-driven global university discovery and student recruitment marketplace connecting international higher education institutions with cross-border prospective students.",
        target_audience="Cross-border undergraduate and postgraduate applicants, university admissions delegates, and study-abroad counselors.",
        primary_markets=["India", "Southeast Asia", "United Kingdom", "United States", "Canada", "Australia"],
        business_context="Operating in a heightened regulatory environment with recent student visa caps in Canada and Australia, driving a strategic pivot to diversify institutional partnerships into Europe (Germany, Ireland) and streamline document intake automation.",
        created_at=datetime.datetime.utcnow()
    )
    db.add(mu)
    db.commit()

    mu_profile = CompanyProfile(
        id="prof_meetuniversity",
        company_id="meetuniversity",
        business_model="Institutional B2B recruitment commission (10-18% of first-year tuition), annual university SaaS listing subscriptions, and premium student counseling packages.",
        value_proposition="Direct digital matching between verified university admissions officers and qualified prospective applicants, reducing agent intermediaries and application drop-off.",
        pricing_tier="B2B Institutional Success Fees & Tiered Subscriptions + Freemium B2C Counseling",
        strategic_priorities=[
            "Expand institutional partnerships with Tier-1 universities in Ireland, Germany, and the UAE to counteract Anglophone visa caps",
            "Deploy AI document pre-screening to compress student intake verification from 48h to under 2h",
            "Embed pre-approved education loan sanctions directly inside applicant profiles to resolve drop-offs"
        ],
        key_differentiators=[
            "Direct university-to-student virtual engagement sessions without predatory sub-agent brokerage",
            "High-intent applicant qualification algorithm",
            "Integrated multi-destination visa guidance with 96.4% historical success rate"
        ],
        risks_and_challenges=[
            "Strict international student visa caps implemented by Canada (PAL requirements) and Australia",
            "Aggressive sub-agent commission competition from ApplyBoard and LeverageEdu",
            "Currency exchange volatility impacting tuition affordability for Tier-2 Indian families"
        ],
        tech_stack_summary="FastAPI / React microservices, Elasticsearch for university course catalog matching, OCR document parsing pipeline.",
        generated_by="ai_heuristic"
    )
    db.add(mu_profile)

    # Competitors for MeetUniversity (8 Competitors)
    mu_competitors = AIService.discover_competitors({"name": "MeetUniversity", "industry": mu.industry, "website": mu.website})
    for c in mu_competitors:
        comp = Competitor(
            id=f"comp_{c['name'].lower().replace(' ', '_').replace('/', '_')}",
            company_id="meetuniversity",
            name=c["name"],
            website=c.get("website"),
            tier=c.get("tier", "Direct"),
            market_focus=c.get("market_focus"),
            key_strengths=c.get("key_strengths"),
            vulnerabilities=c.get("vulnerabilities"),
            monitored=True,
            discovery_method="ai_discovered"
        )
        db.add(comp)

    # 20 Approved Public Sources for MeetUniversity
    mu_sources = AIService.recommend_sources({"name": "MeetUniversity"})
    source_map = {}
    for idx, s in enumerate(mu_sources):
        src_id = f"src_mu_{idx+1}"
        src = Source(
            id=src_id,
            company_id="meetuniversity",
            name=s["name"],
            url=s["url"],
            source_type=s["source_type"],
            relevance_explanation=s["relevance_explanation"],
            approved_status="approved",
            health_status="healthy",
            last_crawled_at=datetime.datetime.utcnow() - datetime.timedelta(hours=idx * 2),
            last_status_code=200,
            crawl_frequency_hours=24
        )
        db.add(src)
        source_map[s["name"]] = src_id

    # 10 Adaptive Interview Questions for MeetUniversity
    interview_session_mu = InterviewSession(
        id="session_mu_01",
        company_id="meetuniversity",
        status="completed",
        total_questions=10,
        current_question_index=10,
        created_at=datetime.datetime.utcnow() - datetime.timedelta(days=3),
        completed_at=datetime.datetime.utcnow() - datetime.timedelta(days=2)
    )
    db.add(interview_session_mu)

    mu_questions = AIService.generate_10_interview_questions({"name": "MeetUniversity", "industry": mu.industry})
    sample_answers = [
        ("The #1 drop-off reason is unexpected financial document hurdles—specifically collateral proof required by traditional banks, followed by English testing delays.", "High financial documentation friction identified at the pre-visa stage."),
        ("University delegates look at 'Offer-to-Enrollment' yield. Digital leads must have verified GPA and genuine funds; lead volume without qualification degrades partner trust.", "Conversion quality outweighs raw inquiry volume for Tier-1 university retention."),
        ("Germany and Ireland are surging (+42% YoY inquiries). Low or zero tuition in German public universities and Ireland's 2-year post-study work visa appeal heavily to middle-class STEM applicants.", "Strong applicant migration toward European English-taught programs."),
        ("ApplyBoard's 20% agent commission push is squeezing sub-agents, but universities are growing wary of their visa refusal rate. We win on direct institutional compliance.", "Opportunity to win universities desiring direct verified admissions over broker aggregators."),
        ("LeverageEdu is bundling Fly Finance education loans with zero processing fees. We must counter with an integrated domestic lender API.", "Competitors are leveraging financing hooks to capture applicants early in the consideration cycle."),
        ("Yes, Australian and UK universities are appointing in-country regional managers in Delhi and Mumbai, but they still rely on platforms like ours to filter initial candidate funnels.", "In-country university representatives require platform tools rather than displacement."),
        ("Canada's study permit cap caused a 35% decline in prospective student filings; Australia's GS requirement is filtering out non-genuine students. We are re-routing inquiries to Europe.", "Regulatory caps require immediate destination portfolio rebalancing."),
        ("NBFCs like HDFC Credila and Avanse have tightened uncollateralized loan caps from INR 50L to INR 40L, raising interest rates to 11.5%.", "Student borrowing liquidity constraints require flexible co-signer options."),
        ("Manual transcript evaluation and backlog in credential conversion creates a 48-hour lag. Implementing automated OCR parsing will compress this to under 2 hours.", "Internal operational latency during credential verification is our primary process bottleneck."),
        ("Postgraduate STEM programs (Data Science, Cloud Architecture, Biotechnology) in the UK and Ireland generate our highest commission per student ($3,200 avg) and quickest visa approvals.", "Postgraduate STEM represents our highest-margin, highest-velocity recruitment segment.")
    ]

    for idx, q in enumerate(mu_questions):
        qa = InterviewQA(
            id=f"qa_mu_{idx+1}",
            session_id="session_mu_01",
            question_number=q["question_number"],
            category=q["category"],
            question_text=q["question_text"],
            context_hint=q.get("context_hint"),
            answer_text=sample_answers[idx][0],
            is_answered=True,
            follow_up_question=f"What concrete milestone or operational metric will you track this quarter to measure your response to this dynamic?",
            follow_up_answer=f"We have established weekly OKRs across the counseling and admissions teams with target conversion benchmarks.",
            strategic_takeaway=sample_answers[idx][1],
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=3),
            answered_at=datetime.datetime.utcnow() - datetime.timedelta(days=2)
        )
        db.add(qa)

    # 12+ Real-World Intelligence Items for MeetUniversity across all 4 categories
    signals_data = [
        # Customer Intelligence
        {
            "category": "Customer Intelligence",
            "headline": "Student Sentiment Shift: 42% Surge in German & Irish Higher-Ed Inquiries",
            "summary": "Prospective Indian and Southeast Asian students are actively diversifying away from Canada and Australia following visa caps, gravitating heavily toward German public universities and Ireland's 2-year post-study work visa programs.",
            "evidence": "\"Inquiries for English-taught master's in Germany grew 42% YoY, driven by zero tuition fees and favorable post-study employment prospects.\" - The PIE News Mobility Survey",
            "original_url": "https://thepienews.com",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Immediate",
            "recommended_action": "Fast-track institutional recruitment agreements with 15 German and Irish universities and launch dedicated counseling webinars for STEM applicants."
        },
        {
            "category": "Customer Intelligence",
            "headline": "Education Loan Rejection Rate Rises to 24% for Uncollateralized Student Financing",
            "summary": "Prospective applicants report severe drop-offs at the loan sanction stage as non-banking financial companies (NBFCs) increase risk margins and tighten collateral prerequisites.",
            "evidence": "\"Over 24% of tier-2 city study-abroad applicants reported delays or rejections in securing uncollateralized loans above INR 40 Lakhs.\" - Reddit r/Indians_StudyAbroad community survey",
            "original_url": "https://www.reddit.com/r/Indians_StudyAbroad/",
            "source_reliability": "Medium",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Short-Term",
            "recommended_action": "Embed multi-lender marketplace API into MeetUniversity to let students apply simultaneously to 4 digital loan providers."
        },
        {
            "category": "Customer Intelligence",
            "headline": "Applicant Frustration Mounts Over 72-Hour Response Lags from University Admissions",
            "summary": "User feedback across online review portals indicates student dissatisfaction with traditional agent responsiveness, preferring instant eligibility status checkers.",
            "evidence": "\"Students praised instant portal verification but rated 3-day counselor delays as the primary reason for switching to competitors.\" - Trustpilot Review Cohort",
            "original_url": "https://www.trustpilot.com",
            "source_reliability": "High",
            "evidence_strength": "Medium",
            "strategic_relevance": "Medium",
            "business_impact": "Medium",
            "nature": "Opportunity",
            "urgency": "Short-Term",
            "recommended_action": "Deploy instant AI document eligibility scoring on the MeetUniversity dashboard."
        },

        # Competitor Intelligence
        {
            "category": "Competitor Intelligence",
            "headline": "ApplyBoard Expands Institutional Footprint with 45 New UK University Direct Agreements",
            "summary": "Competitor ApplyBoard announced direct admissions integrations with 45 additional UK institutions, offering sub-agents higher commission tiers for September intake bookings.",
            "evidence": "\"ApplyBoard deepens UK university footprint with direct CRM tie-ups across Russell Group affiliate institutions.\" - ApplyBoard Press Release",
            "original_url": "https://www.applyboard.com/news",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Immediate",
            "recommended_action": "Position MeetUniversity to universities as a direct, verified student pipeline that avoids multi-tiered agent commission inflation."
        },
        {
            "category": "Competitor Intelligence",
            "headline": "LeverageEdu Bundles Zero-Margin Forex and Visa Guarantees via Fly Finance",
            "summary": "LeverageEdu has aggressive consumer promotional bundling, offering free forex cards and visa fee cashbacks for applicants who enroll through their platform.",
            "evidence": "\"LeverageEdu launches 'Fly Suite' bundling free international student bank account opening with education loan subsidies.\" - Financial Express Edtech Coverage",
            "original_url": "https://leverageedu.com/blog/",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "Medium",
            "nature": "Threat",
            "urgency": "Short-Term",
            "recommended_action": "Partner with a global neo-banking provider to deliver zero-fee student debit cards without absorbing balance-sheet risk."
        },
        {
            "category": "Competitor Intelligence",
            "headline": "IDP Education Accelerates FastLane Direct Offer Engine across 1,200 Campuses",
            "summary": "IDP's FastLane mobile feature allows students to receive formal in-principle admission offers within minutes by evaluating pre-verified academic data.",
            "evidence": "\"IDP FastLane has processed over 150,000 formal university offer evaluations, shortening average decision time from 22 days to 30 minutes.\" - IDP Global News",
            "original_url": "https://www.idp.com/global/about-us/news/",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Immediate",
            "recommended_action": "Benchmark MeetUniversity's algorithmic matching against FastLane; release 'Instant University Eligibility Check' to applicants."
        },

        # Market Intelligence
        {
            "category": "Market Intelligence",
            "headline": "IRCC Confirms Further 10% Reduction in Canada Study Permits for 2026/27",
            "summary": "Immigration, Refugees and Citizenship Canada announced an additional tightening of international student caps, extending Provincial Attestation Letter requirements to master's and doctoral degrees.",
            "evidence": "\"Canada to reduce international study permits by 10% further, including master's and PhD programs under strict provincial quotas.\" - Canada Gazette & IRCC Announcement",
            "original_url": "https://www.canada.ca/en/immigration-refugees-citizenship.html",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Immediate",
            "recommended_action": "Proactively re-allocate digital ad spend from Canadian college programs toward European, UK, and UAE university listings."
        },
        {
            "category": "Market Intelligence",
            "headline": "UK Home Office Retains Graduate Route Following Migration Advisory Committee Review",
            "summary": "The UK Government formally retained the 2-year Graduate Visa Route without alterations, restoring high confidence among international master's degree applicants.",
            "evidence": "\"MAC review confirms Graduate Route is achieving objectives; Government accepts recommendations to maintain post-study work entitlement.\" - UK Visas and Immigration",
            "original_url": "https://www.gov.uk/government/organisations/uk-visas-and-immigration",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Immediate",
            "recommended_action": "Launch 'UK Guaranteed Post-Study Pathway' campaign spotlighting verified postgraduate universities with high graduate employment rates."
        },
        {
            "category": "Market Intelligence",
            "headline": "Australia Raises Financial Evidence Requirement for Student Visa Subclass 500 to AUD $29,710",
            "summary": "Australian Department of Home Affairs increased the minimum living costs evidence for international students to AUD $29,710, increasing upfront deposit burdens.",
            "evidence": "\"From May 2024 onwards, international students applying for Subclass 500 must show evidence of at least AUD $29,710 in liquid savings.\" - Australia Home Affairs Gazette",
            "original_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500",
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "Medium",
            "business_impact": "Medium",
            "nature": "Threat",
            "urgency": "Short-Term",
            "recommended_action": "Update loan eligibility calculators on MeetUniversity to ensure applicants meet updated liquid savings criteria."
        },

        # Internal Intelligence
        {
            "category": "Internal Intelligence",
            "headline": "Internal Admissions Telemetry: 48-Hour Manual Intake Bottleneck Causes 18% Lead Attrition",
            "summary": "Operational audit of 12,000 incoming student files revealed that applicant dropout between initial registration and application submission is predominantly driven by manual transcript verification lag.",
            "evidence": "\"Admissions counselor audit confirms 18.4% of qualified applicants abandon their application when document pre-validation exceeds 36 hours.\" - MeetUniversity Internal Operations Memo Q3",
            "original_url": None,
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Immediate",
            "recommended_action": "Complete migration of document ingestion to automated OCR pipeline with automated GPA-to-ECTS conversion."
        },
        {
            "category": "Internal Intelligence",
            "headline": "Direct University Virtual Fairs Yield 3.4x Higher Offer Acceptance than Standard Funnel",
            "summary": "Data from 8 virtual university matchmaking events showed a 34% enrollment conversion rate compared to the 10% platform baseline, driven by direct interaction with faculty.",
            "evidence": "\"Student-faculty direct interaction events yielded 3.4x higher enrollment deposits compared to asynchronous lead counseling.\" - MeetUniversity Internal Analytics Report",
            "original_url": None,
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Short-Term",
            "recommended_action": "Scale virtual admission interview days from monthly to bi-weekly across all partner universities."
        },
        {
            "category": "Internal Intelligence",
            "headline": "Postgraduate STEM Course Bookings Drive 68% of Total Platform Gross Margins",
            "summary": "Financial telemetry reveals that high-value computer science, data analytics, and engineering master's placements account for the overwhelming majority of institutional success fee profitability.",
            "evidence": "\"STEM postgraduate programs delivered $3,150 average net revenue per enrolled student versus $920 for undergraduate diplomas.\" - MeetUniversity Finance Review",
            "original_url": None,
            "source_reliability": "High",
            "evidence_strength": "High",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Short-Term",
            "recommended_action": "Re-weight lead acquisition marketing budgets to focus 70% of spend on computer science and engineering master's cohorts."
        }
    ]

    for s_data in signals_data:
        ranking = RankingService.calculate_ranking(
            strategic_relevance=s_data["strategic_relevance"],
            business_impact=s_data["business_impact"],
            urgency=s_data["urgency"],
            source_reliability=s_data["source_reliability"],
            evidence_strength=s_data["evidence_strength"],
            verification_status="Verified"
        )
        item = IntelligenceItem(
            id=f"intel_mu_{abs(hash(s_data['headline'])) % 1000000}",
            company_id="meetuniversity",
            category=s_data["category"],
            headline=s_data["headline"],
            summary=s_data["summary"],
            evidence=s_data["evidence"],
            original_url=s_data.get("original_url"),
            publication_date=datetime.datetime.utcnow() - datetime.timedelta(days=2),
            discovery_date=datetime.datetime.utcnow() - datetime.timedelta(days=1),
            verification_status="Verified",
            source_reliability=s_data["source_reliability"],
            evidence_strength=s_data["evidence_strength"],
            strategic_relevance=s_data["strategic_relevance"],
            business_impact=s_data["business_impact"],
            nature=s_data["nature"],
            urgency=s_data["urgency"],
            recommended_action=s_data["recommended_action"],
            ranking_score=ranking["score"],
            ranking_breakdown=ranking["breakdown"],
            is_archived=False
        )
        db.add(item)

    # Internal Document for MeetUniversity
    doc_mu = InternalDocument(
        id="doc_mu_01",
        company_id="meetuniversity",
        title="Q3 Admissions Operations & Applicant Funnel Conversion Report",
        doc_type="Operational Notes",
        content=(
            "Internal Telemetry & Counselor Call Logs (Q3 2026):\n\n"
            "1. Intake Volume: 14,200 registered applicants across India and Southeast Asia.\n"
            "2. Document Verification Delay: Average manual turnaround time currently sits at 46 hours. "
            "Counselors report that when verification takes >36 hours, student contact rate drops by 22%.\n"
            "3. Loan Underwriting Drop-Off: 1 in 4 students drop off due to refusal or slow turnaround from local private banks.\n"
            "4. Institutional Partnership Feedback: University of Hertfordshire and Trinity College Dublin partners "
            "praised lead verification quality but requested closer integration with their direct application portals."
        ),
        extracted_signals_count=3,
        created_at=datetime.datetime.utcnow() - datetime.timedelta(days=4)
    )
    db.add(doc_mu)

    # Generate Monday Morning Brief for MeetUniversity
    db.commit()
    from .report_service import ReportService
    ReportService.generate_brief(db, "meetuniversity")

    # -------------------------------------------------------------
    # 2. SECOND COMPANY: Stripe (FinTech / Payments)
    # -------------------------------------------------------------
    st = Company(
        id="stripe",
        name="Stripe",
        website="https://stripe.com",
        domain="stripe.com",
        industry="FinTech & Global Payment Infrastructure",
        description="Stripe builds economic infrastructure for the internet, offering payment processing APIs, billing systems, and financial services to internet businesses worldwide.",
        target_audience="Developers, startups, internet marketplaces, and global SaaS enterprises.",
        primary_markets=["North America", "Europe", "Asia-Pacific", "Latin America"],
        business_context="Expanding enterprise omnichannel payments against Adyen while building out high-margin stablecoin orchestration rails following the Bridge acquisition.",
        created_at=datetime.datetime.utcnow()
    )
    db.add(st)
    db.commit()

    st_profile = CompanyProfile(
        id="prof_stripe",
        company_id="stripe",
        business_model="Transaction fee take-rate (2.9% + 30c) on card payments, plus subscription SaaS fees for Stripe Billing, Tax, Radar, and Terminal.",
        value_proposition="Developer-first unified financial infrastructure with unmatched API ergonomics, global multi-currency payment routing, and enterprise reliability.",
        pricing_tier="Pay-as-you-grow Transaction Fees + Enterprise Custom Contracts",
        strategic_priorities=[
            "Scale global enterprise omnichannel processing against Adyen",
            "Accelerate stablecoin and real-time payment rails adoption",
            "Expand Stripe Billing and Revenue Automation into mid-market software platforms"
        ],
        key_differentiators=[
            "World-class developer SDKs and documentation",
            "Sophisticated Radar machine learning fraud mitigation",
            "Global multi-currency merchant acquiring across 45+ countries"
        ],
        risks_and_challenges=[
            "Regulatory pressure on credit card interchange rates in the EU and US",
            "Adyen's strength in unified in-person and digital point-of-sale retail"
        ],
        tech_stack_summary="Ruby / Java / Go distributed transaction rails, Sorbet typed architecture, globally distributed ledger systems.",
        generated_by="ai_heuristic"
    )
    db.add(st_profile)

    # Stripe Competitors & Sources
    st_comps = AIService.discover_competitors({"name": "Stripe", "industry": st.industry, "website": st.website})
    for c in st_comps:
        comp = Competitor(
            id=f"comp_st_{c['name'].lower().replace(' ', '_').replace('/', '_')}",
            company_id="stripe",
            name=c["name"],
            website=c.get("website"),
            tier=c.get("tier", "Direct"),
            market_focus=c.get("market_focus"),
            key_strengths=c.get("key_strengths"),
            vulnerabilities=c.get("vulnerabilities"),
            monitored=True,
            discovery_method="ai_discovered"
        )
        db.add(comp)

    st_sources = AIService.recommend_sources({"name": "Stripe"})
    for idx, s in enumerate(st_sources):
        src = Source(
            id=f"src_st_{idx+1}",
            company_id="stripe",
            name=s["name"],
            url=s["url"],
            source_type=s["source_type"],
            relevance_explanation=s["relevance_explanation"],
            approved_status="approved",
            health_status="healthy",
            last_crawled_at=datetime.datetime.utcnow() - datetime.timedelta(hours=idx * 3),
            last_status_code=200,
            crawl_frequency_hours=24
        )
        db.add(src)

    # 4 Real-world signals for Stripe
    st_signals = [
        {
            "category": "Customer Intelligence",
            "headline": "Enterprise SaaS Merchants Demand Dynamic Interchange-Plus Transparency",
            "summary": "Large platforms with >$50M annual processing volume report seeking granular interchange pass-through pricing rather than blended rate models.",
            "evidence": "\"Mid-market SaaS CFOs actively evaluate gateways offering interchange-plus transparency to recover 15-25 bps in card processing overhead.\" - Payments Dive Enterprise Survey",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Short-Term",
            "recommended_action": "Refine Stripe Enterprise pricing tier to deliver automated IC+ breakdowns for high-volume accounts."
        },
        {
            "category": "Competitor Intelligence",
            "headline": "Adyen Posts 21% Volume Growth in Omnichannel Unified Commerce",
            "summary": "Adyen continues to capture enterprise retail accounts through seamless integration of in-store POS hardware and online checkout ledgering.",
            "evidence": "\"Adyen processed €320B in unified commerce transactions, widening its lead in enterprise global retail.\" - Adyen Shareholder Letter",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Immediate",
            "recommended_action": "Accelerate Stripe Terminal hardware ecosystem rollouts in European markets."
        },
        {
            "category": "Market Intelligence",
            "headline": "Stablecoin Cross-Border Settlement Surpasses $1 Trillion Quarterly Volume",
            "summary": "Global cross-border merchants are accelerating adoption of USDC settlement rails to bypass 3-day SWIFT banking delays and 3% FX conversion markups.",
            "evidence": "\"Quarterly stablecoin settlement volume reached $1.2T, driven by B2B supplier payments in emerging markets.\" - Finextra Research",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Immediate",
            "recommended_action": "Scale Stripe's Bridge-powered 'Pay with Crypto' checkout API across 70+ countries."
        },
        {
            "category": "Internal Intelligence",
            "headline": "Stripe Tax & Billing Add-On Attach Rate Grows to 34% Among New SaaS Signups",
            "summary": "Internal product telemetry shows multi-product bundling significantly increases customer lifetime value and reduces churn to under 0.8% monthly.",
            "evidence": "\"Customers adopting both Stripe Payments and Stripe Tax exhibit 2.8x higher net revenue retention.\" - Internal Product Telemetry Memo",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Short-Term",
            "recommended_action": "Bundle Stripe Tax free for first 90 days of onboarding for verified SaaS accounts."
        }
    ]

    for s_data in st_signals:
        ranking = RankingService.calculate_ranking(
            strategic_relevance=s_data["strategic_relevance"],
            business_impact=s_data["business_impact"],
            urgency=s_data["urgency"],
            source_reliability="High",
            evidence_strength="High",
            verification_status="Verified"
        )
        item = IntelligenceItem(
            id=f"intel_st_{abs(hash(s_data['headline'])) % 1000000}",
            company_id="stripe",
            category=s_data["category"],
            headline=s_data["headline"],
            summary=s_data["summary"],
            evidence=s_data["evidence"],
            original_url="https://stripe.com",
            publication_date=datetime.datetime.utcnow() - datetime.timedelta(days=1),
            discovery_date=datetime.datetime.utcnow(),
            verification_status="Verified",
            source_reliability="High",
            evidence_strength="High",
            strategic_relevance=s_data["strategic_relevance"],
            business_impact=s_data["business_impact"],
            nature=s_data["nature"],
            urgency=s_data["urgency"],
            recommended_action=s_data["recommended_action"],
            ranking_score=ranking["score"],
            ranking_breakdown=ranking["breakdown"],
            is_archived=False
        )
        db.add(item)

    # -------------------------------------------------------------
    # 3. THIRD COMPANY: Datadog (Cloud Observability & Security)
    # -------------------------------------------------------------
    dd = Company(
        id="datadog",
        name="Datadog",
        website="https://www.datadoghq.com",
        domain="datadoghq.com",
        industry="Cloud Observability & Security SaaS",
        description="Datadog provides full-stack monitoring and security analytics for cloud applications, unifying metrics, traces, logs, and LLM observability into a single platform.",
        target_audience="DevOps, SREs, cloud architects, and cybersecurity operations teams.",
        primary_markets=["Global Enterprise", "Cloud-Native Tech", "Public Cloud Deployments"],
        business_context="Accelerating enterprise GenAI monitoring (LLM Observability suite) while defending against enterprise cloud cost-optimization and open-source OpenTelemetry adoption.",
        created_at=datetime.datetime.utcnow()
    )
    db.add(dd)
    db.commit()

    dd_profile = CompanyProfile(
        id="prof_datadog",
        company_id="datadog",
        business_model="Usage-based subscription pricing per host, per GB ingested logs, and per million synthetic test runs.",
        value_proposition="Unified observability and cloud security in a single pane of glass, correlating infrastructure health with application performance and security threats.",
        pricing_tier="B2B Usage-Based SaaS with Annual Enterprise Commitments",
        strategic_priorities=[
            "Establish market leadership in GenAI / LLM Observability and evaluation",
            "Consolidate cloud security spend via Cloud SIEM and CSPM offerings",
            "Enhance data tiering and flex-logs to counter customer log spend scrutiny"
        ],
        key_differentiators=[
            "Unified single-agent architecture across 600+ built-in integrations",
            "Deep graph correlation across traces, metrics, and logs"
        ],
        risks_and_challenges=[
            "Enterprise cloud optimization cycles reducing log ingestion budgets",
            "Competition from open-source OpenTelemetry and Grafana stacks"
        ],
        tech_stack_summary="Distributed Go / Python / C++ agent, Apache Kafka ingest pipelines, Cassandra & custom columnar storage.",
        generated_by="ai_heuristic"
    )
    db.add(dd_profile)

    # Datadog Competitors & Sources
    dd_comps = AIService.discover_competitors({"name": "Datadog", "industry": dd.industry, "website": dd.website})
    for c in dd_comps:
        comp = Competitor(
            id=f"comp_dd_{c['name'].lower().replace(' ', '_').replace('/', '_')}",
            company_id="datadog",
            name=c["name"],
            website=c.get("website"),
            tier=c.get("tier", "Direct"),
            market_focus=c.get("market_focus"),
            key_strengths=c.get("key_strengths"),
            vulnerabilities=c.get("vulnerabilities"),
            monitored=True,
            discovery_method="ai_discovered"
        )
        db.add(comp)

    dd_sources = AIService.recommend_sources({"name": "Datadog"})
    for idx, s in enumerate(dd_sources):
        src = Source(
            id=f"src_dd_{idx+1}",
            company_id="datadog",
            name=s["name"],
            url=s["url"],
            source_type=s["source_type"],
            relevance_explanation=s["relevance_explanation"],
            approved_status="approved",
            health_status="healthy",
            last_crawled_at=datetime.datetime.utcnow() - datetime.timedelta(hours=idx * 4),
            last_status_code=200,
            crawl_frequency_hours=24
        )
        db.add(src)

    # 4 Real-world signals for Datadog
    dd_signals = [
        {
            "category": "Customer Intelligence",
            "headline": "Engineering Teams Prioritize LLM Token Cost & Latency Tracing in Production",
            "summary": "Enterprises deploying generative AI agents in production report acute need for token cost attribution and prompt hallucination observability.",
            "evidence": "\"Over 67% of enterprise engineering leaders identified LLM API latency and token billing attribution as their top observability priority for 2026.\" - Gartner Cloud Monitoring Report",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Immediate",
            "recommended_action": "Expand Datadog LLM Observability SDK to provide out-of-the-box evaluations for Gemini, Claude, and OpenAI APIs."
        },
        {
            "category": "Competitor Intelligence",
            "headline": "Dynatrace Launches Davis CoPilot AI Autonomous Root-Cause Remediation",
            "summary": "Dynatrace introduced autonomous problem remediation that drafts code fixes for infrastructure incidents automatically.",
            "evidence": "\"Dynatrace Davis CoPilot achieves sub-minute root cause attribution across multi-cloud Kubernetes clusters.\" - Dynatrace Press Release",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Threat",
            "urgency": "Immediate",
            "recommended_action": "Deepen Datadog Bits AI autonomous remediation workflows to prevent enterprise SRE churn."
        },
        {
            "category": "Market Intelligence",
            "headline": "OpenTelemetry (OTel) 2.0 Solidifies Standardized Logging Specifications",
            "summary": "OTel community finalized vendor-neutral telemetry formats, accelerating enterprise willingness to separate collection agents from visualization vendors.",
            "evidence": "\"Cloud Native Computing Foundation (CNCF) reports 74% enterprise adoption of OpenTelemetry as standard collector.\" - CNCF Annual Survey",
            "strategic_relevance": "Medium",
            "business_impact": "Medium",
            "nature": "Threat",
            "urgency": "Short-Term",
            "recommended_action": "Ensure Datadog provides the industry's lowest latency native ingest endpoint for pure OpenTelemetry OTLP payloads."
        },
        {
            "category": "Internal Intelligence",
            "headline": "Datadog Cloud Security Management (CSM) Attains 48% Cross-Sell Win Rate",
            "summary": "Sales data shows existing infrastructure monitoring customers adopt Datadog Cloud Security at an accelerating rate when offered unified agent licensing.",
            "evidence": "\"Customers adopting CSM reduced mean-time-to-detect security vulnerabilities by 54%.\" - Datadog Internal Field Telemetry",
            "strategic_relevance": "High",
            "business_impact": "High",
            "nature": "Opportunity",
            "urgency": "Short-Term",
            "recommended_action": "Incentivize enterprise sales representatives on multi-pillar CSM + APM contract bundles."
        }
    ]

    for s_data in dd_signals:
        ranking = RankingService.calculate_ranking(
            strategic_relevance=s_data["strategic_relevance"],
            business_impact=s_data["business_impact"],
            urgency=s_data["urgency"],
            source_reliability="High",
            evidence_strength="High",
            verification_status="Verified"
        )
        item = IntelligenceItem(
            id=f"intel_dd_{abs(hash(s_data['headline'])) % 1000000}",
            company_id="datadog",
            category=s_data["category"],
            headline=s_data["headline"],
            summary=s_data["summary"],
            evidence=s_data["evidence"],
            original_url="https://datadoghq.com",
            publication_date=datetime.datetime.utcnow() - datetime.timedelta(days=2),
            discovery_date=datetime.datetime.utcnow(),
            verification_status="Verified",
            source_reliability="High",
            evidence_strength="High",
            strategic_relevance=s_data["strategic_relevance"],
            business_impact=s_data["business_impact"],
            nature=s_data["nature"],
            urgency=s_data["urgency"],
            recommended_action=s_data["recommended_action"],
            ranking_score=ranking["score"],
            ranking_breakdown=ranking["breakdown"],
            is_archived=False
        )
        db.add(item)

    db.commit()
    ReportService.generate_brief(db, "stripe")
    ReportService.generate_brief(db, "datadog")
    db.commit()
