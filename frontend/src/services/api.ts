import {
  PickerInput,
  MoodVector,
  MoodAnalysisResponse,
  FilterCriteria,
  RecommendationResponse
} from '../types';

const API_BASE = '/api';

export async function analyzeMood(
  picker: PickerInput | null,
  freeText: string,
  strategy: string
): Promise<MoodAnalysisResponse> {
  const resp = await fetch(`${API_BASE}/mood/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      picker: picker ? { valence: picker.valence, arousal: picker.arousal } : null,
      free_text: freeText.trim() ? freeText.trim() : null,
      strategy
    })
  });

  if (!resp.ok) {
    throw new Error(`Mood analysis failed: ${resp.statusText}`);
  }
  return resp.json();
}

export async function getRecommendations(
  sessionId: string,
  targetMood: MoodVector,
  strategy: string,
  filters: FilterCriteria,
  limit: number = 36,
  moodName?: string
): Promise<RecommendationResponse> {
  const resp = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      target_mood: targetMood,
      mood_name: moodName,
      strategy,
      filters,
      limit
    })
  });

  if (!resp.ok) {
    throw new Error(`Recommendations failed: ${resp.statusText}`);
  }
  return resp.json();
}

export async function submitFeedback(
  sessionId: string,
  titleId: string,
  feedbackAction: 'watched' | 'helped' | 'skipped' | 'disliked'
): Promise<{ success: boolean; message: string }> {
  const resp = await fetch(`${API_BASE}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      title_id: titleId,
      feedback_action: feedbackAction
    })
  });

  if (!resp.ok) {
    throw new Error(`Feedback failed: ${resp.statusText}`);
  }
  return resp.json();
}

