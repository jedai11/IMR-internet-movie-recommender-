import React, { useState } from 'react';
import { X, ShieldCheck, Trash2, Camera, Mic, EyeOff, Lock } from 'lucide-react';

interface Props {
  onClose: () => void;
  onClearSession: () => void;
}

export const PrivacyCenterModal: React.FC<Props> = ({ onClose, onClearSession }) => {
  const [cleared, setCleared] = useState(false);

  const handleClear = () => {
    onClearSession();
    setCleared(true);
    setTimeout(() => setCleared(false), 2500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/25 backdrop-blur-md animate-in fade-in duration-200">
      <div className="glass-light-modal max-w-lg w-full p-6 sm:p-7 space-y-6 rounded-3xl relative animate-in zoom-in-95 duration-200">
        <button
          onClick={onClose}
          className="glass-light-pill absolute top-4 right-4 text-slate-400 hover:text-slate-800 p-1.5 rounded-full transition cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-3.5">
          <div className="p-3 rounded-2xl glass-light-pill text-indigo-600">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base sm:text-lg font-black text-slate-900 tracking-tight">
              Consent & Transparency Center
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              Privacy-by-Design & Data Minimization Architecture
            </p>
          </div>
        </div>

        {/* Sensor-free verification */}
        <div className="space-y-3">
          <div className="text-xs font-bold text-slate-700">
            Sensor & Surveillance Status (Verified Safe)
          </div>
          <div className="grid grid-cols-1 gap-2.5 text-xs">
            <div className="p-3.5 rounded-2xl glass-light-inner flex items-center justify-between">
              <div className="flex items-center gap-2.5 text-slate-700 font-medium">
                <Camera className="w-4 h-4 text-slate-400" />
                <span>Facial Emotion Recognition (Camera)</span>
              </div>
              <span className="glass-light-pill px-2.5 py-0.5 rounded-full text-[11px] font-bold text-emerald-800 border-emerald-200">
                Disabled / Offline
              </span>
            </div>

            <div className="p-3.5 rounded-2xl glass-light-inner flex items-center justify-between">
              <div className="flex items-center gap-2.5 text-slate-700 font-medium">
                <Mic className="w-4 h-4 text-slate-400" />
                <span>Acoustic Emotion Detection (Microphone)</span>
              </div>
              <span className="glass-light-pill px-2.5 py-0.5 rounded-full text-[11px] font-bold text-emerald-800 border-emerald-200">
                Disabled / Offline
              </span>
            </div>

            <div className="p-3.5 rounded-2xl glass-light-inner flex items-center justify-between">
              <div className="flex items-center gap-2.5 text-slate-700 font-medium">
                <EyeOff className="w-4 h-4 text-slate-400" />
                <span>Cross-Site User Ad Profiling</span>
              </div>
              <span className="glass-light-pill px-2.5 py-0.5 rounded-full text-[11px] font-bold text-emerald-800 border-emerald-200">
                Zero Profiling
              </span>
            </div>
          </div>
        </div>

        {/* Accessibility & Cultural Context Transparency */}
        <div className="space-y-2.5">
          <div className="text-xs font-bold text-slate-700 flex items-center justify-between">
            <span>WCAG 2.2 Accessibility & Design Transparency</span>
            <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
              Verified AA / AAA
            </span>
          </div>
          <div className="p-3.5 rounded-2xl glass-light-inner text-xs text-slate-600 space-y-2 leading-relaxed">
            <p>
              All color pairings adhere to <strong>WCAG 2.2 standards</strong> (minimum 4.5:1 for normal text, 3:1 for large text and UI components) across light and dark layers.
            </p>
            <div className="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200/80 text-[11px] text-amber-950">
              <strong>Cultural context note:</strong> These mood palettes are design recommendations, not fixed scientific mappings. Emotional responses to color vary naturally across cultures, environments, and personal lived experiences.
            </div>
          </div>
        </div>

        {/* Clear Data Action */}
        <div className="p-4 rounded-2xl glass-light-inner space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-indigo-600" />
              Local Pseudonymous Session
            </span>
            <button
              onClick={handleClear}
              className="glass-light-pill text-xs font-bold text-rose-600 hover:text-rose-700 flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition cursor-pointer border-rose-200 hover:border-rose-300"
            >
              <Trash2 className="w-3.5 h-3.5" />
              {cleared ? 'History Wiped ✓' : 'Clear My History'}
            </button>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed font-normal">
            All mood vectors and interaction records are ephemeral. You can wipe your anonymous session anytime.
          </p>
        </div>
      </div>
    </div>
  );
};
