import React, { useState, useEffect, useRef } from 'react';
import {
  Clapperboard,
  Compass,
  Sparkles,
  ShieldCheck,
  AlertCircle,
  RefreshCw,
  Search,
  MessageSquareHeart,
  SlidersHorizontal,
  Palette,
  Film,
  Crosshair,
  ArrowRight,
  RotateCcw,
  ChevronDown,
  ChevronUp,
  X,
  Flame,
  CheckCircle2
} from 'lucide-react';

import {
  PickerInput,
  MoodVector,
  FilterCriteria,
  MovieRecommendation,
  DistressResponse,
  MovieReference
} from './types';
import { analyzeMood, getRecommendations, submitFeedback } from './services/api';
import { determineTherapeuticTheme, ThemePalette } from './utils/theme';

import { ConsentNotice } from './components/safety/ConsentNotice';
import { DistressBanner } from './components/safety/DistressBanner';
import { PrivacyCenterModal } from './components/safety/PrivacyCenterModal';
import { MoodCanvas } from './components/mood/MoodCanvas';
import { EmotionPresets } from './components/mood/EmotionPresets';
import { StrategySelector } from './components/mood/StrategySelector';
import { FilterDrawer } from './components/filters/FilterDrawer';
import { MovieCard } from './components/results/MovieCard';
import { WhyThisModal } from './components/results/WhyThisModal';

const GENRE_KEYWORD_MAP: Record<string, string> = {
  'thriller': 'Thriller', 'thrillers': 'Thriller', 'suspense': 'Thriller', 'thrilling': 'Thriller',
  'comedy': 'Comedy', 'comedies': 'Comedy', 'funny': 'Comedy', 'humor': 'Comedy', 'hilarious': 'Comedy', 'romcom': 'Comedy',
  'romance': 'Romance', 'romantic': 'Romance', 'love story': 'Romance',
  'horror': 'Horror', 'scary': 'Horror', 'spooky': 'Horror',
  'drama': 'Drama', 'dramatic': 'Drama',
  'action': 'Action', 'action-packed': 'Action',
  'adventure': 'Adventure',
  'animation': 'Animation', 'animated': 'Animation', 'anime': 'Animation',
  'sci-fi': 'Sci-Fi', 'scifi': 'Sci-Fi', 'science fiction': 'Sci-Fi',
  'crime': 'Crime', 'heist': 'Crime', 'gangster': 'Crime',
  'mystery': 'Mystery', 'detective': 'Mystery',
  'fantasy': 'Fantasy', 'magical': 'Fantasy',
  'family': 'Family', 'kids': 'Family',
  'music': 'Music', 'musical': 'Music'
};

const POPULAR_MOVIES_MAP: Record<string, { title: string; genres: string[] }> = {
  'parasite': { title: 'Parasite', genres: ['Thriller', 'Drama', 'Comedy'] },
  'crash landing on you': { title: 'Crash Landing on You', genres: ['Drama', 'Romance', 'Comedy'] },
  'squid game': { title: 'Squid Game', genres: ['Drama', 'Mystery', 'Thriller', 'Action'] },
  'train to busan': { title: 'Train to Busan', genres: ['Action', 'Horror', 'Thriller'] },
  'memories of murder': { title: 'Memories of Murder', genres: ['Drama', 'Mystery', 'Thriller', 'Crime'] },
  'the glory': { title: 'The Glory', genres: ['Drama', 'Thriller'] },
  'reply 1988': { title: 'Reply 1988', genres: ['Drama', 'Romance', 'Comedy', 'Family'] },
  'decision to leave': { title: 'Decision to Leave', genres: ['Romance', 'Mystery', 'Thriller', 'Crime'] },
  'vincenzo': { title: 'Vincenzo', genres: ['Drama', 'Comedy', 'Action', 'Crime'] },
  'drive my car': { title: 'Drive My Car', genres: ['Drama', 'Mystery'] },
  'shoplifters': { title: 'Shoplifters', genres: ['Drama', 'Crime'] },
  'alice in borderland': { title: 'Alice in Borderland', genres: ['Drama', 'Mystery', 'Thriller', 'Action', 'Sci-Fi'] },
  'first love': { title: 'First Love: Hatsukoi', genres: ['Drama', 'Romance'] },
  'departures': { title: 'Departures', genres: ['Drama', 'Music'] },
  'in the mood for love': { title: 'In the Mood for Love', genres: ['Drama', 'Romance'] },
  'crouching tiger': { title: 'Crouching Tiger, Hidden Dragon', genres: ['Drama', 'Action', 'Adventure', 'Fantasy'] },
  'reset': { title: 'Reset', genres: ['Drama', 'Mystery', 'Thriller', 'Sci-Fi'] },
  'hidden love': { title: 'Hidden Love', genres: ['Drama', 'Romance', 'Comedy'] },
  'better days': { title: 'Better Days', genres: ['Drama', 'Romance', 'Crime'] },
  'inception': { title: 'Inception', genres: ['Thriller', 'Action', 'Sci-Fi', 'Adventure'] },
  'interstellar': { title: 'Interstellar', genres: ['Drama', 'Sci-Fi', 'Adventure'] },
  'the dark knight': { title: 'The Dark Knight', genres: ['Drama', 'Thriller', 'Action', 'Crime'] },
  'the shawshank redemption': { title: 'The Shawshank Redemption', genres: ['Drama'] },
  'the matrix': { title: 'The Matrix', genres: ['Action', 'Sci-Fi'] },
  'good will hunting': { title: 'Good Will Hunting', genres: ['Drama', 'Romance'] },
  'pulp fiction': { title: 'Pulp Fiction', genres: ['Drama', 'Crime'] },
  'eternal sunshine': { title: 'Eternal Sunshine of the Spotless Mind', genres: ['Drama', 'Romance', 'Sci-Fi'] },
  'spirited away': { title: 'Spirited Away', genres: ['Animation', 'Adventure', 'Fantasy'] },
  'goblin': { title: 'Goblin', genres: ['Drama', 'Romance', 'Fantasy'] },
  'titanic': { title: 'Titanic', genres: ['Drama', 'Romance'] }
};

