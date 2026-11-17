import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.database import SessionLocal
from app.models.source import Source

UPDATES = {
    "src_mu_1": {
        "name": "The PIE News",
        "url": "https://thepienews.com",
        "source_type": "Industry News",
        "relevance_explanation": "The global gold-standard publication for international education policy, university partnerships, and cross-border student mobility trends."
    },
    "src_mu_2": {
        "name": "University World News",
        "url": "https://www.universityworldnews.com",
        "source_type": "Industry News",
        "relevance_explanation": "Authoritative global reporting on higher education governance, international admissions policies, and cross-border university rankings."
    },
    "src_mu_3": {
        "name": "Inside Higher Ed (Global Edition)",
        "url": "https://www.insidehighered.com/news/global",
        "source_type": "Industry News",
        "relevance_explanation": "Global higher education reporting on international recruitment trends, enrollment economics, and institutional partnerships."
    },
    "src_mu_4": {
        "name": "UK Visas and Immigration (UKVI) Updates",
        "url": "https://www.gov.uk/government/organisations/uk-visas-and-immigration",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Official UK government gazette for student visa compliance, Graduate Route post-study work rules, and financial requirements."
    },
    "src_mu_5": {
        "name": "Education in Ireland Official Portal",
        "url": "https://www.educationinireland.com/en/",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Official Irish government agency for international higher education, post-study work visas, and Irish university applications."
    },
    "src_mu_6": {
        "name": "Immigration, Refugees and Citizenship Canada (IRCC) News",
        "url": "https://www.canada.ca/en/immigration-refugees-citizenship/news.html",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Direct federal announcements on Canadian study permit quotas, Provincial Attestation Letters (PAL), and PGWP eligibility rules."
    },
    "src_mu_7": {
        "name": "Australia Dept of Home Affairs Student Visas",
        "url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Official statutory guidelines for Subclass 500 student visas, Genuine Student (GS) assessments, and Australian financial capacity checks."
    },
    "src_mu_8": {
        "name": "ApplyBoard Insights & Higher Ed Blog",
        "url": "https://www.applyboard.com/blog",
        "source_type": "Competitor Website",
        "relevance_explanation": "Competitor market intelligence on international student trends, university recruitment partner networks, and product feature launches."
    },
    "src_mu_9": {
        "name": "IDP Connect Insights Portal",
        "url": "https://www.idp-connect.com/news-and-insights",
        "source_type": "Competitor Website",
        "relevance_explanation": "Monitors competitor international student placement research, FastLane admissions technology, and global survey benchmarks."
    },
    "src_mu_10": {
        "name": "LeverageEdu Blog & Updates",
        "url": "https://leverageedu.com/blog/",
        "source_type": "Competitor Website",
        "relevance_explanation": "Direct insight into competitor student marketing angles, test prep bundling, and Fly Finance loan promotions."
    },
    "src_mu_11": {
        "name": "IDP India Admissions Portal",
        "url": "https://www.idp.com/india/",
        "source_type": "Competitor Website",
        "relevance_explanation": "Tracks incumbent competitor's domestic marketing campaigns, city office counseling networks, and university tie-up fairs across India."
    },
    "src_mu_12": {
        "name": "UK Council for International Student Affairs (UKCISA)",
        "url": "https://www.ukcisa.org.uk/Information--Advice",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "National advisory body providing authoritative guidance on UK immigration law, tuition fee statuses, and international student welfare."
    },
    "src_mu_13": {
        "name": "Times Higher Education (THE) World News",
        "url": "https://www.timeshighereducation.com/news",
        "source_type": "Industry News",
        "relevance_explanation": "Covers university financial sustainability, admissions shifts, international tuition benchmarks, and higher education policy."
    },
    "src_mu_14": {
        "name": "UK Student Visa Official Guidance",
        "url": "https://www.gov.uk/student-visa",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Direct statutory requirements for UK Student visas, Confirmation of Acceptance for Studies (CAS) thresholds, and maintenance funds."
    },
    "src_mu_15": {
        "name": "Irish Council for International Students (ICOS)",
        "url": "https://www.internationalstudents.ie/",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Advocacy and policy updates on international student rights, visa processing times, and student housing conditions in Ireland."
    },
    "src_mu_16": {
        "name": "EdSurge Higher Education",
        "url": "https://www.edsurge.com/news",
        "source_type": "Industry News",
        "relevance_explanation": "Premier reporting on edtech innovation, digital admissions pipelines, and global learning technologies."
    },
    "src_mu_17": {
        "name": "Studyportals Intelligence Unit",
        "url": "https://act.studyportals.com",
        "source_type": "Competitor Website",
        "relevance_explanation": "Provides macro student interest index reports, subject-level demand shifts, and student origin-to-destination analytics."
    },
    "src_mu_18": {
        "name": "NAFSA: Association of International Educators",
        "url": "https://www.nafsa.org/policy-and-advocacy",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Leading advocate for US international education policy, student visa processing reform, and global exchange data."
    },
    "src_mu_19": {
        "name": "Study Australia Official Portal (Austrade)",
        "url": "https://www.studyaustralia.gov.au/en",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Australian government official international student recruitment portal, institutional course offerings, and scholarship updates."
    },
    "src_mu_20": {
        "name": "Study in Sweden Official Portal",
        "url": "https://studyinsweden.se/",
        "source_type": "Regulatory/Govt",
        "relevance_explanation": "Official Swedish institute portal for international degree programs, English-taught STEM courses, and residence permits for study."
    }
}

def main():
    db = SessionLocal()
    updated_count = 0
    print("UPDATING MEETUNIVERSITY SOURCES IN DATABASE...")
    for src_id, data in UPDATES.items():
        src = db.query(Source).filter(Source.id == src_id).first()
        if src:
            src.name = data["name"]
            src.url = data["url"]
            src.source_type = data["source_type"]
            src.relevance_explanation = data["relevance_explanation"]
            src.approved_status = "approved"
            # Reset hash so new URL is crawled fresh on first run
            src.content_hash = None
            src.error_message = None
            updated_count += 1
            print(f"✔ [{src_id}] {src.name} -> {src.url}")
        else:
            print(f"⚠ Source {src_id} not found in DB")

    db.commit()
    db.close()
    print(f"\nMigration successfully updated {updated_count} sources!")

if __name__ == "__main__":
    main()
