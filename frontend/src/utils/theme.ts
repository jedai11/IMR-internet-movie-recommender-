export interface ThemePalette {
  name: string;
  themeId:
    | 'calm_peaceful'
    | 'happy_energetic'
    | 'angry_intense'
    | 'sad_melancholic'
    | 'romantic_love'
    | 'focus_concentration'
    | 'excitement_adrenaline'
    | 'neutral_minimal';
  primaryHex: string;
  secondaryHex: string;
  accentHex: string;
  backgroundHex: string;
  textHex: string;
  feeling: string;
  glowHex: string;
  bgGradient1: string;
  bgGradient2: string;
  badgeBg: string;
  badgeBorder: string;
  badgeText: string;
  // WCAG 2.2 Compliant Properties (>= 4.5:1 for normal text, >= 3:1 for large text / UI components)
  wcagTextOnLight: string;
  wcagButtonText: string;
  contrastRatioOnLight: string;
  contrastRatioOnDark: string;
  contrastRatioButton: string;
  wcagLevel: 'AAA' | 'AA';
  culturalNotice: string;
  defaultValence: number;
  defaultArousal: number;
}

export const CULTURAL_MAPPING_DISCLAIMER =
  'Important distinction: These palettes are mood-inspired design recommendations, not scientifically fixed emotional mappings. Individual responses to colours vary by culture, context and personal experience.';

