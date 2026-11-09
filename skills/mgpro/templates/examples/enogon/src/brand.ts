/** Enogon's own tokens, copied from enogon.com's stylesheet (never invented). */
export const C = {
  paper: "#ffffff",
  ink: "#000000",
  graphit: "#5c5c5c",
  line: "#e2e4e8",
  lineStrong: "#9aa3ad",
  apricot100: "#fee6d8",
  apricot300: "#efb694",
  apricot400: "#e7a780",
  apricot500: "#de8f5e",
  apricot600: "#bd703f",
  tuerkis100: "#e5f3f6",
  tuerkis200: "#cde7eb",
  tuerkis300: "#9bc7ce",
  tuerkis500: "#1e7f8c",
  tuerkis700: "#045e68",
} as const;

export const DISPLAY = "'Inter Tight', 'Inter', system-ui, sans-serif";
export const MONO = "'IBM Plex Mono', ui-monospace, monospace";
export const LOGO = "'Tektur', system-ui, sans-serif";

/** The cube from the site's wordmark SVG (viewBox -2 -2 107.06 123). */
export const CUBE = {
  top: "M0,29.75 L51.53,0 L103.06,29.75 L51.53,59.5 Z",
  right: "M51.53,59.5 L103.06,29.75 L103.06,89.25 L51.53,119 Z",
  left: "M0,29.75 L51.53,59.5 L51.53,119 L0,89.25 Z",
};

/** German number format: 2,87 */
export const de = (v: number, digits = 2) => v.toFixed(digits).replace(".", ",");
