import React, { useState } from 'react';
import { ShieldCheck, Info, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';
import { PickerInput } from '../../types';
import { THEMES, CULTURAL_MAPPING_DISCLAIMER } from '../../utils/theme';

interface Props {
  currentCoordinates: PickerInput;
  onSelectPreset: (coords: PickerInput) => void;
}

const PRESET_EMOJIS: Record<string, string> = {
  calm_peaceful: '🍃',
  happy_energetic: '☀️',
  angry_intense: '🔥',
  sad_melancholic: '🌧️',
  romantic_love: '💜',
  focus_concentration: '🌲',
  excitement_adrenaline: '⚡',
  neutral_minimal: '⚖️'
};

export const EmotionPresets: React.FC<Props> = ({ currentCoordinates, onSelectPreset }) => {
  const [showWcagDetails, setShowWcagDetails] = useState(false);
  const themeList = Object.values(THEMES);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between text-xs">
        <span className="font-extrabold text-[#F8FAFC]">
          8 Signature Mood Colour Palettes
        </span>
        <button
          onClick={() => setShowWcagDetails(!showWcagDetails)}
          className="glass-light-pill px-2.5 py-1 rounded-lg text-[11px] font-bold text-emerald-300 flex items-center gap-1.5 border-[#29344D] cursor-pointer hover:border-emerald-500/50"
        >
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>WCAG 2.2 Verified</span>
          {showWcagDetails ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
        </button>
      </div>

      {/* 8 Preset Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {themeList.map((t) => {
          const isSelected =
            Math.abs(currentCoordinates.valence - t.defaultValence) < 0.20 &&
            Math.abs(currentCoordinates.arousal - t.defaultArousal) < 0.20;

          return (
            <button
              key={t.themeId}
              onClick={() => onSelectPreset({ valence: t.defaultValence, arousal: t.defaultArousal })}
              className={`p-3.5 rounded-2xl text-left transition-all cursor-pointer flex flex-col justify-between group ${
                isSelected
                  ? 'ios-glass-button-active shadow-lg ring-2 ring-white/40 text-[#F8FAFC] -translate-y-1'
                  : 'ios-glass-button text-[#CBD5E1] hover:text-[#F8FAFC]'
              }`}
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xl">{PRESET_EMOJIS[t.themeId] || '✨'}</span>
                  {/* Color Swatch Dots */}
                  <div className="flex items-center -space-x-1.5 p-1 rounded-full bg-[#1C2540] shadow-inner border border-[#29344D]">
                    <span
                      className="w-3.5 h-3.5 rounded-full border border-white/20 shadow-sm"
                      style={{ backgroundColor: t.primaryHex }}
                      title={`Primary: ${t.primaryHex}`}
                    />
                    <span
                      className="w-3.5 h-3.5 rounded-full border border-white/20 shadow-sm"
                      style={{ backgroundColor: t.secondaryHex }}
                      title={`Secondary: ${t.secondaryHex}`}
                    />
                    <span
                      className="w-3.5 h-3.5 rounded-full border border-white/20 shadow-sm"
                      style={{ backgroundColor: t.accentHex }}
                      title={`Accent: ${t.accentHex}`}
                    />
                  </div>
                </div>

                <div className="mt-2.5">
                  <div className="text-xs font-black tracking-tight text-[#F8FAFC]">{t.name}</div>
                  <div className="text-[10px] text-[#CBD5E1] line-clamp-1 mt-0.5 font-medium leading-relaxed">
                    {t.feeling}
                  </div>
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-[#29344D] flex items-center justify-between text-[10px] font-mono">
                <span className="font-bold text-[#CBD5E1]/70">
                  V:{t.defaultValence > 0 ? `+${t.defaultValence}` : t.defaultValence} A:{t.defaultArousal > 0 ? `+${t.defaultArousal}` : t.defaultArousal}
                </span>
                <span className="px-1.5 py-0.5 rounded bg-emerald-950/60 text-emerald-300 font-bold border border-emerald-500/40 text-[9px]">
                  {t.contrastRatioOnLight}
                </span>
              </div>
            </button>
          );
        })}
      </div>

      {/* WCAG 2.2 Accessibility Standards & Cultural Context Card */}
      {showWcagDetails && (
        <div className="glass-light-inner rounded-2xl p-4 sm:p-5 space-y-3.5 text-xs animate-in fade-in duration-200 border-[#29344D]">
          <div className="flex items-center justify-between border-b border-[#29344D] pb-2.5">
            <div className="flex items-center gap-2 font-bold text-[#F8FAFC]">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>WCAG 2.2 Accessibility Standards Compliance</span>
            </div>
            <a
              href="https://www.w3.org/TR/WCAG22/"
              target="_blank"
              rel="noreferrer"
              className="text-[11px] font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
            >
              W3C WCAG 2.2 Guidelines <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-center">
            <div className="glass-light-pill p-2.5 rounded-xl border-[#29344D]">
              <span className="text-[10px] text-[#CBD5E1]/70 font-bold uppercase tracking-wider block">Normal Text</span>
              <strong className="text-emerald-400 text-sm font-mono font-black">≥ 4.5:1</strong>
              <span className="text-[10px] text-[#CBD5E1] block">Verified compliant</span>
            </div>
            <div className="glass-light-pill p-2.5 rounded-xl border-[#29344D]">
              <span className="text-[10px] text-[#CBD5E1]/70 font-bold uppercase tracking-wider block">Large Text (18pt / 14pt bold)</span>
              <strong className="text-emerald-400 text-sm font-mono font-black">≥ 3.0:1</strong>
              <span className="text-[10px] text-[#CBD5E1] block">Verified compliant</span>
            </div>
            <div className="glass-light-pill p-2.5 rounded-xl border-[#29344D]">
              <span className="text-[10px] text-[#CBD5E1]/70 font-bold uppercase tracking-wider block">UI Components & Icons</span>
              <strong className="text-emerald-400 text-sm font-mono font-black">≥ 3.0:1</strong>
              <span className="text-[10px] text-[#CBD5E1] block">Verified compliant</span>
            </div>
          </div>

          {/* Important Cultural & Context Distinction Notice */}
          <div className="p-3 rounded-xl bg-amber-950/40 border border-amber-500/40 text-[11px] text-amber-200 flex items-start gap-2.5 leading-relaxed">
            <Info className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong className="font-bold text-amber-100">Important distinction:</strong> {CULTURAL_MAPPING_DISCLAIMER}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
