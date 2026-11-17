import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { IntelligenceItem } from '../types';
import { RankingModal } from '../components/RankingModal';
import {
  Rss, Search, Filter, Sparkles, ExternalLink,
  ShieldCheck, AlertTriangle, Calendar, Award, CheckCircle2,
  Radio, Globe, Database
} from 'lucide-react';

export const IntelligenceFeedPage: React.FC = () => {
  const { activeCompany } = useCompany();
  const [signals, setSignals] = useState<IntelligenceItem[]>([]);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedImpact, setSelectedImpact] = useState('All');
  const [selectedUrgency, setSelectedUrgency] = useState('All');
  const [selectedVerification, setSelectedVerification] = useState('All');
  const [selectedOrigin, setSelectedOrigin] = useState<'All' | 'Crawled' | 'Seeded'>('All');
  const [loading, setLoading] = useState(true);
  const [selectedSignal, setSelectedSignal] = useState<IntelligenceItem | null>(null);

  const loadData = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const data = await api.getIntelligence(activeCompany.id, {
        category: selectedCategory === 'All' ? undefined : selectedCategory,
        search: search.trim() ? search.trim() : undefined,
        impact: selectedImpact === 'All' ? undefined : selectedImpact,
        urgency: selectedUrgency === 'All' ? undefined : selectedUrgency,
        verification: selectedVerification === 'All' ? undefined : selectedVerification
      });
      setSignals(data);
    } catch (err) {
      console.error('Failed to load intelligence feed:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [activeCompany?.id, selectedCategory, selectedImpact, selectedUrgency, selectedVerification]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  if (!activeCompany) return null;

  // Filter by origin (Genuinely Crawled vs Seeded Baseline)
  const filteredSignals = signals.filter(item => {
    if (selectedOrigin === 'Crawled') return item.is_crawled;
    if (selectedOrigin === 'Seeded') return !item.is_crawled;
    return true;
  });

  const crawledCount = signals.filter(s => s.is_crawled).length;
  const seededCount = signals.filter(s => !s.is_crawled).length;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              Live Verified Feed
            </span>
            <span className="text-xs text-slate-400 font-mono">
              6-Factor Multi-Criteria Ranked
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            {activeCompany.name} Real-Time Intelligence Stream ({signals.length})
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Chronological, explainably ranked evidence items discovered across public and internal intelligence channels.
          </p>

          {/* Data Provenance Counter Bar */}
          <div className="flex flex-wrap items-center gap-3 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs">
            <span className="font-semibold text-slate-600 dark:text-slate-400">Data Origin Breakdown:</span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-cyan-50 dark:bg-cyan-950/50 text-cyan-700 dark:text-cyan-300 font-bold border border-cyan-200 dark:border-cyan-800">
              <Radio className="w-3 h-3 text-cyan-500 animate-pulse" />
              <span>{crawledCount} Genuinely Crawled Live</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold border border-slate-200 dark:border-slate-700">
              <Database className="w-3 h-3 text-indigo-500" />
              <span>{seededCount} Seeded Strategic Baseline</span>
            </span>
          </div>
        </div>
      </div>

      {/* Search & Multi-Filters Toolbar */}
      <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-3">
        <form onSubmit={handleSearchSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search headline, summary, or evidence quotes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 rounded-xl bg-slate-900 text-white dark:bg-white dark:text-slate-900 text-xs font-semibold hover:opacity-90 transition-opacity"
          >
            Search
          </button>
        </form>

        {/* Origin Quick Tabs */}
        <div className="flex items-center gap-2 pt-1 border-t border-slate-100 dark:border-slate-800">
          <span className="text-[11px] font-semibold text-slate-500 mr-1">Provenance:</span>
          {(['All', 'Crawled', 'Seeded'] as const).map((origin) => (
            <button
              key={origin}
              onClick={() => setSelectedOrigin(origin)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                selectedOrigin === origin
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900'
              }`}
            >
              {origin === 'All' ? `All Signals (${signals.length})` : origin === 'Crawled' ? `Genuinely Crawled (${crawledCount})` : `Seeded Baseline (${seededCount})`}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-2">
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">Pillar Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs"
            >
              <option value="All">All 4 Pillars</option>
              <option value="Customer Intelligence">Customer Intelligence</option>
              <option value="Competitor Intelligence">Competitor Intelligence</option>
              <option value="Market Intelligence">Market Intelligence</option>
              <option value="Internal Intelligence">Internal Intelligence</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">Business Impact</label>
            <select
              value={selectedImpact}
              onChange={(e) => setSelectedImpact(e.target.value)}
              className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs"
            >
              <option value="All">All Impacts</option>
              <option value="High">High Impact</option>
              <option value="Medium">Medium Impact</option>
              <option value="Low">Low Impact</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">Action Urgency</label>
            <select
              value={selectedUrgency}
              onChange={(e) => setSelectedUrgency(e.target.value)}
              className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs"
            >
              <option value="All">All Urgencies</option>
              <option value="Immediate">Immediate</option>
              <option value="Short-Term">Short-Term</option>
              <option value="Medium-Term">Medium-Term</option>
              <option value="Watchlist">Watchlist</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">Verification Status</label>
            <select
              value={selectedVerification}
              onChange={(e) => setSelectedVerification(e.target.value)}
              className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs"
            >
              <option value="All">All Verifications</option>
              <option value="Verified">Verified</option>
              <option value="Pending Verification">Pending Verification</option>
              <option value="Unverified">Unverified</option>
            </select>
          </div>
        </div>
      </div>

      {/* Feed Stream */}
      <div className="space-y-4">
        {filteredSignals.map((item) => (
          <div
            key={item.id}
            className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:border-indigo-500/50 transition-all space-y-3"
          >
            {/* Header Tags */}
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2">
                {/* Provenance Badge */}
                {item.is_crawled ? (
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-50 text-cyan-700 dark:bg-cyan-950/60 dark:text-cyan-300 border border-cyan-200 dark:border-cyan-800">
                    <Radio className="w-2.5 h-2.5 text-cyan-500" />
                    <span>Genuinely Crawled</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                    <Database className="w-2.5 h-2.5 text-indigo-500" />
                    <span>Seeded Baseline</span>
                  </span>
                )}

                <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                  {item.category}
                </span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    item.nature === 'Threat'
                      ? 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
                      : 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400'
                  }`}
                >
                  {item.nature}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400">
                  {item.urgency}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                  Impact: {item.business_impact}
                </span>
                <span className="flex items-center gap-1 text-[10px] font-semibold text-emerald-600 dark:text-emerald-400">
                  <CheckCircle2 className="w-3 h-3" />
                  <span>{item.verification_status}</span>
                </span>
              </div>

              {/* Explainable Score Badge */}
              <button
                onClick={() => setSelectedSignal(item)}
                className="flex items-center gap-1 px-3 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/60 dark:hover:bg-indigo-900/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 text-xs font-bold transition-colors cursor-pointer"
              >
                <span>Score: {item.ranking_score}/100</span>
                <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
              </button>
            </div>

            {/* Headline & Summary */}
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white leading-snug">
                {item.headline}
              </h2>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">
                {item.summary}
              </p>
            </div>

            {/* Traceable Evidence Box */}
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border-l-2 border-indigo-500 text-xs text-slate-700 dark:text-slate-300 italic">
              <strong className="not-italic text-slate-900 dark:text-white block text-[10px] uppercase font-bold text-indigo-600 dark:text-indigo-400 mb-0.5">
                Verifiable Ground-Truth Evidence:
              </strong>
              {item.evidence}
            </div>

            {/* Strategic Action & Source Link */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
              <div className="text-slate-700 dark:text-slate-300">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold">Action: </span>
                <span>{item.recommended_action}</span>
              </div>

              <div className="flex items-center gap-3 shrink-0 text-slate-400 font-mono text-[11px]">
                <span className="flex items-center gap-1" title={item.publication_date ? `Published: ${item.publication_date}` : `Crawled: ${item.discovery_date}`}>
                  <Calendar className="w-3 h-3" />
                  <span>
                    {item.publication_date
                      ? `Pub: ${new Date(item.publication_date).toLocaleDateString()}`
                      : `Crawled: ${new Date(item.discovery_date).toLocaleDateString()}`}
                  </span>
                </span>
                {item.original_url && (
                  <a
                    href={item.original_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 text-indigo-600 dark:text-indigo-400 hover:underline font-sans font-medium"
                  >
                    <span>Source</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}

        {filteredSignals.length === 0 && (
          <div className="p-12 text-center rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-400">
            <p className="text-sm">No signals match the selected filters.</p>
          </div>
        )}
      </div>

      {/* Explainable Ranking Breakdown Modal */}
      <RankingModal
        item={selectedSignal}
        onClose={() => setSelectedSignal(null)}
      />
    </div>
  );
};
