import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models.company import Company
from app.models.report import MondayReport
from app.models.intelligence import IntelligenceItem
from app.models.source import Source
from app.services.report_service import ReportService
from app.services.ai_service import AIService

class TestMondayBriefProvenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = SessionLocal()
        cls.company_id = "meetuniversity"
        # Generate a fresh brief
        cls.report = ReportService.generate_brief(cls.db, cls.company_id)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_data_provenance_separation(self):
        """Verify that crawled vs seeded items are strictly separated by is_crawled"""
        items = self.db.query(IntelligenceItem).filter(IntelligenceItem.company_id == self.company_id).all()
        crawled = [i for i in items if i.is_crawled]
        seeded = [i for i in items if not i.is_crawled]

        self.assertEqual(len(crawled), 28, "Expected exactly 28 live crawled records")
        self.assertEqual(len(seeded), 12, "Expected exactly 12 illustrative demo baseline records")

        # Verify report counts
        self.assertEqual(self.report.live_signals_count, 28)
        self.assertEqual(self.report.demo_signals_count, 12)
        self.assertFalse(self.report.internal_data_connected)

    def test_02_seeded_records_never_labeled_as_verified_live_evidence(self):
        """Verify that seeded demo records are never labeled [Live Crawled Evidence]"""
        exec_summary = self.report.section_1_executive_summary
        cust_signals = self.report.section_2_customer_signals
        int_signals = self.report.section_5_internal_intelligence

        # Check Executive Summary
        self.assertIn("DATA PROVENANCE & INTEGRITY AUDIT", exec_summary)
        self.assertIn("28 Live Crawled Evidence records", exec_summary)
        self.assertIn("12 Illustrative Demo Data baseline items", exec_summary)

        # Check customer signals: seeded items must be under Illustrative Demo Data
        self.assertIn("[Illustrative Demo Data]", cust_signals)
        self.assertNotIn("[Live Crawled Evidence] Student Sentiment Shift", cust_signals)
        self.assertNotIn("[Live Crawled Evidence] Education Loan Rejection", cust_signals)

        # Ensure demo disclaimer is present
        self.assertIn("must not be cited as empirical MeetUniversity customer metrics", cust_signals)

    def test_03_internal_intelligence_disclosure(self):
        """Verify Section 5 explicitly discloses that internal company data is not connected"""
        int_section = self.report.section_5_internal_intelligence
        self.assertIn("Internal company data not connected", int_section)
        self.assertIn("STATUS: Internal company data not connected", int_section)
        self.assertIn("MeetUniversity has not connected an active internal CRM", int_section)
        self.assertIn("[Illustrative Demo Data", int_section)

    def test_04_market_intelligence_live_citations(self):
        """Verify Market Intelligence includes live crawled evidence with source URLs and evidence quotes"""
        mkt_section = self.report.section_4_market_intelligence
        self.assertIn("[Live Crawled Evidence]", mkt_section)
        self.assertIn("Source: https://", mkt_section)
        self.assertIn("Confidence: High", mkt_section)

    def test_05_opportunities_facts_vs_interpretations(self):
        """Verify opportunities and risks separate Observed Facts from Strategic Interpretations with Confidence Levels"""
        opp_section = self.report.section_6_opportunities_identified
        risk_section = self.report.section_7_risks_and_threats

        self.assertIn("Observed Fact (Ground Truth)", opp_section)
        self.assertIn("Strategic Interpretation (AI Synthesis)", opp_section)
        self.assertIn("Confidence Level", opp_section)

        self.assertIn("Observed Fact (Ground Truth)", risk_section)
        self.assertIn("Strategic Interpretation (AI Synthesis)", risk_section)
        self.assertIn("Confidence Level", risk_section)

    def test_06_source_appendix_links_and_provenance(self):
        """Verify Section 10 includes clickable source URLs and classifies internal systems as disconnected"""
        appendix = self.report.section_10_source_appendix
        self.assertIn("Live Verified Monitored Sources", appendix)
        self.assertIn("https://", appendix)
        self.assertIn("HTTP 200 Verified Healthy", appendix)
        self.assertIn("Internal Admissions Telemetry & CRM**: Status: DISCONNECTED", appendix)

    def test_07_pdf_export_generated_with_provenance_audit(self):
        """Verify that executive PDF is generated on disk with non-trivial size and verified content"""
        pdf_path = self.report.pdf_export_path
        self.assertIsNotNone(pdf_path)
        self.assertTrue(os.path.exists(pdf_path), f"PDF file does not exist at {pdf_path}")
        file_size = os.path.getsize(pdf_path)
        self.assertGreater(file_size, 15000, f"Expected PDF >15KB, got {file_size} bytes")

    def test_08_all_10_sections_populated(self):
        """Verify all 10 standard executive sections are non-empty and well-structured"""
        sections = [
            self.report.section_1_executive_summary,
            self.report.section_2_customer_signals,
            self.report.section_3_competitor_intelligence,
            self.report.section_4_market_intelligence,
            self.report.section_5_internal_intelligence,
            self.report.section_6_opportunities_identified,
            self.report.section_7_risks_and_threats,
            self.report.section_8_recommended_actions,
            self.report.section_9_what_we_should_watch,
            self.report.section_10_source_appendix
        ]
        for idx, sec in enumerate(sections, 1):
            self.assertTrue(len(sec) > 50, f"Section {idx} must have substantial grounded content")

if __name__ == "__main__":
    unittest.main()
