import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { AppSettings, ScheduledJobLog } from '../types';
import {
  Settings, Key, Clock, ShieldCheck, RefreshCw,
  CheckCircle2, AlertTriangle, Play, Database, Server
} from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [settingsData, setSettingsData] = useState<AppSettings | null>(null);
  const [jobHistory, setJobHistory] = useState<ScheduledJobLog[]>([]);
  const [apiKeyInput, setApiKeyInput] = useState('');
  const [timezoneInput, setTimezoneInput] = useState('UTC');
  const [crawlHours, setCrawlHours] = useState(24);
  const [saving, setSaving] = useState(false);
  const [triggeringJob, setTriggeringJob] = useState<string | null>(null);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [sData, jData] = await Promise.all([
        api.getSettings(),
        api.getJobHistory()
      ]);
      setSettingsData(sData);
      setJobHistory(jData);
      setTimezoneInput(sData.scheduler_timezone);
      setCrawlHours(sData.crawl_interval_hours);
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSaveSettings = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setStatusMsg(null);
    try {
      await api.updateSettings({
        gemini_api_key: apiKeyInput.trim() ? apiKeyInput.trim() : undefined,
        scheduler_timezone: timezoneInput,
        crawl_interval_hours: crawlHours
      });
      setStatusMsg('Configuration updated successfully!');
      setApiKeyInput('');
      await loadData();
    } catch (err: any) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleTriggerJob = async (jobName: string) => {
    setTriggeringJob(jobName);
    try {
      await api.triggerJob(jobName);
      setStatusMsg(`Job ${jobName} executed successfully!`);
      const updatedHistory = await api.getJobHistory();
      setJobHistory(updatedHistory);
    } catch (err: any) {
      setStatusMsg(`Error running job: ${err.message}`);
    } finally {
      setTriggeringJob(null);
    }
  };

  if (!settingsData) return null;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              System Administration
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Engine Diagnostics & Automation
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            Signal Stack Settings & Schedulers
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Configure Gemini AI API credentials, periodic crawl timers, and audit execution logs.
          </p>
        </div>
      </div>

      {statusMsg && (
        <div className="p-3.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-700 dark:text-indigo-300 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-indigo-500 shrink-0" />
          <span>{statusMsg}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left Card: AI Configuration & Engine Status */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-5">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
            <Key className="w-4 h-4 text-indigo-500" />
            <span>AI Reasoning Engine Status</span>
          </h2>

          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-slate-500">Active Engine:</span>
              <span className="font-bold text-indigo-600 dark:text-indigo-400">
                {settingsData.ai_active_engine}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500">API Key Configured:</span>
              <span className={`font-semibold ${settingsData.gemini_api_key_configured ? 'text-emerald-500' : 'text-amber-500'}`}>
                {settingsData.gemini_api_key_configured ? `Yes (${settingsData.gemini_api_key_masked})` : 'No (Using Offline Semantic Heuristics)'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500">Database Engine:</span>
              <span className="font-mono text-slate-700 dark:text-slate-300">
                {settingsData.database_type}
              </span>
            </div>
          </div>

          <form onSubmit={handleSaveSettings} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Update Gemini API Key
              </label>
              <input
                type="password"
                placeholder={settingsData.gemini_api_key_configured ? 'Paste new API key to override...' : 'Enter your GEMINI_API_KEY...'}
                value={apiKeyInput}
                onChange={(e) => setApiKeyInput(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 font-mono text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <p className="text-[11px] text-slate-400 mt-1">
                Also configurable via .env (GEMINI_API_KEY). When unset, the system uses the built-in domain reasoning engine.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Scheduler Timezone
                </label>
                <input
                  type="text"
                  value={timezoneInput}
                  onChange={(e) => setTimezoneInput(e.target.value)}
                  className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Crawl Interval (Hours)
                </label>
                <input
                  type="number"
                  min={1}
                  max={168}
                  value={crawlHours}
                  onChange={(e) => setCrawlHours(Number(e.target.value))}
                  className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs"
                />
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md transition-all disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Settings'}
              </button>
            </div>
          </form>
        </div>

        {/* Right Card: Background Automation Controls & Manual Triggers */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
            <Clock className="w-4 h-4 text-indigo-500" />
            <span>Autonomous Automation Schedulers</span>
          </h2>

          <div className="space-y-3">
            {[
              {
                id: 'weekly_brief',
                title: 'Weekly Monday Morning Brief',
                schedule: 'Every Monday at 08:00 UTC',
                desc: 'Synthesizes all 10 required executive sections, extracts action items, and generates downloadable PDF.',
              },
              {
                id: 'monthly_audit',
                title: 'Monthly Source-Health & Availability Audit',
                schedule: '1st of every month at 00:00 UTC',
                desc: 'Audits latency, HTTP status codes, and reachability across all 20+ monitored public sources.',
              },
              {
                id: 'crawler_sweep',
                title: 'Periodic Background Crawler Sweep',
                schedule: `Every ${settingsData.crawl_interval_hours} Hours`,
                desc: 'Performs change detection, SHA256 diffing, and signal extraction from permitted sources.',
              }
            ].map((job) => (
              <div
                key={job.id}
                className="p-3.5 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 flex items-center justify-between gap-3 text-xs"
              >
                <div>
                  <div className="font-bold text-slate-800 dark:text-slate-200">{job.title}</div>
                  <div className="text-[10px] text-indigo-600 dark:text-indigo-400 font-mono mt-0.5">{job.schedule}</div>
                  <p className="text-[11px] text-slate-500 mt-1">{job.desc}</p>
                </div>
                <button
                  onClick={() => handleTriggerJob(job.id)}
                  disabled={triggeringJob === job.id}
                  className="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold text-xs flex items-center gap-1.5 shrink-0 transition-colors disabled:opacity-50"
                >
                  <Play className={`w-3 h-3 ${triggeringJob === job.id ? 'animate-spin' : ''}`} />
                  <span>Run Now</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Execution Logs Table */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
          <Server className="w-4 h-4 text-indigo-500" />
          <span>Scheduled Job Execution History ({jobHistory.length})</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 dark:bg-slate-800/60 text-slate-500 uppercase font-semibold">
              <tr>
                <th className="p-3 rounded-l-lg">Job Name</th>
                <th className="p-3">Status</th>
                <th className="p-3">Executed At</th>
                <th className="p-3">Duration</th>
                <th className="p-3">Items Processed</th>
                <th className="p-3 rounded-r-lg">Summary</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-mono text-[11px]">
              {jobHistory.map((job) => (
                <tr key={job.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                  <td className="p-3 font-semibold text-slate-800 dark:text-slate-200">
                    {job.job_name}
                  </td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        job.status === 'success'
                          ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400'
                          : 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
                      }`}
                    >
                      {job.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-3 text-slate-500">
                    {new Date(job.started_at).toLocaleString()}
                  </td>
                  <td className="p-3 text-slate-500">
                    {job.duration_ms} ms
                  </td>
                  <td className="p-3 text-slate-500">
                    {job.items_processed} items
                  </td>
                  <td className="p-3 text-slate-500 max-w-xs truncate">
                    {job.summary || job.error_message || '–'}
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
