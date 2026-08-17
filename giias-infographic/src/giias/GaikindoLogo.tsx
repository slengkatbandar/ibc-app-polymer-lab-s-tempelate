import { YELLOW } from "./theme";

// Stylised stand-in for the GIIAS event lockup — recreated with vector shapes
// rather than the official brand asset.
export const GaikindoLogo: React.FC = () => {
  return (
    <div
      style={{
        width: 236,
        height: 106,
        borderRadius: 14,
        backgroundColor: "#11292B",
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        padding: "0 14px",
      }}
    >
      <svg width="54" height="54" viewBox="0 0 54 54" style={{ flexShrink: 0 }}>
        <defs>
          <linearGradient id="giias-swoosh" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#FFD84D" />
            <stop offset="100%" stopColor="#EF8B2C" />
          </linearGradient>
        </defs>
        <circle
          cx="27"
          cy="27"
          r="17"
          fill="none"
          stroke="url(#giias-swoosh)"
          strokeWidth="9"
          strokeLinecap="round"
          strokeDasharray="80 27"
          transform="rotate(-125 27 27)"
        />
        <circle cx="27" cy="27" r="6.5" fill="#11292B" />
        <rect x="27" y="22.5" width="18" height="9" rx="4.5" fill="url(#giias-swoosh)" />
      </svg>

      <div style={{ display: "flex", flexDirection: "column", gap: 1 }}>
        <div style={{ fontSize: 9, fontWeight: 700, color: YELLOW }}>
          The 33
          <span style={{ fontSize: 6, verticalAlign: "super" }}>rd</span>
        </div>
        <div
          style={{
            fontSize: 22,
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: 0.3,
            lineHeight: 1,
          }}
        >
          GAIKINDO
        </div>
        <div
          style={{
            fontSize: 7.4,
            fontWeight: 700,
            color: "#FFFFFF",
            letterSpacing: 0.75,
            lineHeight: 1.2,
          }}
        >
          INDONESIA INTERNATIONAL
        </div>
        <div
          style={{
            fontSize: 16,
            fontWeight: 800,
            color: YELLOW,
            letterSpacing: 0.4,
            lineHeight: 1.05,
          }}
        >
          AUTO SHOW
        </div>
      </div>
    </div>
  );
};
