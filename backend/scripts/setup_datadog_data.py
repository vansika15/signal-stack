import sys
import os
import datetime

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal
from app.models.competitor import Competitor
from app.models.source import Source

db = SessionLocal()

print("Updating Datadog Competitors...")
# Remove old generic competitors if present
old_comps = db.query(Competitor).filter(Competitor.company_id == "datadog").all()
for c in old_comps:
    db.delete(c)
db.commit()

datadog_competitors = [
    Competitor(
        id="comp_dd_dynatrace",
        company_id="datadog",
        name="Dynatrace",
        website="https://www.dynatrace.com",
        tier="Direct",
        market_focus="Enterprise Full-Stack APM, Infrastructure & Autonomous Cloud Operations",
        key_strengths="Davis AI causal engine, automated root-cause detection, deep enterprise Fortune 500 footprint",
        vulnerabilities="High deployment complexity, rigid pricing structures for mid-market engineering teams",
        monitored=True,
        discovery_method="Pre-seeded Domain Competitor"
    ),
    Competitor(
        id="comp_dd_new_relic",
        company_id="datadog",
        name="New Relic",
        website="https://newrelic.com",
        tier="Direct",
        market_focus="Developer-First All-In-One Observability Platform",
        key_strengths="Consumption-based per-user pricing, 700+ turnkey integrations, strong developer community",
        vulnerabilities="Post-private equity restructuring, legacy UI fragmentation across older accounts",
        monitored=True,
        discovery_method="Pre-seeded Domain Competitor"
    ),
    Competitor(
        id="comp_dd_splunk",
        company_id="datadog",
        name="Splunk (Cisco)",
        website="https://www.splunk.com",
        tier="Direct",
        market_focus="Enterprise Security Information Event Management (SIEM) & Heavy Log Analytics",
        key_strengths="Cisco global distribution reach, massive security log index capacity, compliance certification",
        vulnerabilities="High total cost of ownership, high hardware resource overhead for non-security APM",
        monitored=True,
        discovery_method="Pre-seeded Domain Competitor"
    ),
    Competitor(
        id="comp_dd_grafana",
        company_id="datadog",
        name="Grafana Labs",
        website="https://grafana.com",
        tier="Direct",
        market_focus="Open-Source Telemetry (LGTM Stack: Loki, Grafana, Tempo, Mimir)",
        key_strengths="Dominant open-source developer mindshare, zero vendor lock-in, highly modular",
        vulnerabilities="Self-managed operational burden, fragmented configuration compared to single Datadog agent",
        monitored=True,
        discovery_method="Pre-seeded Domain Competitor"
    ),
    Competitor(
        id="comp_dd_elastic",
        company_id="datadog",
        name="Elastic",
        website="https://www.elastic.co",
        tier="Indirect",
        market_focus="Search-Powered Observability, Log Analytics & Vector Search",
        key_strengths="Fast full-text search across petabyte log archives, native OpenSearch/Elasticsearch familiarity",
        vulnerabilities="High memory cluster requirements, steep learning curve for non-log APM workflows",
        monitored=True,
        discovery_method="Pre-seeded Domain Competitor"
    ),
    Competitor(
        id="comp_dd_honeycomb",
        company_id="datadog",
        name="Honeycomb.io",
        website="https://www.honeycomb.io",
        tier="Emerging",
        market_focus="High-Cardinality Distributed Tracing & Observability 2.0",
        key_strengths="Instant sub-second queries across millions of dimensions, superior debugging UX for complex microservices",
        vulnerabilities="Lacks native infrastructure host metric monitors and unified cloud security tooling",
        monitored=True,
        discovery_method="Pre-seeded Domain Competitor"
    ),
]

for comp in datadog_competitors:
    db.add(comp)
db.commit()
print(f"Added {len(datadog_competitors)} Datadog competitors.")

print("\nUpdating Datadog Sources...")
old_sources = db.query(Source).filter(Source.company_id == "datadog").all()
for s in old_sources:
    db.delete(s)
db.commit()

datadog_sources = [
    Source(
        id="src_dd_1",
        company_id="datadog",
        name="InfoQ Cloud & DevOps",
        url="https://www.infoq.com/devops/",
        source_type="Industry News",
        relevance_explanation="Covers distributed tracing, Kubernetes observability, microservices reliability, and cloud architecture patterns.",
        approved_status="approved",
        health_status="healthy",
        crawl_frequency_hours=24
    ),
    Source(
        id="src_dd_2",
        company_id="datadog",
        name="Dynatrace Newsroom",
        url="https://www.dynatrace.com/news/",
        source_type="Competitor Feed",
        relevance_explanation="Primary full-stack APM competitor publishing AI copilot features, enterprise client wins, and quarterly releases.",
        approved_status="approved",
        health_status="healthy",
        crawl_frequency_hours=24
    ),
    Source(
        id="src_dd_3",
        company_id="datadog",
        name="New Relic Engineering Blog",
        url="https://newrelic.com/blog",
        source_type="Competitor Feed",
        relevance_explanation="Direct APM competitor publishing technical benchmarks, consumption pricing updates, and OpenTelemetry capabilities.",
        approved_status="approved",
        health_status="healthy",
        crawl_frequency_hours=24
    ),
    Source(
        id="src_dd_4",
        company_id="datadog",
        name="TechCrunch Enterprise",
        url="https://techcrunch.com/category/enterprise/",
        source_type="Industry News",
        relevance_explanation="Tracks enterprise SaaS spending, cloud infrastructure startup funding, and cybersecurity consolidations.",
        approved_status="approved",
        health_status="healthy",
        crawl_frequency_hours=24
    ),
    Source(
        id="src_dd_5",
        company_id="datadog",
        name="Hacker News Observability Discussions",
        url="https://news.ycombinator.com",
        source_type="Community Sentiment",
        relevance_explanation="Developer community sentiment on cloud observability bill shock, agent performance overhead, and OpenTelemetry tooling.",
        approved_status="approved",
        health_status="healthy",
        crawl_frequency_hours=24
    ),
]

for src in datadog_sources:
    db.add(src)
db.commit()
print(f"Added {len(datadog_sources)} Datadog sources.")

db.close()
