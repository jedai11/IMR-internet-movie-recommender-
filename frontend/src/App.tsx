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

const GENRE_KEYWORD_MAP: Record<string, string | string[]> = {
  'night thriller': ['Thriller', 'Night-Movie'],
  'night-thriller': ['Thriller', 'Night-Movie'],
  'night movie': 'Night-Movie',
  'night-movie': 'Night-Movie',
  'night cinema': 'Night-Movie',
  'late night': 'Night-Movie',
  'midnight': 'Night-Movie',
  'noir': 'Night-Movie',
  'neo-noir': 'Night-Movie',
  'night': 'Night-Movie',
  'thriller': 'Thriller', 'thrillers': 'Thriller', 'suspense': 'Thriller', 'thrilling': 'Thriller',
  'comedy': 'Comedy', 'comedies': 'Comedy', 'funny': 'Comedy', 'humor': 'Comedy', 'hilarious': 'Comedy', 'romcom': 'Comedy',
  'romance': 'Romance', 'romantic': 'Romance', 'love story': 'Romance',
  'some kind of love': 'Romance', 'kind of love': 'Romance', 'with love': 'Romance', 'love': 'Romance',
  'horror': 'Horror', 'scary': 'Horror', 'spooky': 'Horror', 'frightening': 'Horror',
  'supernatural': 'Horror', 'slasher': 'Horror', 'creepy': 'Horror', 'ghost': 'Horror',
  'demon': 'Horror', 'possession': 'Horror', 'haunted': 'Horror',
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
  'titanic': { title: 'Titanic', genres: ['Drama', 'Romance'] },
  // Horror
  'annabelle': { title: 'Annabelle', genres: ['Horror', 'Mystery', 'Thriller'] },
  'the conjuring': { title: 'The Conjuring', genres: ['Horror', 'Mystery', 'Thriller'] },
  'conjuring': { title: 'The Conjuring', genres: ['Horror', 'Mystery', 'Thriller'] },
  'hereditary': { title: 'Hereditary', genres: ['Horror', 'Drama', 'Mystery'] },
  'a quiet place': { title: 'A Quiet Place', genres: ['Horror', 'Sci-Fi', 'Thriller'] },
  'insidious': { title: 'Insidious', genres: ['Horror', 'Mystery', 'Thriller'] },
  'tumbbad': { title: 'Tumbbad', genres: ['Horror', 'Fantasy', 'Drama'] },
  'stree': { title: 'Stree', genres: ['Comedy', 'Horror'] },
  // Bollywood & Indian Cinema
  '3 idiots': { title: '3 Idiots', genres: ['Comedy', 'Drama'] },
  'andhadhun': { title: 'Andhadhun', genres: ['Crime', 'Thriller', 'Comedy'] },
  'dangal': { title: 'Dangal', genres: ['Action', 'Drama'] },
  'zindagi na milegi dobara': { title: 'Zindagi Na Milegi Dobara', genres: ['Comedy', 'Drama', 'Romance'] },
  'dilwale dulhania le jayenge': { title: 'Dilwale Dulhania Le Jayenge', genres: ['Drama', 'Romance'] },
  'gangs of wasseypur': { title: 'Gangs of Wasseypur', genres: ['Action', 'Crime', 'Drama'] },
  // Tollywood
  'rrr': { title: 'RRR', genres: ['Action', 'Drama'] },
  'baahubali': { title: 'Baahubali: The Beginning', genres: ['Action', 'Drama', 'Fantasy'] },
  'pushpa': { title: 'Pushpa: The Rise', genres: ['Action', 'Crime', 'Drama'] },
  'eega': { title: 'Eega', genres: ['Action', 'Comedy', 'Fantasy', 'Romance'] },
  'kantara': { title: 'Kantara', genres: ['Action', 'Drama', 'Thriller'] }
};

