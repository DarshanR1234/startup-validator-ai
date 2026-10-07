import React from 'react';
import { Sparkles, Terminal, Cpu } from 'lucide-react';

export default function Header({ onReset, hasResults }) {
  return (
    <header className="sticky top-0 z-50 bg-black/90 backdrop-blur-md border-b border-zinc-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={hasResults ? onReset : undefined}>
          <div className="w-9 h-9 rounded-lg bg-zinc-900 border border-zinc-700 flex items-center justify-center text-white shadow-inner">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight">Startup Validator</span>
              <span className="bg-zinc-800 text-zinc-300 text-xs px-2 py-0.5 rounded font-mono border border-zinc-700">AI</span>
            </div>
            <p className="text-xs text-zinc-400 hidden sm:block font-mono">Market • Competition • Pricing • MVP Analysis</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="hidden md:flex items-center space-x-2 bg-zinc-900/80 px-3 py-1.5 rounded-full border border-zinc-800 text-xs text-zinc-300">
            <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
            <span>FastAPI Engine Online</span>
          </div>

          {hasResults && (
            <button
              onClick={onReset}
              className="bg-white hover:bg-zinc-200 text-black font-medium text-xs sm:text-sm px-3.5 py-1.5 rounded-md border border-white transition duration-150 flex items-center space-x-1.5 shadow-sm"
            >
              <Terminal className="w-4 h-4" />
              <span>Validate Another</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
