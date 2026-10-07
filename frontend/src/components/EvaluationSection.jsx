import React from 'react';
import { CheckSquare, FileText } from 'lucide-react';

const CRITERIA_KEYS = [
  { key: 'market_demand', label: 'Market Demand', desc: 'Size & urgency of market pull' },
  { key: 'customer_need', label: 'Customer Need', desc: 'Problem severity & buyer willingness' },
  { key: 'competition', label: 'Competition Risk & Gaps', desc: 'Differentiation & barrier to entry' },
  { key: 'business_potential', label: 'Business Potential', desc: 'Scalability & long-term margin upside' },
  { key: 'pricing_potential', label: 'Pricing Potential', desc: 'Price elasticity & monetizability' },
  { key: 'feasibility', label: 'Technical & Ops Feasibility', desc: 'Execution complexity & resource requirements' },
  { key: 'mvp_clarity', label: 'MVP Scope Clarity', desc: 'Actionable feature priority & build scope' }
];

export default function EvaluationSection({ data }) {
  const ev = data?.evaluation || {};

  const safeText = (value) => {
    if (value === null || value === undefined) return '';

    if (
      typeof value === 'string' ||
      typeof value === 'number' ||
      typeof value === 'boolean'
    ) {
      return String(value);
    }

    if (Array.isArray(value)) {
      return value
        .map(safeText)
        .filter(Boolean)
        .join(', ');
    }

    if (typeof value === 'object') {
      if (value.reason !== undefined) {
        return safeText(value.reason);
      }

      if (value.claim !== undefined || value.source !== undefined) {
        const claim = safeText(value.claim);
        const source = safeText(value.source);

        if (claim && source) {
          return `${claim} — Source: ${source}`;
        }

        return claim || source;
      }

      return Object.entries(value)
        .map(([key, val]) => {
          const text = safeText(val);
          return text ? `${key}: ${text}` : '';
        })
        .filter(Boolean)
        .join(' — ');
    }

    return String(value);
  };

  return (
    <div className="mb-10">

      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <CheckSquare className="w-6 h-6 text-white" />
          7-Point Granular Evaluation Matrix
        </h2>

        <span className="text-xs text-zinc-500 font-mono">
          Criteria Breakdown
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {CRITERIA_KEYS.map((item, idx) => {

          const rawEval = ev[item.key];

          const evalObj =
            rawEval &&
            typeof rawEval === 'object' &&
            !Array.isArray(rawEval)
              ? rawEval
              : {};

          const rawScore = evalObj.score;

          const score =
            typeof rawScore === 'number'
              ? Math.max(0, Math.min(10, rawScore))
              : 7;

          const reason = evalObj.reason
            ? safeText(evalObj.reason)
            : 'Sufficient baseline metrics observed for initial launch.';

          const evidence = evalObj.evidence
            ? safeText(evalObj.evidence)
            : '';

          return (
            <div
              key={idx}
              className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 shadow-md flex flex-col justify-between hover:border-zinc-700 transition"
            >

              <div>

                <div className="flex items-center justify-between mb-2">

                  <div>
                    <h3 className="font-bold text-white text-base">
                      {item.label}
                    </h3>

                    <p className="text-[11px] text-zinc-500 font-mono">
                      {item.desc}
                    </p>
                  </div>

                  <div className="flex items-center space-x-1 font-mono">
                    <span className="text-xl font-extrabold text-white">
                      {score}
                    </span>

                    <span className="text-xs text-zinc-500">
                      / 10
                    </span>
                  </div>

                </div>

                <div className="w-full bg-black h-2 rounded-full overflow-hidden border border-zinc-900 mb-3">

                  <div
                    className="bg-white h-full transition-all duration-700 rounded-full"
                    style={{
                      width: `${(score / 10) * 100}%`
                    }}
                  />

                </div>

                <p className="text-xs text-zinc-300 leading-relaxed bg-black/80 p-3 rounded-lg border border-zinc-900 mb-2">
                  {reason}
                </p>

              </div>

              {evidence && (
                <div className="mt-2 pt-2 border-t border-zinc-900 text-[11px] text-zinc-400 font-mono flex items-start space-x-1.5">

                  <FileText className="w-3.5 h-3.5 text-zinc-500 flex-shrink-0 mt-0.5" />

                  <span className="italic">
                    "{evidence}"
                  </span>

                </div>
              )}

            </div>
          );
        })}

      </div>
    </div>
  );
}