export const THEMES: Record<string, ThemePalette> = {
  calm_peaceful: {
    name: 'Calm / Peaceful',
    themeId: 'calm_peaceful',
    primaryHex: '#1B263B', // Midnight Blue
    secondaryHex: '#415A77', // Muted Denim
    accentHex: '#A8DADC', // Ice Cyan
    backgroundHex: '#0D1B2A', // Deep Abyss Navy
    textHex: '#E0E1DD', // Soft Bone
    feeling: 'Peace, stability, mental clarity.',
    glowHex: 'rgba(168, 218, 220, 0.35)',
    bgGradient1: 'rgba(65, 90, 119, 0.30)',
    bgGradient2: 'rgba(168, 218, 220, 0.25)',
    badgeBg: 'rgba(27, 38, 59, 0.08)',
    badgeBorder: 'rgba(65, 90, 119, 0.35)',
    badgeText: '#1B263B',
    wcagTextOnLight: '#1B263B', // 15.14:1 (WCAG AAA)
    wcagButtonText: '#FFFFFF', // 15.14:1 (WCAG AAA)
    contrastRatioOnLight: '15.1:1',
    contrastRatioOnDark: '13.2:1',
    contrastRatioButton: '15.1:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: 0.75,
    defaultArousal: -0.60
  },
  happy_energetic: {
    name: 'Happy / Energetic',
    themeId: 'happy_energetic',
    primaryHex: '#FFB703', // Amber Gold
    secondaryHex: '#FB8500', // Vivid Tangerine
    accentHex: '#FFD166', // Soft Sunbeam
    backgroundHex: '#241A12', // Warm Obsidian Wood
    textHex: '#FFF4DC', // Light Buttercream
    feeling: 'Optimism, excitement, enthusiasm.',
    glowHex: 'rgba(255, 183, 3, 0.35)',
    bgGradient1: 'rgba(251, 133, 0, 0.25)',
    bgGradient2: 'rgba(255, 209, 102, 0.30)',
    badgeBg: 'rgba(255, 183, 3, 0.16)',
    badgeBorder: 'rgba(184, 93, 0, 0.35)',
    badgeText: '#78350F', // Warm Deep Amber (7.2:1, WCAG AAA)
    wcagTextOnLight: '#78350F', // 7.2:1 (WCAG AAA)
    wcagButtonText: '#241A12', // Dark text on amber (9.8:1, WCAG AAA)
    contrastRatioOnLight: '7.2:1',
    contrastRatioOnDark: '15.6:1',
    contrastRatioButton: '9.8:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: 0.85,
    defaultArousal: 0.65
  },
  angry_intense: {
    name: 'Angry / Intense',
    themeId: 'angry_intense',
    primaryHex: '#E63946', // Fiery Crimson
    secondaryHex: '#9D0208', // Deep Oxblood
    accentHex: '#FF6B6B', // Vibrant Coral Rose
    backgroundHex: '#190A0C', // Midnight Bloodwood
    textHex: '#F8EDED', // Ash White
    feeling: 'Power, aggression, urgency.',
    glowHex: 'rgba(230, 57, 70, 0.35)',
    bgGradient1: 'rgba(157, 2, 8, 0.25)',
    bgGradient2: 'rgba(255, 107, 107, 0.25)',
    badgeBg: 'rgba(230, 57, 70, 0.10)',
    badgeBorder: 'rgba(157, 2, 8, 0.30)',
    badgeText: '#9D0208', // 8.59:1 (WCAG AAA)
    wcagTextOnLight: '#9D0208', // 8.59:1 (WCAG AAA)
    wcagButtonText: '#FFFFFF', // 8.59:1 (WCAG AAA)
    contrastRatioOnLight: '8.6:1',
    contrastRatioOnDark: '16.8:1',
    contrastRatioButton: '8.6:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: -0.75,
    defaultArousal: 0.85
  },
  sad_melancholic: {
    name: 'Sad / Melancholic',
    themeId: 'sad_melancholic',
    primaryHex: '#526D82', // Slate Harbor
    secondaryHex: '#334756', // Storm Fog
    accentHex: '#9DB4C0', // Misty Blue
    backgroundHex: '#101820', // Nocturne Deep Blue
    textHex: '#DCE5EA', // Whispering Gray
    feeling: 'Reflection, nostalgia, loneliness.',
    glowHex: 'rgba(157, 180, 192, 0.30)',
    bgGradient1: 'rgba(82, 109, 130, 0.25)',
    bgGradient2: 'rgba(157, 180, 192, 0.20)',
    badgeBg: 'rgba(82, 109, 130, 0.10)',
    badgeBorder: 'rgba(51, 71, 86, 0.30)',
    badgeText: '#2C3E50', // 11.0:1 (WCAG AAA)
    wcagTextOnLight: '#2C3E50', // 11.0:1 (WCAG AAA)
    wcagButtonText: '#FFFFFF', // 9.65:1 (WCAG AAA)
    contrastRatioOnLight: '11.0:1',
    contrastRatioOnDark: '14.0:1',
    contrastRatioButton: '9.7:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: -0.65,
    defaultArousal: -0.50
  },
  romantic_love: {
    name: 'Romantic / Love',
    themeId: 'romantic_love',
    primaryHex: '#9D4EDD', // Royal Violet Amethyst
    secondaryHex: '#C77DFF', // Soft Orchid
    accentHex: '#FFAFCC', // Tender Blossom Pink
    backgroundHex: '#190F24', // Cosmic Velvet Plum
    textHex: '#FFF0F5', // Lavender Rose Mist
    feeling: 'Affection, intimacy, warmth.',
    glowHex: 'rgba(199, 125, 255, 0.35)',
    bgGradient1: 'rgba(157, 78, 221, 0.25)',
    bgGradient2: 'rgba(255, 175, 204, 0.25)',
    badgeBg: 'rgba(157, 78, 221, 0.10)',
    badgeBorder: 'rgba(157, 78, 221, 0.30)',
    badgeText: '#5B1E94', // 10.2:1 (WCAG AAA)
    wcagTextOnLight: '#5B1E94', // 10.2:1 (WCAG AAA)
    wcagButtonText: '#FFFFFF', // 4.60:1 (WCAG AA)
    contrastRatioOnLight: '10.2:1',
    contrastRatioOnDark: '16.8:1',
    contrastRatioButton: '4.6:1',
    wcagLevel: 'AA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: 0.80,
    defaultArousal: 0.10
  },
  focus_concentration: {
    name: 'Focus / Concentration',
    themeId: 'focus_concentration',
    primaryHex: '#2D6A4F', // Forest Pine
    secondaryHex: '#40916C', // Deep Mint Jade
    accentHex: '#95D5B2', // Pale Celadon
    backgroundHex: '#081C15', // Midnight Woodland
    textHex: '#E8F5E9', // Pale Spruce
    feeling: 'Balance, discipline, concentration.',
    glowHex: 'rgba(149, 213, 178, 0.35)',
    bgGradient1: 'rgba(45, 106, 79, 0.25)',
    bgGradient2: 'rgba(149, 213, 178, 0.22)',
    badgeBg: 'rgba(45, 106, 79, 0.10)',
    badgeBorder: 'rgba(64, 145, 108, 0.35)',
    badgeText: '#1B4332', // 11.1:1 (WCAG AAA)
    wcagTextOnLight: '#1B4332', // 11.1:1 (WCAG AAA)
    wcagButtonText: '#FFFFFF', // 6.39:1 (WCAG AAA)
    contrastRatioOnLight: '11.1:1',
    contrastRatioOnDark: '15.7:1',
    contrastRatioButton: '6.4:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: 0.30,
    defaultArousal: -0.10
  },
  excitement_adrenaline: {
    name: 'Excitement / Adrenaline',
    themeId: 'excitement_adrenaline',
    primaryHex: '#00B4D8', // Electric Cyan
    secondaryHex: '#0077B6', // Deep Ocean Blue
    accentHex: '#90E0EF', // Frosted Aqua
    backgroundHex: '#03045E', // Deep Sea Midnight
    textHex: '#CAF0F8', // Luminous Ice
    feeling: 'Movement, stimulation, adventure.',
    glowHex: 'rgba(0, 180, 216, 0.35)',
    bgGradient1: 'rgba(0, 119, 182, 0.25)',
    bgGradient2: 'rgba(144, 224, 239, 0.25)',
    badgeBg: 'rgba(0, 180, 216, 0.12)',
    badgeBorder: 'rgba(0, 119, 182, 0.35)',
    badgeText: '#005F73', // 7.28:1 (WCAG AAA)
    wcagTextOnLight: '#005F73', // 7.28:1 (WCAG AAA)
    wcagButtonText: '#03045E', // 7.20:1 (WCAG AAA)
    contrastRatioOnLight: '7.3:1',
    contrastRatioOnDark: '14.7:1',
    contrastRatioButton: '7.2:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: 0.80,
    defaultArousal: 0.90
  },
  neutral_minimal: {
    name: 'Neutral / Minimal',
    themeId: 'neutral_minimal',
    primaryHex: '#6C757D', // Balanced Graphite
    secondaryHex: '#495057', // Charcoal Slate
    accentHex: '#ADB5BD', // Silver Sheen
    backgroundHex: '#121212', // Pure Minimal Void
    textHex: '#F8F9FA', // Clean Snow
    feeling: 'Simplicity, neutrality, sophistication.',
    glowHex: 'rgba(173, 181, 189, 0.30)',
    bgGradient1: 'rgba(108, 117, 125, 0.22)',
    bgGradient2: 'rgba(173, 181, 189, 0.20)',
    badgeBg: 'rgba(108, 117, 125, 0.10)',
    badgeBorder: 'rgba(108, 117, 125, 0.30)',
    badgeText: '#343A40', // 11.5:1 (WCAG AAA)
    wcagTextOnLight: '#343A40', // 11.5:1 (WCAG AAA)
    wcagButtonText: '#FFFFFF', // 8.18:1 (WCAG AAA)
    contrastRatioOnLight: '11.5:1',
    contrastRatioOnDark: '17.8:1',
    contrastRatioButton: '8.2:1',
    wcagLevel: 'AAA',
    culturalNotice: CULTURAL_MAPPING_DISCLAIMER,
    defaultValence: 0.00,
    defaultArousal: 0.00
  }
};

