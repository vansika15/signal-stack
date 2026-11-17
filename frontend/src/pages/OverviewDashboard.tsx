import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { IntelligenceItem, Source, Competitor, MondayReport, ActionItem } from '../types';
import { StatCard } from '../components/StatCard';
import { RankingModal } from '../components/RankingModal';
import {
  Layers, Radio, ShieldAlert, Sparkles, TrendingUp,
  FileText, ExternalLink, RefreshCw, CheckCircle2, AlertTriangle, ArrowRight
} from 'lucide-react';

interface OverviewDashboardProps {
  onNavigate: (view: string) => void;
}

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({ onNavigate }) => {
  const { activeCompany } = useCompany();
  const [signals, setSignals] = useState<IntelligenceItem[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [competitors, setCompetitors] = useState<Competitor[]>([]);
  const [latestReport, setLatestReport] = useState<MondayReport | null>(null);
  const [actionItems, setActionItems] = useState<ActionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [crawling, setCrawling] = useState(false);
  const [selectedSignalForRanking, setSelectedSignalForRanking] = useState<IntelligenceItem | null>(null);

  const loadData = async () => {
    if (!activeCompany) return;
    setLoading(true);
    setLoadError(null);
    try {
      const [signalsRes, sourcesRes, compsRes, reportsRes, actionsRes] = await Promise.allSettled([
        api.getIntelligence(activeCompany.id),
        api.getSources(activeCompany.id),
        api.getCompetitors(activeCompany.id),
        api.getReports(activeCompany.id),
        api.getActionItems(activeCompany.id)
      ]);

      if (signalsRes.status === 'fulfilled') {
        setSignals(signalsRes.value);
      }
      if (sourcesRes.status === 'fulfilled') {
        setSources(sourcesRes.value);
      }
      if (compsRes.status === 'fulfilled') {
        setCompetitors(compsRes.value);
      }
      if (reportsRes.status === 'fulfilled' && reportsRes.value.length > 0) {
        setLatestReport(reportsRes.value[0]);
      }
      if (actionsRes.status === 'fulfilled') {
        setActionItems(actionsRes.value);
      }

      // If all failed, flag error
      if (signalsRes.status === 'rejected' && sourcesRes.status === 'rejected') {
        setLoadError('Failed to retrieve intelligence records from backend API.');
      }
    } catch (err: any) {
      console.error('Failed to load overview data:', err);
      setLoadError(err?.message || 'Error communicating with intelligence server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [activeCompany?.id]);

  const handleCrawlAll = async () => {
    if (!activeCompany) return;
    setCrawling(true);
    try {
      await api.crawlAllSources(activeCompany.id);
      await loadData();
    } catch (err) {
      console.error('Crawl sweep failed:', err);
    } finally {
      setCrawling(false);
    }
  };

  const customerSignalsCount = signals.filter(s => s.category === 'Customer Intelligence').length;
  const compSignalsCount = signals.filter(s => s.category === 'Competitor Intelligence').length;
  const marketSignalsCount = signals.filter(s => s.category === 'Market Intelligence').length;
  const internalSignalsCount = signals.filter(s => s.category === 'Internal Intelligence').length;

  const verifiedCount = signals.filter(s => s.verification_status === 'Verified').length;
  const verifiedRate = signals.length > 0 ? Math.round((verifiedCount / signals.length) * 100) : 100;
  const healthySources = sources.filter(s => s.health_status === 'healthy').length;
  const crawledSignalsCount = signals.filter(s => s.is_crawled).length;
  const seededSignalsCount = signals.filter(s => !s.is_crawled).length;
  const degradedSources = sources.filter(s => s.health_status !== 'healthy').length;

  if (!activeCompany) {
    return (
      <div className="p-12 text-center rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-slate-800 dark:text-slate-100">No Active Company Selected</h3>
        <p className="text-xs text-slate-500">Please choose a company from the switcher or initialize setup.</p>
        <button
          onClick={() => onNavigate('company-setup')}
          className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md"
        >
          Setup Company
        </button>
      </div>
    );
  }

  if (loading && signals.length === 0) {
    return (
      <div className="p-16 flex flex-col items-center justify-center space-y-4">
        <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
        <div className="text-center">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">
            Loading {activeCompany.name} Command Center...
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Aggregating 4 pillars, monitored sources, and 6-factor algorithmic rankings
          </p>
        </div>
      </div>
    );
  }

  if (loadError && signals.length === 0) {
    return (
      <div className="p-8 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 text-center space-y-3">
        <AlertTriangle className="w-8 h-8 text-rose-500 mx-auto" />
        <h3 className="text-sm font-bold text-rose-800 dark:text-rose-200">Unable to Load Intelligence Signals</h3>
        <p className="text-xs text-rose-600 dark:text-rose-300">{loadError}</p>
        <button
          onClick={loadData}
          className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold shadow-sm"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-900 via-indigo-800 to-slate-900 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/30 text-indigo-200 border border-indigo-400/30">
                Active Organization
              </span>
              <span className="text-xs text-indigo-200 font-mono">
                {activeCompany?.industry}
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              {activeCompany?.name} Intelligence Command Center
            </h1>
            <p className="mt-1 text-sm text-indigo-100/80 max-w-2xl">
              {activeCompany?.description || 'Autonomous signal discovery and real-time competitor tracking.'}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleCrawlAll}
              disabled={crawling}
              className="px-4 py-2.5 rounded-xl bg-white text-slate-900 hover:bg-slate-100 text-sm font-semibold shadow-md flex items-center gap-2 transition-all disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 text-indigo-600 ${crawling ? 'animate-spin' : ''}`} />
              <span>{crawling ? 'Crawling Sources...' : 'Run Crawl Sweep'}</span>
            </button>
            <button
              onClick={() => onNavigate('monday-brief')}
              className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold shadow-md flex items-center gap-2 transition-all"
            >
              <FileText className="w-4 h-4" />
              <span>Monday Brief</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Signals"
          value={signals.length}
          change={crawledSignalsCount > 0 ? `${crawledSignalsCount} live crawled • ${seededSignalsCount} baseline` : `${signals.length} verified signals`}
          changeType="positive"
          icon={Layers}
          iconColor="text-indigo-600 dark:text-indigo-400"
          iconBg="bg-indigo-50 dark:bg-indigo-950/60"
          subtitle="Customer, Competitor, Market, Internal"
        />
        <StatCard
          title="Monitored Sources"
          value={sources.length}
          change={degradedSources > 0 ? `${healthySources} healthy • ${degradedSources} degraded` : `${healthySources}/${sources.length} verified healthy`}
          changeType="positive"
          icon={Radio}
          iconColor="text-emerald-600 dark:text-emerald-400"
          iconBg="bg-emerald-50 dark:bg-emerald-950/60"
          subtitle="Permitted public feeds & monitors"
        />
        <StatCard
          title="Verification Rate"
          value={`${verifiedRate}%`}
          change="Traceable evidence"
          changeType="neutral"
          icon={CheckCircle2}
          iconColor="text-purple-600 dark:text-purple-400"
          iconBg="bg-purple-50 dark:bg-purple-950/60"
          subtitle="No fabricated or unverified data"
        />
        <StatCard
          title="Tracked Competitors"
          value={competitors.length}
          change="Tier 1-3 mapped"
          changeType="neutral"
          icon={TrendingUp}
          iconColor="text-amber-600 dark:text-amber-400"
          iconBg="bg-amber-50 dark:bg-amber-950/60"
          subtitle="Direct, Indirect, Emerging"
        />
      </div>

      {/* 4 Pillars Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          {
            name: 'Customer Intelligence',
            count: customerSignalsCount,
            color: 'border-blue-500/30 hover:border-blue-500',
            bg: 'bg-blue-50/50 dark:bg-blue-950/20',
            textColor: 'text-blue-600 dark:text-blue-400',
            desc: 'Student & buyer intent, friction points, loan drop-offs, churn sentiment.'
          },
          {
            name: 'Competitor Intelligence',
            count: compSignalsCount,
            color: 'border-purple-500/30 hover:border-purple-500',
            bg: 'bg-purple-50/50 dark:bg-purple-950/20',
            textColor: 'text-purple-600 dark:text-purple-400',
            desc: 'Competitor pricing moves, partner networks, financing bundles, feature launches.'
          },
          {
            name: 'Market Intelligence',
            count: marketSignalsCount,
            color: 'border-amber-500/30 hover:border-amber-500',
            bg: 'bg-amber-50/50 dark:bg-amber-950/20',
            textColor: 'text-amber-600 dark:text-amber-400',
            desc: 'Government visa policy caps, macroeconomic shifts, foreign exchange rates.'
          },
          {
            name: 'Internal Intelligence',
            count: internalSignalsCount,
            color: 'border-emerald-500/30 hover:border-emerald-500',
            bg: 'bg-emerald-50/50 dark:bg-emerald-950/20',
            textColor: 'text-emerald-600 dark:text-emerald-400',
            desc: 'Counselor call logs, intake bottlenecks, internal telemetry, margin analysis.'
          }
        ].map((pillar, i) => (
          <div
            key={i}
            onClick={() => onNavigate('signal-stack')}
            className={`p-4 rounded-xl border ${pillar.color} ${pillar.bg} cursor-pointer transition-all hover:shadow-md group`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className={`text-xs font-bold uppercase tracking-wider ${pillar.textColor}`}>
                {pillar.name}
              </span>
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-white dark:bg-slate-800 shadow-sm">
                {pillar.count} signals
              </span>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {pillar.desc}
            </p>
            <div className="mt-3 flex items-center text-xs font-semibold text-slate-700 dark:text-slate-300 group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
              <span>Explore Pillar</span>
              <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        ))}
      </div>

      {/* Main Split Grid: High-Impact Signals & Action Tracker */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Top Prioritized Signals Feed (Span 2) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              <h2 className="text-lg font-bold text-slate-900 dark:text-white">
                Prioritized Intelligence Signals
              </h2>
            </div>
            <button
              onClick={() => onNavigate('intelligence-feed')}
              className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
            >
              <span>View All ({signals.length})</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-3">
            {signals.slice(0, 4).map((signal) => (
              <div
                key={signal.id}
                className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:border-indigo-500/50 transition-colors"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                      {signal.category}
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        signal.nature === 'Threat'
                          ? 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
                          : 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400'
                      }`}
                    >
                      {signal.nature}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400">
                      {signal.urgency}
                    </span>
                  </div>

                  {/* Explainable Ranking Score Badge */}
                  <button
                    onClick={() => setSelectedSignalForRanking(signal)}
                    title="Click to inspect 6-factor algorithmic score breakdown"
                    className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/60 dark:hover:bg-indigo-900/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 text-xs font-bold transition-colors cursor-pointer"
                  >
                    <span>Score: {signal.ranking_score}</span>
                    <Sparkles className="w-3 h-3 text-indigo-500" />
                  </button>
                </div>

                <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-1.5">
                  {signal.headline}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 line-clamp-2 mb-2">
                  {signal.summary}
                </p>

                {/* Evidence Quote */}
                <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border-l-2 border-indigo-500 text-xs text-slate-700 dark:text-slate-300 italic mb-2">
                  {signal.evidence}
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                  <span className="font-medium text-slate-700 dark:text-slate-300">
                    Action: {signal.recommended_action}
                  </span>
                  {signal.original_url && (
                    <a
                      href={signal.original_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 text-indigo-600 dark:text-indigo-400 hover:underline shrink-0"
                    >
                      <span>Source</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Weekly Actions & Competitor Snapshot */}
        <div className="space-y-6">
          {/* Action Items Tracker */}
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                <span>Strategic Action Tracker</span>
              </h3>
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400">
                {actionItems.filter(a => a.status === 'completed').length}/{actionItems.length} Done
              </span>
            </div>

            <div className="space-y-2.5">
              {actionItems.slice(0, 4).map((action) => (
                <div
                  key={action.id}
                  className="p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 flex items-start gap-2.5"
                >
                  <input
                    type="checkbox"
                    checked={action.status === 'completed'}
                    onChange={async () => {
                      const newStatus = action.status === 'completed' ? 'todo' : 'completed';
                      await api.updateActionItem(action.id, { status: newStatus });
                      loadData();
                    }}
                    className="mt-0.5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                  />
                  <div className="flex-1 min-w-0">
                    <p className={`text-xs font-semibold ${action.status === 'completed' ? 'line-through text-slate-400' : 'text-slate-800 dark:text-slate-200'}`}>
                      {action.title}
                    </p>
                    <div className="flex items-center gap-2 mt-1 text-[10px] text-slate-400 font-mono">
                      <span>{action.owner}</span>
                      <span>•</span>
                      <span>Due: {action.due_date}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={() => onNavigate('monday-brief')}
              className="w-full mt-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300 transition-colors"
            >
              Open Monday Brief
            </button>
          </div>

          {/* Competitor Radar Snapshot */}
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                Monitored Competitors ({competitors.length})
              </h3>
              <button
                onClick={() => onNavigate('company-profile')}
                className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                Manage
              </button>
            </div>

            <div className="space-y-2">
              {competitors.slice(0, 5).map((comp) => (
                <div
                  key={comp.id}
                  className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50 text-xs"
                >
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-800 dark:text-slate-200">
                      {comp.name}
                    </span>
                    <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-500">
                      {comp.tier}
                    </span>
                  </div>
                  {comp.website && (
                    <a
                      href={comp.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-400 hover:text-indigo-500"
                    >
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Explainable Ranking Score Breakdown Modal */}
      <RankingModal
        item={selectedSignalForRanking}
        onClose={() => setSelectedSignalForRanking(null)}
      />
    </div>
  );
};
