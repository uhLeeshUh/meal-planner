// Units enum matching backend app.schemas.enums.Unit
// This ensures consistency between frontend and backend
export const UNITS = [
  'each',      // Default for countable items
  'cup',
  'tablespoon',
  'teaspoon',
  'gram',
  'kilogram',
  'ounce',
  'pound',
  'gallon',
  'milliliter',
  'liter',
  'pint',
  'quart',
  'can',
  'bunch',
  'package',
] as const;

// Type for unit values
export type Unit = typeof UNITS[number];

// Helper function to get a display label for a unit (optional, for better UX)
export const getUnitLabel = (unit: string): string => {
  const labels: Record<string, string> = {
    each: 'each',
    cup: 'cup',
    tablespoon: 'tbsp',
    teaspoon: 'tsp',
    gram: 'g',
    kilogram: 'kg',
    ounce: 'oz',
    pound: 'lb',
    gallon: 'gal',
    milliliter: 'ml',
    liter: 'L',
    pint: 'pt',
    quart: 'qt',
    can: 'can',
    bunch: 'bunch',
    package: 'pkg',
  };
  return labels[unit] || unit;
};

