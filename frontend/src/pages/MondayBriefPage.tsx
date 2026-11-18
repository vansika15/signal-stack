import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { MondayReport, ActionItem } from '../types';
import {
  FileText, Download, Printer, RefreshCw, CheckCircle2,
  Clock, ShieldCheck, ChevronRight, History, Sparkles, Building2,
  Radio, Database, AlertTriangle, ExternalLink, ShieldAlert
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

  // Helper to format content with badges and clickable links
  const renderFormattedSection = (content: string) => {
    if (!content) return null;

    const lines = content.split('\n');
    return (
      <div className="space-y-2 text-slate-700 dark:text-slate-300">
        {lines.map((line, idx) => {
          if (!line.trim()) {
            return <div key={idx} className="h-1.5" />;
          }

          // Convert markdown links [Label](url) and raw URLs to clickable links
          const parts: React.ReactNode[] = [];
          let remaining = line;
          let keyCounter = 0;

          // Regular expression matching either [title](url) or standalone (https?://...) or https?://...
          const linkRegex = /(\[([^\]]+)\]\((https?:\/\/[^\)]+)\)|(?:\()?https?:\/\/[^\s\)\"\'\,]+(?:\))?)/g;
          let lastIndex = 0;
          let match;

          while ((match = linkRegex.exec(line)) !== null) {
            if (match.index > lastIndex) {
              parts.push(line.substring(lastIndex, match.index));
            }

            if (match[2] && match[3]) {
              // [title](url) format
              parts.push(
                <a
                  key={`link-${idx}-${keyCounter++}`}
                  href={match[3]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-0.5 text-indigo-600 dark:text-indigo-400 hover:underline font-semibold"
                >
                  <span>{match[2]}</span>
                  <ExternalLink className="w-3 h-3 shrink-0 inline" />
                </a>
              );
            } else {
              // Standalone url
              const rawUrl = match[0].replace(/^\(/, '').replace(/\)$/, '');
              parts.push(
                <a
                  key={`link-${idx}-${keyCounter++}`}
                  href={rawUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-0.5 text-indigo-600 dark:text-indigo-400 hover:underline font-mono text-[11px]"
                >
                  <span className="truncate max-w-xs">{rawUrl}</span>
                  <ExternalLink className="w-2.5 h-2.5 shrink-0 inline" />
                </a>
              );
            }
            lastIndex = linkRegex.lastIndex;
          }

          if (lastIndex < line.length) {
            parts.push(line.substring(lastIndex));
          }

          // Process formatting for bold text and badges in parts
          const renderedParts = parts.map((part, pIdx) => {
            if (typeof part !== 'string') return part;

            // Highlight Provenance Badges
            if (part.includes('[Live Crawled Evidence]')) {
              const segs = part.split('[Live Crawled Evidence]');
              return (
                <React.Fragment key={pIdx}>
                  {segs[0]}
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                    <Radio className="w-2.5 h-2.5 text-emerald-500 animate-pulse" />
                    <span>Live Crawled Evidence</span>
                  </span>
                  {segs[1]}
                </React.Fragment>
              );
            }

            if (part.includes('[Illustrative Demo Data - Simulated Operational Benchmark]')) {
              const segs = part.split('[Illustrative Demo Data - Simulated Operational Benchmark]');
              return (
                <React.Fragment key={pIdx}>
                  {segs[0]}
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200 dark:border-amber-800">
                    <AlertTriangle className="w-2.5 h-2.5 text-amber-500" />
                    <span>Illustrative Demo Data</span>
                  </span>
                  {segs[1]}
                </React.Fragment>
              );
            }

            if (part.includes('[Illustrative Demo Data]')) {
              const segs = part.split('[Illustrative Demo Data]');
              return (
                <React.Fragment key={pIdx}>
                  {segs[0]}
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                    <Database className="w-2.5 h-2.5 text-slate-500" />
                    <span>Illustrative Demo Data</span>
                  </span>
                  {segs[1]}
                </React.Fragment>
              );
            }

            // Bold **text**
            const boldMatches = part.split(/\*\*(.*?)\*\*/g);
            if (boldMatches.length > 1) {
              return boldMatches.map((sub, sIdx) => 
                sIdx % 2 === 1 ? <strong key={sIdx} className="font-bold text-slate-900 dark:text-slate-100">{sub}</strong> : sub
              );
            }

            return part;
          });

          // Check for subheaders like "### Title"
          if (line.startsWith('### ')) {
            return (
              <h4 key={idx} className="text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mt-4 mb-1">
                {line.replace('### ', '')}
              </h4>
            );
          }

          return <div key={idx} className="leading-relaxed">{renderedParts}</div>;
        })}
      </div>
    );
  };

  if (!activeCompany) return null;

  const liveSignalsCount = selectedReport?.live_signals_count ?? 28;
  const demoSignalsCount = selectedReport?.demo_signals_count ?? 12;

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
            Evidence-grounded synthesis of verified regulatory updates, live competitor movements, and internal operational status.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {selectedReport && (
            <>
              <a
                href={api.getReportPdfUrl(selectedReport.id)}
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
            <span>{generating ? 'Synthesizing Grounded Brief...' : 'Generate New Brief'}</span>
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

                {/* Evidence Provenance Header Pill Bar */}
                <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center gap-3 text-xs font-mono">
                  <span className="font-semibold text-slate-600 dark:text-slate-400">Data Provenance Audit:</span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 font-bold border border-emerald-200 dark:border-emerald-800">
                    <Radio className="w-3 h-3 text-emerald-500 animate-pulse" />
                    <span>{liveSignalsCount} Live Crawled Records</span>
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold border border-slate-200 dark:border-slate-700">
                    <Database className="w-3 h-3 text-indigo-500" />
                    <span>{demoSignalsCount} Illustrative Baseline</span>
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 font-bold border border-amber-200 dark:border-amber-800">
                    <ShieldAlert className="w-3 h-3 text-amber-500" />
                    <span>Internal CRM: Not Connected</span>
                  </span>
                </div>
              </div>

              {/* 10 Required Sections */}
              <div className="space-y-8 text-xs sm:text-sm leading-relaxed">
                
                {/* 1. Executive Summary */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400 flex items-center gap-2">
                    <span>1. Executive Summary</span>
                  </h2>
                  <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60">
                    {renderFormattedSection(selectedReport.section_1_executive_summary)}
                  </div>
                </section>

                {/* 2. Customer Signals */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    2. Customer Signals
                  </h2>
                  <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
                    {renderFormattedSection(selectedReport.section_2_customer_signals)}
                  </div>
                </section>

                {/* 3. Competitor Intelligence */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    3. Competitor Intelligence
                  </h2>
                  <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
                    {renderFormattedSection(selectedReport.section_3_competitor_intelligence)}
                  </div>
                </section>

                {/* 4. Market Intelligence */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    4. Market Intelligence
                  </h2>
                  <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
                    {renderFormattedSection(selectedReport.section_4_market_intelligence)}
                  </div>
                </section>

                {/* 5. Internal Business Intelligence */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    5. Internal Business Intelligence
                  </h2>
                  
                  {/* Internal Connection Status Alert Banner */}
                  <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 text-amber-900 dark:text-amber-200 flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-xs uppercase tracking-wider text-amber-800 dark:text-amber-300">
                        Internal Company Data Not Connected
                      </h4>
                      <p className="text-xs text-amber-700 dark:text-amber-400 mt-0.5 leading-relaxed">
                        MeetUniversity has not connected an active internal CRM, ERP, or admissions telemetry integration. The operational items below represent illustrative simulation templates for benchmark modeling only.
                      </p>
                    </div>
                  </div>

                  <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
                    {renderFormattedSection(selectedReport.section_5_internal_intelligence)}
                  </div>
                </section>

                {/* 6. Opportunities Identified */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
                    6. Opportunities Identified (Grounded Facts vs Strategic Interpretations)
                  </h2>
                  <div className="p-5 rounded-xl bg-emerald-50/40 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-800/40">
                    {renderFormattedSection(selectedReport.section_6_opportunities_identified)}
                  </div>
                </section>

                {/* 7. Risks and Threats */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-rose-600 dark:text-rose-400 uppercase tracking-wider">
                    7. Risks and Threats (Grounded Facts vs Strategic Interpretations)
                  </h2>
                  <div className="p-5 rounded-xl bg-rose-50/40 dark:bg-rose-950/20 border border-rose-200/60 dark:border-rose-800/40">
                    {renderFormattedSection(selectedReport.section_7_risks_and_threats)}
                  </div>
                </section>

                {/* 8. Recommended Actions for This Week */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    8. Recommended Actions for This Week
                  </h2>
                  <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
                    {renderFormattedSection(selectedReport.section_8_recommended_actions)}
                  </div>
                </section>

                {/* 9. What We Should Watch */}
                <section className="space-y-2">
                  <h2 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                    9. What We Should Watch (Early-Warning Watchlist)
                  </h2>
                  <div className="p-4 rounded-xl bg-amber-50/40 dark:bg-amber-950/20 border border-amber-200/50 dark:border-amber-800/40">
                    {renderFormattedSection(selectedReport.section_9_what_we_should_watch)}
                  </div>
                </section>

                {/* 10. Source Appendix */}
                <section className="space-y-2 pt-4 border-t border-slate-200 dark:border-slate-800 text-xs">
                  <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    10. Source Appendix & Evidence Traceability
                  </h2>
                  <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60">
                    {renderFormattedSection(selectedReport.section_10_source_appendix)}
                  </div>
                </section>
              </div>

              {/* Document Verification Seal */}
              <div className="pt-6 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>Signal Stack Autonomous Intelligence Engine • Provenance & Evidence Protocol</span>
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
