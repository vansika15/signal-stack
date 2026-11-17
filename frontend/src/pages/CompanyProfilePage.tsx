import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { CompanyProfile, Competitor } from '../types';
import {
  Building2, Globe, Sparkles, TrendingUp, ShieldAlert,
  ExternalLink, Plus, RefreshCw, Save, Check
} from 'lucide-react';

export const CompanyProfilePage: React.FC = () => {
  const { activeCompany, reloadCompanies } = useCompany();
  const [profile, setProfile] = useState<CompanyProfile | null>(null);
  const [competitors, setCompetitors] = useState<Competitor[]>([]);
  const [businessContext, setBusinessContext] = useState('');
  const [savingContext, setSavingContext] = useState(false);
  const [contextSaved, setContextSaved] = useState(false);
  const [discoveringComps, setDiscoveringComps] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadProfile = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const [profData, compsData] = await Promise.all([
        api.getProfile(activeCompany.id),
        api.getCompetitors(activeCompany.id)
      ]);
      setProfile(profData);
      setCompetitors(compsData);
      setBusinessContext(activeCompany.business_context || '');
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, [activeCompany?.id]);

  const handleSaveContext = async () => {
    if (!activeCompany) return;
    setSavingContext(true);
    try {
      await api.updateCompany(activeCompany.id, { business_context: businessContext });
      await reloadCompanies();
      setContextSaved(true);
      setTimeout(() => setContextSaved(false), 3000);
    } catch (err) {
      console.error('Failed to save business context:', err);
    } finally {
      setSavingContext(false);
    }
  };

  const handleDiscoverCompetitors = async () => {
    if (!activeCompany) return;
    setDiscoveringComps(true);
    try {
      const updated = await api.discoverCompetitors(activeCompany.id);
      setCompetitors(updated);
    } catch (err) {
      console.error('Failed to discover competitors:', err);
    } finally {
      setDiscoveringComps(false);
    }
  };

  if (!activeCompany) return null;

  return (
    <div className="space-y-6">
      {/* Header Profile Summary */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 rounded text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              {activeCompany.industry}
            </span>
            <span className="text-xs text-slate-400 font-mono">
              ID: {activeCompany.id}
            </span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            {activeCompany.name} Corporate Profile
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
            {activeCompany.description}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <a
            href={activeCompany.website}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-semibold flex items-center gap-2 transition-colors"
          >
            <Globe className="w-3.5 h-3.5" />
            <span>Visit Website</span>
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
        </div>
      </div>

      {/* Dynamic Business Context Editor (Requirement J) */}
      <div className="p-6 rounded-2xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-200/60 dark:border-indigo-800/40 shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            <h2 className="text-sm font-bold text-slate-900 dark:text-white">
              Dynamic Strategic & Business Context
            </h2>
          </div>
          <span className="text-[11px] text-slate-500 font-mono">
            Directly alters Signal Stack ranking & report synthesis
          </span>
        </div>
        <p className="text-xs text-slate-600 dark:text-slate-400 mb-3">
          Modify the company's immediate operating situation (e.g. visa caps, market entry, cost restructuring) to see the Signal Stack dynamically adjust its strategic priorities.
        </p>

        <textarea
          rows={3}
          value={businessContext}
          onChange={(e) => setBusinessContext(e.target.value)}
          placeholder="E.g. Shifting recruitment from Anglophone destinations to Germany/Ireland following Canadian visa caps..."
          className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-3"
        />

        <div className="flex justify-end">
          <button
            onClick={handleSaveContext}
            disabled={savingContext}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm flex items-center gap-2 transition-all disabled:opacity-50"
          >
            {savingContext ? (
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
            ) : contextSaved ? (
              <Check className="w-3.5 h-3.5 text-emerald-300" />
            ) : (
              <Save className="w-3.5 h-3.5" />
            )}
            <span>{contextSaved ? 'Context Updated!' : 'Update Business Context'}</span>
          </button>
        </div>
      </div>

      {/* Profile Dimensions 4-Grid */}
      {profile && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <h3 className="font-bold text-slate-800 dark:text-slate-200 mb-2 uppercase tracking-wider text-[11px] text-indigo-500">
              Business Model & Monetization
            </h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              {profile.business_model}
            </p>
            <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-slate-500">
              <span>Pricing Structure:</span>
              <span className="font-semibold text-slate-800 dark:text-slate-200">{profile.pricing_tier}</span>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <h3 className="font-bold text-slate-800 dark:text-slate-200 mb-2 uppercase tracking-wider text-[11px] text-indigo-500">
              Customer Value Proposition
            </h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              {profile.value_proposition}
            </p>
            <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-slate-500">
              <span>Primary Markets:</span>
              <span className="font-semibold text-slate-800 dark:text-slate-200">{activeCompany.primary_markets?.join(', ')}</span>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <h3 className="font-bold text-slate-800 dark:text-slate-200 mb-3 uppercase tracking-wider text-[11px] text-indigo-500">
              Key Strategic Priorities
            </h3>
            <div className="space-y-2">
              {profile.strategic_priorities.map((item, i) => (
                <div key={i} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                  <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
            <h3 className="font-bold text-slate-800 dark:text-slate-200 mb-3 uppercase tracking-wider text-[11px] text-rose-500">
              Identified Risks & Vulnerabilities
            </h3>
            <div className="space-y-2">
              {profile.risks_and_challenges.map((item, i) => (
                <div key={i} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                  <div className="w-1.5 h-1.5 rounded-full bg-rose-500 mt-1.5 shrink-0" />
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Competitors Management Table */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
              <span>Competitor Landscape & Market Tiers ({competitors.length})</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Direct, indirect, and emerging competitive threats actively tracked in the Signal Stack.
            </p>
          </div>

          <button
            onClick={handleDiscoverCompetitors}
            disabled={discoveringComps}
            className="px-4 py-2 rounded-xl bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/60 dark:hover:bg-indigo-900/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 text-xs font-semibold flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <Sparkles className={`w-3.5 h-3.5 ${discoveringComps ? 'animate-spin' : ''}`} />
            <span>{discoveringComps ? 'Discovering...' : 'Discover New Competitors'}</span>
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 dark:bg-slate-800/60 text-slate-500 uppercase font-semibold">
              <tr>
                <th className="p-3 rounded-l-lg">Competitor Name</th>
                <th className="p-3">Tier</th>
                <th className="p-3">Market Focus</th>
                <th className="p-3">Key Strengths</th>
                <th className="p-3">Vulnerabilities</th>
                <th className="p-3 rounded-r-lg text-right">Website</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {competitors.map((comp) => (
                <tr key={comp.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                  <td className="p-3 font-bold text-slate-900 dark:text-white whitespace-nowrap">
                    {comp.name}
                  </td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        comp.tier === 'Direct'
                          ? 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
                          : comp.tier === 'Indirect'
                          ? 'bg-amber-50 text-amber-600 dark:bg-amber-950/60 dark:text-amber-400'
                          : 'bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400'
                      }`}
                    >
                      {comp.tier}
                    </span>
                  </td>
                  <td className="p-3 text-slate-600 dark:text-slate-400 max-w-xs">
                    {comp.market_focus || '–'}
                  </td>
                  <td className="p-3 text-slate-600 dark:text-slate-400 max-w-xs">
                    {comp.key_strengths || '–'}
                  </td>
                  <td className="p-3 text-slate-600 dark:text-slate-400 max-w-xs">
                    {comp.vulnerabilities || '–'}
                  </td>
                  <td className="p-3 text-right">
                    {comp.website ? (
                      <a
                        href={comp.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-indigo-600 dark:text-indigo-400 hover:underline inline-flex items-center gap-1"
                      >
                        <span>Visit</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      '–'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
