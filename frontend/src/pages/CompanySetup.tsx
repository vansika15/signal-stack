import React, { useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { Globe, Sparkles, Building2, Check, ArrowRight, Loader2 } from 'lucide-react';

interface CompanySetupProps {
  onNavigate: (view: string) => void;
}

export const CompanySetup: React.FC<CompanySetupProps> = ({ onNavigate }) => {
  const { reloadCompanies, setActiveCompanyId } = useCompany();
  const [website, setWebsite] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [researching, setResearching] = useState(false);
  const [researchResult, setResearchResult] = useState<any | null>(null);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!website.trim()) return;
    setResearching(true);
    setError(null);

    try {
      const data = await api.researchCompany(website, companyName);
      setResearchResult(data);
      if (data.name && !companyName) setCompanyName(data.name);
    } catch (err: any) {
      setError(err.message || 'Failed to research company');
    } finally {
      setResearching(false);
    }
  };

  const handleCreateCompany = async () => {
    if (!researchResult) return;
    setCreating(true);
    setError(null);

    try {
      const newComp = await api.createCompany({
        name: researchResult.name || companyName,
        website: website.startsWith('http') ? website : `https://${website}`,
        domain: researchResult.domain || website.replace('https://', '').replace('http://', '').split('/')[0],
        industry: researchResult.industry || 'Technology',
        description: researchResult.description || '',
        target_audience: researchResult.target_audience || '',
        primary_markets: researchResult.primary_markets || [],
        business_context: `Initial automated AI profile generation for ${researchResult.name}.`
      });

      await reloadCompanies();
      setActiveCompanyId(newComp.id);
      onNavigate('overview');
    } catch (err: any) {
      setError(err.message || 'Failed to initialize company');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400">
            <Building2 className="w-5 h-5" />
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            Add & Dynamically Research Company
          </h1>
        </div>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Enter any company website to let our AI engine analyze their industry, business model, competitors, and generate a tailored Signal Stack.
        </p>

        {error && (
          <div className="mt-4 p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-xs text-rose-600 dark:text-rose-400">
            {error}
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleResearch} className="mt-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Company Website URL *
              </label>
              <div className="relative">
                <Globe className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="text"
                  required
                  placeholder="https://example.com"
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Company Name (Optional)
              </label>
              <input
                type="text"
                placeholder="Auto-detected if left empty"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={researching || !website.trim()}
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold shadow-md flex items-center gap-2 transition-all disabled:opacity-50"
            >
              {researching ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Researching Company & Strategy...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Start AI Company Research</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Research Results Preview */}
      {researchResult && (
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-md space-y-5 animate-in fade-in duration-200">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
            <div>
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400">
                Research Completed
              </span>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white mt-1">
                {researchResult.name}
              </h2>
              <p className="text-xs text-slate-500">{researchResult.industry}</p>
            </div>
            <button
              onClick={handleCreateCompany}
              disabled={creating}
              className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold shadow-md flex items-center gap-2 transition-all disabled:opacity-50"
            >
              {creating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Initializing Signal Stack...</span>
                </>
              ) : (
                <>
                  <Check className="w-4 h-4" />
                  <span>Deploy Signal Stack Workspace</span>
                </>
              )}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50">
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-1">Company Description</span>
              <p className="text-slate-600 dark:text-slate-400">{researchResult.description}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50">
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-1">Target Audience</span>
              <p className="text-slate-600 dark:text-slate-400">{researchResult.target_audience}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50">
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-1">Business Model</span>
              <p className="text-slate-600 dark:text-slate-400">{researchResult.business_model}</p>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50">
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-1">Value Proposition</span>
              <p className="text-slate-600 dark:text-slate-400">{researchResult.value_proposition}</p>
            </div>
          </div>

          {/* Strategic Priorities */}
          {researchResult.strategic_priorities && (
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                Identified Strategic Priorities
              </h3>
              <div className="space-y-1.5">
                {researchResult.strategic_priorities.map((pri: string, i: number) => (
                  <div key={i} className="flex items-center gap-2 text-xs text-slate-700 dark:text-slate-300">
                    <div className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
                    <span>{pri}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
