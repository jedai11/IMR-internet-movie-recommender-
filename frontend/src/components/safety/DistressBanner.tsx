import React from 'react';
import { HeartPulse, PhoneCall, ExternalLink, Sparkles } from 'lucide-react';
import { DistressResponse } from '../../types';

interface Props {
  distress: DistressResponse;
  onSelectGentleContent: () => void;
}

export const DistressBanner: React.FC<Props> = ({ distress, onSelectGentleContent }) => {
  return (
    <div className="bg-rose-50/90 border border-rose-200/80 rounded-3xl p-6 backdrop-blur-xl shadow-[0_10px_30px_rgba(244,63,94,0.08)] space-y-5 animate-in fade-in duration-300">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-rose-100 rounded-2xl text-rose-600 shadow-sm">
          <HeartPulse className="w-7 h-7 text-rose-600 animate-pulse" />
        </div>
        <div className="space-y-1 flex-1">
          <h3 className="text-lg font-bold text-rose-900">
            Immediate Support & Caring Resources
          </h3>
          <p className="text-sm text-rose-800/80 leading-relaxed">
            {distress.message}
          </p>
        </div>
      </div>

      {/* Helplines (International Coverage) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {distress.helplines.map((hl, idx) => (
          <div
            key={idx}
            className="bg-white/90 border border-rose-100 rounded-2xl p-4 flex flex-col justify-between shadow-sm hover:shadow transition"
          >
            <div>
              <div className="font-bold text-rose-950 text-sm">{hl.name}</div>
              <div className="text-xs text-rose-700 mt-1 flex items-center gap-1.5 font-mono font-semibold">
                <PhoneCall className="w-3.5 h-3.5 text-rose-600" />
                {hl.contact}
              </div>
            </div>
            {hl.url && (
              <a
                href={hl.url}
                target="_blank"
                rel="noreferrer"
                className="mt-3 text-xs text-indigo-700 hover:text-indigo-900 flex items-center gap-1 font-bold"
              >
                Online Confidential Help <ExternalLink className="w-3 h-3" />
              </a>
            )}
          </div>
        ))}
      </div>

      {/* Gentle Calming Cinema Alternative */}
      {distress.gentle_content_option && (
        <div className="bg-white/80 border border-indigo-100 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm">
          <div className="text-xs text-slate-700 space-y-1">
            <span className="font-bold text-indigo-900 flex items-center gap-1.5 text-sm">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              {distress.gentle_content_option.title}
            </span>
            <p className="text-slate-600">
              {distress.gentle_content_option.description}
            </p>
          </div>
          <button
            onClick={onSelectGentleContent}
            className="whitespace-nowrap px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-md shadow-indigo-600/20 transition cursor-pointer"
          >
            Switch to Calming Films
          </button>
        </div>
      )}
    </div>
  );
};
