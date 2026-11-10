import React from 'react';
import { Filter, Clock, Film, Tv, Globe, Shield, AlertTriangle, Sparkles } from 'lucide-react';
import { FilterCriteria } from '../../types';

interface Props {
  filters: FilterCriteria;
  onChange: (filters: FilterCriteria) => void;
}

const CINEMA_ORIGINS = [
  { code: 'all', label: '🌐 All Origins' },
  { code: 'hollywood', label: '🎬 Hollywood (US)' },
  { code: 'bollywood', label: '🇮🇳 Bollywood' },
  { code: 'tollywood', label: '⚡ Tollywood (South)' },
  { code: 'korean', label: '🇰🇷 Korean' },
  { code: 'japanese', label: '🇯🇵 Japanese & Anime' },
  { code: 'european', label: '🇪🇺 European' },
  { code: 'asian', label: '🌏 Asian / Intl' }
];

const ADULT_OPTIONS = [
  { code: 'standard', label: '🛡️ Family / Standard (PG-13)', desc: 'Clean cinema (No nudity or explicit sex)' },
  { code: 'all', label: '🌐 All Content (Include 18+)', desc: 'Both standard and adult movies (nudity & sex included)' },
  { code: '18_plus', label: '🔞 18+ Mature (Nudity & Sex)', desc: 'Strictly movies with nudity, sex, erotic & mature themes' }
];

const CENSORSHIP_OPTIONS = [
  { code: 'all', label: '🎞️ All Versions', desc: 'Any release version' },
  { code: 'censored', label: '✂️ Censored Edits', desc: 'Theatrical cuts with blurred/cut scenes' },
  { code: 'uncensored', label: '🎬 Uncensored / Uncut', desc: 'Full explicit nudity, uncut sex & raw director\'s cuts' }
];