const SUGGESTIONS = [
  "Loved Crash Landing on You, feeling exhausted after work, need something warm & comforting",
  "Tense and overwhelmed, loved Parasite and Squid Game, recommend an intense thriller",
  "Feeling nostalgic and contemplative, looking for gentle drama like Drive My Car or Departures",
  "High energy and excited! Want mind-bending sci-fi action like Inception or The Matrix"
];

export function App() {
  const [sessionId, setSessionId] = useState<string>('');

  // Emotion Coordinates & Inputs
  const [pickerCoords, setPickerCoords] = useState<PickerInput>({ valence: 0.70, arousal: -0.40 });
  const [freeText, setFreeText] = useState<string>('');
  const [strategy, setStrategy] = useState<'catharsis' | 'shift'>('catharsis');
  const [inferredTags, setInferredTags] = useState<string[]>([]);
  const [detectedGenres, setDetectedGenres] = useState<string[]>([]);
  const [referencedMovies, setReferencedMovies] = useState<MovieReference[]>([]);

  // Expanded panel state inside the glass search capsule
  const [activeTab, setActiveTab] = useState<'none' | 'canvas' | 'presets' | 'strategy' | 'filters'>('none');

  // Adaptive Chromotherapeutic Theme
  const [currentTheme, setCurrentTheme] = useState<ThemePalette>(
    determineTherapeuticTheme(0.70, -0.40, [], 'catharsis')
  );

  // Hard Filters
  const [filters, setFilters] = useState<FilterCriteria>({
    max_runtime: undefined,
    excluded_genres: [],
    preferred_genres: [],
    excluded_warnings: [],
    streaming_providers: [],
    exclude_seen: true
  });

  // Results & Pipeline State
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [distressData, setDistressData] = useState<DistressResponse | null>(null);
  const [recommendations, setRecommendations] = useState<MovieRecommendation[]>([]);
  const [activeTargetMood, setActiveTargetMood] = useState<MoodVector | null>(null);

  // Modals
  const [inspectMovie, setInspectMovie] = useState<MovieRecommendation | null>(null);
  const [privacyModalOpen, setPrivacyModalOpen] = useState<boolean>(false);

  const resultsRef = useRef<HTMLDivElement>(null);

  // Initialize Anonymous Session
  useEffect(() => {
    let sid = localStorage.getItem('moodreel_session_id');
    if (!sid) {
      sid = `sess_anon_${Math.random().toString(36).substring(2, 9)}`;
      localStorage.setItem('moodreel_session_id', sid);
    }
    setSessionId(sid);
  }, []);

  // Update Dynamic Chromotherapeutic Theme smoothly with 1.8s CSS transitions
  useEffect(() => {
    const theme = determineTherapeuticTheme(
      pickerCoords.valence,
      pickerCoords.arousal,
      inferredTags,
      strategy
    );
    setCurrentTheme(theme);

    document.documentElement.style.setProperty('--theme-primary', theme.primaryHex);
    document.documentElement.style.setProperty('--theme-secondary', theme.secondaryHex);
    document.documentElement.style.setProperty('--theme-glow', theme.glowHex);
    document.documentElement.style.setProperty('--theme-bg-gradient-1', theme.bgGradient1);
    document.documentElement.style.setProperty('--theme-bg-gradient-2', theme.bgGradient2);
  }, [pickerCoords, inferredTags, strategy]);

  // Live movie reference detection
  const detectMovieReferencesRealtime = (text: string): MovieReference[] => {
    const lower = text.toLowerCase();
    const refs: MovieReference[] = [];
    const seen = new Set<string>();
    for (const [key, val] of Object.entries(POPULAR_MOVIES_MAP)) {
      const regex = new RegExp(`\\b${key}\\b`, 'i');
      if (regex.test(lower) && !seen.has(val.title)) {
        seen.add(val.title);
        refs.push(val);
      }
    }
    return refs;
  };

  // Live genre detection from user free-text (combining keywords + movie references)
  const detectGenresRealtime = (text: string): string[] => {
    const lower = text.toLowerCase();
    const found = new Set<string>();
    for (const [kw, genre] of Object.entries(GENRE_KEYWORD_MAP)) {
      const regex = new RegExp(`\\b${kw}\\b`, 'i');
      if (regex.test(lower)) {
        found.add(genre);
      }
    }
    const refs = detectMovieReferencesRealtime(text);
    for (const ref of refs) {
      for (const g of ref.genres) {
        found.add(g);
      }
    }
    return Array.from(found);
  };

  const handleTextChange = (text: string) => {
    setFreeText(text);
    const liveGenres = detectGenresRealtime(text);
    const liveRefs = detectMovieReferencesRealtime(text);
    setDetectedGenres(liveGenres);
    setReferencedMovies(liveRefs);
  };

  // Primary Discovery Pipeline
  const handleDiscover = async (textToUse?: string) => {
    const query = typeof textToUse === 'string' ? textToUse : freeText;
    setLoading(true);
    setError(null);
    setDistressData(null);

    try {
      // 1. Analyze mood and detect semantic genres & distress safeguard
      const analysis = await analyzeMood(pickerCoords, query, strategy);

      if (analysis.distress_detected && analysis.safe_response) {
        setDistressData(analysis.safe_response);
        setRecommendations([]);
        setLoading(false);
        return;
      }

      setInferredTags(analysis.inferred_tags || []);
      if (analysis.referenced_movies && analysis.referenced_movies.length > 0) {
        setReferencedMovies(analysis.referenced_movies);
      }
      const semGenres = Array.from(new Set([
        ...(analysis.desired_genres || []),
        ...detectGenresRealtime(query)
      ]));
      setDetectedGenres(semGenres);

      const target = analysis.target_mood || {
        valence: pickerCoords.valence,
        arousal: pickerCoords.arousal,
        confidence: 1.0
      };
      setActiveTargetMood(target);

      // Merge semantically requested genres into preferred filters
      const updatedFilters: FilterCriteria = {
        ...filters,
        preferred_genres: Array.from(new Set([...(filters.preferred_genres || []), ...semGenres]))
      };

      // 2. Query grounded recommendation engine
      const recsResponse = await getRecommendations(
        sessionId,
        target,
        strategy,
        updatedFilters,
        6
      );

      setRecommendations(recsResponse.recommendations);
      
      // Auto-close expanded drawers on search to showcase results cleanly
      setActiveTab('none');

      // Smooth scroll to recommendations
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 150);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to recommendation service.');
    } finally {
      setLoading(false);
    }
  };

  // Feedback Action Handler
  const handleFeedback = async (
    titleId: string,
    action: 'watched' | 'helped' | 'skipped' | 'disliked'
  ) => {
    try {
      await submitFeedback(sessionId, titleId, action);
    } catch (err) {
      console.error('Feedback recording failed', err);
    }
  };

  // Clear Session & History
  const handleClearSession = () => {
    localStorage.removeItem('moodreel_session_id');
    const newSid = `sess_anon_${Math.random().toString(36).substring(2, 9)}`;
    localStorage.setItem('moodreel_session_id', newSid);
    setSessionId(newSid);
    setRecommendations([]);
    setDistressData(null);
    setDetectedGenres([]);
    setReferencedMovies([]);
    setFreeText('');
  };

  // Trigger gentle soothing recommendations on crisis banner switch
  const handleSwitchToCalming = () => {
    setPickerCoords({ valence: 0.85, arousal: -0.65 });
    setFreeText('');
    setStrategy('shift');
    setDistressData(null);
    setTimeout(() => {
      handleDiscover('');
    }, 100);
  };

  return (
    <div className="min-h-screen flex flex-col custom-scrollbar theme-transition">
      {/* EU AI Act Art. 50 Notice Banner */}
      <ConsentNotice onOpenPrivacyModal={() => setPrivacyModalOpen(true)} />

      {/* Glassmorphic Navigation Header */}
      <header className="border-b border-white/60 bg-white/70 backdrop-blur-xl sticky top-0 z-40 shadow-[0_4px_20px_rgba(0,0,0,0.02)] theme-transition">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-2xl flex items-center justify-center shadow-md transition-all duration-700"
              style={{
                background: `linear-gradient(135deg, ${currentTheme.primaryHex}, ${currentTheme.secondaryHex})`,
                boxShadow: `0 4px 16px ${currentTheme.glowHex}`
              }}
            >
              <Clapperboard className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight text-slate-900">
                MoodReel
              </span>
              <span
                className="hidden sm:inline-block ml-2 text-[10px] uppercase tracking-wider font-bold px-2.5 py-0.5 rounded-full border transition-all duration-700"
                style={{
                  backgroundColor: currentTheme.badgeBg,
                  borderColor: currentTheme.badgeBorder,
                  color: currentTheme.badgeText
                }}
              >
                Affective Cinema
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* Gemini Integration Badge */}
            <div
              className="px-2.5 py-1 rounded-xl text-xs font-bold flex items-center gap-1.5 border border-emerald-200/80 bg-emerald-50 text-emerald-800 shadow-sm"
              title="Google Gemini AI is active for affective psychology NLP and movie genre analysis"
            >
              <Sparkles className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
              <span className="hidden sm:inline font-mono text-[11px]">Gemini AI Active</span>
            </div>

            {/* Chromotherapeutic UI Theme Indicator */}
            <div
              className="px-2.5 py-1 rounded-xl text-xs font-bold flex items-center gap-1.5 border transition-all duration-700 shadow-sm"
              style={{
                backgroundColor: currentTheme.badgeBg,
                borderColor: currentTheme.badgeBorder,
                color: currentTheme.badgeText
              }}
              title={currentTheme.objective}
            >
              <Palette className="w-3.5 h-3.5" />
              <span className="hidden md:inline font-mono text-[11px]">{currentTheme.name}</span>
            </div>

            <button
              onClick={() => setPrivacyModalOpen(true)}
              className="px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 hover:text-slate-900 bg-white/80 hover:bg-white border border-slate-200/80 transition flex items-center gap-1.5 cursor-pointer shadow-sm"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
              <span className="hidden sm:inline">Privacy</span>
            </button>

            {recommendations.length > 0 && (
              <button
                onClick={handleClearSession}
                title="Reset discovery session"
                className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 border border-transparent hover:border-slate-200 transition cursor-pointer"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-10 space-y-12">
        
        {/* ========================================================================= */}
        {/* CENTER HERO SEARCH CAPSULE (Glass-Light Morphism)                        */}
        {/* ========================================================================= */}
        <section className="max-w-3xl mx-auto space-y-6 text-center">
          
          {/* Hero Headlines */}
          <div className="space-y-2">
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
              Discover Cinema Grounded in Your Mood
            </h1>
            <p className="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed">
              Express your feelings, mention movies or dramas you love, or fine-tune your affective coordinates on Russell's Circumplex.
            </p>
          </div>

          {/* Central Glassmorphic Search Bar Capsule */}
          <div className="bg-white/80 backdrop-blur-2xl border border-white rounded-3xl p-4 sm:p-5 shadow-[0_15px_45px_rgba(31,38,135,0.07)] ring-1 ring-black/[0.03] space-y-4 text-left transition-all">
            
            {/* Input Row */}
            <div className="relative flex items-start gap-3">
              <div className="mt-2.5 text-indigo-600 shrink-0">
                <Search className="w-5 h-5 text-indigo-600" />
              </div>

              <div className="flex-1 space-y-2">
                <textarea
                  value={freeText}
                  onChange={(e) => handleTextChange(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleDiscover();
                    }
                  }}
                  placeholder="How are you feeling? e.g. Loved Parasite and Train to Busan, feeling exhausted after work, recommend an exciting thriller or K-drama..."
                  rows={2}
                  className="w-full bg-transparent text-slate-900 placeholder:text-slate-400 text-sm sm:text-base font-medium focus:outline-none resize-none leading-relaxed"
                />

                {/* Real-time Analyzed Badges */}
                {(referencedMovies.length > 0 || detectedGenres.length > 0) && (
                  <div className="flex items-center gap-1.5 flex-wrap pt-1 border-t border-slate-100">
                    {referencedMovies.map((ref) => (
                      <span
                        key={ref.title}
                        className="px-2.5 py-0.5 rounded-full text-xs font-bold border border-amber-300 bg-amber-50 text-amber-900 flex items-center gap-1 shadow-sm"
                      >
                        🎬 {ref.title}
                        <span className="opacity-70 font-normal text-[10px]">({ref.genres.join(', ')})</span>
                      </span>
                    ))}
                    {detectedGenres.map((g) => (
                      <span
                        key={g}
                        className="px-2.5 py-0.5 rounded-full text-xs font-bold border border-indigo-200 bg-indigo-50 text-indigo-800 shadow-sm"
                      >
                        🎯 {g}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {freeText.trim() && (
                <button
                  onClick={() => handleTextChange('')}
                  className="text-slate-400 hover:text-slate-700 p-1.5 rounded-full hover:bg-slate-100 transition mt-1"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Quick Action Ribbon */}
            <div className="flex items-center justify-between flex-wrap gap-2 pt-3 border-t border-slate-100/90">
              <div className="flex items-center gap-1.5 flex-wrap">
                {/* 2D Mood Canvas Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'canvas' ? 'none' : 'canvas')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition flex items-center gap-1.5 cursor-pointer shadow-sm ${
                    activeTab === 'canvas'
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-indigo-600/20'
                      : 'bg-white/90 text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-white'
                  }`}
                >
                  <Crosshair className="w-3.5 h-3.5" />
                  <span>2D Mood Canvas</span>
                  <span className="font-mono text-[10px] opacity-75">
                    ({pickerCoords.valence > 0 ? `+${pickerCoords.valence}` : pickerCoords.valence}, {pickerCoords.arousal > 0 ? `+${pickerCoords.arousal}` : pickerCoords.arousal})
                  </span>
                </button>

                {/* Presets Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'presets' ? 'none' : 'presets')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition flex items-center gap-1.5 cursor-pointer shadow-sm ${
                    activeTab === 'presets'
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-indigo-600/20'
                      : 'bg-white/90 text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-white'
                  }`}
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Mood Presets</span>
                </button>

                {/* Strategy Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'strategy' ? 'none' : 'strategy')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition flex items-center gap-1.5 cursor-pointer shadow-sm ${
                    activeTab === 'strategy'
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-indigo-600/20'
                      : 'bg-white/90 text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-white'
                  }`}
                >
                  <Compass className="w-3.5 h-3.5" />
                  <span className="capitalize">{strategy} Mode</span>
                </button>

                {/* Filters Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'filters' ? 'none' : 'filters')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition flex items-center gap-1.5 cursor-pointer shadow-sm ${
                    activeTab === 'filters'
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-indigo-600/20'
                      : 'bg-white/90 text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-white'
                  }`}
                >
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span>Filters</span>
                </button>
              </div>

              {/* Primary Search / Discover Action Button */}
              <button
                type="button"
                onClick={() => handleDiscover()}
                disabled={loading}
                className="w-full sm:w-auto px-6 py-2.5 rounded-2xl text-white font-bold text-sm shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer active:scale-95 ml-auto"
                style={{
                  background: `linear-gradient(135deg, ${currentTheme.primaryHex}, ${currentTheme.secondaryHex})`,
                  boxShadow: `0 6px 20px ${currentTheme.glowHex}`
                }}
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin text-white" />
                    <span>Analyzing Affect...</span>
                  </>
                ) : (
                  <>
                    <span>Discover Movies</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>

            {/* Expandable Interior Drawers */}
            {activeTab !== 'none' && (
              <div className="pt-4 border-t border-slate-100 animate-in fade-in duration-200">
                {activeTab === 'canvas' && (
                  <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/70">
                    <MoodCanvas
                      coordinates={pickerCoords}
                      onChange={(coords) => setPickerCoords(coords)}
                    />
                  </div>
                )}

                {activeTab === 'presets' && (
                  <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/70">
                    <EmotionPresets
                      currentCoordinates={pickerCoords}
                      onSelectPreset={(coords) => {
                        setPickerCoords(coords);
                      }}
                    />
                  </div>
                )}

                {activeTab === 'strategy' && (
                  <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/70">
                    <StrategySelector
                      strategy={strategy}
                      onChange={(strat) => setStrategy(strat)}
                    />
                  </div>
                )}

                {activeTab === 'filters' && (
                  <FilterDrawer
                    filters={filters}
                    onChange={(f) => setFilters(f)}
                  />
                )}
              </div>
            )}
          </div>

          {/* Inspirational Prompt Chips (Quick suggestions) */}
          {recommendations.length === 0 && !loading && (
            <div className="space-y-2 pt-2">
              <span className="text-xs font-semibold text-slate-400">
                Or click to explore common moods:
              </span>
              <div className="flex flex-wrap items-center justify-center gap-2">
                {SUGGESTIONS.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setFreeText(s);
                      handleDiscover(s);
                    }}
                    className="text-xs text-slate-600 hover:text-indigo-900 bg-white/70 hover:bg-white border border-slate-200/80 px-3 py-1.5 rounded-full transition shadow-sm text-left truncate max-w-md cursor-pointer"
                  >
                    ✨ {s}
                  </button>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* ========================================================================= */}
        {/* RECOMMENDATION RESULTS DECK BELOW                                        */}
        {/* ========================================================================= */}
        <section ref={resultsRef} className="max-w-6xl mx-auto space-y-6 pt-2">
          
          {/* Error Message */}
          {error && (
            <div className="p-4 rounded-3xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold flex items-center gap-3 shadow-sm">
              <AlertCircle className="w-5 h-5 text-rose-500 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Distress Banner Interception */}
          {distressData && (
            <DistressBanner
              distress={distressData}
              onSelectGentleContent={handleSwitchToCalming}
            />
          )}

          {/* Loading Indicator */}
          {loading && (
            <div className="py-16 text-center space-y-3">
              <RefreshCw className="w-8 h-8 animate-spin text-indigo-600 mx-auto" />
              <p className="text-sm font-bold text-slate-700">
                Calculating Russell Circumplex Affect Vectors & Querying Catalog...
              </p>
            </div>
          )}

          {/* Results Grid */}
          {!loading && recommendations.length > 0 && !distressData && (
            <div className="space-y-6 animate-in fade-in duration-300">
              <div className="flex items-center justify-between flex-wrap gap-3 pb-3 border-b border-slate-200/80">
                <div>
                  <h2 className="text-xl font-extrabold text-slate-900 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-indigo-600" />
                    Recommended Cinema ({recommendations.length})
                  </h2>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Grounded math recommendations matching your exact affect and requested genres.
                  </p>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  {detectedGenres.length > 0 && (
                    <span className="text-xs font-bold text-indigo-800 bg-indigo-50 px-2.5 py-1 rounded-xl border border-indigo-200 shadow-sm">
                      Filtered: {detectedGenres.join(', ')}
                    </span>
                  )}
                  {activeTargetMood && (
                    <span className="text-xs font-mono font-bold text-slate-700 bg-white/90 px-3 py-1 rounded-xl border border-slate-200 shadow-sm">
                      Target: ({activeTargetMood.valence}, {activeTargetMood.arousal})
                    </span>
                  )}
                </div>
              </div>

              {/* 3-Column Glass Card Grid with Real Theatrical Posters */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.map((movie) => (
                  <MovieCard
                    key={movie.title_id}
                    movie={movie}
                    onOpenWhyThis={() => setInspectMovie(movie)}
                    onFeedback={(action) => handleFeedback(movie.title_id, action)}
                  />
                ))}
              </div>
            </div>
          )}
        </section>
      </main>

      {/* Modals */}
      {inspectMovie && activeTargetMood && (
        <WhyThisModal
          movie={inspectMovie}
          targetMood={activeTargetMood}
          onClose={() => setInspectMovie(null)}
        />
      )}

      {privacyModalOpen && (
        <PrivacyCenterModal
          onClose={() => setPrivacyModalOpen(false)}
          onClearSession={handleClearSession}
        />
      )}
    </div>
  );
}

export default App;
