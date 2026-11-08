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
    <div className="bg-white/70 backdrop-blur-xl border border-white/80 rounded-3xl overflow-hidden hover:border-indigo-400/60 transition-all duration-300 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_16px_40px_rgba(31,38,135,0.08)] hover:-translate-y-1 flex flex-col justify-between group">
      <div>
        {/* Real Front Page / Theatrical Poster */}
        <div className="relative aspect-[2/3] w-full overflow-hidden bg-slate-100 flex items-center justify-center">
          <img
            src={movie.poster_url || `/api/catalog/poster/${movie.title_id}`}
            alt={`${movie.title} official poster`}
            loading="lazy"
            referrerPolicy="no-referrer"
            className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent pointer-events-none" />

          {/* Match Score Badge */}
          <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-md text-slate-800 px-3 py-1 rounded-full text-xs font-extrabold shadow-md border border-white/60 flex items-center gap-1 font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            {movie.mood_compatibility.fit_percentage}% Match
          </div>

          {/* Runtime */}
          <div className="absolute bottom-3 left-3 text-[11px] font-semibold text-white bg-slate-900/75 backdrop-blur-md px-2.5 py-1 rounded-lg flex items-center gap-1 shadow-sm">
            <Clock className="w-3 h-3 text-indigo-300" />
            {movie.runtime_minutes}m • {movie.release_year}
          </div>
        </div>

        {/* Details */}
        <div className="p-5 space-y-3.5">
          <div>
            <h4 className="text-base font-extrabold text-slate-900 group-hover:text-indigo-600 transition-colors">
              {movie.title}
            </h4>
            <div className="flex flex-wrap gap-1.5 mt-2">
              {movie.genres.map((g) => (
                <span
                  key={g}
                  className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200/70"
                >
                  {g}
                </span>
              ))}
            </div>
          </div>

          {/* Rationale Quote */}
          <p className="text-xs text-slate-700 leading-relaxed italic bg-indigo-50/70 border-l-2 border-indigo-500 rounded-r-lg pl-3 pr-2 py-1.5">
            "{movie.match_rationale}"
          </p>

          {/* Synopsis */}
          {movie.synopsis && (
            <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed">
              {movie.synopsis}
            </p>
          )}

          {/* Platforms */}
          {movie.streaming_platforms.length > 0 && (
            <div className="flex items-center gap-1.5 text-[11px] text-slate-500 pt-0.5">
              <Tv className="w-3 h-3 text-indigo-500" />
              <span className="capitalize font-medium">
                {movie.streaming_platforms.join(', ')}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Footer Actions */}
      <div className="p-5 pt-0 space-y-3">
        <button
          onClick={onOpenWhyThis}
          className="w-full py-2 px-3 rounded-xl text-xs font-semibold text-indigo-700 hover:text-indigo-900 bg-indigo-50/80 hover:bg-indigo-100/90 border border-indigo-200/60 transition flex items-center justify-center gap-1.5 cursor-pointer shadow-sm"
        >
          <Info className="w-3.5 h-3.5" />
          Why this recommendation?
        </button>

        {/* 1-Tap Feedback Buttons */}
        <div className="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
          <span className="text-[11px] font-medium text-slate-400">Rate fit:</span>
          {feedbackGiven ? (
            <span className="text-[11px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md">
              Feedback saved ✓
            </span>
          ) : (
            <div className="flex items-center gap-1">
              <button
                onClick={() => handleFeedbackClick('helped')}
                title="Helped my mood"
                className="p-1.5 rounded-lg hover:bg-emerald-50 text-slate-400 hover:text-emerald-600 transition cursor-pointer"
              >
                <Heart className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleFeedbackClick('watched')}
                title="I'll watch this"
                className="p-1.5 rounded-lg hover:bg-indigo-50 text-slate-400 hover:text-indigo-600 transition cursor-pointer"
              >
                <Eye className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleFeedbackClick('skipped')}
                title="Not what I need"
                className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition cursor-pointer"
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
