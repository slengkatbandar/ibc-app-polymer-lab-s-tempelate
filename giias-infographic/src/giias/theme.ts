// Palette lifted from the GIIAS visitor infographic.
export const CREAM = "#F8E3C6";
export const DARK_TEAL = "#17393B";
export const PINK = "#EA3B67";
export const TEAL = "#34BFA6";
export const YELLOW = "#F5C63C";
export const ORANGE = "#EF9040";
export const YEAR_GREY = "#90A9A9";
export const COVID_RED = "#FF3B30";

export const FACE_COLORS = [PINK, YELLOW, TEAL, ORANGE];

export type YearDatum = {
  year: string;
  value: number;
  note?: string;
};

// One person icon represents 10.000 visitors.
export const PEOPLE_PER_ICON = 10000;
export const ICONS_PER_ROW = 6;

export const YEARS: YearDatum[] = [
  { year: "2021", value: 293252, note: "Dibatasi penanganan\nCovid-19" },
  { year: "2022", value: 385487 },
  { year: "2023", value: 462291 },
  { year: "2024", value: 475084 },
  { year: "2025", value: 485569 },
  { year: "2026", value: 496378 },
];

export const MAX_VALUE = 496378;

// Deterministic scatter so the face colours look random but render identically
// on every frame and on every machine.
export const pickFace = (barIndex: number, iconIndex: number) => {
  const hash = (barIndex * 977 + iconIndex * 131 + 7) ^ (iconIndex << 3);
  return FACE_COLORS[Math.abs(hash) % FACE_COLORS.length];
};

export const hasBun = (barIndex: number, iconIndex: number) => {
  return (barIndex * 31 + iconIndex * 17) % 5 === 0;
};

export const formatId = (value: number) => {
  return Math.round(value).toLocaleString("id-ID");
};
