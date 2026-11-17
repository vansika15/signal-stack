import React from 'react';
import { IntelligenceItem } from '../types';
import { X, Award, ShieldCheck, Zap, Activity, Clock, Sparkles } from 'lucide-react';

interface RankingModalProps {
  item: IntelligenceItem | null;
  onClose: () => void;
}

export const RankingModal: React.FC<RankingModalProps> = ({ item, onClose }) => {
  if (!item) return null;

  const breakdown = item.ranking_breakdown;
  const components = breakdown?.components;

  const factorItems = [
    {
      name: 'Strategic Relevance',
      weight: '25%',
      score: components?.strategic_relevance?.score || 90,
      contribution: components?.strategic_relevance?.contribution || 22.5,
      icon: Award,
      color: 'text-indigo-500 bg-indigo-50 dark:bg-indigo-950/50',
      barColor: 'bg-indigo-500',
      description: 'Alignment with core company business model, markets, and strategic priorities.'
    },
    {
      name: 'Business Impact',
      weight: '25%',
      score: components?.business_impact?.score || 85,
      contribution: components?.business_impact?.contribution || 21.2,
      icon: Zap,
      color: 'text-purple-500 bg-purple-50 dark:bg-purple-950/50',
      barColor: 'bg-purple-500',
      description: 'Potential revenue, market share, or operational disruption to the organization.'
    },
    {
      name: 'Action Urgency',
      weight: '20%',
      score: components?.action_urgency?.score || 80,
      contribution: components?.action_urgency?.contribution || 16.0,
      icon: Activity,
      color: 'text-rose-500 bg-rose-50 dark:bg-rose-950/50',
      barColor: 'bg-rose-500',
      description: 'Required decision timeframe: Immediate vs Short-Term vs Watchlist.'
    },
    {
      name: 'Credibility & Evidence',
      weight: '15%',
      score: components?.credibility?.score || 95,
      contribution: components?.credibility?.contribution || 14.2,
      icon: ShieldCheck,
      color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/50',
      barColor: 'bg-emerald-500',
      description: 'Source authority tier, direct factual citation, and verification status.'
    },
    {
      name: 'Recency Decay',
      weight: '10%',
      score: components?.recency?.score || 85,
      contribution: components?.recency?.contribution || 8.5,
      icon: Clock,
      color: 'text-amber-500 bg-amber-50 dark:bg-amber-950/50',
      barColor: 'bg-amber-500',
      description: 'Temporal freshness relative to publication and detection timestamps.'
    },
    {
      name: 'Information Novelty',
      weight: '5%',
      score: components?.novelty?.score || 100,
      contribution: components?.novelty?.contribution || 5.0,
      icon: Sparkles,
      color: 'text-sky-500 bg-sky-50 dark:bg-sky-950/50',
      barColor: 'bg-sky-500',
      description: 'Uniqueness of development compared to existing stored intelligence items.'
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
                Explainable Multi-Criteria Ranking
              </span>
              <span className="text-xs text-slate-400">
                Score: <strong className="text-slate-800 dark:text-slate-100 text-sm">{item.ranking_score}/100</strong>
              </span>
            </div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 line-clamp-2">
              {item.headline}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Narrative Explanation */}
        <div className="my-4 p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-mono">
          <p className="font-semibold text-slate-900 dark:text-white mb-1">Algorithmic Reasoning Breakdown:</p>
          {breakdown?.explanation || `Item calculated at ${item.ranking_score}/100. Prioritized due to ${item.strategic_relevance} strategic relevance and ${item.business_impact} business impact.`}
        </div>

        {/* 6 Components Breakdown */}
        <div className="space-y-3.5">
          {factorItems.map((f, i) => {
            const Icon = f.icon;
            return (
              <div key={i} className="p-3 rounded-xl border border-slate-100 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-800/30">
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <div className={`p-1.5 rounded-lg ${f.color}`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-slate-800 dark:text-slate-200">{f.name}</span>
                      <span className="text-[10px] text-slate-400 ml-1.5 font-mono">Weight: {f.weight}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-bold text-slate-900 dark:text-slate-100 font-mono">
                      +{f.contribution} pts
                    </span>
                    <span className="text-[10px] text-slate-400 ml-1">({f.score}%)</span>
                  </div>
                </div>
                
                {/* Progress bar */}
                <div className="w-full bg-slate-200 dark:bg-slate-700 h-1.5 rounded-full overflow-hidden mb-1">
                  <div 
                    className={`h-full rounded-full ${f.barColor}`}
                    style={{ width: `${Math.min(100, f.score)}%` }}
                  />
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  {f.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-slate-900 text-white dark:bg-white dark:text-slate-900 text-sm font-semibold hover:opacity-90 transition-opacity"
          >
            Close Breakdown
          </button>
        </div>
      </div>
    </div>
  );
};
