import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import datetime

from ..database import get_db
from ..models.company import Company
from ..models.report import MondayReport
from ..models.action_item import ActionItem
from ..schemas.report import MondayReportResponse, ActionItemResponse, ActionItemUpdate
from ..services.report_service import ReportService

router = APIRouter(prefix="/api/reports", tags=["Monday Morning Brief & Action Tracking"])

@router.get("/{company_id}", response_model=List[MondayReportResponse])
def get_reports_history(company_id: str, db: Session = Depends(get_db)):
    return db.query(MondayReport).filter(
        MondayReport.company_id == company_id
    ).order_by(MondayReport.created_at.desc()).all()

@router.get("/detail/{report_id}", response_model=MondayReportResponse)
def get_report_detail(report_id: str, db: Session = Depends(get_db)):
    report = db.query(MondayReport).filter(MondayReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/generate/{company_id}", response_model=MondayReportResponse)
def generate_report(company_id: str, db: Session = Depends(get_db)):
    try:
        report = ReportService.generate_brief(db, company_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate brief: {str(e)}")

@router.get("/{report_id}/download-pdf")
def download_pdf(report_id: str, db: Session = Depends(get_db)):
    report = db.query(MondayReport).filter(MondayReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    company = db.query(Company).filter(Company.id == report.company_id).first()
    comp_name = company.name if company else "Company"

    if not report.pdf_export_path or not os.path.exists(report.pdf_export_path):
        pdf_path = ReportService.generate_pdf(report, comp_name)
    else:
        pdf_path = report.pdf_export_path

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF export file not found")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"Monday_Brief_{comp_name.replace(' ', '_')}_{report.id}.pdf"
    )

@router.get("/{company_id}/actions", response_model=List[ActionItemResponse])
def get_action_items(company_id: str, db: Session = Depends(get_db)):
    return db.query(ActionItem).filter(
        ActionItem.company_id == company_id
    ).order_by(ActionItem.created_at.desc()).all()

@router.put("/actions/{action_id}", response_model=ActionItemResponse)
def update_action_item(action_id: str, req: ActionItemUpdate, db: Session = Depends(get_db)):
    action = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action item not found")

    if req.status is not None:
        action.status = req.status
        if req.status == "completed":
            action.completed_at = datetime.datetime.utcnow()
        else:
            action.completed_at = None

    if req.title is not None: action.title = req.title
    if req.description is not None: action.description = req.description
    if req.priority is not None: action.priority = req.priority
    if req.owner is not None: action.owner = req.owner
    if req.due_date is not None: action.due_date = req.due_date

    db.commit()
    db.refresh(action)
    return action
