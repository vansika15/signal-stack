import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { IntelligenceItem } from '../types';
import { RankingModal } from '../components/RankingModal';
import {
  Layers, Users, Building, Globe2, Cpu, Sparkles,
  ExternalLink, Plus, Filter, ShieldCheck, AlertTriangle
} from 'lucide-react';

export const SignalStackPage: React.FC = () => {
  const { activeCompany } = useCompany();
  const [activeCategory, setActiveCategory] = useState<string>('Customer Intelligence');
  const [signals, setSignals] = useState<IntelligenceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSignal, setSelectedSignal] = useState<IntelligenceItem | null>(null);

  // New Signal Form Modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [newHeadline, setNewHeadline] = useState('');
  const [newSummary, setNewSummary] = useState('');
  const [newEvidence, setNewEvidence] = useState('');
  const [newAction, setNewAction] = useState('');
  const [newImpact, setNewImpact] = useState('High');
  const [newUrgency, setNewUrgency] = useState('Immediate');
  const [newNature, setNewNature] = useState('Opportunity');
  const [addingSignal, setAddingSignal] = useState(false);

  const categories = [
    { id: 'Customer Intelligence', label: '1. Customer Intelligence', icon: Users, desc: 'Student/buyer behavior, application friction, loan bottlenecks, drop-offs, churn sentiment.' },
    { id: 'Competitor Intelligence', label: '2. Competitor Intelligence', icon: Building, desc: 'Direct moves by ApplyBoard, LeverageEdu, Adyen, Dynatrace; commission wars, financing bundling.' },
    { id: 'Market Intelligence', label: '3. Market Intelligence', icon: Globe2, desc: 'IRCC visa caps, UK Graduate Route, Australia Subclass 500 savings rules, foreign currency rates.' },
    { id: 'Internal Intelligence', label: '4. Internal Intelligence', icon: Cpu, desc: 'Counselor intake logs, manual 48h transcript latency, virtual event conversion yields.' },
  ];

  const loadSignals = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const data = await api.getIntelligence(activeCompany.id, { category: activeCategory });
      setSignals(data);
    } catch (err) {
      console.error('Failed to load signals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSignals();
  }, [activeCompany?.id, activeCategory]);

  const handleCreateSignal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCompany || !newHeadline.trim() || !newSummary.trim()) return;
    setAddingSignal(true);
    try {
      await api.createIntelligence(activeCompany.id, {
        category: activeCategory,
        headline: newHeadline,
        summary: newSummary,
        evidence: newEvidence || 'Manual executive signal entry',
        recommended_action: newAction || 'Review with cross-functional leadership',
        business_impact: newImpact,
        strategic_relevance: 'High',
        urgency: newUrgency,
        nature: newNature,
        source_reliability: 'High',
        evidence_strength: 'High',
        verification_status: 'Verified'
      });
      setShowAddModal(false);
      setNewHeadline('');
      setNewSummary('');
      setNewEvidence('');
      setNewAction('');
      await loadSignals();
    } catch (err) {
      console.error('Failed to create signal:', err);
    } finally {
      setAddingSignal(false);
    }
  };

  if (!activeCompany) return null;

  const currentPillar = categories.find(c => c.id === activeCategory);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              The 4 Signal Stack Pillars
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Ground-Truth Intelligence Architecture
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            {activeCompany.name} Signal Stack Matrix
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Categorized across Customer, Competitor, Market, and Internal intelligence dimensions.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md flex items-center gap-2 transition-all self-start md:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Add Custom Signal</span>
        </button>
      </div>

      {/* 4 Category Tabs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const isSelected = activeCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`p-4 rounded-xl text-left border transition-all ${
                isSelected
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-600/20'
                  : 'bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200 border-slate-200 dark:border-slate-800 hover:border-indigo-400'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className={`p-2 rounded-lg ${isSelected ? 'bg-white/20 text-white' : 'bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400'}`}>
                  <Icon className="w-4 h-4" />
                </div>
                {isSelected && (
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-white/20 text-white uppercase tracking-wider">
                    Active Pillar
                  </span>
                )}
              </div>
              <h3 className="text-xs font-bold mb-1">{cat.label}</h3>
              <p className={`text-[11px] line-clamp-2 ${isSelected ? 'text-indigo-100' : 'text-slate-500 dark:text-slate-400'}`}>
                {cat.desc}
              </p>
            </button>
          );
        })}
      </div>

      {/* Pillar Scope Card */}
      {currentPillar && (
        <div className="p-4 rounded-xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-200/50 dark:border-indigo-800/40 text-xs text-slate-700 dark:text-slate-300 flex items-center justify-between">
          <div>
            <strong className="text-slate-900 dark:text-white mr-1.5">{currentPillar.label} Scope:</strong>
            <span>{currentPillar.desc}</span>
          </div>
          <span className="font-mono text-xs font-bold text-indigo-600 dark:text-indigo-400 shrink-0 ml-4">
            {signals.length} Signals Verified
          </span>
        </div>
      )}

      {/* Signals List */}
      <div className="space-y-3">
        {signals.map((signal) => (
          <div
            key={signal.id}
            className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:border-indigo-500/50 transition-all space-y-3"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2">
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
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                  Impact: {signal.business_impact}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                  Relevance: {signal.strategic_relevance}
                </span>
              </div>

              {/* Explainable Ranking Score Badge */}
              <button
                onClick={() => setSelectedSignal(signal)}
                title="Inspect 6-factor algorithmic score breakdown"
                className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/60 dark:hover:bg-indigo-900/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 text-xs font-bold transition-colors cursor-pointer"
              >
                <span>Explainable Score: {signal.ranking_score}/100</span>
                <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
              </button>
            </div>

            <div>
              <h2 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white">
                {signal.headline}
              </h2>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">
                {signal.summary}
              </p>
            </div>

            {/* Direct Evidence Excerpt */}
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border-l-2 border-indigo-500 text-xs text-slate-700 dark:text-slate-300 italic">
              <strong className="not-italic text-slate-900 dark:text-white block text-[10px] uppercase font-bold text-indigo-600 dark:text-indigo-400 mb-0.5">
                Traceable Evidence / Quote:
              </strong>
              {signal.evidence}
            </div>

            {/* Recommended Action & URL */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
              <div className="text-slate-700 dark:text-slate-300 font-medium">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold">Recommended Action: </span>
                <span>{signal.recommended_action}</span>
              </div>

              {signal.original_url && (
                <a
                  href={signal.original_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-indigo-600 dark:text-indigo-400 hover:underline shrink-0"
                >
                  <span>Verify Original Source</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Add Custom Signal Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-lg w-full p-6 space-y-4">
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              Add Intelligence Signal to {activeCategory}
            </h3>

            <form onSubmit={handleCreateSignal} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold mb-1">Headline *</label>
                <input
                  type="text"
                  required
                  value={newHeadline}
                  onChange={(e) => setNewHeadline(e.target.value)}
                  placeholder="E.g. Competitor introduces new financing incentive..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div>
                <label className="block font-semibold mb-1">Executive Summary *</label>
                <textarea
                  rows={2}
                  required
                  value={newSummary}
                  onChange={(e) => setNewSummary(e.target.value)}
                  placeholder="Synthesize the development and strategic implications..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div>
                <label className="block font-semibold mb-1">Direct Evidence / Quote *</label>
                <textarea
                  rows={2}
                  value={newEvidence}
                  onChange={(e) => setNewEvidence(e.target.value)}
                  placeholder="Verifiable excerpt or data point..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div>
                <label className="block font-semibold mb-1">Recommended Action</label>
                <input
                  type="text"
                  value={newAction}
                  onChange={(e) => setNewAction(e.target.value)}
                  placeholder="Specific response recommended for leadership..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                />
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="block font-semibold mb-1">Nature</label>
                  <select
                    value={newNature}
                    onChange={(e) => setNewNature(e.target.value)}
                    className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                  >
                    <option value="Opportunity">Opportunity</option>
                    <option value="Threat">Threat</option>
                    <option value="Neutral">Neutral</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold mb-1">Impact</label>
                  <select
                    value={newImpact}
                    onChange={(e) => setNewImpact(e.target.value)}
                    className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                  >
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold mb-1">Urgency</label>
                  <select
                    value={newUrgency}
                    onChange={(e) => setNewUrgency(e.target.value)}
                    className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"
                  >
                    <option value="Immediate">Immediate</option>
                    <option value="Short-Term">Short-Term</option>
                    <option value="Medium-Term">Medium-Term</option>
                    <option value="Watchlist">Watchlist</option>
                  </select>
                </div>
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
                  disabled={addingSignal}
                  className="px-4 py-2 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-500"
                >
                  {addingSignal ? 'Calculating Ranking...' : 'Add Signal'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Explainable Ranking Breakdown Modal */}
      <RankingModal
        item={selectedSignal}
        onClose={() => setSelectedSignal(null)}
      />
    </div>
  );
};
