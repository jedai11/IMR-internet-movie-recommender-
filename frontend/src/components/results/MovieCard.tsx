import React, { useState } from 'react';
import { Clock, Eye, Heart, FastForward, Info, Tv } from 'lucide-react';
import { MovieRecommendation } from '../../types';

interface Props {
  movie: MovieRecommendation;
  onOpenWhyThis: () => void;
  onFeedback: (action: 'watched' | 'helped' | 'skipped' | 'disliked') => void;
}

export const MovieCard: React.FC<Props> = ({ movie, onOpenWhyThis, onFeedback }) => {
  const [feedbackGiven, setFeedbackGiven] = useState<string | null>(null);

  const handleFeedbackClick = (action: 'watched' | 'helped' | 'skipped') => {
    setFeedbackGiven(action);
    onFeedback(action);
  };

  return (
    <div className="glass-light-card rounded-3xl overflow-hidden flex flex-col justify-between group relative border-[#29344D]">
      <div>
        {/* Real Front Page / Theatrical Poster */}
        <div className="relative aspect-[2/3] w-full overflow-hidden bg-slate-900 flex items-center justify-center">
          <img
            src={movie.poster_url || `/api/catalog/poster/${movie.title_id}`}
            alt={`${movie.title} official poster`}
            loading="lazy"
            referrerPolicy="no-referrer"
            className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-700 ease-out"
          />
          {/* Ambient Frosted Sheen */}
          <div className="absolute inset-0 bg-gradient-to-t from-[#080B16] via-transparent to-white/5 pointer-events-none" />

          {/* Origin Badge */}
          {movie.origin && (
            <div className="absolute top-3 left-3 text-[11px] font-bold text-cyan-200 bg-[#080B16]/85 backdrop-blur-md px-2.5 py-1 rounded-full border border-[#29344D] shadow-md flex items-center gap-1">
              <span>
                {movie.origin === 'Bollywood'
                  ? '🇮🇳 Bollywood'
                  : movie.origin === 'Tollywood'
                  ? '⚡ Tollywood'
                  : movie.origin === 'Korean'
                  ? '🇰🇷 Korean'
                  : movie.origin === 'Japanese'
                  ? '🇯🇵 Japanese'
                  : '🎬 ' + movie.origin}
              </span>
            </div>
          )}

          {/* Match Score Badge (Glass Pill) */}
          <div className="absolute top-3 right-3 glass-light-pill text-[#F8FAFC] px-3 py-1 rounded-full text-xs font-black flex items-center gap-1.5 font-mono shadow-md border-[#29344D]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            {movie.mood_compatibility.fit_percentage}% Match
          </div>

          {/* Runtime */}
          <div className="absolute bottom-3 left-3 text-[11px] font-semibold text-[#F8FAFC] bg-[#080B16]/80 backdrop-blur-md px-3 py-1 rounded-xl flex items-center gap-1.5 border border-[#29344D] shadow-md">
            <Clock className="w-3.5 h-3.5 text-cyan-300" />
            {movie.runtime_minutes}m • {movie.release_year}
          </div>
        </div>

        {/* Details */}
        <div className="p-5 sm:p-6 space-y-4">
          <div>
            <h4 className="text-lg font-black text-[#F8FAFC] group-hover:text-cyan-300 transition-colors tracking-tight">
              {movie.title}
            </h4>
            <div className="flex flex-wrap gap-1.5 mt-2.5">
              {movie.genres.map((g) => (
                <span
                  key={g}
                  className="glass-light-pill px-2.5 py-0.5 rounded-full text-[10px] font-bold text-[#CBD5E1] border-[#29344D]"
                >
                  {g}
                </span>
              ))}
            </div>
          </div>

          {/* Rationale Quote */}
          <div className="glass-light-inner rounded-2xl p-3 border-l-4 border-cyan-400 shadow-sm">
            <p className="text-xs text-[#CBD5E1] leading-relaxed italic">
              "{movie.match_rationale}"
            </p>
          </div>

          {/* Synopsis */}
          {movie.synopsis && (
            <p className="text-xs text-[#CBD5E1]/90 line-clamp-2 leading-relaxed font-normal">
              {movie.synopsis}
            </p>
          )}

          {/* Platforms */}
          {movie.streaming_platforms.length > 0 && (
            <div className="flex items-center gap-2 text-xs text-[#CBD5E1] pt-1 font-medium">
              <Tv className="w-3.5 h-3.5 text-cyan-400" />
              <span className="capitalize font-semibold">
                {movie.streaming_platforms.join(', ')}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Footer Actions */}
      <div className="p-5 sm:p-6 pt-0 space-y-3.5">
        <button
          onClick={onOpenWhyThis}
          className="glass-light-pill w-full py-2.5 px-4 rounded-2xl text-xs font-black text-cyan-300 hover:text-[#F8FAFC] transition flex items-center justify-center gap-2 cursor-pointer hover:border-cyan-400/50 shadow-sm border-[#29344D]"
        >
          <Info className="w-4 h-4 text-cyan-400" />
          Why this recommendation?
        </button>

        {/* 1-Tap Feedback Buttons */}
        <div className="pt-3 border-t border-[#29344D] flex items-center justify-between text-xs">
          <span className="text-[11px] font-semibold text-[#CBD5E1]/70">Rate fit:</span>
          {feedbackGiven ? (
            <span className="glass-light-pill text-[11px] font-bold text-emerald-300 bg-emerald-950/60 px-2.5 py-1 rounded-lg border-emerald-500/40">
              Feedback saved ✓
            </span>
          ) : (
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => handleFeedbackClick('helped')}
                title="Helped my mood"
                className="glass-light-pill p-2 rounded-xl hover:text-emerald-400 text-[#CBD5E1] transition cursor-pointer border-[#29344D]"
              >
                <Heart className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleFeedbackClick('watched')}
                title="I'll watch this"
                className="glass-light-pill p-2 rounded-xl hover:text-cyan-400 text-[#CBD5E1] transition cursor-pointer border-[#29344D]"
              >
                <Eye className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleFeedbackClick('skipped')}
                title="Not what I need"
                className="glass-light-pill p-2 rounded-xl hover:text-rose-400 text-[#CBD5E1] transition cursor-pointer border-[#29344D]"
              >
                <FastForward className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
