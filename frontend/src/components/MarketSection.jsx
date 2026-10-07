import React from 'react';
import {
  LineChart,
  Target,
  Zap,
  AlertCircle,
  ArrowUpRight,
  FileText,
  Compass,
} from 'lucide-react';

export default function MarketSection({ data }) {
  const mr = data?.market_research || {};

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
      return value.map(safeText).filter(Boolean).join(', ');
    }

    if (typeof value === 'object') {
      const claim = value.claim ? String(value.claim) : '';
      const source = value.source ? String(value.source) : '';

      if (claim && source) {
        return `${claim} — Source: ${source}`;
      }

      if (claim) return claim;
      if (source) return `Source: ${source}`;

      return Object.values(value)
        .map(safeText)
        .filter(Boolean)
        .join(' — ');
    }

    return String(value);
  };

  const asArray = (value) => {
    if (Array.isArray(value)) return value;
    if (value !== null && value !== undefined && value !== '') {
      return [value];
    }
    return [];
  };

  const marketDemand = safeText(
    mr.market_demand || 'No market demand information available.'
  );

  const targetMarket = safeText(
    mr.target_market || 'No target market information available.'
  );

  const industryTrends = asArray(mr.industry_trends);
  const growthDrivers = asArray(mr.growth_drivers);
  const customerProblems = asArray(mr.customer_problems);
  const opportunities = asArray(mr.opportunities);
  const evidence = asArray(mr.evidence);

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <LineChart className="w-6 h-6 text-white" />
          Market Research & Industry Demand
        </h2>
        <span className="text-xs text-zinc-500 font-mono">
          Market Dynamics
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-2 text-white font-semibold text-sm">
            <Compass className="w-4 h-4" />
            <span>Market Demand Analysis</span>
          </div>
          <p className="text-sm text-zinc-300 leading-relaxed bg-black p-3.5 rounded-lg border border-zinc-900">
            {marketDemand}
          </p>
        </div>

        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-2 text-white font-semibold text-sm">
            <Target className="w-4 h-4" />
            <span>Target Market Scoping</span>
          </div>
          <p className="text-sm text-zinc-300 leading-relaxed bg-black p-3.5 rounded-lg border border-zinc-900">
            {targetMarket}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-3 flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Industry Trends
          </h3>

          {industryTrends.length > 0 ? (
            <ul className="space-y-2 text-sm text-zinc-300">
              {industryTrends.map((item, index) => (
                <li
                  key={index}
                  className="flex gap-2 bg-black/60 p-2.5 rounded border border-zinc-900"
                >
                  <span className="text-white">•</span>
                  <span>{safeText(item)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500">
              No industry trends listed.
            </p>
          )}
        </div>

        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-3 flex items-center gap-2">
            <ArrowUpRight className="w-4 h-4" />
            Growth Drivers
          </h3>

          {growthDrivers.length > 0 ? (
            <ul className="space-y-2 text-sm text-zinc-300">
              {growthDrivers.map((item, index) => (
                <li
                  key={index}
                  className="flex gap-2 bg-black/60 p-2.5 rounded border border-zinc-900"
                >
                  <span className="text-white">•</span>
                  <span>{safeText(item)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500">
              No growth drivers listed.
            </p>
          )}
        </div>

        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-3 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            Core Customer Problems
          </h3>

          {customerProblems.length > 0 ? (
            <ul className="space-y-2 text-sm text-zinc-300">
              {customerProblems.map((item, index) => (
                <li
                  key={index}
                  className="flex gap-2 bg-black/60 p-2.5 rounded border border-zinc-900"
                >
                  <span className="text-white font-bold">!</span>
                  <span>{safeText(item)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500">
              No core problems specified.
            </p>
          )}
        </div>

        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-3 flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Market Opportunities & Evidence
          </h3>

          {opportunities.length > 0 && (
            <div className="mb-4">
              <span className="text-xs font-mono text-zinc-400 block mb-2">
                Key Opportunities:
              </span>

              <ul className="space-y-2 text-xs text-zinc-300">
                {opportunities.map((item, index) => (
                  <li key={index} className="flex gap-2">
                    <span className="text-white">•</span>
                    <span>{safeText(item)}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {evidence.length > 0 && (
            <div className="bg-black p-3 rounded border border-zinc-900 text-xs text-zinc-400 font-mono">
              <span className="text-white font-bold block mb-2">
                Market Evidence Data:
              </span>

              {evidence.map((item, index) => (
                <p key={index} className="mb-2 text-zinc-300">
                  "{safeText(item)}"
                </p>
              ))}
            </div>
          )}

          {opportunities.length === 0 && evidence.length === 0 && (
            <p className="text-xs text-zinc-500 italic">
              No additional market opportunities or evidence available.
            </p>
          )}
        </div>

      </div>
    </div>
  );
}
