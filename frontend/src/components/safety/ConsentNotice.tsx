import React, { useState } from 'react';
import { ShieldCheck, Info, X } from 'lucide-react';

interface Props {
  onOpenPrivacyModal: () => void;
}

export const ConsentNotice: React.FC<Props> = ({ onOpenPrivacyModal }) => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return (
    <div className="glass-light-header px-4 py-2 text-xs text-[#CBD5E1] flex items-center justify-between gap-4 transition-all border-b border-[#29344D]">
      <div className="flex items-center gap-2.5 flex-wrap">
        <span className="glass-light-pill inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-cyan-300 font-bold text-[11px] border-[#29344D] bg-[#141B2D]">
          <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
          Designed with Privacy in Mind
        </span>
        <span className="font-medium text-[#CBD5E1]">
          IMR processes emotional affect solely to match movies against your stated mood. Zero biometric tracking or surveillance.
        </span>
        <button
          onClick={onOpenPrivacyModal}
          className="text-cyan-400 hover:text-cyan-300 underline font-bold inline-flex items-center gap-1 cursor-pointer"
        >
          <Info className="w-3.5 h-3.5" />
          Transparency & Consent
        </button>
      </div>

      <button
        onClick={() => setDismissed(true)}
        className="glass-light-pill text-[#CBD5E1] hover:text-[#F8FAFC] p-1 rounded-lg transition cursor-pointer border-[#29344D]"
        aria-label="Dismiss notice"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
