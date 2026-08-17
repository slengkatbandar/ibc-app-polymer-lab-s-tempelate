import { Easing, interpolate, useCurrentFrame } from "remotion";
import { PersonIcon } from "./PersonIcon";
import {
  COVID_RED,
  DARK_TEAL,
  ICONS_PER_ROW,
  PEOPLE_PER_ICON,
  YEAR_GREY,
  formatId,
  hasBun,
  pickFace,
} from "./theme";

// Six icons plus their gaps have to fit the ~152px bar width.
const ICON_SIZE = 18;
const ICON_GAP = 6;
const YEAR_ZONE = 88;

// The remainder row sits on top, so every bar keeps a flush bottom edge and
// only the top row is partially filled — same as the source infographic.
const buildRows = (iconCount: number) => {
  const remainder = iconCount % ICONS_PER_ROW;
  const rows: number[] = [];
  if (remainder > 0) {
    rows.push(remainder);
  }
  for (let i = 0; i < Math.floor(iconCount / ICONS_PER_ROW); i++) {
    rows.push(ICONS_PER_ROW);
  }
  return rows;
};

export const BarColumn: React.FC<{
  barIndex: number;
  year: string;
  value: number;
  note?: string;
  targetHeight: number;
  growStart: number;
}> = ({ barIndex, year, value, note, targetHeight, growStart }) => {
  const frame = useCurrentFrame();

  const iconCount = Math.round(value / PEOPLE_PER_ICON);
  const rows = buildRows(iconCount);
  const rowCount = rows.length;

  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
        height: "100%",
      }}
    >
      <div
        style={{
          width: "100%",
          backgroundColor: DARK_TEAL,
          position: "relative",
          overflow: "hidden",
          height: interpolate(
            frame,
            [growStart, growStart + 42],
            [0, targetHeight],
            {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.22, 1, 0.36, 1),
            },
          ),
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 16,
            left: 0,
            right: 0,
            textAlign: "center",
            fontSize: 34,
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: -0.5,
            fontVariantNumeric: "tabular-nums",
            opacity: interpolate(
              frame,
              [growStart + 14, growStart + 28],
              [0, 1],
              {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: Easing.out(Easing.quad),
              },
            ),
          }}
        >
          {formatId(
            interpolate(frame, [growStart + 14, growStart + 48], [0, value], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.out(Easing.cubic),
            }),
          )}
        </div>

        {note ? (
          <div
            style={{
              position: "absolute",
              top: 58,
              left: 2,
              right: 2,
              textAlign: "center",
              fontSize: 15,
              lineHeight: 1.3,
              fontWeight: 700,
              color: COVID_RED,
              whiteSpace: "pre-line",
              opacity: interpolate(
                frame,
                [growStart + 46, growStart + 62],
                [0, 1],
                {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                  easing: Easing.out(Easing.quad),
                },
              ),
            }}
          >
            {note}
          </div>
        ) : null}

        <div
          style={{
            position: "absolute",
            bottom: YEAR_ZONE,
            left: 6,
            right: 6,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: ICON_GAP,
          }}
        >
          {rows.map((countInRow, rowIndex) => (
            <div
              key={rowIndex}
              style={{
                display: "flex",
                flexDirection: "row",
                gap: ICON_GAP,
                justifyContent: "center",
              }}
            >
              {new Array(countInRow).fill(true).map((_, colIndex) => {
                const iconIndex = rowIndex * ICONS_PER_ROW + colIndex;
                return (
                  <PersonIcon
                    key={colIndex}
                    size={ICON_SIZE}
                    color={pickFace(barIndex, iconIndex)}
                    bun={hasBun(barIndex, iconIndex)}
                    // Bottom row lights up first, wave travels upward.
                    appearAt={
                      growStart + 22 + (rowCount - 1 - rowIndex) * 2.4 + colIndex * 0.9
                    }
                  />
                );
              })}
            </div>
          ))}
        </div>

        <div
          style={{
            position: "absolute",
            bottom: 74,
            left: 16,
            right: 16,
            height: 2,
            backgroundColor: "rgba(255,255,255,0.30)",
            transformOrigin: "left center",
            scale: interpolate(
              frame,
              [growStart + 12, growStart + 30],
              ["0 1", "1 1"],
              {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: Easing.bezier(0.22, 1, 0.36, 1),
              },
            ),
          }}
        />

        <div
          style={{
            position: "absolute",
            bottom: 4,
            left: 0,
            right: 0,
            textAlign: "center",
            fontSize: 47,
            fontWeight: 800,
            color: YEAR_GREY,
            letterSpacing: 1,
            opacity: interpolate(frame, [growStart + 6, growStart + 24], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.out(Easing.quad),
            }),
          }}
        >
          {year}
        </div>
      </div>
    </div>
  );
};
