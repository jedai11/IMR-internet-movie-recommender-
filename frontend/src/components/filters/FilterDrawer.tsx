import React from 'react';
import { Filter, AlertTriangle, Clock, Film, Tv, ShieldAlert } from 'lucide-react';
import { FilterCriteria } from '../../types';

interface Props {
  filters: FilterCriteria;
  onChange: (filters: FilterCriteria) => void;
}

const AVAILABLE_GENRES = [
  'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
  'Drama', 'Family', 'Fantasy', 'Horror', 'Music', 'Mystery',
  'Romance', 'Sci-Fi', 'Thriller'
];

const AVAILABLE_WARNINGS = [
  { code: 'self_harm', label: 'Self-Harm / Suicide' },
  { code: 'sexual_violence', label: 'Sexual Violence' },
  { code: 'substance_abuse', label: 'Substance Abuse' },
  { code: 'panic_attacks', label: 'Panic / Extreme Anxiety' },
  { code: 'grief_loss', label: 'Grief / Loss of Loved One' },
  { code: 'violence', label: 'Graphic Violence' }
];

const STREAMING_PLATFORMS = [
  { code: 'netflix', label: 'Netflix' },
  { code: 'prime', label: 'Prime Video' },
  { code: 'max', label: 'Max' },
  { code: 'hulu', label: 'Hulu' },
  { code: 'apple_tv', label: 'Apple TV' },
  { code: 'free', label: 'Free Services' }
];

export const FilterDrawer: React.FC<Props> = ({ filters, onChange }) => {
  const toggleGenre = (genre: string) => {
    const current = filters.excluded_genres;
    const next = current.includes(genre)
      ? current.filter((g) => g !== genre)
      : [...current, genre];
    onChange({ ...filters, excluded_genres: next });
  };

  const toggleWarning = (warningCode: string) => {
    const current = filters.excluded_warnings;
    const next = current.includes(warningCode)
      ? current.filter((w) => w !== warningCode)
      : [...current, warningCode];
    onChange({ ...filters, excluded_warnings: next });
  };

  const togglePlatform = (platform: string) => {
    const current = filters.streaming_providers;
    const next = current.includes(platform)
      ? current.filter((p) => p !== platform)
      : [...current, platform];
    onChange({ ...filters, streaming_providers: next });
  };

  return (
    <div className="bg-white/70 backdrop-blur-xl border border-white/90 rounded-3xl p-6 space-y-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-indigo-600" />
          <h3 className="text-sm font-bold text-slate-800">
            Hard Exclusion & Preference Engine
          </h3>
        </div>
        <span className="text-[11px] font-semibold text-indigo-600 bg-indigo-50 border border-indigo-200/60 px-2 py-0.5 rounded-full">
          Grounded Catalog
        </span>
      </div>

      {/* 1. Runtime Cap */}
      <div className="space-y-2">
        <label className="text-xs font-bold text-slate-700 flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-slate-500" />
            Maximum Runtime
          </span>
          <span className="font-mono text-indigo-700 font-bold bg-indigo-50 px-2 py-0.5 rounded-md border border-indigo-100">
            {filters.max_runtime ? `${filters.max_runtime} min` : 'Any Length'}
          </span>
        </label>
        <input
          type="range"
          min="60"
          max="200"
          step="10"
          value={filters.max_runtime || 200}
          onChange={(e) => {
            const val = Number(e.target.value);
            onChange({ ...filters, max_runtime: val >= 200 ? undefined : val });
          }}
          className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
        />
        <div className="flex justify-between text-[10px] text-slate-400">
          <span>60 min</span>
          <span>120 min</span>
          <span>No Cap</span>
        </div>
      </div>

      {/* 2. Content Warnings */}
      <div className="space-y-2.5">
        <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
          Exclude Trigger Warnings
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {AVAILABLE_WARNINGS.map((w) => {
            const isExcluded = filters.excluded_warnings.includes(w.code);
            return (
              <button
                key={w.code}
                onClick={() => toggleWarning(w.code)}
                className={`p-2.5 rounded-xl text-xs text-left border transition cursor-pointer flex items-center justify-between ${
                  isExcluded
                    ? 'bg-rose-50 border-rose-300 text-rose-800 font-semibold'
                    : 'bg-white/80 border-slate-200/80 text-slate-600 hover:border-slate-300'
                }`}
              >
                <span>{w.label}</span>
                {isExcluded && <span className="text-[10px] text-rose-600 font-bold">EXCLUDED</span>}
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. Genre Exclusions */}
      <div className="space-y-2.5">
        <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
          <Film className="w-3.5 h-3.5 text-slate-500" />
          Exclude Specific Genres
        </label>
        <div className="flex flex-wrap gap-1.5">
          {AVAILABLE_GENRES.map((g) => {
            const isExcluded = filters.excluded_genres.includes(g);
            return (
              <button
                key={g}
                onClick={() => toggleGenre(g)}
                className={`px-3 py-1 rounded-full text-xs transition cursor-pointer border ${
                  isExcluded
                    ? 'bg-rose-50 text-rose-700 border-rose-300 font-semibold line-through'
                    : 'bg-white/80 text-slate-700 border-slate-200 hover:border-slate-300'
                }`}
              >
                {g}
              </button>
            );
          })}
        </div>
      </div>

      {/* 4. Streaming Availability */}
      <div className="space-y-2.5">
        <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
          <Tv className="w-3.5 h-3.5 text-slate-500" />
          Filter by Streaming Platforms
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {STREAMING_PLATFORMS.map((p) => {
            const isSelected = filters.streaming_providers.includes(p.code);
            return (
              <button
                key={p.code}
                onClick={() => togglePlatform(p.code)}
                className={`p-2 rounded-xl text-xs border transition cursor-pointer font-medium ${
                  isSelected
                    ? 'bg-indigo-50 border-indigo-300 text-indigo-700 font-bold'
                    : 'bg-white/80 border-slate-200 text-slate-600 hover:border-slate-300'
                }`}
              >
                {p.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Strict UNKNOWN Defense Notice */}
      <div className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/80 text-[11px] text-slate-600 flex items-start gap-2.5">
        <ShieldAlert className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">UNKNOWN-Metadata Defense Active:</strong> Titles missing verified trigger data are strictly excluded whenever any trigger filter is set.
        </div>
      </div>
    </div>
  );
};
