import React, { createContext, useContext, useEffect, useState } from 'react';
import { Company } from '../types';
import { api } from '../services/api';

interface CompanyContextType {
  activeCompany: Company | null;
  companies: Company[];
  loading: boolean;
  setActiveCompanyId: (id: string) => void;
  reloadCompanies: () => Promise<void>;
}

const CompanyContext = createContext<CompanyContextType>({
  activeCompany: null,
  companies: [],
  loading: true,
  setActiveCompanyId: () => {},
  reloadCompanies: async () => {},
});

export const CompanyProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [activeCompanyId, setActiveCompanyIdState] = useState<string>(() => {
    return localStorage.getItem('signal_stack_active_company') || 'meetuniversity';
  });
  const [loading, setLoading] = useState(true);

  const reloadCompanies = async () => {
    try {
      const data = await api.getCompanies();
      setCompanies(data);
      if (data.length > 0) {
        const found = data.find(c => c.id === activeCompanyId);
        if (!found) {
          setActiveCompanyIdState(data[0].id);
          localStorage.setItem('signal_stack_active_company', data[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load companies:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    reloadCompanies();
  }, []);

  const setActiveCompanyId = (id: string) => {
    setActiveCompanyIdState(id);
    localStorage.setItem('signal_stack_active_company', id);
  };

  const activeCompany = companies.find(c => c.id === activeCompanyId) || (companies.length > 0 ? companies[0] : null);

  return (
    <CompanyContext.Provider value={{ activeCompany, companies, loading, setActiveCompanyId, reloadCompanies }}>
      {children}
    </CompanyContext.Provider>
  );
};

export const useCompany = () => useContext(CompanyContext);
