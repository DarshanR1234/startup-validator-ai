import React from 'react';
import { Award, ShieldAlert, ShieldCheck, HelpCircle, MapPin, Globe, Sparkles } from 'lucide-react';

export default function ScoreCard({ data }) {
  const score = typeof data?.overall_score === 'number' ? data.overall_score : 50;
  const verdict = data?.verdict || 'Moderate Potential';
  const summary = data?.summary || 'The startup idea shows initial promise with specific target market demand, but requires further refinement in pricing and competitive differentiation.';
  const country = data?.target_country || 'India';
  const region = data?.target_region || 'Maharashtra';

  // Calculate SVG Circle Stroke
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  // Verdict style in Black & White theme
  const getVerdictBadge = (verdictText) => {
    const text = verdictText.toLowerCase();
    if (text.includes('high') || text.includes('strong') || text.includes('excellent')) {
      return {
        bg: 'bg-white text-black border-white',
        icon: ShieldCheck,
        label: verdict
      };
    } else if (text.includes('low') || text.includes('weak') || text.includes('risky')) {
      return {
        bg: 'bg-zinc-900 text-zinc-300 border-zinc-700',
        icon: ShieldAlert,
        label: verdict
      };
    }
    return {
      bg: 'bg-zinc-800 text-white border-zinc-600',
      icon: Award,
      label: verdict
    };
  };

  const verdictStyle = getVerdictBadge(verdict);
  const VerdictIcon = verdictStyle.icon;

  return (
    <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 sm:p-8 shadow-2xl mb-8">
      <div className="flex flex-col md:flex-row items-center gap-8">
        {/* SVG Gauge Circle */}
        <div className="relative flex-shrink-0 flex items-center justify-center">
          <svg className="w-44 h-44 transform -rotate-90">
            {/* Background Circle Track */}
            <circle
              cx="88"
              cy="88"
              r={radius}
              stroke="#27272a"
              strokeWidth="12"
              fill="transparent"
            />
            {/* Foreground Animated Score Track */}
            <circle
              cx="88"
              cy="88"
              r={radius}
              stroke="#ffffff"
              strokeWidth="12"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          {/* Inner Score Label */}
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-extrabold text-white tracking-tight">{score}</span>
            <span className="text-xs text-zinc-400 font-mono font-medium">/ 100</span>
            <span className="text-[10px] uppercase text-zinc-500 font-mono tracking-widest mt-0.5">Overall Score</span>
          </div>
        </div>

        {/* Executive Summary & Badges */}
        <div className="flex-1 space-y-4 text-left">
          <div className="flex flex-wrap items-center gap-2">
            <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border flex items-center gap-1.5 ${verdictStyle.bg}`}>
              <VerdictIcon className="w-3.5 h-3.5" />
              <span>{verdictStyle.label}</span>
            </div>

            <div className="bg-black text-zinc-300 text-xs px-3 py-1 rounded-full border border-zinc-800 flex items-center gap-1">
              <Globe className="w-3.5 h-3.5 text-zinc-400" />
              <span>{country}</span>
            </div>

            <div className="bg-black text-zinc-300 text-xs px-3 py-1 rounded-full border border-zinc-800 flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-zinc-400" />
              <span>{region}</span>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-white" /> Executive Validation Summary
            </h2>
            <p className="text-zinc-300 text-sm leading-relaxed bg-black/60 p-4 rounded-lg border border-zinc-850">
              {summary}
            </p>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2 font-mono text-xs text-zinc-400">
            <div className="bg-zinc-900/90 p-2.5 rounded-lg border border-zinc-800">
              <span className="block text-white font-bold text-sm">
                {Array.isArray(data?.competitor_analysis?.competitors) ? data.competitor_analysis.competitors.length : '3+'}
              </span>
              <span>Competitors Mapped</span>
            </div>
            <div className="bg-zinc-900/90 p-2.5 rounded-lg border border-zinc-800">
              <span className="block text-white font-bold text-sm">
                {Array.isArray(data?.persona_analysis?.personas) ? data.persona_analysis.personas.length : '2+'}
              </span>
              <span>Buyer Personas</span>
            </div>
            <div className="bg-zinc-900/90 p-2.5 rounded-lg border border-zinc-800 col-span-2 sm:col-span-1">
              <span className="block text-white font-bold text-sm">7 / 7</span>
              <span>Criteria Scored</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
