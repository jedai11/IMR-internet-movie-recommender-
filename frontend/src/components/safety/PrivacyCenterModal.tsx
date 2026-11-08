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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-white/90 backdrop-blur-2xl border border-white max-w-lg w-full p-6 space-y-6 rounded-3xl shadow-[0_20px_60px_rgba(0,0,0,0.15)] relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1 rounded-full hover:bg-slate-100 transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-indigo-50 text-indigo-600 border border-indigo-200/50">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-extrabold text-slate-900">
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
          <div className="grid grid-cols-1 gap-2 text-xs">
            <div className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/80 flex items-center justify-between">
              <div className="flex items-center gap-2.5 text-slate-700 font-medium">
                <Camera className="w-4 h-4 text-slate-400" />
                <span>Facial Emotion Recognition (Camera)</span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                Disabled / Offline
              </span>
            </div>

            <div className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/80 flex items-center justify-between">
              <div className="flex items-center gap-2.5 text-slate-700 font-medium">
                <Mic className="w-4 h-4 text-slate-400" />
                <span>Acoustic Emotion Detection (Microphone)</span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                Disabled / Offline
              </span>
            </div>

            <div className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/80 flex items-center justify-between">
              <div className="flex items-center gap-2.5 text-slate-700 font-medium">
                <EyeOff className="w-4 h-4 text-slate-400" />
                <span>Cross-Site User Ad Profiling</span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                Zero Profiling
              </span>
            </div>
          </div>
        </div>

        {/* Clear Data Action */}
        <div className="p-4 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-indigo-600" />
              Local Pseudonymous Session
            </span>
            <button
              onClick={handleClear}
              className="text-xs font-bold text-rose-600 hover:text-rose-700 flex items-center gap-1 bg-white hover:bg-rose-50 border border-rose-200/70 px-3 py-1.5 rounded-xl transition cursor-pointer shadow-sm"
            >
              <Trash2 className="w-3.5 h-3.5" />
              {cleared ? 'History Wiped ✓' : 'Clear My History'}
            </button>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            All mood vectors and interaction records are ephemeral. You can wipe your anonymous session anytime.
          </p>
        </div>
      </div>
    </div>
  );
};
