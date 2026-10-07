import React, { useState } from 'react';
import Header from './components/Header';
import StartupForm from './components/StartupForm';
import LoadingState from './components/LoadingState';
import ScoreCard from './components/ScoreCard';
import SwotSection from './components/SwotSection';
import MarketSection from './components/MarketSection';
import CompetitorSection from './components/CompetitorSection';
import PersonaSection from './components/PersonaSection';
import PricingSection from './components/PricingSection';
import MVPSection from './components/MVPSection';
import EvaluationSection from './components/EvaluationSection';
import SourcesSection from './components/SourcesSection';
import ErrorState from './components/ErrorState';
import { validateStartupIdea } from './services/api';
import { Award, LineChart, Users, DollarSign, Cpu, CheckSquare, BookOpen, ArrowUp } from 'lucide-react';

export default function App() {
  const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'results' | 'error'
  const [resultData, setResultData] = useState(null);
  const [errorObj, setErrorObj] = useState(null);
  const [activeTab, setActiveTab] = useState('all');

  const handleValidate = async (formData) => {
    setStatus('loading');
    setErrorObj(null);
    try {
      const data = await validateStartupIdea(formData);
      setResultData(data);
      setStatus('results');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      console.error('Validation error:', err);
      setErrorObj(err);
      setStatus('error');
    }
  };

  const handleReset = () => {
    setStatus('idle');
    setResultData(null);
    setErrorObj(null);
    setActiveTab('all');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col selection:bg-zinc-800 selection:text-white">
      {/* Header */}
      <Header onReset={handleReset} hasResults={status === 'results'} />

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {status === 'idle' && (
          <StartupForm onSubmit={handleValidate} isLoading={false} />
        )}

        {status === 'loading' && <LoadingState />}

        {status === 'error' && (
          <ErrorState error={errorObj} onRetry={handleReset} />
        )}

        {status === 'results' && resultData && (
          <div className="space-y-8 animate-fadeIn">
            {/* Quick Section Filter Bar */}
            <div className="sticky top-16 z-40 bg-black/90 backdrop-blur-md py-3 border-b border-zinc-800 -mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8 flex items-center overflow-x-auto no-scrollbar space-x-2">
              <button
                onClick={() => setActiveTab('all')}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition flex-shrink-0 ${
                  activeTab === 'all'
                    ? 'bg-white text-black font-bold'
                    : 'bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`}
              >
                Full Dashboard
              </button>
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition flex-shrink-0 flex items-center gap-1.5 ${
                  activeTab === 'overview'
                    ? 'bg-white text-black font-bold'
                    : 'bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`}
              >
                <Award className="w-3.5 h-3.5" /> Score & SWOT
              </button>
              <button
                onClick={() => setActiveTab('market')}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition flex-shrink-0 flex items-center gap-1.5 ${
                  activeTab === 'market'
                    ? 'bg-white text-black font-bold'
                    : 'bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`}
              >
                <LineChart className="w-3.5 h-3.5" /> Market & Competitors
              </button>
              <button
                onClick={() => setActiveTab('personas')}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition flex-shrink-0 flex items-center gap-1.5 ${
                  activeTab === 'personas'
                    ? 'bg-white text-black font-bold'
                    : 'bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`}
              >
                <Users className="w-3.5 h-3.5" /> Personas & Pricing
              </button>
              <button
                onClick={() => setActiveTab('mvp')}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition flex-shrink-0 flex items-center gap-1.5 ${
                  activeTab === 'mvp'
                    ? 'bg-white text-black font-bold'
                    : 'bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`}
              >
                <Cpu className="w-3.5 h-3.5" /> MVP & Scoping
              </button>
              <button
                onClick={() => setActiveTab('evaluation')}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition flex-shrink-0 flex items-center gap-1.5 ${
                  activeTab === 'evaluation'
                    ? 'bg-white text-black font-bold'
                    : 'bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`}
              >
                <CheckSquare className="w-3.5 h-3.5" /> 7-Point Matrix
              </button>
            </div>

            {/* Dashboard Content Sections */}
            {(activeTab === 'all' || activeTab === 'overview') && (
              <>
                <ScoreCard data={resultData} />
                <SwotSection data={resultData} />
              </>
            )}

            {(activeTab === 'all' || activeTab === 'market') && (
              <>
                <MarketSection data={resultData} />
                <CompetitorSection data={resultData} />
              </>
            )}

            {(activeTab === 'all' || activeTab === 'personas') && (
              <>
                <PersonaSection data={resultData} />
                <PricingSection data={resultData} />
              </>
            )}

            {(activeTab === 'all' || activeTab === 'mvp') && (
              <MVPSection data={resultData} />
            )}

            {(activeTab === 'all' || activeTab === 'evaluation') && (
              <>
                <EvaluationSection data={resultData} />
                <SourcesSection data={resultData} />
              </>
            )}

            {/* Bottom Actions Bar */}
            <div className="pt-8 border-t border-zinc-900 flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-xs text-zinc-500">
              <div>Validation Report Generated • Startup Validator AI</div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={scrollToTop}
                  className="bg-zinc-900 hover:bg-zinc-800 text-zinc-300 px-3 py-1.5 rounded border border-zinc-800 transition flex items-center gap-1 cursor-pointer"
                >
                  <ArrowUp className="w-3.5 h-3.5" /> Back to top
                </button>
                <button
                  onClick={handleReset}
                  className="bg-white hover:bg-zinc-200 text-black font-bold px-3 py-1.5 rounded border border-white transition cursor-pointer"
                >
                  Validate Another Concept
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-900 bg-black text-center py-6 text-xs text-zinc-400 font-mono">
        Startup Validator AI • Autonomous Multi-Agent Idea Benchmarking Engine
      </footer>
    </div>
  );
}
