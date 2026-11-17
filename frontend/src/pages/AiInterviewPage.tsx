import React, { useEffect, useState } from 'react';
import { useCompany } from '../context/CompanyContext';
import { api } from '../services/api';
import { InterviewSession, InterviewQA } from '../types';
import {
  Sparkles, CheckCircle2, MessageSquare, ArrowRight,
  RefreshCw, Send, HelpCircle, Award, ChevronRight, ChevronLeft
} from 'lucide-react';

export const AiInterviewPage: React.FC = () => {
  const { activeCompany } = useCompany();
  const [session, setSession] = useState<InterviewSession | null>(null);
  const [activeQAIndex, setActiveQAIndex] = useState(0);
  const [answerInput, setAnswerInput] = useState('');
  const [followUpInput, setFollowUpInput] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadSession = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const data = await api.getInterviewSession(activeCompany.id);
      setSession(data);
      // Find first unanswered or keep 0
      const firstUnanswered = data.qas.findIndex(q => !q.is_answered);
      if (firstUnanswered !== -1) {
        setActiveQAIndex(firstUnanswered);
      } else {
        setActiveQAIndex(0);
      }
    } catch (err) {
      console.error('Failed to load interview session:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSession();
  }, [activeCompany?.id]);

  const currentQA: InterviewQA | undefined = session?.qas[activeQAIndex];

  useEffect(() => {
    if (currentQA) {
      setAnswerInput(currentQA.answer_text || '');
      setFollowUpInput(currentQA.follow_up_answer || '');
    }
  }, [currentQA?.id]);

  const handleSubmitAnswer = async () => {
    if (!session || !currentQA || !answerInput.trim()) return;
    setSubmitting(true);
    try {
      const updatedQA = await api.submitAnswer(session.id, currentQA.id, answerInput);
      setSession(prev => {
        if (!prev) return null;
        const newQAs = [...prev.qas];
        newQAs[activeQAIndex] = updatedQA;
        return {
          ...prev,
          qas: newQAs,
          current_question_index: Math.min(prev.total_questions, prev.current_question_index + 1)
        };
      });
    } catch (err) {
      console.error('Failed to submit answer:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleSubmitFollowUp = async () => {
    if (!session || !currentQA || !followUpInput.trim()) return;
    setSubmitting(true);
    try {
      const updatedQA = await api.submitFollowUp(session.id, currentQA.id, followUpInput);
      setSession(prev => {
        if (!prev) return null;
        const newQAs = [...prev.qas];
        newQAs[activeQAIndex] = updatedQA;
        return { ...prev, qas: newQAs };
      });
    } catch (err) {
      console.error('Failed to submit follow-up answer:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRestart = async () => {
    if (!activeCompany) return;
    setLoading(true);
    try {
      const newSession = await api.startNewInterview(activeCompany.id);
      setSession(newSession);
      setActiveQAIndex(0);
      setAnswerInput('');
      setFollowUpInput('');
    } catch (err) {
      console.error('Failed to restart interview:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!activeCompany || !session) return null;

  const answeredCount = session.qas.filter(q => q.is_answered).length;
  const progressPercent = Math.round((answeredCount / session.total_questions) * 100);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              AI Adaptive Diagnostic
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Status: {session.status === 'completed' ? 'Fully Completed' : `${answeredCount}/10 Answered`}
            </span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">
            10-Question Strategic Intelligence Interview
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Interviews the executive on customer friction, competitor encroachment, regulatory headwinds, and internal bottlenecks.
          </p>
        </div>

        <button
          onClick={handleRestart}
          className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-2 transition-colors self-start md:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5 text-slate-400" />
          <span>Generate New Interview</span>
        </button>
      </div>

      {/* Progress Bar & Question Step Indicator */}
      <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-3">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-700 dark:text-slate-300">
          <span>Diagnostic Progress ({progressPercent}%)</span>
          <span>{answeredCount} of 10 Completed</span>
        </div>
        <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* 10 Step Buttons */}
        <div className="grid grid-cols-5 sm:grid-cols-10 gap-2 pt-2">
          {session.qas.map((q, idx) => {
            const isCurrent = idx === activeQAIndex;
            const isAnswered = q.is_answered;
            return (
              <button
                key={q.id}
                onClick={() => setActiveQAIndex(idx)}
                className={`py-2 px-1 rounded-xl text-xs font-bold transition-all text-center flex flex-col items-center justify-center gap-0.5 ${
                  isCurrent
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 ring-2 ring-indigo-400/50'
                    : isAnswered
                    ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-800/60'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-700'
                }`}
              >
                <span>Q{q.question_number}</span>
                {isAnswered && <CheckCircle2 className="w-3 h-3 text-emerald-500" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Active Question Interrogation Card */}
      {currentQA && (
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-6 animate-in fade-in duration-150">
          
          {/* Question Title & Pillar Category */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-400">
                {currentQA.category}
              </span>
              <span className="text-xs text-slate-400">
                Question {currentQA.question_number} of 10
              </span>
            </div>
            <h2 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-snug">
              {currentQA.question_text}
            </h2>
            {currentQA.context_hint && (
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 flex items-center gap-1.5">
                <HelpCircle className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                <span>Strategic Context: {currentQA.context_hint}</span>
              </p>
            )}
          </div>

          {/* Primary Answer Submission */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
              Executive Assessment / Ground Truth Answer:
            </label>
            <textarea
              rows={4}
              value={answerInput}
              onChange={(e) => setAnswerInput(e.target.value)}
              placeholder="Provide specific metrics, customer quotes, or operational facts..."
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <div className="flex justify-end">
              <button
                onClick={handleSubmitAnswer}
                disabled={submitting || !answerInput.trim()}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md flex items-center gap-2 transition-all disabled:opacity-50"
              >
                {submitting ? (
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Send className="w-3.5 h-3.5" />
                )}
                <span>{currentQA.is_answered ? 'Update Answer' : 'Submit & Generate Follow-up'}</span>
              </button>
            </div>
          </div>

          {/* Adaptive Follow-Up Question & Strategic Takeaway (Contextual) */}
          {currentQA.is_answered && currentQA.follow_up_question && (
            <div className="p-4 rounded-xl bg-purple-50/50 dark:bg-purple-950/20 border border-purple-200/60 dark:border-purple-800/40 space-y-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Sparkles className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                  <span className="text-xs font-bold text-purple-900 dark:text-purple-200 uppercase tracking-wider">
                    Adaptive Follow-Up Interrogation
                  </span>
                </div>
                <p className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                  {currentQA.follow_up_question}
                </p>
              </div>

              {currentQA.strategic_takeaway && (
                <div className="p-3 rounded-lg bg-white/80 dark:bg-slate-900/80 border border-purple-200/40 dark:border-purple-800/30 text-xs text-purple-900 dark:text-purple-200">
                  <strong className="block text-[10px] uppercase font-bold text-purple-600 dark:text-purple-400 mb-0.5">
                    Signal Synthesis Takeaway:
                  </strong>
                  {currentQA.strategic_takeaway}
                </div>
              )}

              {/* Follow-Up Answer Input */}
              <div className="space-y-2">
                <input
                  type="text"
                  value={followUpInput}
                  onChange={(e) => setFollowUpInput(e.target.value)}
                  placeholder="Elaborate with operational target or action item..."
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <div className="flex justify-end">
                  <button
                    onClick={handleSubmitFollowUp}
                    disabled={submitting || !followUpInput.trim()}
                    className="px-3.5 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold shadow-sm transition-all disabled:opacity-50"
                  >
                    Save Follow-Up Answer
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Navigation Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-800">
            <button
              onClick={() => setActiveQAIndex(prev => Math.max(0, prev - 1))}
              disabled={activeQAIndex === 0}
              className="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1 disabled:opacity-30"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>Previous</span>
            </button>
            <button
              onClick={() => setActiveQAIndex(prev => Math.min(session.total_questions - 1, prev + 1))}
              disabled={activeQAIndex === session.total_questions - 1}
              className="px-3 py-1.5 rounded-lg bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-xs font-semibold flex items-center gap-1 disabled:opacity-30"
            >
              <span>Next Question</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
