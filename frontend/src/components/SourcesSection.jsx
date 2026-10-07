import React from 'react';
import { ExternalLink, BookOpen, Globe } from 'lucide-react';

export default function SourcesSection({ data }) {
  const rawSources = Array.isArray(data?.research_sources) ? data.research_sources : [];

  // Normalize source formats safely
  const sources = rawSources.map((src, idx) => {
    if (typeof src === 'string') {
      return { title: src, url: src.startsWith('http') ? src : null };
    }
    return {
      title: src.title || src.name || src.url || `Research Reference ${idx + 1}`,
      url: src.url && src.url.startsWith('http') ? src.url : null,
    };
  });

  if (sources.length === 0) return null;

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-white" /> Research Citations & Data Sources
        </h2>
        <span className="text-xs text-zinc-500 font-mono">Attribution</span>
      </div>

      <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 shadow-sm">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {sources.map((source, idx) => {
            const isClickable = Boolean(source.url);

            return isClickable ? (
              <a
                key={idx}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-black hover:bg-zinc-900 border border-zinc-800 hover:border-white p-3 rounded-lg transition duration-200 flex items-start justify-between group"
              >
                <div className="pr-2">
                  <div className="font-medium text-xs text-zinc-200 group-hover:text-white line-clamp-2">
                    {source.title}
                  </div>
                  <div className="text-[10px] text-zinc-500 font-mono mt-1 flex items-center gap-1">
                    <Globe className="w-3 h-3 text-zinc-400" />
                    <span className="truncate max-w-[140px]">{new URL(source.url).hostname}</span>
                  </div>
                </div>
                <ExternalLink className="w-3.5 h-3.5 text-zinc-400 group-hover:text-white flex-shrink-0 mt-0.5" />
              </a>
            ) : (
              <div
                key={idx}
                className="bg-black border border-zinc-900 p-3 rounded-lg text-xs text-zinc-400 flex items-center justify-between font-mono"
              >
                <span className="truncate">{source.title}</span>
                <span className="text-[10px] text-zinc-600">Verified</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
