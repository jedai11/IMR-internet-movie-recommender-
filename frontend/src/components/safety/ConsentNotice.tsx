import React, { useState } from 'react';
import { ShieldCheck, Info, X } from 'lucide-react';

interface Props {
  onOpenPrivacyModal: () => void;
}

export const ConsentNotice: React.FC<Props> = ({ onOpenPrivacyModal }) => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return (
    <div className="bg-white/80 border-b border-indigo-100 backdrop-blur-md px-4 py-2 text-xs text-slate-600 flex items-center justify-between gap-4 transition-all shadow-sm">
      <div className="flex items-center gap-2.5 flex-wrap">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200/60 font-bold text-[11px]">
          <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
          Designed with Privacy in Mind
        </span>
        <span>
          MoodReel processes emotional affect solely to match movies against your stated mood. Zero biometric tracking or surveillance.
        </span>
        <button
          onClick={onOpenPrivacyModal}
          className="text-indigo-600 hover:text-indigo-800 underline font-semibold inline-flex items-center gap-1 cursor-pointer"
        >
          <Info className="w-3 h-3" />
          Transparency & Consent
        </button>
      </div>

      <button
        onClick={() => setDismissed(true)}
        className="text-slate-400 hover:text-slate-700 p-1 rounded-md hover:bg-slate-100 transition cursor-pointer"
        aria-label="Dismiss notice"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
