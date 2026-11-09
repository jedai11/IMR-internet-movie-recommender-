import React from 'react';
import { ExternalLink } from 'lucide-react';
import { MovieRecommendation } from '../../types';

interface Props {
  movie: MovieRecommendation;
  onOpenWhyThis?: () => void;
  onFeedback?: (action: 'watched' | 'helped' | 'skipped' | 'disliked') => void;
}

export const MovieCard: React.FC<Props> = ({ movie }) => {
  const tmdbUrl =
    movie.tmdb_url ||
    (movie.tmdb_id
      ? `https://www.themoviedb.org/movie/${movie.tmdb_id}`
      : `https://www.themoviedb.org/search?query=${encodeURIComponent(movie.title)}`);

  return (
    <a
      href={tmdbUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="glass-light-card rounded-3xl overflow-hidden flex flex-col group relative border-[#29344D] hover:border-cyan-400/50 hover:shadow-xl transition-all duration-300 block cursor-pointer"
      title={`Open ${movie.title} on TMDB`}
    >
      {/* Real Theatrical Poster / Banner with Lazy-Loading */}
      <div className="relative aspect-[2/3] w-full overflow-hidden bg-slate-900 flex items-center justify-center">
        <img
          src={movie.poster_url || `/api/catalog/poster/${movie.title_id}`}
          alt={`${movie.title} poster`}
          loading="lazy"
          referrerPolicy="no-referrer"
          className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 ease-out"
        />
        {/* Subtle Ambient Vignette */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#080B16] via-transparent to-transparent pointer-events-none" />

        {/* Hover Hint to TMDB */}
        <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200 glass-light-pill px-2.5 py-1 rounded-xl text-[11px] font-bold text-cyan-200 border-[#29344D] flex items-center gap-1 shadow-lg bg-[#080B16]/90">
          <span>TMDB</span>
          <ExternalLink className="w-3 h-3" />
        </div>
      </div>

      {/* Movie Title Only (No synopsis, rating, cast, or extra clutter) */}
      <div className="p-4 sm:p-5">
        <h4 className="text-base sm:text-lg font-black text-[#F8FAFC] group-hover:text-cyan-300 transition-colors tracking-tight line-clamp-1">
          {movie.title}
        </h4>
      </div>
    </a>
  );
};
