import React from 'react';
import { DollarSign, Check, AlertOctagon, HelpCircle, Sparkles, Layers } from 'lucide-react';

export default function PricingSection({ data }) {
  const pa = data?.pricing_analysis || {};

  const pricingModel = pa.pricing_model || 'Subscription / Tiered SaaS';
  const recommendedPrice = pa.recommended_price || '₹499 - ₹1,999 / month';
  const pricingTiers = Array.isArray(pa.pricing_tiers) ? pa.pricing_tiers : [];
  const pricingRationale = pa.pricing_rationale || 'Monetization reflects regional purchasing power and value proposition.';
  
  const pricingRisks = Array.isArray(pa.pricing_risks) 
    ? pa.pricing_risks 
    : typeof pa.pricing_risks === 'string' ? [pa.pricing_risks] : [];

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <DollarSign className="w-6 h-6 text-white" /> Monetization & Pricing Strategy
        </h2>
        <span className="text-xs text-zinc-500 font-mono">Unit Economics</span>
      </div>

      {/* Hero Overview Box */}
      <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 shadow-xl mb-6 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        <div>
          <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider block mb-1">Recommended Pricing Model</span>
          <h3 className="text-2xl font-extrabold text-white tracking-tight">{pricingModel}</h3>
          <p className="text-xs text-zinc-400 mt-1 font-mono">Optimized for target market willingness to pay</p>
        </div>

        <div className="bg-black border border-zinc-700 p-4 rounded-xl text-center">
          <span className="text-xs text-zinc-400 font-mono uppercase tracking-wider block mb-1">Recommended Starting Price</span>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">{recommendedPrice}</div>
        </div>
      </div>

      {/* Pricing Tiers Grid */}
      {pricingTiers.length > 0 && (
        <div className="mb-6">
          <h3 className="font-bold text-white text-base mb-3 flex items-center gap-2">
            <Layers className="w-4 h-4 text-white" /> Recommended Pricing Tiers
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {pricingTiers.map((tier, idx) => {
              const name = tier.name || `Tier ${idx + 1}`;
              const price = tier.price || 'Contact Sales';
              const targetAudience = tier.target_audience || 'General Users';
              const features = Array.isArray(tier.features) ? tier.features : [];
              const isPopular = idx === 1;

              return (
                <div
                  key={idx}
                  className={`rounded-xl p-5 border flex flex-col justify-between transition ${
                    isPopular
                      ? 'bg-zinc-900 border-white shadow-2xl relative'
                      : 'bg-zinc-950 border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  {isPopular && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-white text-black font-bold font-mono text-[10px] uppercase px-3 py-0.5 rounded-full border border-white">
                      Recommended Tier
                    </div>
                  )}

                  <div>
                    <div className="mb-3">
                      <h4 className="font-extrabold text-white text-lg">{name}</h4>
                      <p className="text-xs text-zinc-400 font-mono">{targetAudience}</p>
                    </div>

                    <div className="text-2xl font-black text-white font-mono mb-4 border-b border-zinc-800 pb-3">
                      {price}
                    </div>

                    <div className="space-y-2 mb-4 text-xs text-zinc-300">
                      {features.map((feat, fIdx) => (
                        <div key={fIdx} className="flex items-start space-x-2">
                          <Check className="w-3.5 h-3.5 text-white flex-shrink-0 mt-0.5" />
                          <span>{feat}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-3 border-t border-zinc-850 text-center">
                    <span className="text-[11px] font-mono text-zinc-400">Full Access Tier</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Rationale & Risks Callouts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-zinc-950 border border-zinc-850 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-2 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-white" /> Pricing Rationale
          </h3>
          <p className="text-sm text-zinc-300 leading-relaxed bg-black p-3.5 rounded-lg border border-zinc-900">
            {pricingRationale}
          </p>
        </div>

        <div className="bg-zinc-950 border border-zinc-850 rounded-xl p-5">
          <h3 className="font-bold text-white text-sm mb-2 flex items-center gap-2">
            <AlertOctagon className="w-4 h-4 text-white" /> Pricing Risks & Considerations
          </h3>
          {pricingRisks.length > 0 ? (
            <ul className="space-y-2 text-sm text-zinc-300">
              {pricingRisks.map((risk, i) => (
                <li key={i} className="flex items-start space-x-2 bg-black p-2.5 rounded border border-zinc-900">
                  <span className="text-white font-bold text-xs mt-0.5">!</span>
                  <span>{risk}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500 italic">No explicit pricing risks flagged.</p>
          )}
        </div>
      </div>
    </div>
  );
}
