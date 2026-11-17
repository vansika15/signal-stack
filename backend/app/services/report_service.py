import os
import time
import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from ..models.report import MondayReport
from ..models.action_item import ActionItem
from ..models.intelligence import IntelligenceItem
from ..models.company import Company
from .ai_service import AIService

class ReportService:
    """
    Monday Morning Intelligence Brief Generator & Exporter:
    - Synthesizes 10 standard executive sections
    - Action item extraction and tracking
    - PDF export generation using ReportLab
    - Historical report versioning
    """

    @classmethod
    def generate_brief(cls, db: Session, company_id: str) -> MondayReport:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValueError(f"Company {company_id} not found")

        # Fetch top unarchived signals
        signals = db.query(IntelligenceItem).filter(
            IntelligenceItem.company_id == company_id,
            IntelligenceItem.is_archived == False
        ).order_by(IntelligenceItem.ranking_score.desc()).limit(30).all()

        signal_dicts = [
            {
                "id": s.id,
                "category": s.category,
                "headline": s.headline,
                "summary": s.summary,
                "evidence": s.evidence,
                "strategic_relevance": s.strategic_relevance,
                "business_impact": s.business_impact,
                "nature": s.nature,
                "urgency": s.urgency,
                "recommended_action": s.recommended_action,
                "ranking_score": s.ranking_score,
                "source_id": s.source_id
            }
            for s in signals
        ]

        company_data = {
            "name": company.name,
            "industry": company.industry,
            "business_context": company.business_context or ""
        }

        # Generate brief content
        brief_data = AIService.generate_monday_brief(signal_dicts, company_data)

        report_id = f"rpt_{int(time.time())}_{company_id[:4]}"
        new_report = MondayReport(
            id=report_id,
            company_id=company_id,
            report_week=brief_data.get("report_week", f"Week {datetime.datetime.utcnow().isocalendar()[1]}, {datetime.datetime.utcnow().year}"),
            title=brief_data.get("title", f"Monday Morning Intelligence Brief - {company.name}"),
            section_1_executive_summary=brief_data.get("section_1_executive_summary", ""),
            section_2_customer_signals=brief_data.get("section_2_customer_signals", ""),
            section_3_competitor_intelligence=brief_data.get("section_3_competitor_intelligence", ""),
            section_4_market_intelligence=brief_data.get("section_4_market_intelligence", ""),
            section_5_internal_intelligence=brief_data.get("section_5_internal_intelligence", ""),
            section_6_opportunities_identified=brief_data.get("section_6_opportunities_identified", ""),
            section_7_risks_and_threats=brief_data.get("section_7_risks_and_threats", ""),
            section_8_recommended_actions=brief_data.get("section_8_recommended_actions", ""),
            section_9_what_we_should_watch=brief_data.get("section_9_what_we_should_watch", ""),
            section_10_source_appendix=brief_data.get("section_10_source_appendix", ""),
            included_signals_ids=[s.id for s in signals],
            created_at=datetime.datetime.utcnow()
        )
        db.add(new_report)

        # Create action items extracted from the report
        import uuid
        for idx, act in enumerate(brief_data.get("action_items", [])):
            item = ActionItem(
                id=f"act_{int(time.time()*1000)}_{idx}_{uuid.uuid4().hex[:6]}",
                report_id=report_id,
                company_id=company_id,
                title=act.get("title", "Action Item"),
                description=act.get("description", ""),
                category=act.get("category", "Strategic"),
                priority=act.get("priority", "High"),
                status="todo",
                owner=act.get("owner", "Leadership Team"),
                due_date=act.get("due_date", "Friday"),
                created_at=datetime.datetime.utcnow()
            )
            db.add(item)

        db.commit()
        db.refresh(new_report)

        # Generate PDF file
        cls.generate_pdf(new_report, company.name)

        return new_report

    @classmethod
    def generate_pdf(cls, report: MondayReport, company_name: str) -> str:
        """Generates a styled executive PDF document for the Monday Brief"""
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports_pdf")
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, f"{report.id}.pdf")

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E1B4B')
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#4F46E5')
        )
        section_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1E1B4B'),
            spaceBefore=14,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#1E293B')
        )

        story = []
        # Header banner
        story.append(Paragraph(f"SIGNAL STACK EXECUTIVE BRIEF", subtitle_style))
        story.append(Paragraph(report.title, title_style))
        story.append(Paragraph(f"Company: {company_name} | Generated: {report.created_at.strftime('%B %d, %Y')} | Cycle: {report.report_week}", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#6366F1'), spaceBefore=5, spaceAfter=15))

        sections = [
            ("1. Executive Summary", report.section_1_executive_summary),
            ("2. Customer Signals", report.section_2_customer_signals),
            ("3. Competitor Intelligence", report.section_3_competitor_intelligence),
            ("4. Market Intelligence", report.section_4_market_intelligence),
            ("5. Internal Business Intelligence", report.section_5_internal_intelligence),
            ("6. Opportunities Identified", report.section_6_opportunities_identified),
            ("7. Risks & Threats", report.section_7_risks_and_threats),
            ("8. Recommended Actions for This Week", report.section_8_recommended_actions),
            ("9. What We Should Watch", report.section_9_what_we_should_watch),
            ("10. Source Appendix & Evidence Traceability", report.section_10_source_appendix),
        ]

        for sec_title, sec_content in sections:
            story.append(Paragraph(sec_title, section_heading))
            # Format lines
            clean_content = sec_content.replace("\n", "<br/>")
            story.append(Paragraph(clean_content, body_style))
            story.append(Spacer(1, 8))

        try:
            doc.build(story)
            report.pdf_export_path = pdf_path
        except Exception as e:
            print(f"Error building PDF: {e}")

        return pdf_path
