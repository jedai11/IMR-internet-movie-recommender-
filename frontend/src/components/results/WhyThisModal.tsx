import React from 'react';
import { X, HelpCircle, ShieldCheck, Crosshair, Sparkles, Film } from 'lucide-react';
import { MovieRecommendation, MoodVector } from '../../types';

interface Props {
  movie: MovieRecommendation;
  targetMood: MoodVector;
  onClose: () => void;
}

export const WhyThisModal: React.FC<Props> = ({ movie, targetMood, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-white/90 backdrop-blur-2xl border border-white max-w-lg w-full p-6 space-y-5 rounded-3xl shadow-[0_20px_60px_rgba(0,0,0,0.15)] relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1 rounded-full hover:bg-slate-100 transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3">
          {movie.poster_url ? (
            <img
              src={movie.poster_url}
              alt={movie.title}
              className="w-12 h-16 object-cover rounded-xl border border-slate-200 shrink-0 shadow-md"
            />
          ) : (
            <div className="p-2.5 rounded-xl bg-indigo-50 text-indigo-600 border border-indigo-200/50">
              <HelpCircle className="w-6 h-6" />
            </div>
          )}
          <div>
            <h3 className="text-base font-extrabold text-slate-900">
              Why was "{movie.title}" recommended?
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Mathematical Transparency & Safety Audit • {movie.release_year}
            </p>
          </div>
        </div>

        {/* 1. Circumplex Affective Match */}
        <div className="bg-slate-50/80 border border-slate-200/80 rounded-2xl p-4 space-y-3">
          <div className="flex items-center justify-between text-xs font-bold text-slate-800">
            <span className="flex items-center gap-1.5">
              <Crosshair className="w-4 h-4 text-indigo-600" />
              Russell's Circumplex Affective Coordinates
            </span>
            <span className="bg-indigo-50 border border-indigo-200 text-indigo-700 px-2 py-0.5 rounded-full font-mono text-xs">
              {movie.mood_compatibility.fit_percentage}% Fit
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-sm">
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
                Your Target Mood
              </span>
              <div className="font-mono text-slate-800 mt-1">
                Valence: <strong>{targetMood.valence > 0 ? `+${targetMood.valence}` : targetMood.valence}</strong><br />
                Arousal: <strong>{targetMood.arousal > 0 ? `+${targetMood.arousal}` : targetMood.arousal}</strong>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-white border border-slate-200/70 shadow-sm">
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
                Movie Affect Profile
              </span>
              <div className="font-mono text-slate-800 mt-1">
                Valence: <strong>{movie.mood_compatibility.title_valence > 0 ? `+${movie.mood_compatibility.title_valence}` : movie.mood_compatibility.title_valence}</strong><br />
                Arousal: <strong>{movie.mood_compatibility.title_arousal > 0 ? `+${movie.mood_compatibility.title_arousal}` : movie.mood_compatibility.title_arousal}</strong>
              </div>
            </div>
          </div>

          <div className="text-[11px] text-slate-600 leading-relaxed font-mono bg-white p-2.5 rounded-lg border border-slate-200/60">
            Euclidean Affect Distance: <strong>{movie.mood_compatibility.distance}</strong> (Max: 2.83)
          </div>
        </div>

        {/* 2. Rationale Narrative */}
        <div className="bg-slate-50/80 border border-slate-200/80 rounded-2xl p-4 space-y-1.5">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            Affective Rationale
          </div>
          <p className="text-xs text-slate-700 leading-relaxed italic bg-white p-3 rounded-xl border border-slate-200/60">
            "{movie.match_rationale}"
          </p>
        </div>

        {/* 3. Safety Check Verification */}
        <div className="bg-slate-50/80 border border-slate-200/80 rounded-2xl p-4 space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            Safety & Exclusions Audit
          </div>
          <div className="space-y-1 text-xs text-slate-600">
            <div className="flex items-center justify-between">
              <span>Evaluated Content Warning Flags:</span>
              <strong className="text-slate-800">{movie.safety_check.flags_evaluated} verified</strong>
            </div>
            <div className="flex items-center justify-between">
              <span>Passed Hard Filter Defense:</span>
              <span className="text-emerald-700 font-bold">100% Passed</span>
            </div>
          </div>
        </div>

        {/* 4. Verified Front-Page Poster Description */}
        {movie.front_page_description && (
          <div className="bg-amber-50/70 border border-amber-200/80 rounded-2xl p-3.5 space-y-1">
            <div className="flex items-center gap-1.5 text-xs font-bold text-amber-900">
              <Film className="w-3.5 h-3.5 text-amber-600" />
              Verified Authentic Front-Page Cover
            </div>
            <p className="text-xs text-amber-950/80 leading-relaxed">
              {movie.front_page_description}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