/**
 * Maps emotion coordinates (valence, arousal) and optional tags/strategy
 * to one of the 8 signature Mood Palettes.
 */
export function determineTherapeuticTheme(
  valence: number,
  arousal: number,
  tags: string[] = [],
  strategy: 'catharsis' | 'shift' = 'catharsis'
): ThemePalette {
  const lowerTags = tags.map((t) => t.toLowerCase());

  // 1. Direct emotional keyword matching
  if (lowerTags.some((t) => ['angry', 'mad', 'furious', 'rage', 'frustrated', 'intense', 'power', 'irritated'].includes(t))) {
    return strategy === 'shift' ? THEMES.focus_concentration : THEMES.angry_intense;
  }

  if (lowerTags.some((t) => ['love', 'romantic', 'romance', 'affection', 'intimacy', 'warmth', 'tender', 'heart', 'dating'].includes(t))) {
    return THEMES.romantic_love;
  }

  if (lowerTags.some((t) => ['sad', 'melancholic', 'melancholy', 'depressed', 'grief', 'lonely', 'loneliness', 'gloomy', 'crying', 'nostalgia', 'nostalgic', 'reflective'].includes(t))) {
    return strategy === 'shift' ? THEMES.calm_peaceful : THEMES.sad_melancholic;
  }

  if (lowerTags.some((t) => ['focus', 'concentrate', 'concentration', 'work', 'study', 'discipline', 'clarity', 'mindful'].includes(t))) {
    return THEMES.focus_concentration;
  }

  if (lowerTags.some((t) => ['adrenaline', 'hyped', 'thrill', 'thrilled', 'action', 'adventure', 'stimulation', 'wild', 'pumping'].includes(t))) {
    return THEMES.excitement_adrenaline;
  }

  if (lowerTags.some((t) => ['happy', 'joy', 'joyful', 'excited', 'optimism', 'optimistic', 'cheerful', 'fun', 'laugh'].includes(t))) {
    return THEMES.happy_energetic;
  }

  if (lowerTags.some((t) => ['calm', 'peaceful', 'relaxed', 'peace', 'serene', 'tranquil', 'cozy', 'rest', 'exhausted', 'tired'].includes(t))) {
    return THEMES.calm_peaceful;
  }

  if (lowerTags.some((t) => ['neutral', 'minimal', 'bored', 'numb', 'blank', 'fine', 'okay'].includes(t))) {
    return THEMES.neutral_minimal;
  }

  // 2. Circumplex Coordinate Vector Classification
  // High Valence, High Arousal
  if (valence >= 0.25 && arousal >= 0.25) {
    return arousal > 0.75 ? THEMES.excitement_adrenaline : THEMES.happy_energetic;
  }

  // High Valence, Low Arousal
  if (valence >= 0.25 && arousal < 0.25) {
    return valence > 0.7 && arousal > -0.2 ? THEMES.romantic_love : THEMES.calm_peaceful;
  }

  // Low Valence, High Arousal
  if (valence <= -0.25 && arousal >= 0.25) {
    return strategy === 'shift' ? THEMES.focus_concentration : THEMES.angry_intense;
  }

  // Low Valence, Low Arousal
  if (valence <= -0.25 && arousal < 0.25) {
    return strategy === 'shift' ? THEMES.calm_peaceful : THEMES.sad_melancholic;
  }

  // Balanced Center
  if (Math.abs(valence) < 0.25 && Math.abs(arousal) < 0.25) {
    return THEMES.neutral_minimal;
  }

  return THEMES.focus_concentration;
}
