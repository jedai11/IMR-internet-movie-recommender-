import React from 'react';
import { Compass, Sparkles } from 'lucide-react';

interface Props {
  strategy: 'catharsis' | 'shift';
  onChange: (strategy: 'catharsis' | 'shift') => void;
}

export const StrategySelector: React.FC<Props> = ({ strategy, onChange }) => {
  return (
    <div className="space-y-2.5">
      <div className="text-xs font-bold text-[#F8FAFC]">
        Affective Strategy
      </div>
      <div className="grid grid-cols-2 gap-2 p-1.5 glass-light-inner rounded-2xl border-[#29344D]">
        <button
          onClick={() => onChange('catharsis')}
          className={`py-2.5 px-3.5 rounded-xl text-xs font-medium transition cursor-pointer flex flex-col items-center gap-1 border border-transparent ${
            strategy === 'catharsis'
              ? 'glass-light-pill-active text-[#F8FAFC] font-black border-cyan-400'
              : 'text-[#CBD5E1] hover:text-[#F8FAFC]'
          }`}
        >
          <div className="flex items-center gap-1.5 font-bold">
            <Compass className="w-3.5 h-3.5 text-cyan-400" />
            Catharsis Mode
          </div>
          <span className="text-[10px] text-[#CBD5E1]/70 font-medium">
            "Meet me where I am"
          </span>
        </button>

        <button
          onClick={() => onChange('shift')}
          className={`py-2.5 px-3.5 rounded-xl text-xs font-medium transition cursor-pointer flex flex-col items-center gap-1 border border-transparent ${
            strategy === 'shift'
              ? 'glass-light-pill-active text-[#F8FAFC] font-black border-cyan-400'
              : 'text-[#CBD5E1] hover:text-[#F8FAFC]'
          }`}
        >
          <div className="flex items-center gap-1.5 font-bold">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            Shift Mode
          </div>
          <span className="text-[10px] text-[#CBD5E1]/70 font-medium">
            "Gently lift or soothe me"
          </span>
        </button>
      </div>
      <div className="text-[11px] text-[#CBD5E1] italic px-1 font-medium">
        {strategy === 'catharsis'
          ? 'Deeply validates and mirrors your current state with matching cinematic intensity.'
          : 'Calculates an emotional regulation vector to gently transition toward warmth and calm equilibrium.'}
      </div>
    </div>
  );
};
