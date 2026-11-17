import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { Source } from '../types';
import {
  Radio, Check, X, Trash2, RefreshCw, ExternalLink,
  ShieldCheck, AlertCircle, AlertTriangle, Sparkles, Plus, Clock, Search,
  Activity, CheckCircle2, ShieldAlert
} from 'lucide-react';

export const SourceManagerPage: React.FC = () => {
  const { activeCompany } = useCompany();
  const [sources, setSources] = useState<Source[]>([]);
  const [filterType, setFilterType] = useState<string>('All');
  const [healthFilter, setHealthFilter] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [auditing, setAuditing] = useState(false);
  const [crawlingSourceId, setCrawlingSourceId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // New source modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [newName, setNewName] = useState('');
  const [newUrl, setNewUrl] = useState('');
  const [newType, setNewType] = useState('Industry News');
  const [newExplanation, setNewExplanation] = useState('');

  const loadSources = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const data = await api.getSources(activeCompany.id);
      setSources(data);
    } catch (err) {
      console.error('Failed to load sources:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSources();
  }, [activeCompany?.id]);

  const handleUpdateStatus = async (sourceId: string, status: 'approved' | 'rejected') => {
    try {
      const updated = await api.updateSourceStatus(sourceId, status);
      setSources(prev => prev.map(s => s.id === sourceId ? updated : s));
    } catch (err) {
      console.error('Failed to update source status:', err);
    }
  };

  const handleDelete = async (sourceId: string) => {
    try {
      await api.deleteSource(sourceId);
      setSources(prev => prev.filter(s => s.id !== sourceId));
    } catch (err) {
      console.error('Failed to delete source:', err);
    }
  };

  const handleCrawl = async (sourceId: string) => {
    setCrawlingSourceId(sourceId);
    try {
      await api.crawlSource(sourceId);
      await loadSources();
    } catch (err) {
      console.error('Crawl failed:', err);
    } finally {
      setCrawlingSourceId(null);
    }
  };

  const handleAudit = async () => {
    if (!activeCompany) return;
    setAuditing(true);
    try {
      await api.auditSources(activeCompany.id);
      await loadSources();
    } catch (err) {
      console.error('Audit failed:', err);
    } finally {
      setAuditing(false);
    }
  };

  const handleAddSource = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCompany || !newName || !newUrl) return;
    try {
      const created = await api.addSource(activeCompany.id, {
        name: newName,
        url: newUrl.startsWith('http') ? newUrl : `https://${newUrl}`,
        source_type: newType,
        relevance_explanation: newExplanation || 'Permitted monitoring source.',
        approved_status: 'approved'
      });
      setSources(prev => [created, ...prev]);
      setShowAddModal(false);
      setNewName('');
      setNewUrl('');
      setNewExplanation('');
    } catch (err) {
      console.error('Failed to add source:', err);
    }
  };

  if (!activeCompany) return null;

  const filteredSources = sources.filter(s => {
    const matchesSearch = s.name.toLowerCase().includes(searchQuery.toLowerCase()) || s.url.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterType === 'All' ? true : s.approved_status === filterType.toLowerCase();
    const matchesHealth = healthFilter === 'All' ? true : s.health_status === healthFilter.toLowerCase();
    return matchesSearch && matchesFilter && matchesHealth;
  });

  const approvedCount = sources.filter(s => s.approved_status === 'approved').length;
  const healthyCount = sources.filter(s => s.health_status === 'healthy').length;
  const slowCount = sources.filter(s => s.health_status === 'slow').length;
  const rateLimitedCount = sources.filter(s => s.health_status === 'rate_limited').length;
  const unreachableCount = sources.filter(s => s.health_status === 'unreachable').length;
  const pendingCount = sources.filter(s => !s.health_status || s.health_status === 'pending').length;

  const renderHealthBadge = (health: string, statusCode?: number) => {
    switch (health) {
      case 'healthy':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
            <CheckCircle2 className="w-3 h-3 text-emerald-500" />
            <span>Healthy {statusCode ? `(${statusCode})` : ''}</span>
          </span>
        );
      case 'slow':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200 dark:border-amber-800">
            <Activity className="w-3 h-3 text-amber-500" />
            <span>Slow {statusCode ? `(${statusCode})` : ''}</span>
          </span>
        );
      case 'rate_limited':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-orange-50 text-orange-700 dark:bg-orange-950/60 dark:text-orange-400 border border-orange-200 dark:border-orange-800">
            <ShieldAlert className="w-3 h-3 text-orange-500" />
            <span>Rate Limited {statusCode ? `(${statusCode})` : ''}</span>
          </span>
        );
      case 'unreachable':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-400 border border-rose-200 dark:border-rose-800">
            <AlertTriangle className="w-3 h-3 text-rose-500" />
            <span>Unreachable {statusCode ? `(${statusCode})` : ''}</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
            <Clock className="w-3 h-3 text-slate-400" />
            <span>Pending Check</span>
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              Source Discovery & Verification
            </span>
            <span className="text-xs text-slate-500 font-medium">
              {approvedCount} Approved Feeds
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            {activeCompany.name} Monitored Public Sources ({sources.length})
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Permitted public news hubs, government regulatory gazettes, competitor portals, and student advisory bodies.
          </p>

          {/* Source Health Tally Bar */}
          <div className="flex flex-wrap items-center gap-3 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs">
            <span className="font-semibold text-slate-600 dark:text-slate-400">Live Health Audit:</span>
            <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              {healthyCount} Healthy
            </span>
            {slowCount > 0 && (
              <span className="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400 font-medium">
                <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                {slowCount} Slow
              </span>
            )}
            {rateLimitedCount > 0 && (
              <span className="inline-flex items-center gap-1 text-orange-600 dark:text-orange-400 font-medium">
                <span className="w-2 h-2 rounded-full bg-orange-500"></span>
                {rateLimitedCount} Rate-Limited
              </span>
            )}
            {unreachableCount > 0 && (
              <span className="inline-flex items-center gap-1 text-rose-600 dark:text-rose-400 font-medium">
                <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                {unreachableCount} Unreachable
              </span>
            )}
            {pendingCount > 0 && (
              <span className="inline-flex items-center gap-1 text-slate-500 font-medium">
                <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                {pendingCount} Pending
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={handleAudit}
            disabled={auditing}
            className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <ShieldCheck className={`w-3.5 h-3.5 text-indigo-500 ${auditing ? 'animate-pulse' : ''}`} />
            <span>{auditing ? 'Auditing Availability...' : 'Run Live Health Audit'}</span>
          </button>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md flex items-center gap-2 transition-all"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Source</span>
          </button>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl">
            {['All', 'Approved', 'Pending', 'Rejected'].map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                  filterType === type
                    ? 'bg-white text-slate-900 dark:bg-slate-900 dark:text-white shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
                }`}
              >
                {type}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl">
            {['All', 'Healthy', 'Slow', 'Unreachable'].map((hType) => (
              <button
                key={hType}
                onClick={() => setHealthFilter(hType)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-colors ${
                  healthFilter === hType
                    ? 'bg-white text-slate-900 dark:bg-slate-900 dark:text-white shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
                }`}
              >
                {hType}
              </button>
            ))}
          </div>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search sources or URLs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredSources.map((source) => {
          const isCrawling = crawlingSourceId === source.id;
          return (
            <div
              key={source.id}
              className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:border-indigo-500/40 transition-colors flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                      {source.source_type}
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        source.approved_status === 'approved'
                          ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400'
                          : source.approved_status === 'rejected'
                          ? 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
                          : 'bg-amber-50 text-amber-600 dark:bg-amber-950/60 dark:text-amber-400'
                      }`}
                    >
                      {source.approved_status.toUpperCase()}
                    </span>
                    {renderHealthBadge(source.health_status, source.last_status_code)}
                  </div>

                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-slate-400 hover:text-indigo-600"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>

                <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-1">
                  {source.name}
                </h3>
                <p className="text-[11px] text-slate-400 font-mono truncate mb-2">
                  {source.url}
                </p>

                {source.error_message && (
                  <div className="mb-2 p-2 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 text-[11px] text-rose-700 dark:text-rose-400 flex items-center gap-1.5">
                    <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">{source.error_message}</span>
                  </div>
                )}

                {/* Relevance Explanation */}
                <div className="p-2.5 rounded-lg bg-indigo-50/60 dark:bg-indigo-950/30 border border-indigo-200/40 dark:border-indigo-800/30 text-xs text-slate-700 dark:text-slate-300">
                  <strong className="block text-[10px] uppercase font-bold text-indigo-600 dark:text-indigo-400 mb-0.5">
                    Strategic Relevance:
                  </strong>
                  {source.relevance_explanation}
                </div>
              </div>

              {/* Crawl Status & Action Controls */}
              <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
                <span className="text-[11px] text-slate-400 font-mono">
                  {source.last_crawled_at ? `Crawled ${new Date(source.last_crawled_at).toLocaleDateString()}` : 'Pending crawl'}
                </span>

                <div className="flex items-center gap-1.5">
                  <button
                    onClick={() => handleCrawl(source.id)}
                    disabled={isCrawling}
                    title="Run live crawl on this source"
                    className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-indigo-600 dark:text-indigo-400 transition-colors"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${isCrawling ? 'animate-spin' : ''}`} />
                  </button>

                  {source.approved_status !== 'approved' && (
                    <button
                      onClick={() => handleUpdateStatus(source.id, 'approved')}
                      title="Approve source"
                      className="p-1.5 rounded-lg bg-emerald-50 text-emerald-600 hover:bg-emerald-100 transition-colors"
                    >
                      <Check className="w-3.5 h-3.5" />
                    </button>
                  )}

                  {source.approved_status !== 'rejected' && (
                    <button
                      onClick={() => handleUpdateStatus(source.id, 'rejected')}
                      title="Reject source"
                      className="p-1.5 rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100 transition-colors"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  )}

                  <button
                    onClick={() => handleDelete(source.id)}
                    title="Remove source"
                    className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Add Source Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-lg w-full p-6 space-y-4">
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              Add Permitted Monitoring Source
            </h3>

            <form onSubmit={handleAddSource} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold mb-1">Source Name *</label>
                <input
                  type="text"
                  required
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  placeholder="E.g. UKCISA"
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div>
                <label className="block font-semibold mb-1">Source URL *</label>
                <input
                  type="text"
                  required
                  value={newUrl}
                  onChange={(e) => setNewUrl(e.target.value)}
                  placeholder="https://www.ukcisa.org.uk"
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div>
                <label className="block font-semibold mb-1">Source Category</label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value)}
                  className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                >
                  <option value="Industry News">Industry News</option>
                  <option value="Competitor Website">Competitor Website</option>
                  <option value="Regulatory/Govt">Regulatory/Govt</option>
                  <option value="Community/Forums">Community/Forums</option>
                  <option value="Review Platform">Review Platform</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold mb-1">Relevance Explanation *</label>
                <textarea
                  rows={2}
                  required
                  value={newExplanation}
                  onChange={(e) => setNewExplanation(e.target.value)}
                  placeholder="Why is this source essential for this company's Signal Stack?"
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-500"
                >
                  Add Source
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
