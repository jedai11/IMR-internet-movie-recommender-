export interface ThemePalette {
  name: string;
  themeId: 'gentle_solace' | 'tranquil_horizon' | 'warm_radiance' | 'invigorating_coral' | 'cool_balance' | 'serene_equilibrium';
  primaryHex: string;
  secondaryHex: string;
  glowHex: string;
  bgGradient1: string;
  bgGradient2: string;
  objective: string;
  badgeBg: string;
  badgeBorder: string;
  badgeText: string;
}

export const THEMES: Record<string, ThemePalette> = {
  gentle_solace: {
    name: "Gentle Solace",
    themeId: "gentle_solace",
    primaryHex: "#4A7C59", // Deep Sage
    secondaryHex: "#5B8E99", // Soft Slate Blue
    glowHex: "rgba(74, 124, 89, 0.25)",
    bgGradient1: "rgba(164, 195, 178, 0.35)",
    bgGradient2: "rgba(186, 216, 230, 0.30)",
    objective: "Alleviates emotional fatigue; evokes freshness, safety, and breathing room.",
    badgeBg: "rgba(74, 124, 89, 0.10)",
    badgeBorder: "rgba(74, 124, 89, 0.25)",
    badgeText: "#2D5A38"
  },
  tranquil_horizon: {
    name: "Tranquil Horizon",
    themeId: "tranquil_horizon",
    primaryHex: "#6D597A", // Dusty Lavender Plum
    secondaryHex: "#457B9D", // Soft Sea Blue
    glowHex: "rgba(109, 89, 122, 0.25)",
    bgGradient1: "rgba(184, 169, 201, 0.35)",
    bgGradient2: "rgba(168, 218, 220, 0.30)",
    objective: "Lowers heart rate, reduces visual clutter, induces grounding and stillness.",
    badgeBg: "rgba(109, 89, 122, 0.10)",
    badgeBorder: "rgba(109, 89, 122, 0.25)",
    badgeText: "#4A3B53"
  },
  warm_radiance: {
    name: "Warm Radiance",
    themeId: "warm_radiance",
    primaryHex: "#E76F51", // Sunburst Terracotta
    secondaryHex: "#F4A261", // Warm Amber
    glowHex: "rgba(231, 111, 81, 0.25)",
    bgGradient1: "rgba(244, 162, 97, 0.35)",
    bgGradient2: "rgba(231, 111, 81, 0.25)",
    objective: "Sustains positive arousal without harsh, fatiguing saturation.",
    badgeBg: "rgba(231, 111, 81, 0.10)",
    badgeBorder: "rgba(231, 111, 81, 0.25)",
    badgeText: "#A3432C"
  },
  invigorating_coral: {
    name: "Invigorating Coral",
    themeId: "invigorating_coral",
    primaryHex: "#E63946", // Coral Rose
    secondaryHex: "#2A9D8F", // Mint Teal
    glowHex: "rgba(230, 57, 70, 0.25)",
    bgGradient1: "rgba(240, 113, 103, 0.35)",
    bgGradient2: "rgba(42, 157, 143, 0.25)",
    objective: "Gently stimulates sensory focus and sparks curiosity.",
    badgeBg: "rgba(230, 57, 70, 0.10)",
    badgeBorder: "rgba(230, 57, 70, 0.25)",
    badgeText: "#9E2A2B"
  },
  cool_balance: {
    name: "Cool Balance",
    themeId: "cool_balance",
    primaryHex: "#2D6A4F", // Forest Moss
    secondaryHex: "#52B788", // Fresh Jade
    glowHex: "rgba(45, 106, 79, 0.25)",
    bgGradient1: "rgba(116, 198, 157, 0.35)",
    bgGradient2: "rgba(82, 183, 136, 0.25)",
    objective: "Neutralizes aggressive stimuli; replaces high-arousal reds with cooling earth tones.",
    badgeBg: "rgba(45, 106, 79, 0.10)",
    badgeBorder: "rgba(45, 106, 79, 0.25)",
    badgeText: "#1B4332"
  },
  serene_equilibrium: {
    name: "Serene Equilibrium",
    themeId: "serene_equilibrium",
    primaryHex: "#5B21B6", // Royal Iris
    secondaryHex: "#0284C7", // Cyan Sky
    glowHex: "rgba(99, 102, 241, 0.25)",
    bgGradient1: "rgba(196, 181, 253, 0.35)",
    bgGradient2: "rgba(186, 230, 253, 0.30)",
    objective: "Balanced resting state; clarity, openness, and psychological equilibrium.",
    badgeBg: "rgba(91, 33, 182, 0.08)",
    badgeBorder: "rgba(91, 33, 182, 0.25)",
    badgeText: "#4C1D95"
  }
};

/**
 * Maps emotion coordinates (valence, arousal) and optional tags/strategy
 * to the ideal Chromotherapeutic Palette.
 */
export function determineTherapeuticTheme(
  valence: number,
  arousal: number,
  tags: string[] = [],
  strategy: 'catharsis' | 'shift' = 'catharsis'
): ThemePalette {
  const lowerTags = tags.map((t) => t.toLowerCase());

  // 1. Tag-based specific targeting
  if (lowerTags.some((t) => ["angry", "frustrated", "furious", "irritated", "mad"].includes(t))) {
    return THEMES.cool_balance;
  }
  if (lowerTags.some((t) => ["sad", "depressed", "melancholy", "grief", "heartbroken", "gloomy"].includes(t))) {
    return THEMES.gentle_solace;
  }
  if (lowerTags.some((t) => ["anxious", "stressed", "overwhelmed", "tense", "panicked", "nervous"].includes(t))) {
    return THEMES.tranquil_horizon;
  }
  if (lowerTags.some((t) => ["tired", "exhausted", "drained", "bored", "lethargic"].includes(t))) {
    return strategy === 'shift' ? THEMES.invigorating_coral : THEMES.gentle_solace;
  }
  if (lowerTags.some((t) => ["happy", "joy", "excited", "energized", "cheerful", "thrilled"].includes(t))) {
    return THEMES.warm_radiance;
  }

  // 2. Circumplex coordinate mapping
  if (valence < -0.2 && arousal > 0.3) {
    return arousal > 0.65 ? THEMES.cool_balance : THEMES.tranquil_horizon;
  }
  if (valence < -0.2 && arousal <= 0.3) {
    return strategy === 'shift' ? THEMES.invigorating_coral : THEMES.gentle_solace;
  }
  if (valence >= 0.2 && arousal >= 0.2) {
    return THEMES.warm_radiance;
  }
  if (valence >= 0.2 && arousal < 0.2) {
    return THEMES.gentle_solace;
  }

  return THEMES.serene_equilibrium;
}
