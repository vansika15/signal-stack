export interface Company {
  id: string;
  name: string;
  website: string;
  domain: string;
  industry: string;
  description?: string;
  target_audience?: string;
  primary_markets: string[];
  business_context?: string;
  created_at: string;
  updated_at: string;
  profile?: CompanyProfile;
}

export interface CompanyProfile {
  id: string;
  company_id: string;
  business_model?: string;
  value_proposition?: string;
  pricing_tier?: string;
  strategic_priorities: string[];
  key_differentiators: string[];
  risks_and_challenges: string[];
  tech_stack_summary?: string;
  generated_by: string;
  updated_at: string;
}

export interface InterviewQA {
  id: string;
  session_id: string;
  question_number: number;
  category: string;
  question_text: string;
  context_hint?: string;
  answer_text?: string;
  is_answered: boolean;
  follow_up_question?: string;
  follow_up_answer?: string;
  strategic_takeaway?: string;
  created_at: string;
  answered_at?: string;
}

export interface InterviewSession {
  id: string;
  company_id: string;
  status: string;
  total_questions: number;
  current_question_index: number;
  created_at: string;
  completed_at?: string;
  qas: InterviewQA[];
}

export interface Competitor {
  id: string;
  company_id: string;
  name: string;
  website?: string;
  tier: string;
  market_focus?: string;
  key_strengths?: string;
  vulnerabilities?: string;
  monitored: boolean;
  discovery_method: string;
  created_at: string;
}

export interface Source {
  id: string;
  company_id: string;
  name: string;
  url: string;
  source_type: string;
  relevance_explanation: string;
  approved_status: 'approved' | 'pending' | 'rejected';
  health_status: 'healthy' | 'slow' | 'unreachable' | 'rate_limited';
  last_crawled_at?: string;
  last_status_code?: number;
  error_message?: string;
  crawl_frequency_hours: number;
  content_hash?: string;
  created_at: string;
}

export interface RankingBreakdown {
  total_score: number;
  components: {
    strategic_relevance: { score: number; weight: number; contribution: number };
    business_impact: { score: number; weight: number; contribution: number };
    action_urgency: { score: number; weight: number; contribution: number };
    credibility: { score: number; weight: number; contribution: number };
    recency: { score: number; weight: number; contribution: number };
    novelty: { score: number; weight: number; contribution: number };
  };
  explanation: string;
}

export interface IntelligenceItem {
  id: string;
  company_id: string;
  source_id?: string;
  competitor_id?: string;
  category: 'Customer Intelligence' | 'Competitor Intelligence' | 'Market Intelligence' | 'Internal Intelligence';
  headline: string;
  summary: string;
  evidence: string;
  original_url?: string;
  publication_date?: string;
  discovery_date: string;
  verification_status: 'Verified' | 'Pending Verification' | 'Unverified';
  source_reliability: 'High' | 'Medium' | 'Low';
  evidence_strength: 'High' | 'Medium' | 'Low';
  strategic_relevance: 'High' | 'Medium' | 'Low';
  business_impact: 'High' | 'Medium' | 'Low';
  nature: 'Opportunity' | 'Threat' | 'Neutral';
  urgency: 'Immediate' | 'Short-Term' | 'Medium-Term' | 'Watchlist';
  recommended_action: string;
  ranking_score: number;
  ranking_breakdown?: RankingBreakdown;
  is_crawled?: boolean;
  is_archived: boolean;
  created_at: string;
}

export interface InternalDocument {
  id: string;
  company_id: string;
  title: string;
  doc_type: string;
  content: string;
  extracted_signals_count: number;
  created_at: string;
}

export interface ActionItem {
  id: string;
  report_id?: string;
  company_id: string;
  title: string;
  description?: string;
  category: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  status: 'todo' | 'in_progress' | 'completed';
  owner?: string;
  due_date?: string;
  created_at: string;
  completed_at?: string;
}

export interface MondayReport {
  id: string;
  company_id: string;
  report_week: string;
  title: string;
  section_1_executive_summary: string;
  section_2_customer_signals: string;
  section_3_competitor_intelligence: string;
  section_4_market_intelligence: string;
  section_5_internal_intelligence: string;
  section_6_opportunities_identified: string;
  section_7_risks_and_threats: string;
  section_8_recommended_actions: string;
  section_9_what_we_should_watch: string;
  section_10_source_appendix: string;
  included_signals_ids: string[];
  pdf_export_path?: string;
  created_at: string;
  action_items?: ActionItem[];
}

export interface ScheduledJobLog {
  id: string;
  job_name: string;
  job_type: string;
  status: 'success' | 'failed' | 'running';
  started_at: string;
  finished_at?: string;
  duration_ms: number;
  items_processed: number;
  summary?: string;
  error_message?: string;
}

export interface AppSettings {
  app_name: string;
  app_env: string;
  database_url: string;
  database_type: string;
  gemini_api_key_configured: boolean;
  gemini_api_key_masked: string;
  ai_active_engine: string;
  scheduler_enabled: boolean;
  scheduler_timezone: string;
  crawl_interval_hours: number;
  default_company_id: string;
}
