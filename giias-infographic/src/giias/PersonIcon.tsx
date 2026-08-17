import { Easing, interpolate, useCurrentFrame } from "remotion";

export const PersonIcon: React.FC<{
  color: string;
  bun: boolean;
  size: number;
  appearAt: number;
}> = ({ color, bun, size, appearAt }) => {
  const frame = useCurrentFrame();

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      style={{
        display: "block",
        opacity: interpolate(frame, [appearAt, appearAt + 8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.out(Easing.quad),
        }),
        scale: interpolate(frame, [appearAt, appearAt + 12], [0.2, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(0.22, 1.4, 0.36, 1),
          output: "perceptual-scale",
        }),
      }}
    >
      {bun ? <circle cx="12" cy="2.9" r="2.3" fill="#0E2B2D" /> : null}
      <circle cx="12" cy="13" r="9" fill={color} />
      <path d="M3.71 9.5 A9 9 0 0 1 20.29 9.5 Z" fill="#0E2B2D" />
      <circle cx="8.9" cy="13.6" r="1.55" fill="#0E2B2D" />
      <circle cx="15.1" cy="13.6" r="1.55" fill="#0E2B2D" />
    </svg>
  );
};
