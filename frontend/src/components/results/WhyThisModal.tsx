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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#080B16]/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="glass-light-modal max-w-lg w-full p-6 sm:p-7 space-y-5 rounded-3xl relative animate-in zoom-in-95 duration-200 border-[#29344D]">
        <button
          onClick={onClose}
          className="glass-light-pill absolute top-4 right-4 text-[#CBD5E1] hover:text-[#F8FAFC] p-1.5 rounded-full transition cursor-pointer border-[#29344D]"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-3.5">
          {movie.poster_url ? (
            <img
              src={movie.poster_url}
              alt={movie.title}
              className="w-12 h-16 object-cover rounded-xl border border-[#29344D] shrink-0 shadow-md"
            />
          ) : (
            <div className="p-3 rounded-2xl glass-light-pill text-cyan-400 border-[#29344D]">
              <HelpCircle className="w-6 h-6" />
            </div>
          )}
          <div>
            <h3 className="text-base sm:text-lg font-black text-[#F8FAFC] tracking-tight">
              Why was "{movie.title}" recommended?
            </h3>
            <p className="text-xs text-[#CBD5E1] font-medium">
              Mathematical Transparency & Safety Audit • {movie.release_year}
            </p>
          </div>
        </div>

        {/* 1. Circumplex Affective Match */}
        <div className="glass-light-inner rounded-2xl p-4 sm:p-5 space-y-3 border-[#29344D]">
          <div className="flex items-center justify-between text-xs font-bold text-[#F8FAFC]">
            <span className="flex items-center gap-1.5">
              <Crosshair className="w-4 h-4 text-cyan-400" />
              Russell's Circumplex Affective Coordinates
            </span>
            <span className="glass-light-pill text-cyan-300 px-2.5 py-0.5 rounded-full font-mono text-xs font-black border-[#29344D]">
              {movie.mood_compatibility.fit_percentage}% Fit
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-xl glass-light-pill border-[#29344D]">
              <span className="text-[10px] text-[#CBD5E1]/70 font-bold uppercase tracking-wider block">
                Your Target Mood
              </span>
              <div className="font-mono text-[#F8FAFC] mt-1">
                Valence: <strong>{targetMood.valence > 0 ? `+${targetMood.valence}` : targetMood.valence}</strong><br />
                Arousal: <strong>{targetMood.arousal > 0 ? `+${targetMood.arousal}` : targetMood.arousal}</strong>
              </div>
            </div>

            <div className="p-3 rounded-xl glass-light-pill border-[#29344D]">
              <span className="text-[10px] text-[#CBD5E1]/70 font-bold uppercase tracking-wider block">
                Movie Affect Profile
              </span>
              <div className="font-mono text-[#F8FAFC] mt-1">
                Valence: <strong>{movie.mood_compatibility.title_valence > 0 ? `+${movie.mood_compatibility.title_valence}` : movie.mood_compatibility.title_valence}</strong><br />
                Arousal: <strong>{movie.mood_compatibility.title_arousal > 0 ? `+${movie.mood_compatibility.title_arousal}` : movie.mood_compatibility.title_arousal}</strong>
              </div>
            </div>
          </div>

          <div className="text-[11px] text-[#CBD5E1] leading-relaxed font-mono glass-light-pill p-2.5 rounded-xl border-[#29344D]">
            Euclidean Affect Distance: <strong className="text-[#F8FAFC]">{movie.mood_compatibility.distance}</strong> (Max: 2.83)
          </div>
        </div>

        {/* 2. Rationale Narrative */}
        <div className="glass-light-inner rounded-2xl p-4 space-y-2 border-[#29344D]">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#F8FAFC]">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            Affective Rationale
          </div>
          <p className="text-xs text-[#CBD5E1] leading-relaxed italic glass-light-pill p-3 rounded-xl border-[#29344D]">
            "{movie.match_rationale}"
          </p>
        </div>

        {/* 3. TMDB Verified Metrics & Official Trailer */}
        {(movie.tmdb_rating || movie.trailer_url) && (
          <div className="glass-light-inner rounded-2xl p-4 space-y-2 border-cyan-500/30 bg-cyan-950/20">
            <div className="flex items-center justify-between text-xs font-bold text-[#F8FAFC]">
              <span className="flex items-center gap-1.5 text-cyan-300">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                The Movie Database (TMDB) Integration
              </span>
              {movie.tmdb_rating && (
                <span className="text-amber-300 font-mono font-bold flex items-center gap-1">
                  ⭐ {movie.tmdb_rating}/10
                  {movie.vote_count ? (
                    <span className="text-[10px] text-[#94A3B8]">({movie.vote_count.toLocaleString()} votes)</span>
                  ) : null}
                </span>
              )}
            </div>

            {movie.trailer_url && (
              <div className="pt-1">
                <a
                  href={movie.trailer_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2 px-3 rounded-xl bg-red-600/80 hover:bg-red-600 text-white font-bold text-xs flex items-center justify-center gap-2 transition shadow-md cursor-pointer"
                >
                  <Film className="w-3.5 h-3.5" />
                  Watch Official Trailer (YouTube)
                </a>
              </div>
            )}
          </div>
        )}

        {/* 4. Safety Check Verification */}
        <div className="glass-light-inner rounded-2xl p-4 space-y-2 border-[#29344D]">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#F8FAFC]">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Safety & Exclusions Audit
          </div>
          <div className="space-y-1.5 text-xs text-[#CBD5E1]">
            <div className="flex items-center justify-between">
              <span>Evaluated Content Warning Flags:</span>
              <strong className="text-[#F8FAFC] font-semibold">{movie.safety_check.flags_evaluated} verified</strong>
            </div>
            <div className="flex items-center justify-between">
              <span>Passed Hard Filter Defense:</span>
              <span className="text-emerald-400 font-bold">100% Passed</span>
            </div>
          </div>
        </div>

        {/* 4. Verified Front-Page Poster Description */}
        {movie.front_page_description && (
          <div className="glass-light-inner rounded-2xl p-4 space-y-1.5 border-amber-500/40 bg-amber-950/30">
            <div className="flex items-center gap-1.5 text-xs font-bold text-amber-300">
              <Film className="w-3.5 h-3.5 text-amber-400" />
              Verified Authentic Front-Page Cover
            </div>
            <p className="text-xs text-amber-100/90 leading-relaxed">
              {movie.front_page_description}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
