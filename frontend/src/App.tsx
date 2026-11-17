import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { CompanyProvider, useCompany } from './context/CompanyContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

// Pages
import { OverviewDashboard } from './pages/OverviewDashboard';
import { CompanySetup } from './pages/CompanySetup';
import { CompanyProfilePage } from './pages/CompanyProfilePage';
import { AiInterviewPage } from './pages/AiInterviewPage';
import { SignalStackPage } from './pages/SignalStackPage';
import { SourceManagerPage } from './pages/SourceManagerPage';
import { IntelligenceFeedPage } from './pages/IntelligenceFeedPage';
import { MondayBriefPage } from './pages/MondayBriefPage';
import { InternalIntelligencePage } from './pages/InternalIntelligencePage';
import { SettingsPage } from './pages/SettingsPage';

const AppContent: React.FC = () => {
  const [currentView, setCurrentView] = useState<string>('overview');
  const { loading } = useCompany();

  const renderView = () => {
    switch (currentView) {
      case 'overview':
        return <OverviewDashboard onNavigate={setCurrentView} />;
      case 'company-setup':
        return <CompanySetup onNavigate={setCurrentView} />;
      case 'company-profile':
        return <CompanyProfilePage />;
      case 'ai-interview':
        return <AiInterviewPage />;
      case 'signal-stack':
        return <SignalStackPage />;
      case 'source-manager':
        return <SourceManagerPage />;
      case 'intelligence-feed':
        return <IntelligenceFeedPage />;
      case 'monday-brief':
        return <MondayBriefPage />;
      case 'internal-intelligence':
        return <InternalIntelligencePage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <OverviewDashboard onNavigate={setCurrentView} />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-200">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm font-semibold tracking-wide">Initializing Signal Stack Engine...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 transition-colors">
      <Navbar onNavigate={setCurrentView} activeView={currentView} />
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <div className="no-print">
          <Sidebar currentView={currentView} onNavigate={setCurrentView} />
        </div>
        <main className="flex-1 p-4 sm:p-6 lg:p-8 min-w-0 overflow-y-auto">
          {renderView()}
        </main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <CompanyProvider>
        <AppContent />
      </CompanyProvider>
    </ThemeProvider>
  );
};

export default App;
