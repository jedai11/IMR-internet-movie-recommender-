import React from 'react';
import { Compass, Sparkles } from 'lucide-react';

interface Props {
  strategy: 'catharsis' | 'shift';
  onChange: (strategy: 'catharsis' | 'shift') => void;
}

export const StrategySelector: React.FC<Props> = ({ strategy, onChange }) => {
  return (
    <div className="space-y-2">
      <div className="text-xs font-bold text-slate-700">
        Affective Strategy
      </div>
      <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100/80 rounded-2xl border border-slate-200/80 shadow-inner">
        <button
          onClick={() => onChange('catharsis')}
          className={`py-2 px-3 rounded-xl text-xs font-medium transition cursor-pointer flex flex-col items-center gap-0.5 ${
            strategy === 'catharsis'
              ? 'bg-white text-indigo-900 shadow-sm font-bold border border-slate-200/60'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          <div className="flex items-center gap-1.5 font-bold">
            <Compass className="w-3.5 h-3.5 text-indigo-600" />
            Catharsis Mode
          </div>
          <span className="text-[10px] text-slate-500">
            "Meet me where I am"
          </span>
        </button>

        <button
          onClick={() => onChange('shift')}
          className={`py-2 px-3 rounded-xl text-xs font-medium transition cursor-pointer flex flex-col items-center gap-0.5 ${
            strategy === 'shift'
              ? 'bg-white text-indigo-900 shadow-sm font-bold border border-slate-200/60'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          <div className="flex items-center gap-1.5 font-bold">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            Shift Mode
          </div>
          <span className="text-[10px] text-slate-500">
            "Gently lift or soothe me"
          </span>
        </button>
      </div>
      <div className="text-[11px] text-slate-500 italic px-1">
        {strategy === 'catharsis'
          ? 'Deeply validates and mirrors your current state with matching cinematic intensity.'
          : 'Calculates an emotional regulation vector to gently transition toward warmth and calm equilibrium.'}
      </div>
    </div>
  );
};
