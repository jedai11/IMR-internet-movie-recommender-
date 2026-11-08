import React from 'react';
import { PickerInput } from '../../types';

interface Preset {
  label: string;
  emoji: string;
  valence: number;
  arousal: number;
  description: string;
}

const PRESETS: Preset[] = [
  { label: 'Joyful', emoji: '🌟', valence: 0.80, arousal: 0.60, description: 'Bright, celebratory' },
  { label: 'Peaceful', emoji: '🍃', valence: 0.75, arousal: -0.60, description: 'Serene, cozy' },
  { label: 'Melancholic', emoji: '🌧️', valence: -0.65, arousal: -0.50, description: 'Reflective, tender' },
  { label: 'Anxious', emoji: '⚡', valence: -0.60, arousal: 0.75, description: 'Overwhelmed, tense' },
  { label: 'Energized', emoji: '🔥', valence: 0.85, arousal: 0.85, description: 'High adrenaline' },
  { label: 'Exhausted', emoji: '🛋️', valence: -0.40, arousal: -0.80, description: 'Low energy, resting' },
  { label: 'Angry', emoji: '🌋', valence: -0.75, arousal: 0.85, description: 'Frustrated, raw' },
  { label: 'Hopeful', emoji: '🌅', valence: 0.70, arousal: 0.20, description: 'Optimistic' }
];

interface Props {
  currentCoordinates: PickerInput;
  onSelectPreset: (coords: PickerInput) => void;
}

export const EmotionPresets: React.FC<Props> = ({ currentCoordinates, onSelectPreset }) => {
  return (
    <div className="space-y-2">
      <div className="text-xs font-bold text-slate-700">
        Quick Mood Presets
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {PRESETS.map((p) => {
          const isSelected =
            Math.abs(currentCoordinates.valence - p.valence) < 0.15 &&
            Math.abs(currentCoordinates.arousal - p.arousal) < 0.15;

          return (
            <button
              key={p.label}
              onClick={() => onSelectPreset({ valence: p.valence, arousal: p.arousal })}
              className={`p-2.5 rounded-2xl text-left border transition-all cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'bg-white border-indigo-500 shadow-md ring-2 ring-indigo-500/20 text-slate-900 -translate-y-0.5'
                  : 'bg-white/60 hover:bg-white/90 border-slate-200/70 text-slate-700 hover:border-slate-300 shadow-sm'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-base">{p.emoji}</span>
                <span className="text-[10px] font-mono text-slate-400">
                  {p.valence > 0 ? `+${p.valence}` : p.valence}
                </span>
              </div>
              <div className="mt-1">
                <div className="text-xs font-bold">{p.label}</div>
                <div className="text-[10px] text-slate-500 truncate">{p.description}</div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
