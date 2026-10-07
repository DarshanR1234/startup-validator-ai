import React, { useState, useEffect } from 'react';
import { Cpu, Search, Users, DollarSign, Target, Sparkles, CheckCircle2 } from 'lucide-react';

const MESSAGES = [
  { text: "Analyzing startup idea structure...", icon: Sparkles },
  { text: "Researching market demand & trends...", icon: Search },
  { text: "Analyzing competitors & market gaps...", icon: Target },
  { text: "Building customer buyer personas...", icon: Users },
  { text: "Evaluating pricing models & unit economics...", icon: DollarSign },
  { text: "Scoping MVP features & technical feasibility...", icon: Cpu },
  { text: "Generating 7-point evaluation breakdown...", icon: CheckCircle2 }
];

export default function LoadingState() {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % MESSAGES.length);
    }, 2800);
    return () => clearInterval(timer);
  }, []);

  const CurrentIcon = MESSAGES[currentIndex].icon;

  return (
    <div className="max-w-2xl mx-auto py-20 px-4 text-center">
      {/* Outer Glow & Animated Radar Ring */}
      <div className="relative w-28 h-28 mx-auto mb-8 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border border-zinc-700 animate-ping opacity-25" />
        <div className="absolute inset-2 rounded-full border border-zinc-800 animate-pulse-ring" />
        <div className="w-20 h-20 bg-zinc-950 rounded-full border border-zinc-700 flex items-center justify-center shadow-2xl relative z-10">
          <CurrentIcon className="w-9 h-9 text-white animate-bounce" />
        </div>
      </div>

      {/* Dynamic Status Text */}
      <h2 className="text-xl sm:text-2xl font-bold text-white mb-2 min-h-[2.5rem] flex items-center justify-center transition-all duration-300">
        {MESSAGES[currentIndex].text}
      </h2>

      <p className="text-zinc-400 text-sm max-w-md mx-auto mb-8 font-mono">
        Connecting with FastAPI backend engine & multi-agent reasoning pipelines...
      </p>

      {/* Progress Steps Indicators */}
      <div className="flex items-center justify-center space-x-2">
        {MESSAGES.map((msg, idx) => (
          <div
            key={idx}
            className={`h-1.5 rounded-full transition-all duration-500 ${
              idx === currentIndex
                ? 'w-8 bg-white'
                : idx < currentIndex
                ? 'w-3 bg-zinc-600'
                : 'w-2 bg-zinc-800'
            }`}
          />
        ))}
      </div>

      <div className="mt-10 p-4 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-400 max-w-lg mx-auto font-mono">
        <span className="text-white font-bold">INFO:</span> Real AI deep analysis in progress. Please do not close or refresh this tab.
      </div>
    </div>
  );
}
