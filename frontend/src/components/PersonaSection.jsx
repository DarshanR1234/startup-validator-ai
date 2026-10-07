import React from 'react';
import { UserCheck, Target, AlertCircle, HeartHandshake, DollarSign, Briefcase } from 'lucide-react';

export default function PersonaSection({ data }) {
  const pa = data?.persona_analysis || {};
  const personas = Array.isArray(pa.personas) ? pa.personas : [];

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <UserCheck className="w-6 h-6 text-white" /> Target Customer Buyer Personas
        </h2>
        <span className="text-xs text-zinc-500 font-mono">User Profiling</span>
      </div>

      {personas.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {personas.map((persona, idx) => {
            const name = persona.name || `Persona ${idx + 1}`;
            const role = persona.role || 'Target User';
            const businessType = persona.business_type || 'B2C / B2B';
            const goals = Array.isArray(persona.goals) ? persona.goals : [];
            const painPoints = Array.isArray(persona.pain_points) ? persona.pain_points : [];
            const needs = Array.isArray(persona.needs) ? persona.needs : [];
            const willingnessToPay = persona.willingness_to_pay || 'Moderate to High';

            return (
              <div
                key={idx}
                className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 shadow-xl flex flex-col justify-between hover:border-zinc-700 transition"
              >
                <div>
                  {/* Persona Header */}
                  <div className="flex items-start justify-between border-b border-zinc-850 pb-4 mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-full bg-black border border-zinc-700 flex items-center justify-center font-extrabold text-white text-base font-mono">
                        {name.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h3 className="font-bold text-white text-lg tracking-tight">{name}</h3>
                        <p className="text-xs text-zinc-400 font-mono flex items-center gap-1">
                          <Briefcase className="w-3 h-3 text-zinc-400" /> {role}
                        </p>
                      </div>
                    </div>
                    <span className="bg-zinc-900 border border-zinc-700 text-zinc-300 text-xs px-2.5 py-1 rounded font-mono">
                      {businessType}
                    </span>
                  </div>

                  {/* Goals */}
                  <div className="mb-4">
                    <span className="text-xs font-mono uppercase text-zinc-400 tracking-wider block mb-1.5 flex items-center gap-1">
                      <Target className="w-3.5 h-3.5 text-white" /> Primary Goals
                    </span>
                    <ul className="space-y-1 text-xs text-zinc-300">
                      {goals.map((g, gIdx) => (
                        <li key={gIdx} className="flex items-start space-x-2">
                          <span className="text-white">•</span>
                          <span>{g}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Pain Points */}
                  <div className="mb-4">
                    <span className="text-xs font-mono uppercase text-zinc-400 tracking-wider block mb-1.5 flex items-center gap-1">
                      <AlertCircle className="w-3.5 h-3.5 text-white" /> Pain Points
                    </span>
                    <ul className="space-y-1 text-xs text-zinc-300">
                      {painPoints.map((p, pIdx) => (
                        <li key={pIdx} className="flex items-start space-x-2">
                          <span className="text-white font-bold">!</span>
                          <span>{p}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Needs */}
                  {needs.length > 0 && (
                    <div className="mb-4">
                      <span className="text-xs font-mono uppercase text-zinc-400 tracking-wider block mb-1.5 flex items-center gap-1">
                        <HeartHandshake className="w-3.5 h-3.5 text-white" /> Core Needs
                      </span>
                      <ul className="space-y-1 text-xs text-zinc-300">
                        {needs.map((n, nIdx) => (
                          <li key={nIdx} className="flex items-start space-x-2">
                            <span className="text-white">✓</span>
                            <span>{n}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Willingness to Pay Footer */}
                <div className="mt-4 pt-3 border-t border-zinc-900 flex items-center justify-between bg-black p-3 rounded-lg border border-zinc-900">
                  <span className="text-xs text-zinc-400 font-mono flex items-center gap-1">
                    <DollarSign className="w-3.5 h-3.5 text-white" /> Willingness to Pay
                  </span>
                  <span className="text-xs font-bold text-white bg-zinc-900 border border-zinc-700 px-2.5 py-0.5 rounded font-mono">
                    {willingnessToPay}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-zinc-950 p-6 rounded-xl border border-zinc-800 text-center text-zinc-400 text-sm font-mono">
          No personas generated.
        </div>
      )}
    </div>
  );
}
