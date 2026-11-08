export interface MoodVector {
  valence: number;
  arousal: number;
  confidence?: number;
}

export interface PickerInput {
  valence: number;
  arousal: number;
}

export interface DistressResource {
  name: string;
  contact: string;
  url?: string;
}

export interface DistressResponse {
  distress_detected: boolean;
  message: string;
  helplines: DistressResource[];
  gentle_content_option?: {
    title: string;
    description: string;
    recommended_genre: string;
  };
}

export interface MovieReference {
  title: string;
  genres: string[];
}

export interface MoodAnalysisResponse {
  distress_detected: boolean;
  safe_response?: DistressResponse;
  fused_mood?: MoodVector;
  strategy_applied: string;
  target_mood?: MoodVector;
  inferred_tags: string[];
  desired_genres?: string[];
  referenced_movies?: MovieReference[];
  source_breakdown: Record<string, number>;
}

export interface FilterCriteria {
  max_runtime?: number;
  min_runtime?: number;
  excluded_genres: string[];
  preferred_genres?: string[];
  excluded_warnings: string[];
  streaming_providers: string[];
  exclude_seen: boolean;
}

export interface MoodCompatibility {
  title_valence: number;
  title_arousal: number;
  distance: number;
  fit_percentage: number;
}

export interface SafetyCheckResult {
  flags_evaluated: number;
  exclusions_passed: boolean;
  unknown_metadata_excluded: string[];
}

export interface MovieRecommendation {
  title_id: string;
  title: string;
  release_year: number;
  runtime_minutes: number;
  genres: string[];
  poster_url?: string;
  synopsis?: string;
  streaming_platforms: string[];
  score: number;
  mood_compatibility: MoodCompatibility;
  match_rationale: string;
  front_page_description?: string;
  safety_check: SafetyCheckResult;
}

export interface RecommendationResponse {
  session_id: string;
  recommendations: MovieRecommendation[];
  meta: {
    initial_candidates: number;
    surviving_candidates: number;
    dropped_reasons: Record<string, number>;
    weights_used: Record<string, number>;
    latency_ms: number;
  };
}