const SUGGESTIONS = [
  "Night thriller with some kind of love",
  "Calm & peaceful evening, looking for soothing comfort like Drive My Car or Departures",
  "Happy & energetic! Want upbeat optimism and fun comedy like Crash Landing on You",
  "Angry & intense after a long day, need a gripping high-stakes thriller like Parasite",
  "Sad & melancholic, looking for deep nostalgic cinema like In the Mood for Love",
  "Romantic mood, looking for tender intimacy and love story like Before Sunrise",
  "Focus & concentration, want disciplined balanced cinema like Oppenheimer"
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
    origins: [],
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
    document.documentElement.style.setProperty('--theme-accent', theme.accentHex);
    document.documentElement.style.setProperty('--theme-bg', theme.backgroundHex);
    document.documentElement.style.setProperty('--theme-text', theme.textHex);
    document.documentElement.style.setProperty('--theme-glow', theme.glowHex);
    document.documentElement.style.setProperty('--theme-bg-gradient-1', theme.bgGradient1);
    document.documentElement.style.setProperty('--theme-bg-gradient-2', theme.bgGradient2);
    document.documentElement.style.setProperty('--theme-wcag-text-on-light', theme.wcagTextOnLight);
    document.documentElement.style.setProperty('--theme-wcag-button-text', theme.wcagButtonText);

    // Sync [data-mood] attribute for dynamic CSS mood morphing & glow
    const moodKeyMap: Record<string, string> = {
      'calm_peaceful': 'calm',
      'happy_energetic': 'happy',
      'angry_intense': 'angry',
      'sad_melancholic': 'sad',
      'romantic_love': 'romantic',
      'focus_concentration': 'focus',
      'excitement_adrenaline': 'adrenaline',
      'neutral_minimal': 'neutral'
    };
    const moodAttr = moodKeyMap[theme.themeId] || 'neutral';
    document.documentElement.setAttribute('data-mood', moodAttr);
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
        if (Array.isArray(genre)) {
          genre.forEach((g) => found.add(g));
        } else {
          found.add(genre);
        }
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
    <div className="min-h-screen flex flex-col custom-scrollbar theme-transition relative overflow-x-hidden">
      {/* Dynamic Ambient Refraction Light Orbs (VisionOS / macOS style) */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div
          className="ambient-orb ambient-orb-1"
          style={{ background: currentTheme.primaryHex }}
        />
        <div
          className="ambient-orb ambient-orb-2"
          style={{ background: currentTheme.secondaryHex }}
        />
        <div
          className="ambient-orb ambient-orb-3"
          style={{ background: currentTheme.accentHex }}
        />
      </div>

      {/* Left Exterior Brand: IMR */}
      <div className="fixed top-4 left-4 sm:left-6 z-40 flex items-center gap-2.5 pointer-events-auto">
        <div
          className="w-10 h-10 rounded-2xl flex items-center justify-center shadow-lg transition-all duration-700"
          style={{
            background: `linear-gradient(135deg, ${currentTheme.primaryHex}, ${currentTheme.secondaryHex})`,
            boxShadow: `0 4px 18px ${currentTheme.glowHex}`
          }}
        >
          <Clapperboard className="w-5 h-5 text-white" />
        </div>
        <div className="flex flex-col">
          <span className="font-black text-2xl tracking-tight text-[#F8FAFC] leading-none">
            IMR
          </span>
          <span className="text-[10px] uppercase tracking-wider font-bold text-cyan-300/80 mt-0.5">
            Internet Movie Recommender
          </span>
        </div>
      </div>

      {/* Floating Top-Right Exterior Utility Cluster */}
      <div className="fixed top-4 right-4 sm:right-6 z-40 flex items-center gap-2 pointer-events-auto">
        {/* Gemini AI Status Badge */}
        <div
          className="glass-light-pill px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 text-emerald-400 border-[#29344D]"
          title="Google Gemini AI is active for affective psychology NLP and movie genre analysis"
        >
          <Sparkles className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span className="hidden sm:inline font-mono text-[11px]">Gemini AI</span>
        </div>

        {/* Dynamic Mood Palette Swatch Indicator with WCAG Compliance Tag */}
        <div
          className="glass-light-pill px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all duration-700 shadow-sm border-[#29344D]"
          style={{
            borderColor: currentTheme.badgeBorder,
            color: '#F8FAFC'
          }}
          title={`${currentTheme.name}: ${currentTheme.feeling} • WCAG 2.2 ${currentTheme.wcagLevel} compliant (${currentTheme.contrastRatioOnLight})`}
        >
          <div className="flex items-center -space-x-1">
            <span
              className="w-2.5 h-2.5 rounded-full border border-white/40 shadow-sm"
              style={{ backgroundColor: currentTheme.primaryHex }}
              title={`Primary: ${currentTheme.primaryHex}`}
            />
            <span
              className="w-2.5 h-2.5 rounded-full border border-white/40 shadow-sm"
              style={{ backgroundColor: currentTheme.secondaryHex }}
              title={`Secondary: ${currentTheme.secondaryHex}`}
            />
            <span
              className="w-2.5 h-2.5 rounded-full border border-white/40 shadow-sm"
              style={{ backgroundColor: currentTheme.accentHex }}
              title={`Accent: ${currentTheme.accentHex}`}
            />
          </div>
          <span className="hidden md:inline font-mono text-[11px] text-[#F8FAFC]">{currentTheme.name}</span>
          <span className="hidden lg:inline-block px-1.5 py-0.5 rounded-md bg-emerald-950/80 text-emerald-300 text-[9px] font-mono font-black border border-emerald-600/50">
            WCAG {currentTheme.wcagLevel}
          </span>
        </div>

        <button
          onClick={() => setPrivacyModalOpen(true)}
          className="glass-light-pill px-3.5 py-1.5 rounded-xl text-xs font-bold text-[#CBD5E1] hover:text-[#F8FAFC] border-[#29344D] transition flex items-center gap-1.5 cursor-pointer"
        >
          <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
          <span className="hidden sm:inline">Privacy</span>
        </button>

        {recommendations.length > 0 && (
          <button
            onClick={handleClearSession}
            title="Reset discovery session"
            className="glass-light-pill p-2 rounded-xl text-[#CBD5E1] hover:text-[#F8FAFC] border-[#29344D] transition cursor-pointer"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Main Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 pt-28 sm:pt-36 lg:pt-40 pb-16 space-y-14 relative z-10">
        
        {/* ========================================================================= */}
        {/* CENTER HERO SEARCH CAPSULE (Glass-Light Morphism)                        */}
        {/* ========================================================================= */}
        <section className="max-w-3xl mx-auto space-y-8 text-center mt-2 sm:mt-4">
          
          {/* Hero Headlines & Information */}
          <div className="space-y-3">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-[#F8FAFC] drop-shadow-md">
              Discover Cinema Grounded in Your Mood
            </h1>
            <p className="text-sm sm:text-base text-[#CBD5E1] max-w-xl mx-auto leading-relaxed font-medium">
              Express your feelings, mention movies or dramas you love, or fine-tune your affective coordinates on Russell's Circumplex.
            </p>
          </div>

          {/* Central Glassmorphic Search Bar Capsule */}
          <div className="glass-light-panel rounded-3xl p-5 sm:p-6 space-y-4 text-left transition-all relative">
            
            {/* Input Row */}
            <div className="relative flex items-start gap-3">
              <div className="mt-2.5 text-indigo-400 shrink-0">
                <Search className="w-5 h-5 text-indigo-400" />
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
                  className="w-full bg-transparent text-[#F8FAFC] placeholder:text-slate-400 text-sm sm:text-base font-medium focus:outline-none resize-none leading-relaxed"
                />

                {/* Real-time Analyzed Badges */}
                {(referencedMovies.length > 0 || detectedGenres.length > 0) && (
                  <div className="flex items-center gap-2 flex-wrap pt-2 border-t border-[#29344D]">
                    {referencedMovies.map((ref) => (
                      <span
                        key={ref.title}
                        className="glass-light-pill px-3 py-1 rounded-full text-xs font-bold text-amber-300 flex items-center gap-1 border-amber-500/40 bg-amber-950/40"
                      >
                        🎬 {ref.title}
                        <span className="opacity-70 font-normal text-[10px]">({ref.genres.join(', ')})</span>
                      </span>
                    ))}
                    {detectedGenres.map((g) => (
                      <span
                        key={g}
                        className="glass-light-pill px-3 py-1 rounded-full text-xs font-bold text-cyan-300 border-cyan-500/40 bg-cyan-950/40"
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
                  className="glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] p-1.5 rounded-full transition mt-1"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Tool Toggles Ribbon */}
            <div className="flex items-center justify-between flex-wrap gap-2.5 pt-3.5 border-t border-[#29344D]">
              <div className="flex items-center gap-2 flex-wrap">
                {/* 2D Mood Canvas Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'canvas' ? 'none' : 'canvas')}
                  className={`px-3.5 py-2 rounded-2xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                    activeTab === 'canvas'
                      ? 'bg-indigo-600 text-white border border-indigo-500 shadow-md shadow-indigo-600/30'
                      : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC]'
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
                  className={`px-3.5 py-2 rounded-2xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                    activeTab === 'presets'
                      ? 'bg-indigo-600 text-white border border-indigo-500 shadow-md shadow-indigo-600/30'
                      : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC]'
                  }`}
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Mood Presets</span>
                </button>

                {/* Strategy Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'strategy' ? 'none' : 'strategy')}
                  className={`px-3.5 py-2 rounded-2xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                    activeTab === 'strategy'
                      ? 'bg-indigo-600 text-white border border-indigo-500 shadow-md shadow-indigo-600/30'
                      : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC]'
                  }`}
                >
                  <Compass className="w-3.5 h-3.5" />
                  <span className="capitalize">{strategy} Mode</span>
                </button>

                {/* Filters Toggle */}
                <button
                  type="button"
                  onClick={() => setActiveTab(activeTab === 'filters' ? 'none' : 'filters')}
                  className={`px-3.5 py-2 rounded-2xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                    activeTab === 'filters'
                      ? 'bg-indigo-600 text-white border border-indigo-500 shadow-md shadow-indigo-600/30'
                      : 'glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC]'
                  }`}
                >
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span>Filters</span>
                </button>
              </div>
            </div>

            {/* Dedicated Primary Discover Mode Action (Placed Lower) */}
            <div className="pt-3 flex items-center justify-between flex-wrap gap-3">
              <span className="text-xs text-[#CBD5E1]/60 hidden sm:inline-flex items-center gap-1.5 font-medium">
                Tip: Press <kbd className="px-2 py-0.5 rounded-lg bg-[#1C2540] text-[11px] font-mono text-[#F8FAFC] border border-[#29344D] shadow-sm">Enter ↵</kbd> to initiate discovery
              </span>

              <button
                type="button"
                onClick={() => handleDiscover()}
                disabled={loading}
                className="w-full sm:w-auto px-7 py-3 rounded-2xl font-black text-sm shadow-lg transition-all flex items-center justify-center gap-2.5 disabled:opacity-50 cursor-pointer active:scale-95 ml-auto hover:brightness-110"
                style={{
                  background: `linear-gradient(135deg, ${currentTheme.primaryHex}, ${currentTheme.secondaryHex})`,
                  color: currentTheme.wcagButtonText,
                  boxShadow: `0 8px 26px ${currentTheme.glowHex}`
                }}
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" style={{ color: currentTheme.wcagButtonText }} />
                    <span>Analyzing Affect & Catalog...</span>
                  </>
                ) : (
                  <>
                    <span>Discover Movies</span>
                    <ArrowRight className="w-4 h-4" style={{ color: currentTheme.wcagButtonText }} />
                  </>
                )}
              </button>
            </div>

            {/* Expandable Interior Drawers */}
            {activeTab !== 'none' && (
              <div className="pt-4 border-t border-[#29344D] animate-in fade-in duration-200">
                {activeTab === 'canvas' && (
                  <div className="p-4 sm:p-5 rounded-2xl glass-light-inner">
                    <MoodCanvas
                      coordinates={pickerCoords}
                      onChange={(coords) => setPickerCoords(coords)}
                    />
                  </div>
                )}

                {activeTab === 'presets' && (
                  <div className="p-4 sm:p-5 rounded-2xl glass-light-inner">
                    <EmotionPresets
                      currentCoordinates={pickerCoords}
                      onSelectPreset={(coords) => {
                        setPickerCoords(coords);
                      }}
                    />
                  </div>
                )}

                {activeTab === 'strategy' && (
                  <div className="p-4 sm:p-5 rounded-2xl glass-light-inner">
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
              <span className="text-xs font-semibold text-[#CBD5E1]">
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
                    className="glass-light-pill text-xs text-[#CBD5E1] hover:text-[#F8FAFC] px-3.5 py-1.5 rounded-full text-left truncate max-w-md cursor-pointer border-[#29344D]"
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
            <div className="p-4 rounded-3xl glass-light-panel border-rose-500/50 text-rose-300 text-xs font-semibold flex items-center gap-3 shadow-sm bg-rose-950/40">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
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
            <div className="py-20 text-center space-y-4 glass-light-card rounded-3xl max-w-md mx-auto border-[#29344D]">
              <RefreshCw className="w-9 h-9 animate-spin text-indigo-400 mx-auto" />
              <p className="text-sm font-bold text-[#F8FAFC]">
                Calculating Russell Circumplex Affect Vectors & Querying Catalog...
              </p>
            </div>
          )}

          {/* Results Grid */}
          {!loading && recommendations.length > 0 && !distressData && (
            <div className="space-y-6 animate-in fade-in duration-300">
              <div className="flex items-center justify-between flex-wrap gap-3 pb-4 border-b border-[#29344D]">
                <div>
                  <h2 className="text-xl font-black text-[#F8FAFC] flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-indigo-400" />
                    Recommended Cinema ({recommendations.length})
                  </h2>
                  <p className="text-xs text-[#CBD5E1] mt-0.5 font-medium">
                    Grounded math recommendations matching your exact affect and requested genres.
                  </p>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  {detectedGenres.length > 0 && (
                    <span className="glass-light-pill text-xs font-bold text-cyan-300 px-3 py-1 rounded-xl border-cyan-500/40 bg-cyan-950/30">
                      Filtered: {detectedGenres.join(', ')}
                    </span>
                  )}
                  {activeTargetMood && (
                    <span className="glass-light-pill text-xs font-mono font-bold text-[#CBD5E1] px-3 py-1 rounded-xl border-[#29344D]">
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
