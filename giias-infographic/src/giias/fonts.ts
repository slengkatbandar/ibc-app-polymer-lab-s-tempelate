import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Poppins is vendored into public/fonts so rendering never depends on a
// network fetch to fonts.gstatic.com.
export const POPPINS = "Poppins";

await Promise.all([
  loadFont({
    family: POPPINS,
    url: staticFile("fonts/poppins-400.woff2"),
    weight: "400",
  }),
  loadFont({
    family: POPPINS,
    url: staticFile("fonts/poppins-600.woff2"),
    weight: "600",
  }),
  loadFont({
    family: POPPINS,
    url: staticFile("fonts/poppins-700.woff2"),
    weight: "700",
  }),
  loadFont({
    family: POPPINS,
    url: staticFile("fonts/poppins-800.woff2"),
    weight: "800",
  }),
]);