const AVAILABLE_GENRES = [
  'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
  'Drama', 'Family', 'Fantasy', 'Horror', 'Music', 'Mystery',
  'Night-Movie', 'Romance', 'Sci-Fi', 'Thriller'
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

  const togglePlatform = (platform: string) => {
    const current = filters.streaming_providers;
    const next = current.includes(platform)
      ? current.filter((p) => p !== platform)
      : [...current, platform];
    onChange({ ...filters, streaming_providers: next });
  };

  const toggleOrigin = (originCode: string) => {
    if (originCode === 'all') {
      onChange({ ...filters, origins: [] });
      return;
    }
    const current = (filters.origins || []).filter((o) => o !== 'all');
    const next = current.includes(originCode)
      ? current.filter((o) => o !== originCode)
      : [...current, originCode];
    onChange({ ...filters, origins: next });
  };

  const setAdultMode = (mode: 'standard' | 'all' | '18_plus') => {
    onChange({ ...filters, adult_mode: mode });
  };

  const setCensorship = (mode: 'all' | 'censored' | 'uncensored') => {
    onChange({ ...filters, censorship: mode });
  };

  const currentAdultMode = filters.adult_mode || 'all';
  const currentCensorship = filters.censorship || 'all';

  return (
    <div className="glass-light-panel rounded-3xl p-6 sm:p-7 space-y-6 border-[#29344D]">
      <div className="flex items-center justify-between border-b border-[#29344D] pb-3.5">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-black text-[#F8FAFC] tracking-tight">
            Discovery & Exclusion Filters
          </h3>
        </div>
        <span className="glass-light-pill text-[11px] font-bold text-cyan-300 px-3 py-1 rounded-full border-[#29344D]">
          IMR Verified
        </span>
      </div>

      {/* 1. 18+ Mature & Adult Content Filter */}
      <div className="space-y-3 p-4 rounded-2xl glass-light-inner border border-amber-500/20 bg-amber-950/10">
        <label className="text-xs font-bold text-[#F8FAFC] flex items-center justify-between">
          <span className="flex items-center gap-1.5 text-amber-300">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
            18+ Adult Cinema (Nudity, Sex & Erotica)
          </span>
          <span className="glass-light-pill font-mono text-[10px] text-amber-200 font-bold px-2 py-0.5 rounded-lg border-[#29344D]">
            {currentAdultMode === '18_plus' ? '🔞 18+ Nudity/Sex' : currentAdultMode === 'standard' ? '🛡️ Family' : '🌐 All Ratings'}
          </span>
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          {ADULT_OPTIONS.map((opt) => {
            const isSelected = currentAdultMode === opt.code;
            return (
              <button
                key={opt.code}
                onClick={() => setAdultMode(opt.code as any)}
                className={`p-3 rounded-2xl text-left transition cursor-pointer border flex flex-col justify-between gap-1 ${
                  isSelected
                    ? 'border-amber-400 bg-amber-950/40 text-amber-200 shadow-sm'
                    : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] border-[#29344D]'
                }`}
              >
                <span className="text-xs font-black">{opt.label}</span>
                <span className="text-[10px] text-[#CBD5E1]/70 leading-tight">{opt.desc}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 2. Censorship Setting: Censored vs Uncensored */}
      <div className="space-y-3 p-4 rounded-2xl glass-light-inner border border-cyan-500/20 bg-cyan-950/10">
        <label className="text-xs font-bold text-[#F8FAFC] flex items-center justify-between">
          <span className="flex items-center gap-1.5 text-cyan-300">
            <Shield className="w-3.5 h-3.5 text-cyan-400" />
            Censorship & Version Preference
          </span>
          <span className="glass-light-pill font-mono text-[10px] text-cyan-200 font-bold px-2 py-0.5 rounded-lg border-[#29344D]">
            {currentCensorship === 'uncensored' ? '🎬 Uncut' : currentCensorship === 'censored' ? '✂️ Censored' : '🎞️ All'}
          </span>
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          {CENSORSHIP_OPTIONS.map((opt) => {
            const isSelected = currentCensorship === opt.code;
            return (
              <button
                key={opt.code}
                onClick={() => setCensorship(opt.code as any)}
                className={`p-3 rounded-2xl text-left transition cursor-pointer border flex flex-col justify-between gap-1 ${
                  isSelected
                    ? 'border-cyan-400 bg-cyan-950/40 text-cyan-200 shadow-sm'
                    : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] border-[#29344D]'
                }`}
              >
                <span className="text-xs font-black">{opt.label}</span>
                <span className="text-[10px] text-[#CBD5E1]/70 leading-tight">{opt.desc}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. Movie Origin / Cinema Industry */}
      <div className="space-y-3">
        <label className="text-xs font-bold text-[#F8FAFC] flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <Globe className="w-3.5 h-3.5 text-cyan-400" />
            Cinema Origin & Industry
          </span>
          <span className="text-[10px] text-[#CBD5E1]/70 font-semibold">
            {(!filters.origins || filters.origins.length === 0) ? 'All World Cinema' : `${filters.origins.length} Selected`}
          </span>
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {CINEMA_ORIGINS.map((orig) => {
            const isAll = orig.code === 'all';
            const isSelected = isAll
              ? !filters.origins || filters.origins.length === 0
              : (filters.origins || []).includes(orig.code);

            return (
              <button
                key={orig.code}
                onClick={() => toggleOrigin(orig.code)}
                className={`p-2.5 rounded-2xl text-xs transition cursor-pointer font-bold border flex items-center justify-center gap-1.5 ${
                  isSelected
                    ? 'glass-light-pill-active border-cyan-400 text-cyan-300 shadow-sm'
                    : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] border-[#29344D]'
                }`}
              >
                <span>{orig.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 4. Runtime Cap */}
      <div className="space-y-2.5">
        <label className="text-xs font-bold text-[#F8FAFC] flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-[#CBD5E1]" />
            Maximum Runtime
          </span>
          <span className="glass-light-pill font-mono text-cyan-300 font-bold px-2.5 py-0.5 rounded-lg border-[#29344D]">
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
          className="w-full h-2 bg-[#1C2540] rounded-lg appearance-none cursor-pointer accent-cyan-400"
        />
        <div className="flex justify-between text-[10px] text-[#CBD5E1]/70 font-semibold">
          <span>60 min</span>
          <span>120 min</span>
          <span>No Cap</span>
        </div>
      </div>

      {/* 5. Genre Exclusions */}
      <div className="space-y-3">
        <label className="text-xs font-bold text-[#F8FAFC] flex items-center gap-1.5">
          <Film className="w-3.5 h-3.5 text-[#CBD5E1]" />
          Exclude Specific Genres
        </label>
        <div className="flex flex-wrap gap-2">
          {AVAILABLE_GENRES.map((g) => {
            const isExcluded = filters.excluded_genres.includes(g);
            return (
              <button
                key={g}
                onClick={() => toggleGenre(g)}
                className={`px-3.5 py-1.5 rounded-full text-xs transition cursor-pointer ${
                  isExcluded
                    ? 'glass-light-pill bg-rose-950/40 text-rose-300 border-rose-500/50 font-bold line-through'
                    : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] font-medium border-[#29344D]'
                }`}
              >
                {g}
              </button>
            );
          })}
        </div>
      </div>

      {/* 6. Streaming Availability */}
      <div className="space-y-3">
        <label className="text-xs font-bold text-[#F8FAFC] flex items-center gap-1.5">
          <Tv className="w-3.5 h-3.5 text-[#CBD5E1]" />
          Filter by Streaming Platforms
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
          {STREAMING_PLATFORMS.map((p) => {
            const isSelected = filters.streaming_providers.includes(p.code);
            return (
              <button
                key={p.code}
                onClick={() => togglePlatform(p.code)}
                className={`p-2.5 rounded-2xl text-xs transition cursor-pointer font-bold border ${
                  isSelected
                    ? 'glass-light-pill-active border-cyan-400 text-cyan-300 shadow-sm'
                    : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] border-[#29344D]'
                }`}
              >
                {p.label}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
