import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  useCurrentFrame,
} from "remotion";
import { BarColumn } from "./BarColumn";
import { GaikindoLogo } from "./GaikindoLogo";
import { POPPINS } from "./fonts";
import { CREAM, DARK_TEAL, MAX_VALUE, PINK, TEAL, YEARS } from "./theme";

const CHART_HEIGHT = 620;

export const GiiasInfographic: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      name="Infografis GIIAS"
      style={{ backgroundColor: CREAM, fontFamily: POPPINS }}
    >
      <Interactive.Div
        name="Judul"
        style={{
          position: "absolute",
          left: 56,
          top: 46,
          fontSize: 34,
          fontWeight: 800,
          letterSpacing: 5,
          color: DARK_TEAL,
          opacity: interpolate(frame, [0, 18], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          translate: interpolate(frame, [0, 18], ["0px -14px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        PENGUNJUNG GIIAS 2021-2026
      </Interactive.Div>

      <Interactive.Div
        name="Garis judul"
        style={{
          position: "absolute",
          left: 56,
          top: 97,
          width: 404,
          height: 5,
          backgroundColor: PINK,
          transformOrigin: "left center",
          scale: interpolate(frame, [10, 30], ["0 1", "1 1"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      />

      <Interactive.Div
        name="Subjudul"
        style={{
          position: "absolute",
          left: 56,
          top: 124,
          width: 890,
          fontSize: 25,
          lineHeight: 1.45,
          fontWeight: 400,
          color: "#24494B",
          opacity: interpolate(frame, [16, 36], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          translate: interpolate(frame, [16, 36], ["0px 12px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        Sebelum pandemi Covid-19, pengunjung GIIAS 2019 mencapai 472.956 orang
        yang merupakan rekor saat itu.
      </Interactive.Div>

      <div
        style={{
          position: "absolute",
          left: 56,
          right: 56,
          top: 218,
          height: CHART_HEIGHT,
          display: "flex",
          flexDirection: "row",
          alignItems: "flex-end",
          gap: 11,
        }}
      >
        {YEARS.map((datum, index) => (
          <BarColumn
            key={datum.year}
            barIndex={index}
            year={datum.year}
            value={datum.value}
            note={datum.note}
            targetHeight={(datum.value / MAX_VALUE) * CHART_HEIGHT}
            growStart={34 + index * 13}
          />
        ))}
      </div>

      <Interactive.Div
        name="Logo"
        style={{
          position: "absolute",
          left: 56,
          top: 878,
          opacity: interpolate(frame, [195, 215], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          scale: interpolate(frame, [195, 215], [0.86, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
            output: "perceptual-scale",
          }),
        }}
      >
        <GaikindoLogo />
      </Interactive.Div>

      <Interactive.Div
        name="Rekor baru"
        style={{
          position: "absolute",
          right: 56,
          top: 860,
          fontSize: 57,
          fontWeight: 800,
          lineHeight: 1.05,
          letterSpacing: 0.5,
          color: DARK_TEAL,
          textAlign: "right",
          opacity: interpolate(frame, [203, 223], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          translate: interpolate(frame, [203, 223], ["36px 0px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        REKOR BARU
      </Interactive.Div>

      <Interactive.Div
        name="GIIAS 2026"
        style={{
          position: "absolute",
          right: 56,
          top: 924,
          fontSize: 72,
          fontWeight: 800,
          lineHeight: 1.08,
          letterSpacing: 0.5,
          display: "flex",
          flexDirection: "row",
          gap: 16,
          opacity: interpolate(frame, [213, 235], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          translate: interpolate(frame, [213, 235], ["36px 0px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        <span style={{ color: TEAL }}>GIIAS</span>
        <span style={{ color: PINK }}>2026</span>
      </Interactive.Div>

      <Interactive.Div
        name="Garis GIIAS"
        style={{
          position: "absolute",
          right: 56,
          top: 1010,
          width: 474,
          height: 5,
          backgroundColor: PINK,
          transformOrigin: "right center",
          scale: interpolate(frame, [233, 253], ["0 1", "1 1"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      />

      <Interactive.Div
        name="Sumber"
        style={{
          position: "absolute",
          left: 56,
          top: 1030,
          fontSize: 19,
          fontWeight: 400,
          color: "#3A5658",
          opacity: interpolate(frame, [243, 263], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        Sumber: indonesiaautoshow.com dan gaikindo.or.id
      </Interactive.Div>
    </AbsoluteFill>
  );
};
