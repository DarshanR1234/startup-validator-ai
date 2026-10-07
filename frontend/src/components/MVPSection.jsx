import React from 'react';
import {
  Cpu,
  CheckCircle2,
  Rocket,
  Ban,
  ListOrdered,
  Sparkles
} from 'lucide-react';

export default function MVPSection({ data }) {
  const mvp = data?.mvp_analysis || {};

  // Safely convert any backend value into React-renderable text.
  const safeText = (value) => {
    if (value === null || value === undefined) {
      return '';
    }

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
      // Handle { reason: "..." }
      if (value.reason !== undefined) {
        return safeText(value.reason);
      }

      // Handle { claim: "...", source: "..." }
      if (
        value.claim !== undefined ||
        value.source !== undefined
      ) {
        const claim = safeText(value.claim);
        const source = safeText(value.source);

        if (claim && source) {
          return `${claim} — Source: ${source}`;
        }

        return claim || source;
      }

      // Generic object fallback.
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

  const coreFeatures = Array.isArray(mvp.core_features)
    ? mvp.core_features
    : [];

  const futureFeatures = Array.isArray(mvp.future_features)
    ? mvp.future_features
    : [];

  const excludedFeatures = Array.isArray(mvp.excluded_features)
    ? mvp.excluded_features
    : [];

  const devPriority = Array.isArray(mvp.development_priority)
    ? mvp.development_priority
    : [];

  const mvpRationale = mvp.mvp_rationale
    ? safeText(mvp.mvp_rationale)
    : 'Focus initial release strictly on high-impact core problem solving to shorten time-to-market.';

  return (
    <div className="mb-10">

      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Cpu className="w-6 h-6 text-white" />
          MVP Scope & Product Roadmap
        </h2>

        <span className="text-xs text-zinc-500 font-mono">
          Build Architecture
        </span>
      </div>

      {/* Rationale */}
      <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 shadow-sm mb-6">

        <h3 className="font-bold text-white text-sm mb-1.5 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-white" />
          MVP Strategic Rationale
        </h3>

        <p className="text-sm text-zinc-300 leading-relaxed bg-black p-3 rounded-lg border border-zinc-900">
          {mvpRationale}
        </p>

      </div>

      {/* Feature Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">

        {/* CORE FEATURES */}
        <div className="bg-zinc-950 border border-zinc-700 rounded-xl p-5 shadow-lg flex flex-col justify-between">

          <div>

            <div className="flex items-center justify-between border-b border-zinc-800 pb-3 mb-3">

              <h3 className="font-extrabold text-white text-base flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-white" />
                Core MVP Features
              </h3>

              <span className="text-[10px] font-mono uppercase bg-white text-black font-bold px-2 py-0.5 rounded">
                v1.0 Scope
              </span>

            </div>

            {coreFeatures.length > 0 ? (
              <ul className="space-y-2.5 text-xs text-zinc-300">

                {coreFeatures.map((feature, i) => (
                  <li
                    key={i}
                    className="flex items-start space-x-2 bg-black p-2.5 rounded border border-zinc-900"
                  >
                    <span className="text-white font-bold">
                      •
                    </span>

                    <span className="leading-snug">
                      {safeText(feature)}
                    </span>
                  </li>
                ))}

              </ul>
            ) : (
              <p className="text-xs text-zinc-500 italic">
                No core features listed.
              </p>
            )}

          </div>

          <div className="mt-4 pt-2 border-t border-zinc-900 text-[11px] text-zinc-500 font-mono text-right">
            {coreFeatures.length} Core Modules
          </div>

        </div>

        {/* FUTURE FEATURES */}
        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 flex flex-col justify-between">

          <div>

            <div className="flex items-center justify-between border-b border-zinc-800 pb-3 mb-3">

              <h3 className="font-extrabold text-white text-base flex items-center gap-2">
                <Rocket className="w-4 h-4 text-zinc-300" />
                Future Expansion
              </h3>

              <span className="text-[10px] font-mono uppercase bg-zinc-900 text-zinc-400 border border-zinc-800 px-2 py-0.5 rounded">
                Post-Launch
              </span>

            </div>

            {futureFeatures.length > 0 ? (
              <ul className="space-y-2.5 text-xs text-zinc-300">

                {futureFeatures.map((feature, i) => (
                  <li
                    key={i}
                    className="flex items-start space-x-2 bg-black/60 p-2.5 rounded border border-zinc-900"
                  >
                    <span className="text-zinc-400">
                      •
                    </span>

                    <span className="leading-snug">
                      {safeText(feature)}
                    </span>
                  </li>
                ))}

              </ul>
            ) : (
              <p className="text-xs text-zinc-500 italic">
                No future features listed.
              </p>
            )}

          </div>

          <div className="mt-4 pt-2 border-t border-zinc-900 text-[11px] text-zinc-500 font-mono text-right">
            {futureFeatures.length} Future Roadmap Items
          </div>

        </div>

        {/* EXCLUDED FEATURES */}
        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 flex flex-col justify-between">

          <div>

            <div className="flex items-center justify-between border-b border-zinc-800 pb-3 mb-3">

              <h3 className="font-extrabold text-white text-base flex items-center gap-2">
                <Ban className="w-4 h-4 text-zinc-500" />
                Excluded Scope
              </h3>

              <span className="text-[10px] font-mono uppercase bg-black text-zinc-500 border border-zinc-800 px-2 py-0.5 rounded">
                Out of Scope
              </span>

            </div>

            {excludedFeatures.length > 0 ? (
              <ul className="space-y-2.5 text-xs text-zinc-400">

                {excludedFeatures.map((feature, i) => (
                  <li
                    key={i}
                    className="flex items-start space-x-2 bg-black/40 p-2.5 rounded border border-zinc-900"
                  >
                    <span className="text-zinc-600">
                      ×
                    </span>

                    <span className="leading-snug">
                      {safeText(feature)}
                    </span>
                  </li>
                ))}

              </ul>
            ) : (
              <p className="text-xs text-zinc-500 italic">
                No features explicitly excluded.
              </p>
            )}

          </div>

          <div className="mt-4 pt-2 border-t border-zinc-900 text-[11px] text-zinc-500 font-mono text-right">
            {excludedFeatures.length} Out-of-scope Items
          </div>

        </div>

      </div>

      {/* DEVELOPMENT PRIORITY */}
      {devPriority.length > 0 && (
        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">

          <h3 className="font-bold text-white text-sm mb-3 flex items-center gap-2">
            <ListOrdered className="w-4 h-4 text-white" />
            Recommended Development Sequence
          </h3>

          <div className="space-y-2">

            {devPriority.map((step, idx) => (
              <div
                key={idx}
                className="flex items-center space-x-3 bg-black p-3 rounded-lg border border-zinc-900 text-xs text-zinc-300 font-mono"
              >

                <span className="bg-white text-black font-extrabold px-2 py-0.5 rounded text-[11px]">
                  P{idx + 1}
                </span>

                <span className="flex-1">
                  {safeText(step)}
                </span>

              </div>
            ))}

          </div>

        </div>
      )}

    </div>
  );
}
