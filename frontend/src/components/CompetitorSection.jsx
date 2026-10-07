import React from 'react';
import { Users, ShieldAlert, Award, Tag, Check, X, Layers, AlertTriangle } from 'lucide-react';

export default function CompetitorSection({ data }) {
  const ca = data?.competitor_analysis || {};
  const competitors = Array.isArray(ca.competitors) ? ca.competitors : [];
  
  const marketGaps = Array.isArray(ca.market_gaps) 
    ? ca.market_gaps 
    : typeof ca.market_gaps === 'string' ? [ca.market_gaps] : [];

  const competitiveRisks = Array.isArray(ca.competitive_risks) 
    ? ca.competitive_risks 
    : typeof ca.competitive_risks === 'string' ? [ca.competitive_risks] : [];

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Users className="w-6 h-6 text-white" /> Competitor Benchmarking & Matrix
        </h2>
        <span className="text-xs text-zinc-500 font-mono">Market Landscape</span>
      </div>

      {/* Competitors Cards */}
      {competitors.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {competitors.map((comp, idx) => {
            const name = comp.name || `Competitor ${idx + 1}`;
            const product = comp.product || 'N/A';
            const pricing = comp.pricing || 'Custom / Variable';
            const strengths = Array.isArray(comp.strengths) ? comp.strengths : [];
            const weaknesses = Array.isArray(comp.weaknesses) ? comp.weaknesses : [];
            const evidence = comp.evidence || '';

            return (
              <div
                key={idx}
                className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 shadow-md flex flex-col justify-between hover:border-zinc-700 transition"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-bold text-white text-base tracking-tight">{name}</h3>
                    <span className="bg-black border border-zinc-800 text-zinc-300 text-xs px-2 py-0.5 rounded font-mono">
                      {pricing}
                    </span>
                  </div>

                  <p className="text-xs text-zinc-400 mb-4 line-clamp-2">
                    <span className="text-zinc-500 font-mono">Product:</span> {product}
                  </p>

                  {/* Strengths */}
                  <div className="mb-3">
                    <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider block mb-1.5 flex items-center gap-1">
                      <Check className="w-3 h-3 text-white" /> Strengths
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {strengths.length > 0 ? (
                        strengths.map((str, sIdx) => (
                          <span
                            key={sIdx}
                            className="bg-zinc-900 text-zinc-300 border border-zinc-800 text-[11px] px-2 py-0.5 rounded"
                          >
                            {str}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-zinc-600 italic">None specified</span>
                      )}
                    </div>
                  </div>

                  {/* Weaknesses */}
                  <div className="mb-3">
                    <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider block mb-1.5 flex items-center gap-1">
                      <X className="w-3 h-3 text-zinc-500" /> Weaknesses
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {weaknesses.length > 0 ? (
                        weaknesses.map((wk, wIdx) => (
                          <span
                            key={wIdx}
                            className="bg-black text-zinc-400 border border-zinc-850 text-[11px] px-2 py-0.5 rounded"
                          >
                            {wk}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-zinc-600 italic">None specified</span>
                      )}
                    </div>
                  </div>
                </div>

                {evidence && (
                  <div className="mt-3 pt-2.5 border-t border-zinc-900 text-[11px] text-zinc-400 italic">
                    "{evidence}"
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-zinc-950 p-6 rounded-xl border border-zinc-800 text-center text-zinc-400 text-sm mb-6 font-mono">
          No explicit direct competitors identified in this niche. First-mover advantage potential high.
        </div>
      )}

      {/* Market Gaps & Competitive Risks */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-zinc-950 border border-zinc-850 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-3 flex items-center space-x-2">
            <Layers className="w-4 h-4 text-white" />
            <span>Unserved Market Gaps</span>
          </h3>
          {marketGaps.length > 0 ? (
            <ul className="space-y-2 text-sm text-zinc-300">
              {marketGaps.map((gap, i) => (
                <li key={i} className="flex items-start space-x-2 bg-black p-2.5 rounded border border-zinc-900">
                  <span className="text-white text-xs mt-0.5">•</span>
                  <span>{gap}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500 italic">No market gaps listed.</p>
          )}
        </div>

        <div className="bg-zinc-950 border border-zinc-850 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-3 flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-white" />
            <span>Competitive Risks</span>
          </h3>
          {competitiveRisks.length > 0 ? (
            <ul className="space-y-2 text-sm text-zinc-300">
              {competitiveRisks.map((risk, i) => (
                <li key={i} className="flex items-start space-x-2 bg-black p-2.5 rounded border border-zinc-900">
                  <span className="text-white font-bold text-xs mt-0.5">!</span>
                  <span>{risk}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500 italic">No competitive risks specified.</p>
          )}
        </div>
      </div>
    </div>
  );
}
