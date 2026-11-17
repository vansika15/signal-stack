import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { InternalDocument } from '../types';
import {
  FileCode2, Upload, FileText, CheckCircle2,
  Sparkles, ArrowRight, Clock, Plus, Loader2
} from 'lucide-react';

export const InternalIntelligencePage: React.FC = () => {
  const { activeCompany } = useCompany();
  const [documents, setDocuments] = useState<InternalDocument[]>([]);
  const [title, setTitle] = useState('');
  const [docType, setDocType] = useState('Operational Notes');
  const [content, setContent] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadDocs = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const data = await api.getInternalDocs(activeCompany.id);
      setDocuments(data);
    } catch (err) {
      console.error('Failed to load internal documents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocs();
  }, [activeCompany?.id]);

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCompany || !title.trim() || !content.trim()) return;
    setIngesting(true);
    setSuccessMsg(null);

    try {
      const doc = await api.ingestInternalDoc(activeCompany.id, {
        title,
        doc_type: docType,
        content
      });
      setSuccessMsg(`Document ingested! ${doc.extracted_signals_count} internal intelligence signals extracted and ranked.`);
      setTitle('');
      setContent('');
      await loadDocs();
    } catch (err) {
      console.error('Failed to ingest document:', err);
    } finally {
      setIngesting(false);
    }
  };

  const handleLoadSample = () => {
    setTitle('Q3 Admissions Operations & Applicant Funnel Conversion Report');
    setDocType('Operational Notes');
    setContent(
      "Internal Telemetry & Counselor Call Logs (Q3 2026):\n\n" +
      "1. Intake Volume: 14,200 registered applicants across India and Southeast Asia.\n" +
      "2. Document Verification Delay: Average manual turnaround time currently sits at 46 hours. " +
      "Counselors report that when verification takes >36 hours, student contact rate drops by 22%.\n" +
      "3. Loan Underwriting Drop-Off: 1 in 4 students drop off due to refusal or slow turnaround from local private banks.\n" +
      "4. Institutional Partnership Feedback: University of Hertfordshire and Trinity College Dublin partners " +
      "praised lead verification quality but requested closer integration with their direct application portals."
    );
  };

  if (!activeCompany) return null;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              Pillar 4 Ground-Truth
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Telemetry, Counselor Feedback & Operational Notes
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            {activeCompany.name} Internal Business Intelligence
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Ingest internal operational logs, sales friction notes, and customer interviews to extract actionable signals.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Form: Ingest New Document (Span 2) */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Upload className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
              <span>Ingest Internal Ground-Truth Telemetry</span>
            </h2>

            <button
              type="button"
              onClick={handleLoadSample}
              className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline font-semibold"
            >
              Load Sample Data
            </button>
          </div>

          {successMsg && (
            <div className="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-xs text-emerald-700 dark:text-emerald-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-500" />
              <span>{successMsg}</span>
            </div>
          )}

          <form onSubmit={handleIngest} className="space-y-4 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Document Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="E.g. Q3 Admissions Intake Drop-Off Log"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Telemetry / Document Category
                </label>
                <select
                  value={docType}
                  onChange={(e) => setDocType(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="Operational Notes">Operational Notes</option>
                  <option value="Sales Signals">Sales Signals / CRM Logs</option>
                  <option value="Customer Feedback">Customer Feedback & Interviews</option>
                  <option value="Executive Memo">Executive Strategy Memo</option>
                  <option value="Product Telemetry">Product Usage & Funnel Telemetry</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Document Raw Content / Notes *
              </label>
              <textarea
                rows={8}
                required
                placeholder="Paste customer service call transcripts, counselor bottleneck logs, sales win/loss notes..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={ingesting || !title.trim() || !content.trim()}
                className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md flex items-center gap-2 transition-all disabled:opacity-50"
              >
                {ingesting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Extracting & Ranking Signals...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Ingest & Extract Signals</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Right List: Ingested Documents History */}
        <div className="space-y-4">
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-3">
              Ingested Telemetry Archive ({documents.length})
            </h3>

            <div className="space-y-3">
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="p-3.5 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
                      {doc.doc_type}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      {new Date(doc.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200">
                    {doc.title}
                  </h4>

                  <p className="text-[11px] text-slate-500 line-clamp-2">
                    {doc.content}
                  </p>

                  <div className="pt-1 flex items-center justify-between text-[10px] text-slate-400">
                    <span className="text-emerald-600 dark:text-emerald-400 font-semibold">
                      +{doc.extracted_signals_count} Signals Extracted
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
