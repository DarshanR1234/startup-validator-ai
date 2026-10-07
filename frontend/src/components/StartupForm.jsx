import React, { useState } from 'react';
import { ArrowRight, Sparkles, MapPin, Globe, Lightbulb, Zap, HelpCircle } from 'lucide-react';

const PRESET_IDEAS = [
  {
    title: "Healthy Meal Delivery (Pune)",
    idea: "A subscription-based healthy meal delivery service for working professionals in Pune that provides affordable calorie-controlled home-style meals.",
    country: "India",
    region: "Maharashtra"
  },
  {
    title: "AI Code Auditor for Startups",
    idea: "An automated security and compliance audit tool for fast-growing SaaS startups that scans pull requests and generates SOC2 compliance evidence in real-time.",
    country: "India",
    region: "Karnataka"
  },
  {
    title: "Solar Installer CRM & Logistics",
    idea: "A vertical B2B SaaS platform specifically built for residential solar installations in Tier-2 Indian cities to manage site surveys, inventory, and government subsidy filings.",
    country: "India",
    region: "Gujarat"
  }
];

export default function StartupForm({ onSubmit, isLoading }) {
  const [startupIdea, setStartupIdea] = useState(
    'A subscription-based healthy meal delivery service for working professionals in Pune that provides affordable calorie-controlled home-style meals.'
  );
  const [targetCountry, setTargetCountry] = useState('India');
  const [targetRegion, setTargetRegion] = useState('Maharashtra');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!startupIdea.trim()) return;
    onSubmit({
      startup_idea: startupIdea,
      target_country: targetCountry,
      target_region: targetRegion,
    });
  };

  const applyPreset = (preset) => {
    setStartupIdea(preset.idea);
    setTargetCountry(preset.country);
    setTargetRegion(preset.region);
  };

  return (
    <div className="max-w-4xl mx-auto py-8 sm:py-12 px-4 sm:px-6">
      {/* Hero Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 text-xs font-mono mb-4">
          <Sparkles className="w-3.5 h-3.5 text-white" />
          <span>AI-Powered Startup Analysis Engine</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mb-4">
          Validate Your Startup Idea
        </h1>
        <p className="text-zinc-400 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
          Comprehensive real-time analysis evaluating market demand, competition, customer personas, pricing strategy, MVP scoping, and overall business potential.
        </p>
      </div>

      {/* Preset Suggestions */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
            <Lightbulb className="w-3.5 h-3.5 text-white" /> Quick Preset Examples
          </span>
          <span className="text-xs text-zinc-500">Click to auto-fill</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
          {PRESET_IDEAS.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => applyPreset(preset)}
              className="text-left px-3.5 py-2.5 bg-zinc-950 hover:bg-zinc-900 border border-zinc-800 hover:border-zinc-700 rounded-lg transition text-xs text-zinc-300 hover:text-white"
            >
              <div className="font-semibold text-white mb-0.5">{preset.title}</div>
              <div className="text-zinc-500 truncate">{preset.region}, {preset.country}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Main Form Card */}
      <form onSubmit={handleSubmit} className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 sm:p-8 shadow-2xl space-y-6">
        {/* Startup Idea Input */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label htmlFor="startupIdea" className="block text-sm font-medium text-zinc-200">
              Startup Concept / Value Proposition <span className="text-white font-bold">*</span>
            </label>
            <span className="text-xs text-zinc-500 font-mono">
              {startupIdea.length} chars
            </span>
          </div>
          <textarea
            id="startupIdea"
            rows={5}
            value={startupIdea}
            onChange={(e) => setStartupIdea(e.target.value)}
            placeholder="Describe your startup concept, target audience, core problem, unique solution, and monetization model in detail..."
            required
            className="w-full bg-black border border-zinc-800 focus:border-white focus:ring-1 focus:ring-white rounded-lg p-3.5 text-white placeholder-zinc-600 text-sm leading-relaxed outline-none transition"
          />
          <p className="mt-1.5 text-xs text-zinc-500">
            Tip: Be as specific as possible regarding your target customer, product offering, and geographic region for higher accuracy.
          </p>
        </div>

        {/* Location Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label htmlFor="targetCountry" className="block text-sm font-medium text-zinc-200 mb-1.5 flex items-center gap-1.5">
              <Globe className="w-4 h-4 text-zinc-400" /> Target Country
            </label>
            <select
              id="targetCountry"
              value={targetCountry}
              onChange={(e) => setTargetCountry(e.target.value)}
              className="w-full bg-black border border-zinc-800 focus:border-white focus:ring-1 focus:ring-white rounded-lg px-3.5 py-2.5 text-white text-sm outline-none transition"
            >
              <option value="India">India</option>
              <option value="United States">United States</option>
              <option value="United Kingdom">United Kingdom</option>
              <option value="Singapore">Singapore</option>
              <option value="United Arab Emirates">United Arab Emirates</option>
              <option value="Germany">Germany</option>
              <option value="Canada">Canada</option>
              <option value="Global">Global</option>
            </select>
          </div>

          <div>
            <label htmlFor="targetRegion" className="block text-sm font-medium text-zinc-200 mb-1.5 flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-zinc-400" /> Target Region / State / City
            </label>
            <input
              type="text"
              id="targetRegion"
              value={targetRegion}
              onChange={(e) => setTargetRegion(e.target.value)}
              placeholder="e.g. Maharashtra, Pune, California, London"
              required
              className="w-full bg-black border border-zinc-800 focus:border-white focus:ring-1 focus:ring-white rounded-lg px-3.5 py-2.5 text-white text-sm outline-none transition"
            />
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !startupIdea.trim()}
          className="w-full bg-white hover:bg-zinc-200 disabled:bg-zinc-800 disabled:text-zinc-500 text-black font-semibold py-3.5 px-6 rounded-lg transition duration-200 flex items-center justify-center space-x-2 shadow-lg group cursor-pointer disabled:cursor-not-allowed"
        >
          <Zap className="w-4 h-4 text-black group-hover:scale-110 transition" />
          <span className="text-base">Validate Startup Idea</span>
          <ArrowRight className="w-4 h-4 text-black group-hover:translate-x-1 transition" />
        </button>

        {/* Features Checklist footer */}
        <div className="pt-2 border-t border-zinc-900 grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs text-zinc-500 font-mono">
          <div>✓ SWOT Breakdown</div>
          <div>✓ Competitor Matrix</div>
          <div>✓ Buyer Personas</div>
          <div>✓ MVP Roadmap</div>
        </div>
      </form>
    </div>
  );
}
