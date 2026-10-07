import React from 'react';
import { AlertTriangle, RefreshCw, Terminal } from 'lucide-react';

export default function ErrorState({ error, onRetry }) {
  return (
    <div className="max-w-xl mx-auto py-16 px-4 text-center">
      <div className="bg-zinc-950 border border-zinc-700 rounded-xl p-8 shadow-2xl space-y-6">
        <div className="w-16 h-16 bg-black border border-zinc-600 rounded-full flex items-center justify-center mx-auto text-white">
          <AlertTriangle className="w-8 h-8 text-white" />
        </div>

        <div>
          <h2 className="text-2xl font-bold text-white mb-2 tracking-tight">Validation Failed</h2>
          <p className="text-zinc-400 text-sm leading-relaxed max-w-md mx-auto">
            We encountered an error while communicating with the AI validation engine.
          </p>
        </div>

        <div className="bg-black p-4 rounded-lg border border-zinc-800 text-left font-mono text-xs text-zinc-300 overflow-x-auto">
          <span className="text-white font-bold block mb-1">ERROR DETAIL:</span>
          {error?.message || 'Failed to connect to http://127.0.0.1:8000/api/validate-startup'}
        </div>

        <div className="pt-2 text-xs text-zinc-500 font-mono text-left space-y-1">
          <div>• Ensure FastAPI backend server is running on <code className="text-zinc-300">http://127.0.0.1:8000</code></div>
          <div>• Check network connectivity and CORS headers</div>
        </div>

        <button
          onClick={onRetry}
          className="w-full bg-white hover:bg-zinc-200 text-black font-semibold py-3 px-6 rounded-lg transition duration-150 flex items-center justify-center space-x-2 cursor-pointer shadow"
        >
          <RefreshCw className="w-4 h-4 text-black" />
          <span>Try Validation Again</span>
        </button>
      </div>
    </div>
  );
}
