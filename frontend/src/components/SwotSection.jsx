import React from 'react';
import { ShieldCheck, AlertTriangle, TrendingUp, ShieldAlert, CheckCircle2, XCircle } from 'lucide-react';

export default function SwotSection({ data }) {
  const strengths = Array.isArray(data?.key_strengths) ? data.key_strengths : [];
  const weaknesses = Array.isArray(data?.key_weaknesses) ? data.key_weaknesses : [];
  const opportunities = Array.isArray(data?.opportunities) ? data.opportunities : [];
  const threats = Array.isArray(data?.threats) ? data.threats : [];

  const cards = [
    {
      title: "Key Strengths",
      items: strengths,
      icon: ShieldCheck,
      badgeText: "Internal Drivers",
      border: "border-zinc-700",
      accentBg: "bg-zinc-900"
    },
    {
      title: "Key Weaknesses",
      items: weaknesses,
      icon: AlertTriangle,
      badgeText: "Internal Limitations",
      border: "border-zinc-800",
      accentBg: "bg-zinc-950"
    },
    {
      title: "Market Opportunities",
      items: opportunities,
      icon: TrendingUp,
      badgeText: "External Catalysts",
      border: "border-zinc-700",
      accentBg: "bg-zinc-900"
    },
    {
      title: "Threats & Risks",
      items: threats,
      icon: ShieldAlert,
      badgeText: "External Obstacles",
      border: "border-zinc-800",
      accentBg: "bg-zinc-950"
    }
  ];

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          SWOT Analysis Matrix
        </h2>
        <span className="text-xs text-zinc-500 font-mono">4-Quadrant Evaluation</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards.map((card, idx) => {
          const CardIcon = card.icon;
          return (
            <div
              key={idx}
              className={`bg-zinc-950 border ${card.border} rounded-xl p-5 shadow-lg flex flex-col justify-between hover:border-zinc-600 transition`}
            >
              <div>
                <div className="flex items-center justify-between mb-3 border-b border-zinc-850 pb-3">
                  <div className="flex items-center space-x-2.5">
                    <div className="w-8 h-8 rounded-lg bg-black border border-zinc-700 flex items-center justify-center">
                      <CardIcon className="w-4 h-4 text-white" />
                    </div>
                    <h3 className="font-bold text-white text-base">{card.title}</h3>
                  </div>
                  <span className="text-[10px] font-mono uppercase bg-zinc-900 text-zinc-400 border border-zinc-800 px-2 py-0.5 rounded">
                    {card.badgeText}
                  </span>
                </div>

                {card.items.length > 0 ? (
                  <ul className="space-y-2.5 text-sm text-zinc-300">
                    {card.items.map((item, i) => (
                      <li key={i} className="flex items-start space-x-2.5">
                        <span className="text-white mt-1 text-xs">•</span>
                        <span className="leading-snug">{item}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-zinc-500 italic py-2 font-mono">No items specified.</p>
                )}
              </div>

              <div className="mt-4 pt-2 border-t border-zinc-900 text-[11px] text-zinc-500 font-mono text-right">
                {card.items.length} Factors Identified
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
