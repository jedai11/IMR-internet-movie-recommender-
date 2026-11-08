import React, { useRef, useState, useEffect } from 'react';
import { Crosshair, Sparkles } from 'lucide-react';
import { PickerInput } from '../../types';

interface Props {
  coordinates: PickerInput;
  onChange: (coords: PickerInput) => void;
}

export const MoodCanvas: React.FC<Props> = ({ coordinates, onChange }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const updateCoordinates = (clientX: number, clientY: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    
    const clampX = Math.max(0, Math.min(rect.width, clientX - rect.left));
    const clampY = Math.max(0, Math.min(rect.height, clientY - rect.top));

    const valence = Number(((clampX / rect.width) * 2 - 1).toFixed(2));
    const arousal = Number((1 - (clampY / rect.height) * 2).toFixed(2));

    onChange({ valence, arousal });
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    updateCoordinates(e.clientX, e.clientY);
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    setIsDragging(true);
    if (e.touches.length > 0) {
      updateCoordinates(e.touches[0].clientX, e.touches[0].clientY);
    }
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging) updateCoordinates(e.clientX, e.clientY);
    };
    const handleMouseUp = () => setIsDragging(false);

    const handleTouchMove = (e: TouchEvent) => {
      if (isDragging && e.touches.length > 0) {
        updateCoordinates(e.touches[0].clientX, e.touches[0].clientY);
      }
    };
    const handleTouchEnd = () => setIsDragging(false);

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
      window.addEventListener('touchmove', handleTouchMove);
      window.addEventListener('touchend', handleTouchEnd);
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('touchmove', handleTouchMove);
      window.removeEventListener('touchend', handleTouchEnd);
    };
  }, [isDragging]);

  const leftPercent = ((coordinates.valence + 1) / 2) * 100;
  const topPercent = ((1 - coordinates.arousal) / 2) * 100;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between text-xs">
        <span className="font-bold text-slate-800 flex items-center gap-1.5">
          <Crosshair className="w-3.5 h-3.5 text-indigo-600" />
          Circumplex 2D Affect Space
        </span>
        <div className="flex items-center gap-2 font-mono text-[11px] text-slate-700 bg-white/80 px-2.5 py-1 rounded-lg border border-slate-200/80 shadow-sm">
          <span>Valence: <strong>{coordinates.valence > 0 ? `+${coordinates.valence}` : coordinates.valence}</strong></span>
          <span className="text-slate-300">|</span>
          <span>Arousal: <strong>{coordinates.arousal > 0 ? `+${coordinates.arousal}` : coordinates.arousal}</strong></span>
        </div>
      </div>

      <div
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onTouchStart={handleTouchStart}
        className="relative w-full aspect-square max-w-[340px] mx-auto rounded-3xl bg-white/80 backdrop-blur-xl border border-white shadow-[0_8px_30px_rgb(0,0,0,0.05)] overflow-hidden cursor-crosshair select-none touch-none"
      >
        {/* Soft Quadrant Pastels */}
        {/* Top-Right: Joy (Warm Peach / Amber) */}
        <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-amber-500/[0.08] pointer-events-none" />
        {/* Bottom-Right: Serene (Fresh Sage) */}
        <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-emerald-500/[0.08] pointer-events-none" />
        {/* Bottom-Left: Sadness / Depressed (Muted Sky) */}
        <div className="absolute bottom-0 left-0 w-1/2 h-1/2 bg-sky-500/[0.08] pointer-events-none" />
        {/* Top-Left: Anxiety / Agitated (Dusty Lavender Rose) */}
        <div className="absolute top-0 left-0 w-1/2 h-1/2 bg-purple-500/[0.08] pointer-events-none" />

        {/* Center Axes */}
        <div className="absolute inset-y-0 left-1/2 w-[1px] bg-slate-300/60 pointer-events-none" />
        <div className="absolute inset-x-0 top-1/2 h-[1px] bg-slate-300/60 pointer-events-none" />

        {/* Quadrant Micro-labels */}
        <span className="absolute top-3 right-3 text-[10px] font-bold text-amber-700 uppercase tracking-wider pointer-events-none bg-amber-50/80 px-2 py-0.5 rounded-full border border-amber-200/50">
          Euphoric / Joy
        </span>
        <span className="absolute bottom-3 right-3 text-[10px] font-bold text-emerald-700 uppercase tracking-wider pointer-events-none bg-emerald-50/80 px-2 py-0.5 rounded-full border border-emerald-200/50">
          Calm / Peaceful
        </span>
        <span className="absolute bottom-3 left-3 text-[10px] font-bold text-sky-700 uppercase tracking-wider pointer-events-none bg-sky-50/80 px-2 py-0.5 rounded-full border border-sky-200/50">
          Sad / Reflective
        </span>
        <span className="absolute top-3 left-3 text-[10px] font-bold text-purple-700 uppercase tracking-wider pointer-events-none bg-purple-50/80 px-2 py-0.5 rounded-full border border-purple-200/50">
          Tense / Anxious
        </span>

        {/* Interactive Puck */}
        <div
          className="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-none transition-transform duration-75"
          style={{ left: `${leftPercent}%`, top: `${topPercent}%` }}
        >
          <div className="relative flex items-center justify-center">
            <span className="absolute w-8 h-8 rounded-full bg-indigo-500/20 animate-ping" />
            <div className="w-5 h-5 rounded-full bg-indigo-600 border-2 border-white shadow-[0_2px_10px_rgba(79,70,229,0.5)] flex items-center justify-center">
              <Sparkles className="w-2.5 h-2.5 text-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between text-[11px] text-slate-500 px-1 font-medium">
        <span>← Unpleasant (-1)</span>
        <span>Drag circle anywhere to feel</span>
        <span>Pleasant (+1) →</span>
      </div>
    </div>
  );
};
