/* Runtime catalog compatibility; core state and storage load before this script. */
const GamesCatalog = (typeof FULL_GAMES_CATALOG !== 'undefined' && Array.isArray(FULL_GAMES_CATALOG) && FULL_GAMES_CATALOG.length > 0)
    ? FULL_GAMES_CATALOG
    : (typeof window !== 'undefined' && window.GamesCatalog && window.GamesCatalog.length > 0)
        ? window.GamesCatalog
        : [];

