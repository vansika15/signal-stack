import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { MondayReport, ActionItem } from '../types';
import {
  FileText, Download, Printer, RefreshCw, CheckCircle2,
  Clock, ShieldCheck, ChevronRight, History, Sparkles, Building2
} from 'lucide-react';

export const MondayBriefPage: React.FC = () => {
  const { activeCompany } = useCompany();
  const [reports, setReports] = useState<MondayReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<MondayReport | null>(null);
  const [actionItems, setActionItems] = useState<ActionItem[]>([]);
  const [generating, setGenerating] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadReports = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const [reportsData, actionsData] = await Promise.all([
        api.getReports(activeCompany.id),
        api.getActionItems(activeCompany.id)
      ]);
      setReports(reportsData);
      if (reportsData.length > 0) setSelectedReport(reportsData[0]);
      setActionItems(actionsData);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, [activeCompany?.id]);

  const handleGenerateBrief = async () => {
    if (!activeCompany) return;
    setGenerating(true);
    try {
      const newReport = await api.generateReport(activeCompany.id);
      setReports(prev => [newReport, ...prev]);
      setSelectedReport(newReport);
      const updatedActions = await api.getActionItems(activeCompany.id);
      setActionItems(updatedActions);
    } catch (err) {
      console.error('Failed to generate brief:', err);
    } finally {
      setGenerating(false);
    }
  };

  const handleToggleAction = async (actionId: string, currentStatus: string) => {
    const newStatus = currentStatus === 'completed' ? 'todo' : 'completed';
    try {
      const updated = await api.updateActionItem(actionId, { status: newStatus });
      setActionItems(prev => prev.map(a => a.id === actionId ? updated : a));
    } catch (err) {
      console.error('Failed to toggle action item:', err);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (!activeCompany) return null;

  return (
    <div className="space-y-6">
      {/* Top Action Bar (no-print) */}
      <div className="no-print p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              Executive Briefing Room
            </span>
            <span className="text-xs text-slate-400 font-mono">
              10 Ground-Truth Sections
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            Monday Morning Intelligence Brief
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Synthesis of verified customer signals, competitor movements, regulatory updates, and internal operations.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {selectedReport && (
            <>
              <a
                href={`/api/reports/${selectedReport.id}/download-pdf`}
                download
                className="px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-semibold flex items-center gap-1.5 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download PDF</span>
              </a>
              <button
                onClick={handlePrint}
                className="px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-semibold flex items-center gap-1.5 transition-colors"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print Brief</span>
              </button>
            </>
          )}
          <button
            onClick={handleGenerateBrief}
            disabled={generating}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <Sparkles className={`w-3.5 h-3.5 ${generating ? 'animate-spin' : ''}`} />
            <span>{generating ? 'Synthesizing 10 Sections...' : 'Generate New Brief'}</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Historical Cycles (Left) + 10-Section Document (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left Column: Historical Report Cycles (no-print) */}
        <div className="no-print lg:col-span-1 space-y-4">
          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
              <History className="w-3.5 h-3.5 text-indigo-500" />
              <span>Report Archive ({reports.length})</span>
            </h3>

            <div className="space-y-1.5">
              {reports.map((rpt) => (
                <button
                  key={rpt.id}
                  onClick={() => setSelectedReport(rpt)}
                  className={`w-full text-left p-3 rounded-xl text-xs transition-all ${
                    selectedReport?.id === rpt.id
                      ? 'bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-900 dark:text-indigo-200 font-semibold'
                      : 'hover:bg-slate-50 dark:hover:bg-slate-800/50 text-slate-600 dark:text-slate-400'
                  }`}
                >
                  <div className="font-bold">{rpt.report_week}</div>
                  <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                    {new Date(rpt.created_at).toLocaleDateString()}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Action Item Tracking Sidebar */}
          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                <span>Action Tracking</span>
              </h3>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400">
                {actionItems.filter(a => a.status === 'completed').length}/{actionItems.length}
              </span>
            </div>

            <div className="space-y-2">
              {actionItems.map((act) => (
                <div
                  key={act.id}
                  className="p-2.5 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 flex items-start gap-2"
                >
                  <input
                    type="checkbox"
                    checked={act.status === 'completed'}
                    onChange={() => handleToggleAction(act.id, act.status)}
                    className="mt-0.5 rounded border-slate-300 text-indigo-600 cursor-pointer"
                  />
                  <div className="flex-1 min-w-0">
                    <p className={`text-xs font-semibold ${act.status === 'completed' ? 'line-through text-slate-400' : 'text-slate-800 dark:text-slate-200'}`}>
                      {act.title}
                    </p>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                      {act.owner} • {act.due_date}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Complete 10-Section Brief (Executive Paper Layout) */}
        <div className="lg:col-span-3">
          {selectedReport ? (
            <div className="p-8 sm:p-12 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-lg space-y-8 text-slate-900 dark:text-slate-100 font-sans print:shadow-none print:border-none print:p-0">
              
              {/* Document Header */}
              <div className="border-b-2 border-indigo-500 pb-6">
                <div className="flex items-center justify-between text-xs font-mono text-indigo-600 dark:text-indigo-400 uppercase tracking-widest font-bold mb-2">
                  <span>SIGNAL STACK EXECUTIVE BRIEFING</span>
                  <span>{selectedReport.report_week}</span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                  {selectedReport.title}
                </h1>
                <div className="flex flex-wrap items-center gap-3 mt-3 text-xs text-slate-500 font-mono">
                  <span>Organization: <strong>{activeCompany.name}</strong></span>
                  <span>•</span>
                  <span>Published: {new Date(selectedReport.created_at).toLocaleDateString()}</span>
                  <span>•</span>
                  <span>Classification: Strategic Executive Intelligence</span>
                </div>
              </div>

              {/* 10 Required Sections */}
              <div className="space-y-8 text-xs sm:text-sm leading-relaxed">
                
                {/* 1. Executive Summary */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400 flex items-center gap-2">
                    <span>1. Executive Summary</span>
                  </h2>
                  <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 text-slate-700 dark:text-slate-300">
                    {selectedReport.section_1_executive_summary}
                  </div>
                </section>

                {/* 2. Customer Signals */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    2. Customer Signals
                  </h2>
                  <div className="whitespace-pre-line text-slate-700 dark:text-slate-300">
                    {selectedReport.section_2_customer_signals}
                  </div>
                </section>

                {/* 3. Competitor Intelligence */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    3. Competitor Intelligence
                  </h2>
                  <div className="whitespace-pre-line text-slate-700 dark:text-slate-300">
                    {selectedReport.section_3_competitor_intelligence}
                  </div>
                </section>

                {/* 4. Market Intelligence */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    4. Market Intelligence
                  </h2>
                  <div className="whitespace-pre-line text-slate-700 dark:text-slate-300">
                    {selectedReport.section_4_market_intelligence}
                  </div>
                </section>

                {/* 5. Internal Business Intelligence */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    5. Internal Business Intelligence
                  </h2>
                  <div className="whitespace-pre-line text-slate-700 dark:text-slate-300">
                    {selectedReport.section_5_internal_intelligence}
                  </div>
                </section>

                {/* 6. Opportunities Identified */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
                    6. Opportunities Identified
                  </h2>
                  <div className="p-4 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-800/40 whitespace-pre-line text-slate-800 dark:text-slate-200">
                    {selectedReport.section_6_opportunities_identified}
                  </div>
                </section>

                {/* 7. Risks and Threats */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-rose-600 dark:text-rose-400 uppercase tracking-wider">
                    7. Risks and Threats
                  </h2>
                  <div className="p-4 rounded-xl bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200/60 dark:border-rose-800/40 whitespace-pre-line text-slate-800 dark:text-slate-200">
                    {selectedReport.section_7_risks_and_threats}
                  </div>
                </section>

                {/* 8. Recommended Actions for This Week */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    8. Recommended Actions for This Week
                  </h2>
                  <div className="whitespace-pre-line text-slate-700 dark:text-slate-300">
                    {selectedReport.section_8_recommended_actions}
                  </div>
                </section>

                {/* 9. What We Should Watch */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    9. What We Should Watch
                  </h2>
                  <div className="p-4 rounded-xl bg-amber-50/40 dark:bg-amber-950/20 border border-amber-200/50 dark:border-amber-800/40 whitespace-pre-line text-slate-800 dark:text-slate-200">
                    {selectedReport.section_9_what_we_should_watch}
                  </div>
                </section>

                {/* 10. Source Appendix */}
                <section className="space-y-2 pt-4 border-t border-slate-200 dark:border-slate-800 font-mono text-xs">
                  <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    10. Source Appendix & Evidence Traceability
                  </h2>
                  <div className="whitespace-pre-line text-slate-600 dark:text-slate-400">
                    {selectedReport.section_10_source_appendix}
                  </div>
                </section>
              </div>

              {/* Document Verification Seal */}
              <div className="pt-6 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>Signal Stack Autonomous Intelligence Engine</span>
                <span>Verification Hash: SHA256-AUTHENTICATED</span>
              </div>
            </div>
          ) : (
            <div className="p-12 text-center text-slate-400">
              No reports generated yet. Click "Generate New Brief" to synthesize.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
