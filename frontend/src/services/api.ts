import {
  Company, CompanyProfile, InterviewSession, InterviewQA,
  Competitor, Source, IntelligenceItem, InternalDocument,
  MondayReport, ActionItem, ScheduledJobLog, AppSettings
} from '../types';

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url}`;
  const res = await fetch(fullUrl, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    let errorMsg = `HTTP Error ${res.status}`;
    try {
      const err = await res.json();
      errorMsg = err.detail || errorMsg;
    } catch {
      // ignore
    }
    throw new Error(errorMsg);
  }

  return res.json();
}

export const api = {
  // Companies
  getCompanies: () => fetchJson<Company[]>('/api/companies'),
  getCompany: (id: string) => fetchJson<Company>(`/api/companies/${id}`),
  researchCompany: (website: string, company_name?: string) => 
    fetchJson<any>('/api/companies/research', {
      method: 'POST',
      body: JSON.stringify({ website, company_name })
    }),
  createCompany: (data: Partial<Company>) => 
    fetchJson<Company>('/api/companies', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  updateCompany: (id: string, data: Partial<Company>) =>
    fetchJson<Company>(`/api/companies/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
  deleteCompany: (id: string) =>
    fetchJson<any>(`/api/companies/${id}`, { method: 'DELETE' }),

  // Profiles
  getProfile: (companyId: string) => fetchJson<CompanyProfile>(`/api/profiles/${companyId}`),
  generateProfile: (companyId: string) => fetchJson<CompanyProfile>(`/api/profiles/${companyId}/generate`, { method: 'POST' }),

  // Interview
  getInterviewSession: (companyId: string) => fetchJson<InterviewSession>(`/api/interviews/${companyId}/session`),
  startNewInterview: (companyId: string) => fetchJson<InterviewSession>(`/api/interviews/${companyId}/start`, { method: 'POST' }),
  submitAnswer: (sessionId: string, qaId: string, answer_text: string) =>
    fetchJson<InterviewQA>(`/api/interviews/${sessionId}/answer/${qaId}`, {
      method: 'POST',
      body: JSON.stringify({ answer_text })
    }),
  submitFollowUp: (sessionId: string, qaId: string, follow_up_answer: string) =>
    fetchJson<InterviewQA>(`/api/interviews/${sessionId}/followup/${qaId}`, {
      method: 'POST',
      body: JSON.stringify({ follow_up_answer })
    }),

  // Competitors
  getCompetitors: (companyId: string) => fetchJson<Competitor[]>(`/api/competitors/${companyId}`),
  addCompetitor: (companyId: string, data: Partial<Competitor>) =>
    fetchJson<Competitor>(`/api/competitors/${companyId}`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  discoverCompetitors: (companyId: string) =>
    fetchJson<Competitor[]>(`/api/competitors/${companyId}/discover`, { method: 'POST' }),
  deleteCompetitor: (id: string) => fetchJson<any>(`/api/competitors/${id}`, { method: 'DELETE' }),

  // Sources
  getSources: (companyId: string) => fetchJson<Source[]>(`/api/sources/${companyId}`),
  addSource: (companyId: string, data: Partial<Source>) =>
    fetchJson<Source>(`/api/sources/${companyId}`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  discoverSources: (companyId: string) =>
    fetchJson<Source[]>(`/api/sources/${companyId}/discover`, { method: 'POST' }),
  updateSourceStatus: (sourceId: string, approved_status: string) =>
    fetchJson<Source>(`/api/sources/${sourceId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ approved_status })
    }),
  deleteSource: (sourceId: string) => fetchJson<any>(`/api/sources/${sourceId}`, { method: 'DELETE' }),
  auditSources: (companyId?: string) =>
    fetchJson<any[]>(`/api/sources/audit${companyId ? `?company_id=${companyId}` : ''}`, { method: 'POST' }),

  // Crawler
  crawlSource: (sourceId: string) => fetchJson<any>(`/api/crawler/crawl/${sourceId}`, { method: 'POST' }),
  crawlAllSources: (companyId: string) => fetchJson<any>(`/api/crawler/crawl-all/${companyId}`, { method: 'POST' }),
  getCrawlHistory: (companyId: string) => fetchJson<any[]>(`/api/crawler/history/${companyId}`),

  // Intelligence
  getIntelligence: (
    companyId: string,
    params?: {
      category?: string;
      search?: string;
      impact?: string;
      urgency?: string;
      verification?: string;
      include_archived?: boolean;
    }
  ) => {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.set('category', params.category);
    if (params?.search) searchParams.set('search', params.search);
    if (params?.impact) searchParams.set('impact', params.impact);
    if (params?.urgency) searchParams.set('urgency', params.urgency);
    if (params?.verification) searchParams.set('verification', params.verification);
    if (params?.include_archived) searchParams.set('include_archived', 'true');
    const qs = searchParams.toString();
    return fetchJson<IntelligenceItem[]>(`/api/intelligence/${companyId}${qs ? `?${qs}` : ''}`);
  },
  createIntelligence: (companyId: string, data: any) =>
    fetchJson<IntelligenceItem>(`/api/intelligence/${companyId}`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  getRankingBreakdown: (itemId: string) =>
    fetchJson<any>(`/api/intelligence/${itemId}/ranking-breakdown`),
  toggleArchiveIntelligence: (itemId: string) =>
    fetchJson<IntelligenceItem>(`/api/intelligence/${itemId}/archive`, { method: 'PUT' }),
  deleteIntelligence: (itemId: string) =>
    fetchJson<any>(`/api/intelligence/${itemId}`, { method: 'DELETE' }),

  // Internal Docs
  getInternalDocs: (companyId: string) => fetchJson<InternalDocument[]>(`/api/internal-docs/${companyId}`),
  ingestInternalDoc: (companyId: string, data: { title: string; doc_type: string; content: string }) =>
    fetchJson<InternalDocument>(`/api/internal-docs/${companyId}`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  // Reports
  getReports: (companyId: string) => fetchJson<MondayReport[]>(`/api/reports/${companyId}`),
  getReportDetail: (reportId: string) => fetchJson<MondayReport>(`/api/reports/detail/${reportId}`),
  generateReport: (companyId: string) => fetchJson<MondayReport>(`/api/reports/generate/${companyId}`, { method: 'POST' }),
  getReportPdfUrl: (reportId: string) => `${API_BASE_URL}/api/reports/${reportId}/download-pdf`,
  getActionItems: (companyId: string) => fetchJson<ActionItem[]>(`/api/reports/${companyId}/actions`),
  updateActionItem: (actionId: string, data: Partial<ActionItem>) =>
    fetchJson<ActionItem>(`/api/reports/actions/${actionId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

  // Scheduler
  getSchedulerStatus: () => fetchJson<any>('/api/scheduler/status'),
  getJobHistory: () => fetchJson<ScheduledJobLog[]>('/api/scheduler/history'),
  triggerJob: (jobName: string) => fetchJson<any>(`/api/scheduler/trigger/${jobName}`, { method: 'POST' }),

  // Settings
  getSettings: () => fetchJson<AppSettings>('/api/settings'),
  updateSettings: (data: any) =>
    fetchJson<any>('/api/settings', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
};
