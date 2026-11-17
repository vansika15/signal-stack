import React from 'react';
import {
  LayoutDashboard,
  Building2,
  Sparkles,
  Layers,
  Radio,
  Rss,
  FileText,
  FileCode2,
  Settings,
  HelpCircle,
  PlusCircle
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onNavigate: (view: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onNavigate }) => {
  const navItems = [
    { id: 'overview', label: 'Overview Dashboard', icon: LayoutDashboard },
    { id: 'company-profile', label: 'Company Profile', icon: Building2 },
    { id: 'ai-interview', label: 'AI Diagnostic Interview', icon: Sparkles, badge: '10 Qs' },
    { id: 'signal-stack', label: 'Signal Stack', icon: Layers, badge: '4 Pillars' },
    { id: 'source-manager', label: 'Source Manager', icon: Radio, badge: '20 Sources' },
    { id: 'intelligence-feed', label: 'Intelligence Feed', icon: Rss },
    { id: 'monday-brief', label: 'Monday Brief', icon: FileText, badge: '10 Sections' },
    { id: 'internal-intelligence', label: 'Internal Intelligence', icon: FileCode2 },
    { id: 'company-setup', label: 'Add / Research Company', icon: PlusCircle },
    { id: 'settings', label: 'Engine Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="p-4 flex-1 space-y-1">
        <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2">
          Intelligence Workspace
        </p>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/20'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400 dark:text-slate-500'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200/50 dark:border-slate-700/50'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer Support Info */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400">
        <div className="flex items-center gap-2 mb-1">
          <HelpCircle className="w-3.5 h-3.5 text-indigo-500" />
          <span className="font-semibold text-slate-700 dark:text-slate-300">EDXSO Assignment 1</span>
        </div>
        <p className="text-[11px] text-slate-400 dark:text-slate-500">
          Fully autonomous AI & crawl pipeline
        </p>
      </div>
    </aside>
  );
};
